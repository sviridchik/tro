from .datatypes import Token, User, Patient
from .utils import conn_cursor


def get_token(token):
    query = f"""
SELECT 
    authtoken_token.key,
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
    auth_user.date_joined,
    managment_patient.id,
    managment_patient.first_name,
    managment_patient.last_name,
    managment_patient.age,
    managment_patient.phone
FROM authtoken_token
    INNER JOIN auth_user ON (authtoken_token.user_id = auth_user.id)
    INNER JOIN managment_patient ON (auth_user.id = managment_patient.user_id)
WHERE authtoken_token.key = '{token}'
LIMIT 21
"""
    with conn_cursor() as cur:
        cur.execute(query)
        records = cur.fetchall()

    if not records:
        return None
    else:
        r = records[0]
        patient = Patient(id=r[14], first_name=r[15], last_name=r[16], age=r[17], phone=r[18])
        user = User(id=r[3], password=r[4], username=r[7],
                    email=r[10], is_active=r[12], patient=patient)
        return Token(key=r[0], created=r[2], user=user)


if __name__ == '__main__':
    tk = get_token('3e2617f07ec679b43ed5764d0e8684245f268fd2')
    print(tk.user)
    print(tk.user.is_active)
