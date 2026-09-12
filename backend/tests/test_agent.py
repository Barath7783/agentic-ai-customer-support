from agents.customer_support_agent import customer_support_agent

def test_order_agent():
    result = customer_support_agent.invoke({
        "message": "Where is order #1001?",
        "customer_id": "test-user",
        "history": [],
        "context": "",
        "intent": "",
        "tool_result": "",
        "response": "",
    })
    assert result["intent"] == "order"
    assert "1001" in result["tool_result"]
