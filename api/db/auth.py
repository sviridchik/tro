from datetime import datetime
from .datatypes import Token, User
from .utils import conn_cursor


def create_user(username, password, email):
    query = f"""
INSERT INTO "auth_user" (
        "password",
        "last_login",
        "is_superuser",
        "username",
        "first_name",
        "last_name",
        "email",
        "is_staff",
        "is_active",
        "date_joined"
    )
VALUES (
        '{password}',
        NULL,
        false,
        '{username}',
        '',
        '',
        '{email}',
        false,
        true,
        '{datetime.now().isoformat()}'
    )
RETURNING "auth_user"."id"
"""
    with conn_cursor() as cur:
        cur.execute(query)
        records = cur.fetchall()

    if not records:
        return None
    else:
        return records[0]


def get_user_id_by_username_and_password(username, password):
    query = f"""
SELECT "auth_user"."id"
FROM "auth_user"
WHERE "auth_user"."username" = '{username}' AND "auth_user"."password" = '{password}'
LIMIT 1
    """
    with conn_cursor() as cur:
        cur.execute(query)
        records = cur.fetchall()

    return records[0][0]


def get_token(user_id):
    query = f"""
SELECT "authtoken_token"."key",
    "authtoken_token"."user_id",
    "authtoken_token"."created"
FROM "authtoken_token"
WHERE "authtoken_token"."user_id" = {user_id}
LIMIT 21
    """
    with conn_cursor() as cur:
        cur.execute(query)
        records = cur.fetchall()

    if not records:
        return None
    else:
        record = records[0]
        return Token(key=record[0], user=record[1], created=record[2])


def create_token(user_id, key):
    query = f"""
INSERT INTO "authtoken_token" ("key", "user_id", "created")
VALUES (
        '{key}',
        {user_id},
        '{datetime.now().isoformat()}'::timestamptz
    )
RETURNING "authtoken_token"."key"
    """
    with conn_cursor() as cur:
        cur.execute(query)
        records = cur.fetchall()

    return Token(key=records[0])
