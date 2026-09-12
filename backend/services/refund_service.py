from agents.tools import process_refund

def request_refund(order_id: str) -> str:
    return process_refund(order_id)
