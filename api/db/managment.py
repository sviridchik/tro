from .datatypes import Patient, User, Guardian
from .utils import conn_cursor


def filter_patient_by_user(user_id):
    query = f"""
SELECT 
    "managment_patient"."id",
    "managment_patient"."user_id",
    "managment_patient"."first_name",
    "managment_patient"."last_name",
    "managment_patient"."age",
    "managment_patient"."phone",
    "auth_user"."id",
    "auth_user"."password",
    "auth_user"."last_login",
    "auth_user"."is_superuser",
    "auth_user"."username",
    "auth_user"."first_name",
    "auth_user"."last_name",
    "auth_user"."email",
    "auth_user"."is_staff",
    "auth_user"."is_active",
    "auth_user"."date_joined"
FROM "managment_patient"
    INNER JOIN "auth_user" ON ("managment_patient"."user_id" = "auth_user"."id")
WHERE "managment_patient"."user_id" = {user_id}
ORDER BY "managment_patient"."id" ASC;
"""
    with conn_cursor() as cur:
        cur.execute(query)
        records = cur.fetchall()

    result = list()
    for record in records:
        user = User(id=record[6], username=record[11], email=record[14])
        patient = Patient(id=record[0], user=user, first_name=record[2],
                          last_name=record[3], age=record[4], phone=record[5])
        result.append(patient)

    return result


def filter_guardian_by_user(user_id):
    query = f"""
SELECT 
    "managment_guardian"."id",
    "managment_guardian"."banned",
    "managment_guardian"."is_send",
    "managment_guardian"."relationship",
    "managment_guardian"."user_id",
    "managment_guardian"."first_name",
    "managment_guardian"."last_name",
    "managment_guardian"."phone",
    "managment_guardian"."care_about_id",
    "auth_user"."id",
    "auth_user"."password",
    "auth_user"."last_login",
    "auth_user"."is_superuser",
    "auth_user"."username",
    "auth_user"."first_name",
    "auth_user"."last_name",
    "auth_user"."email",
    "auth_user"."is_staff",
    "auth_user"."is_active",
    "auth_user"."date_joined"
FROM "managment_guardian"
    INNER JOIN "auth_user" ON (
        "managment_guardian"."user_id" = "auth_user"."id"
    )
WHERE "managment_guardian"."user_id" = {user_id}
ORDER BY "managment_guardian"."id" ASC
"""
    with conn_cursor() as cur:
        cur.execute(query)
        records = cur.fetchall()

    result = list()
    for record in records:
        user = User(id=record[9], username=record[14], email=record[17])
        guard = Guardian(id=record[0], banned=record[1], is_send=record[2], relationship=record[3], user=user, first_name=record[5],
                         last_name=record[6], phone=record[7], care_about=Patient(id=record[8]))
        result.append(guard)

    return result
