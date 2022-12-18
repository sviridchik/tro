from .datatypes import Token, User
from .utils import conn_cursor


def get_token(token):
    query = f"""
SELECT authtoken_token.key,
    authtoken_token.user_id,
    authtoken_token.created,
    auth_user.id,
    auth_user.password,
    auth_user.last_login,
    auth_user.is_superuser,
    auth_user.username,
    auth_user.first_name,
    auth_user.last_name,
    auth_user.email,
    auth_user.is_staff,
    auth_user.is_active,
    auth_user.date_joined
FROM authtoken_token
    INNER JOIN auth_user ON (authtoken_token.user_id = auth_user.id)
WHERE authtoken_token.key = '{token}'
LIMIT 21
"""
    with conn_cursor() as cur:
        cur.execute(query)
        records = cur.fetchall()

    if not records:
        return None
    else:
        record = records[0]
        return Token(key=record[0], created=record[2], user=User(id=record[3], password=record[4], username=record[7], email=record[10], is_active=record[12]))


if __name__ == '__main__':
    tk = get_token('3e2617f07ec679b43ed5764d0e8684245f268fd2')
    print(tk.user)
    print(tk.user.is_active)
