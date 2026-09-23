import pytest
from models.workflow import Workflow, Node, Edge, NodeType, ExecutionStatus, NodeConfig
from services.workflow_engine import WorkflowEngine

def create_sample_workflow():
    return Workflow(
        id="wf_1",
        name="Test Workflow",
        nodes=[
            Node(id="n1", type=NodeType.LLM_ANALYZE, config=NodeConfig(prompt="test")),
            Node(id="n2", type=NodeType.FILTER, config=NodeConfig(regex="test")),
            Node(id="n3", type=NodeType.NOTIFY, config=NodeConfig(target="test"))
        ],
        edges=[
            Edge(id="e1", source="n1", target="n2"),
            Edge(id="e2", source="n2", target="n3")
        ]
    )

def test_topological_sort():
    wf = create_sample_workflow()
    engine = WorkflowEngine(wf)
    order = engine._topological_sort()
    assert order == ["n1", "n2", "n3"]

def test_cycle_detection():
    wf = create_sample_workflow()
    wf.edges.append(Edge(id="e3", source="n3", target="n1"))
    engine = WorkflowEngine(wf)
    with pytest.raises(ValueError, match="Cycle detected"):
        engine._topological_sort()

def test_execution_success():
    wf = create_sample_workflow()
    engine = WorkflowEngine(wf)
    res = engine.execute()
    assert res["status"] == ExecutionStatus.SUCCESS
    assert wf.nodes[0].status == ExecutionStatus.SUCCESS
    assert wf.nodes[1].status == ExecutionStatus.SUCCESS
    assert wf.nodes[2].status == ExecutionStatus.SUCCESS

def test_idempotent_execution():
    wf = create_sample_workflow()
    wf.nodes[0].status = ExecutionStatus.SUCCESS
    wf.nodes[0].result = {"mock": "data"}
    engine = WorkflowEngine(wf)
    res = engine.execute()
    assert res["status"] == ExecutionStatus.SUCCESS
    assert wf.nodes[0].result == {"mock": "data"} # Should not be re-executed
