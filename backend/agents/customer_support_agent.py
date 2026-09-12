import re

from langgraph.graph import StateGraph, START, END

from agents.agent_state import AgentState
from agents.tools import (
    check_order,
    create_ticket,
    process_refund,
    cancel_order,
)
from rag.retriever import retrieve
from services.ai_service import generate_response


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are an AI customer-support agent.

Rules:
1. Be concise, polite, and helpful.
2. Use the supplied company knowledge and tool result.
3. Do not invent order facts.
4. Explain what action was taken.
5. If a request needs human review, clearly say so.
6. For policy questions, answer using the supplied company knowledge.
7. Do not perform an order action when the customer is only asking
   about a policy.
8. If an actual cancellation, refund, order lookup, or support-ticket
   request is made, use the corresponding tool result.
9. Never claim an action was completed unless the tool result confirms it.
"""


# ============================================================
# UNDERSTAND CUSTOMER INTENT
# ============================================================

def understand(state: AgentState):
    text = state["message"].lower().strip()

    # --------------------------------------------------------
    # 1. CANCELLATION REQUEST
    # --------------------------------------------------------

    if any(x in text for x in [
        "cancel my order",
        "cancel order",
        "cancel the order",
        "i want to cancel",
        "i need to cancel",
        "please cancel",
        "can i cancel",
        "could i cancel",
        "can you cancel",
    ]):
        intent = "cancellation"

    # --------------------------------------------------------
    # 2. REFUND REQUEST
    # --------------------------------------------------------

    elif any(x in text for x in [
        "refund my order",
        "refund order",
        "request a refund",
        "request refund",
        "i want a refund",
        "i need a refund",
        "please refund",
        "can you refund",
        "give me a refund",
        "money back",
    ]):
        intent = "refund"

    # --------------------------------------------------------
    # 3. SUPPORT TICKET REQUEST
    # --------------------------------------------------------

    elif any(x in text for x in [
        "support ticket",
        "create a ticket",
        "create support ticket",
        "open a ticket",
        "open support ticket",
        "raise a ticket",
        "raise support ticket",
        "create a support ticket",
        "human support",
        "talk to an agent",
        "speak to an agent",
    ]):
        intent = "ticket"

    # --------------------------------------------------------
    # 4. POLICY / KNOWLEDGE QUESTIONS
    # --------------------------------------------------------

    elif any(x in text for x in [
        "refund policy",
        "cancellation policy",
        "shipping policy",
        "return policy",
        "delivery policy",

        "how long does a refund take",
        "how long will my refund take",
        "how long does refund take",
        "how many days does a refund take",
        "how many days for a refund",

        "how long does shipping take",
        "how long will shipping take",
        "how many days does shipping take",
        "how many days for shipping",

        "what is your refund policy",
        "what is the refund policy",
        "what is your cancellation policy",
        "what is the cancellation policy",
        "what is your shipping policy",
        "what is the shipping policy",

        "are refunds allowed",
        "am i eligible for a refund",
        "eligible for a refund",
        "refund eligibility",

        "what are the refund rules",
        "what are the cancellation rules",
        "what are the shipping rules",
    ]):
        intent = "knowledge"

    # --------------------------------------------------------
    # 5. ORDER TRACKING
    # --------------------------------------------------------

    elif any(x in text for x in [
        "where is my order",
        "where's my order",
        "order status",
        "track my order",
        "track order",
        "tracking my order",
        "order tracking",
        "tracking",
        "delivery status",
        "when will my order arrive",
        "when will my order be delivered",
        "has my order shipped",
        "is my order shipped",
    ]):
        intent = "order"

    # --------------------------------------------------------
    # 6. GENERAL
    # --------------------------------------------------------

    else:
        intent = "general"

    return {
        "intent": intent
    }


# ============================================================
# RETRIEVE COMPANY KNOWLEDGE
# ============================================================

def retrieve_knowledge(state: AgentState):

    context = retrieve(
        state["message"]
    )

    return {
        "context": context
    }


# ============================================================
# EXECUTE BUSINESS ACTION
# ============================================================

def execute_action(state: AgentState):

    text = state["message"]
    intent = state["intent"]

    # --------------------------------------------------------
    # Extract order number
    #
    # Supports:
    # order 1001
    # order #1001
    # #1001
    # --------------------------------------------------------

    order_match = re.search(
        r"(?:order\s*#?\s*|#)([0-9]{3,})",
        text.lower()
    )

    order_id = (
        order_match.group(1)
        if order_match
        else None
    )

    # --------------------------------------------------------
    # KNOWLEDGE
    # --------------------------------------------------------

    if intent == "knowledge":

        result = (
            "No external action required. "
            "Answer using the company knowledge."
        )

    # --------------------------------------------------------
    # ORDER
    # --------------------------------------------------------

    elif intent == "order":

        if order_id:

            result = check_order(
                order_id
            )

        else:

            result = (
                "Please provide your order number "
                "so I can check the order status."
            )

    # --------------------------------------------------------
    # REFUND
    # --------------------------------------------------------

    elif intent == "refund":

        if order_id:

            result = process_refund(
                order_id
            )

        else:

            result = (
                "Please provide your order number "
                "for the refund request."
            )

    # --------------------------------------------------------
    # CANCELLATION
    # --------------------------------------------------------

    elif intent == "cancellation":

        if order_id:

            result = cancel_order(
                order_id
            )

        else:

            result = (
                "Please provide your order number "
                "for cancellation."
            )

    # --------------------------------------------------------
    # SUPPORT TICKET
    # --------------------------------------------------------

    elif intent == "ticket":

        result = create_ticket(
            state["customer_id"],
            "Order delivery issue",
            text
        )

    # --------------------------------------------------------
    # GENERAL
    # --------------------------------------------------------

    else:

        result = (
            "No external action required."
        )

    return {
        "tool_result": result
    }


# ============================================================
# GENERATE FINAL CUSTOMER RESPONSE
# ============================================================

def respond(state: AgentState):

    prompt = f"""
Customer message:
{state["message"]}

Detected intent:
{state["intent"]}

Relevant company knowledge:
{state["context"]}

Tool/action result:
{state["tool_result"]}

Write the final customer-facing response.

Important instructions:

- Answer the customer's actual question.
- Be concise and professional.
- For knowledge or policy questions, answer directly using
  the supplied company knowledge.
- Do not ask for an order number when the customer is only
  asking about a general policy.
- For order actions, clearly explain the result returned by
  the business tool.
- Do not invent order information.
- Do not claim an action was completed unless the tool result
  confirms it.
- If the tool says that human review is required, clearly
  explain that to the customer.
"""


    response = generate_response(
        SYSTEM_PROMPT,
        prompt
    )

    return {
        "response": response
    }


# ============================================================
# LANGGRAPH WORKFLOW
# ============================================================

graph = StateGraph(
    AgentState
)


# ------------------------------------------------------------
# Add nodes
# ------------------------------------------------------------

graph.add_node(
    "understand",
    understand
)

graph.add_node(
    "retrieve_knowledge",
    retrieve_knowledge
)

graph.add_node(
    "execute_action",
    execute_action
)

graph.add_node(
    "respond",
    respond
)


# ------------------------------------------------------------
# Connect workflow
# ------------------------------------------------------------

graph.add_edge(
    START,
    "understand"
)

graph.add_edge(
    "understand",
    "retrieve_knowledge"
)

graph.add_edge(
    "retrieve_knowledge",
    "execute_action"
)

graph.add_edge(
    "execute_action",
    "respond"
)

graph.add_edge(
    "respond",
    END
)


# ============================================================
# COMPILE AGENT
# ============================================================

customer_support_agent = graph.compile()