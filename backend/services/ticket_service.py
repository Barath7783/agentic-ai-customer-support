from agents.tools import create_ticket

def open_ticket(customer_id: str, subject: str, description: str) -> str:
    return create_ticket(customer_id, subject, description)
