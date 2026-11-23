
import hashlib
from sqlalchemy import text
from backend.database.connection import engine


with engine.begin() as connection:

    # Read existing revoked tokens
    rows = connection.execute(
        text("SELECT id, token FROM revoked_tokens")
    ).fetchall()

    # Add the new hash column
    connection.execute(
        text("""
            ALTER TABLE revoked_tokens
            ADD COLUMN token_hash VARCHAR(64)
        """)
    )

    # Convert existing tokens into SHA-256 hashes
    for row in rows:
        token_hash = hashlib.sha256(
            row.token.encode("utf-8")
        ).hexdigest()

        connection.execute(
            text("""
                UPDATE revoked_tokens
                SET token_hash = :token_hash
                WHERE id = :id
            """),
            {"token_hash": token_hash, "id": row.id}
        )

    # Make the new column required and unique
    connection.execute(
        text("""
            ALTER TABLE revoked_tokens
            ALTER COLUMN token_hash SET NOT NULL
        """)
    )

    connection.execute(
        text("""
            ALTER TABLE revoked_tokens
            ADD CONSTRAINT uq_revoked_token_hash UNIQUE (token_hash)
        """)
    )

    # Remove the old raw-token column
    connection.execute(
        text("ALTER TABLE revoked_tokens DROP COLUMN token")
    )

print("Revoked token migration completed successfully!")
