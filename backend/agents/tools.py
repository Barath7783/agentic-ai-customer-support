from datetime import datetime

from database.connection import SessionLocal
from database.models import SupportTicket


# Demo order data for now.
# We can move orders to PostgreSQL later.
ORDERS = {
    "1001": {
        "status": "shipped",
        "eta": "tomorrow"
    },
    "1002": {
        "status": "delayed",
        "eta": "2 days"
    },
    "1003": {
        "status": "delivered",
        "eta": "delivered"
    },
}


def check_order(order_id: str) -> str:
    order = ORDERS.get(order_id)

    if not order:
        return f"Order {order_id} was not found."

    return (
        f"Order {order_id}: "
        f"status={order['status']}, "
        f"estimated_delivery={order['eta']}."
    )


def create_ticket(
    customer_id: str,
    subject: str,
    description: str
) -> str:

    db = SessionLocal()

    try:
        ticket = SupportTicket(
            customer_id=customer_id,
            subject=subject,
            description=description,
            status="open",
        )

        db.add(ticket)
        db.commit()
        db.refresh(ticket)

        ticket_id = f"T-{ticket.id}"

        return (
            f"Support ticket {ticket_id} created "
            f"for customer {customer_id}."
        )

    except Exception as e:
        db.rollback()

        return (
            f"Unable to create support ticket: {str(e)}"
        )

    finally:
        db.close()


def process_refund(order_id: str) -> str:
    return (
        f"Refund request for order {order_id} "
        f"has been submitted for review."
    )


def cancel_order(order_id: str) -> str:
    return (
        f"Cancellation request for order {order_id} "
        f"has been submitted."
    )
