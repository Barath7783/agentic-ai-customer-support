from agents.tools import check_order

def get_order_status(order_id: str) -> str:
    return check_order(order_id)
