from pathlib import Path

KNOWLEDGE = {
    "refund": """
Refund Policy:
Customers can request a refund for eligible orders. Damaged or incorrect
items should be reported to support. Refunds may require verification.
""",
    "shipping": """
Shipping Policy:
Standard delivery usually takes 3-7 business days. Delayed shipments
should be checked against the latest tracking status.
""",
    "cancellation": """
Cancellation Policy:
Orders can be cancelled before they enter the final fulfillment stage.
Requests after shipment may require a return/refund process.
""",
    "faq": """
FAQ:
Customers can contact support for order status, refunds, cancellations,
damaged products, account questions, and delivery issues.
"""
}

def retrieve(query: str, top_k: int = 3) -> str:
    query = query.lower()
    matches = []
    for key, text in KNOWLEDGE.items():
        if key in query:
            matches.append(text.strip())
    if not matches:
        matches = [KNOWLEDGE["faq"].strip()]
    return "\n\n".join(matches[:top_k])
