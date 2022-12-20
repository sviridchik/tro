from .datatypes import TimeTable, Schedule, Cure
from .utils import conn_cursor, get_create_values, get_set_items, get_create_keys


def get_time(patient_id, time_id):
    query = f"""
SELECT 
    "medicine_timetable"."id",
    "medicine_timetable"."time"
FROM "medicine_timetable"
WHERE "medicine_timetable"."id" = {time_id}
LIMIT 21
    """

    with conn_cursor() as cur:
        cur.execute(query)
        records = cur.fetchall()

    if not records:
        return None

    r = records[0]
    return TimeTable(id=r[0], time=r[1])


def list_times(patient_id):
    query = f"""
SELECT 
    "medicine_timetable"."id",
    "medicine_timetable"."time"
FROM "medicine_timetable"
ORDER BY "medicine_timetable"."time" ASC
    """

    with conn_cursor() as cur:
        cur.execute(query)
        records = cur.fetchall()

    result = list()
    print(len(records))
    for r in records:
        time = TimeTable(id=r[0], time=r[1])
        result.append(time)

    return result


def delete_time(patient_id, time_id):
    query = f"""
BEGIN;
DELETE FROM "medicine_timetable" WHERE "medicine_timetable"."id" = {time_id};
COMMIT;
    """

    with conn_cursor() as cur:
        cur.execute(query)


def update_time(patient_id, time_id, data):
    set_statement = get_set_items(data.items())
    query = f"""
UPDATE "medicine_timetable"
SET {set_statement}
WHERE "medicine_timetable"."id" = {time_id}
    """

    with conn_cursor() as cur:
        cur.execute(query)


def create_time(data):
    create_values = get_create_values(data.values())
    create_keys = get_create_keys(data.keys())
    query = f"""
INSERT INTO "medicine_timetable" ({create_keys})
VALUES ({create_values})
RETURNING "medicine_timetable"."id"
    """

    with conn_cursor() as cur:
        cur.execute(query)
        records = cur.fetchall()

    return TimeTable(id=records[0][0])
