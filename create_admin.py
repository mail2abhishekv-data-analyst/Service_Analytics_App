import bcrypt
from sqlalchemy import text

from database.connection import engine


# ============================================================
# CREATE ADMIN USER
# ============================================================

username = input("Enter admin username: ").strip()
password = input("Enter admin password: ").strip()
full_name = input("Enter full name: ").strip()


# Hash password
password_hash = bcrypt.hashpw(
    password.encode("utf-8"),
    bcrypt.gensalt()
).decode("utf-8")


# Save user to SQL Server
with engine.begin() as connection:

    connection.execute(
        text("""
            INSERT INTO app_users
            (
                username,
                password_hash,
                full_name,
                role,
                is_active
            )
            VALUES
            (
                :username,
                :password_hash,
                :full_name,
                'Admin',
                1
            )
        """),
        {
            "username": username,
            "password_hash": password_hash,
            "full_name": full_name
        }
    )


print()
print("=" * 50)
print("ADMIN USER CREATED SUCCESSFULLY")
print("=" * 50)
print("Username:", username)
print("Role: Admin")