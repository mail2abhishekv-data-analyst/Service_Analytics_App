import bcrypt
from sqlalchemy import text

from database.connection import engine


def authenticate_user(username, password):
    """
    Verify username and password against app_users.
    Returns user information if credentials are valid.
    Returns None if authentication fails.
    """

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT
                    user_id,
                    username,
                    password_hash,
                    full_name,
                    role,
                    is_active
                FROM app_users
                WHERE username = :username
            """),
            {
                "username": username
            }
        )

        user = result.mappings().fetchone()

    if user is None:
        return None

    # Check whether the account is active
    if not user["is_active"]:
        return None

    # Verify password against stored bcrypt hash
    password_valid = bcrypt.checkpw(
        password.encode("utf-8"),
        user["password_hash"].encode("utf-8")
    )

    if not password_valid:
        return None

    return {
        "user_id": user["user_id"],
        "username": user["username"],
        "full_name": user["full_name"],
        "role": user["role"]
    }