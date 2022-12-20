from .datatypes import Patient, User, Guardian, Doctor
from .utils import conn_cursor, get_create_values, get_set_items


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


def get_doctor(patient_id, doctor_id):
    query = f"""
SELECT 
    "managment_doctor"."id",
    "managment_doctor"."first_name",
    "managment_doctor"."last_name",
    "managment_doctor"."specialty",
    "managment_doctor"."patient_id"
FROM "managment_doctor"
WHERE "managment_doctor"."id" = {doctor_id} AND "managment_doctor"."patient_id" = {patient_id}
LIMIT 21
    """

    with conn_cursor() as cur:
        cur.execute(query)
        records = cur.fetchall()

    if not records:
        return None

    r = records[0]
    return Doctor(id=r[0], first_name=r[1], last_name=r[2], specialty=r[3], patient=Patient(id=r[4]))


def list_doctors(patient_id):
    query = f"""
SELECT 
    "managment_doctor"."id",
    "managment_doctor"."first_name",
    "managment_doctor"."last_name",
    "managment_doctor"."specialty",
    "managment_doctor"."patient_id"
FROM "managment_doctor"
WHERE "managment_doctor"."patient_id" = {patient_id}
ORDER BY "managment_doctor"."id" ASC
LIMIT 21
    """

    with conn_cursor() as cur:
        cur.execute(query)
        records = cur.fetchall()

    result = list()
    for r in records:
        doctor = Doctor(id=r[0], first_name=r[1], last_name=r[2], specialty=r[3], patient=Patient(id=r[4]))
        result.append(doctor)

    return result


def delete_doctor(patient_id, doctor_id):
    query = f"""
BEGIN;
DELETE FROM "managment_doctorvisit" WHERE "managment_doctorvisit"."doctor_id" = {doctor_id};
DELETE FROM "managment_doctor" WHERE "managment_doctor"."id" = {doctor_id} AND "managment_doctor"."patient_id" = {patient_id};
COMMIT;
    """

    with conn_cursor() as cur:
        cur.execute(query)


def update_doctor(patient_id, doctor_id, **kwargs):
    set_statement = get_set_items(kwargs.items())
    query = f"""
UPDATE "managment_doctor"
SET {set_statement}
WHERE "managment_doctor"."id" = {doctor_id} AND "managment_doctor"."patient_id" = {patient_id}
    """

    with conn_cursor() as cur:
        cur.execute(query)


def create_doctor(values):
    create_values = get_create_values(values)
    query = f"""
INSERT INTO "managment_doctor" (
        "first_name",
        "last_name",
        "specialty",
        "patient_id"
    )
VALUES ({create_values})
RETURNING "managment_doctor"."id"
    """

    with conn_cursor() as cur:
        cur.execute(query)
        records = cur.fetchall()

    return Doctor(id=records[0][0])
