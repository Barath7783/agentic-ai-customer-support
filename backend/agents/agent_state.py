from typing import TypedDict, List, Dict, Any

class AgentState(TypedDict):
    message: str
    customer_id: str
    history: List[Dict[str, str]]
    context: str
    intent: str
    tool_result: str
    response: str
