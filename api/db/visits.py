from .datatypes import Patient, User, Guardian, Doctor, DoctorVisit
from .utils import conn_cursor, get_create_values, get_set_items, get_create_keys


def get_visit(patient_id, visit_id):
    query = f"""
SELECT 
    "managment_doctorvisit"."id",
    "managment_doctorvisit"."date",
    "managment_doctorvisit"."doctor_id",
    "managment_doctorvisit"."patient_id",
    "managment_doctor"."id",
    "managment_doctor"."first_name",
    "managment_doctor"."last_name",
    "managment_doctor"."specialty",
    "managment_doctor"."patient_id"
FROM "managment_doctorvisit"
    INNER JOIN "managment_patient" ON (
        "managment_doctorvisit"."patient_id" = "managment_patient"."id"
    )
    INNER JOIN "managment_doctor" ON (
        "managment_doctorvisit"."doctor_id" = "managment_doctor"."id"
    )
WHERE "managment_patient"."id" = {patient_id} AND "managment_doctorvisit"."id" = {visit_id}
LIMIT 21
    """

    with conn_cursor() as cur:
        cur.execute(query)
        records = cur.fetchall()

    if not records:
        return None

    r = records[0]
    doctor = Doctor(id=r[4], first_name=r[5], last_name=r[6], specialty=r[7], patient=Patient(id=r[8]))
    return DoctorVisit(id=r[0], date=r[1], doctor=doctor, patient=Patient(id=r[3]))


def list_visits(patient_id):
    query = f"""
SELECT 
    "managment_doctorvisit"."id",
    "managment_doctorvisit"."date",
    "managment_doctorvisit"."doctor_id",
    "managment_doctorvisit"."patient_id",
    "managment_doctor"."id",
    "managment_doctor"."first_name",
    "managment_doctor"."last_name",
    "managment_doctor"."specialty",
    "managment_doctor"."patient_id"
FROM "managment_doctorvisit"
    INNER JOIN "managment_patient" ON (
        "managment_doctorvisit"."patient_id" = "managment_patient"."id"
    )
    INNER JOIN "managment_doctor" ON (
        "managment_doctorvisit"."doctor_id" = "managment_doctor"."id"
    )
WHERE "managment_patient"."id" = {patient_id}
ORDER BY "managment_doctorvisit"."id" ASC
    """

    with conn_cursor() as cur:
        cur.execute(query)
        records = cur.fetchall()

    result = list()
    print(len(records))
    for r in records:
        doctor = Doctor(id=r[4], first_name=r[5], last_name=r[6], specialty=r[7], patient=Patient(id=r[8]))
        visit = DoctorVisit(id=r[0], date=r[1], doctor=doctor, patient=Patient(id=r[3]))
        result.append(visit)

    return result


def delete_visit(patient_id, visit_id):
    query = f"""
BEGIN;
DELETE FROM "managment_doctorvisit" WHERE "managment_doctorvisit"."id" = {visit_id} AND "managment_doctorvisit"."patient_id" = {patient_id};
COMMIT;
    """

    with conn_cursor() as cur:
        cur.execute(query)


def update_visit(patient_id, visit_id, data):
    set_statement = get_set_items(data.items())
    query = f"""
UPDATE "managment_doctorvisit"
SET {set_statement}
WHERE "managment_doctorvisit"."id" = {visit_id} AND "managment_doctorvisit"."patient_id" = {patient_id}
    """

    with conn_cursor() as cur:
        cur.execute(query)


def create_visit(data):
    create_values = get_create_values(data.values())
    create_keys = get_create_keys(data.keys())
    query = f"""
INSERT INTO "managment_doctorvisit" ({create_keys})
VALUES ({create_values})
RETURNING "managment_doctorvisit"."id"
    """

    with conn_cursor() as cur:
        cur.execute(query)
        records = cur.fetchall()

    return DoctorVisit(id=records[0][0])
