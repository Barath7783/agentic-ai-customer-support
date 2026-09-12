from database.connection import Base, engine
from database.models import SupportTicket

Base.metadata.create_all(bind=engine)
print("Database tables created.")
