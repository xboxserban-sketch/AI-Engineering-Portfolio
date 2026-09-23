import logging
from typing import Dict, Any, List, Set
from models.workflow import Workflow, ExecutionStatus, Node, Edge
from services.node_executors import EXECUTORS

logger = logging.getLogger(__name__)

class WorkflowEngine:
    def __init__(self, workflow: Workflow):
        self.workflow = workflow
        self.nodes = {n.id: n for n in workflow.nodes}
        self.edges = workflow.edges
        self.adjacency_list = self._build_adjacency_list()
        self.indegree = self._build_indegree()
    
    def _build_adjacency_list(self) -> Dict[str, List[str]]:
        adj: Dict[str, List[str]] = {node_id: [] for node_id in self.nodes}
        for edge in self.edges:
            if edge.source in adj:
                adj[edge.source].append(edge.target)
        return adj
    
    def _build_indegree(self) -> Dict[str, int]:
        indegree = {node_id: 0 for node_id in self.nodes}
        for edge in self.edges:
            if edge.target in indegree:
                indegree[edge.target] += 1
        return indegree

    def _topological_sort(self) -> List[str]:
        zero_indegree = [n_id for n_id, deg in self.indegree.items() if deg == 0]
        topo_order = []
        indegree_copy = self.indegree.copy()
        
        while zero_indegree:
            curr = zero_indegree.pop(0)
            topo_order.append(curr)
            for neighbor in self.adjacency_list[curr]:
                indegree_copy[neighbor] -= 1
                if indegree_copy[neighbor] == 0:
                    zero_indegree.append(neighbor)
                    
        if len(topo_order) != len(self.nodes):
            raise ValueError("Cycle detected in workflow DAG")
            
        return topo_order

    def execute(self) -> Dict[str, Any]:
        logger.info(f"Starting execution of workflow {self.workflow.id}")
        try:
            topo_order = self._topological_sort()
        except Exception as e:
            logger.error(f"Workflow execution failed: {e}")
            return {"status": ExecutionStatus.FAILED, "error": str(e)}

        results = {}
        for node_id in topo_order:
            node = self.nodes[node_id]
            if node.status == ExecutionStatus.SUCCESS:
                logger.info(f"Skipping already successful node {node_id} (Idempotent)")
                results[node_id] = node.result
                continue
                
            node.status = ExecutionStatus.RUNNING
            
            # Gather inputs from predecessors
            inputs = []
            predecessors = [edge.source for edge in self.edges if edge.target == node_id]
            skip_node = False
            for p in predecessors:
                pred_node = self.nodes[p]
                if pred_node.status != ExecutionStatus.SUCCESS:
                    logger.warning(f"Node {node_id} depends on failed/pending node {p}. Failing {node_id}.")
                    node.status = ExecutionStatus.FAILED
                    node.error = f"Dependency {p} failed"
                    skip_node = True
                    break
                if pred_node.result:
                    inputs.append(pred_node.result)
                    
            if skip_node:
                results[node_id] = {"error": node.error}
                continue
                
            # Execute node
            executor = EXECUTORS.get(node.type)
            if not executor:
                node.status = ExecutionStatus.FAILED
                node.error = f"No executor found for type {node.type}"
                results[node_id] = {"error": node.error}
                continue
                
            try:
                res = executor(node, inputs)
                node.status = ExecutionStatus.SUCCESS
                node.result = res
                results[node_id] = res
            except Exception as e:
                logger.error(f"Node {node_id} execution failed: {e}")
                node.status = ExecutionStatus.FAILED
                node.error = str(e)
                results[node_id] = {"error": str(e)}
                
        # Check overall status
        failed_nodes = [n for n in self.nodes.values() if n.status == ExecutionStatus.FAILED]
        status = ExecutionStatus.FAILED if failed_nodes else ExecutionStatus.SUCCESS
        
        return {
            "status": status,
            "node_results": results
        }
