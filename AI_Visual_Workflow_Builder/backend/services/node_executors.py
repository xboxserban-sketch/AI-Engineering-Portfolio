import logging
import re
from typing import Dict, Any, List
# import openai  # In a real scenario, we'd use this. Mocked for deterministic tests.
from models.workflow import Node, NodeConfig

logger = logging.getLogger(__name__)

def execute_llm_analyze(node: Node, inputs: List[Dict[str, Any]]) -> Dict[str, Any]:
    logger.info(f"Executing LLM_ANALYZE for node {node.id}")
    prompt = node.config.prompt or "Analyze this"
    # Mock LLM call
    input_text = str(inputs)
    return {"analysis": f"Processed '{input_text}' with prompt: {prompt}"}

def execute_filter(node: Node, inputs: List[Dict[str, Any]]) -> Dict[str, Any]:
    logger.info(f"Executing FILTER for node {node.id}")
    regex = node.config.regex or ".*"
    pattern = re.compile(regex)
    filtered = []
    for inp in inputs:
        for k, v in inp.items():
            if pattern.search(str(v)):
                filtered.append(inp)
                break
    return {"filtered_data": filtered}

def execute_transform(node: Node, inputs: List[Dict[str, Any]]) -> Dict[str, Any]:
    logger.info(f"Executing TRANSFORM for node {node.id}")
    mapping = node.config.mapping or {}
    transformed = []
    for inp in inputs:
        new_item = {}
        for old_k, new_k in mapping.items():
            if old_k in inp:
                new_item[new_k] = inp[old_k]
        if new_item:
            transformed.append(new_item)
    return {"transformed_data": transformed}

def execute_notify(node: Node, inputs: List[Dict[str, Any]]) -> Dict[str, Any]:
    logger.info(f"Executing NOTIFY for node {node.id}")
    target = node.config.target or "console"
    logger.info(f"Notifying target {target} with data: {inputs}")
    return {"notified": True, "target": target}

EXECUTORS = {
    "LLM_ANALYZE": execute_llm_analyze,
    "FILTER": execute_filter,
    "TRANSFORM": execute_transform,
    "NOTIFY": execute_notify,
}
