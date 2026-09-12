from fastapi import APIRouter
from pydantic import BaseModel
from agents.customer_support_agent import customer_support_agent

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    customer_id: str = "demo-user"
    history: list[dict[str, str]] = []

class ChatResponse(BaseModel):
    response: str
    intent: str
    tool_result: str

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    state = {
        "message": request.message,
        "customer_id": request.customer_id,
        "history": request.history,
        "context": "",
        "intent": "",
        "tool_result": "",
        "response": "",
    }

    result = customer_support_agent.invoke(state)

    return ChatResponse(
        response=result["response"],
        intent=result["intent"],
        tool_result=result["tool_result"],
    )
