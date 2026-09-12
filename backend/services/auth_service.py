def authenticate_demo(email: str, password: str) -> bool:
    # Replace with JWT/OAuth and hashed passwords in production.
    return bool(email and password)
