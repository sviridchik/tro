from .datatypes import TimeTable, Schedule, Cure
from .utils import conn_cursor, get_create_values, get_set_items, get_create_keys
from typing import List

# TIMETABLE


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


# SCHEDULE

def prefetch_related_timesheet(schedule_id=None) -> List[TimeTable]:
    query = f"""
SELECT 
    "medicine_schedule_timesheet"."schedule_id",
    "medicine_timetable"."id",
    "medicine_timetable"."time"
FROM "medicine_timetable"
    INNER JOIN "medicine_schedule_timesheet" ON (
        "medicine_timetable"."id" = "medicine_schedule_timesheet"."timetable_id"
    )
    """
    if schedule_id:
        query += f'WHERE "medicine_schedule_timesheet"."schedule_id" IN ({schedule_id})'

    with conn_cursor() as cur:
        cur.execute(query)
        records = cur.fetchall()

    result = list()

    for r in records:
        time = TimeTable(schedule_id=r[0], id=r[1], time=r[2])
        result.append(time)

    return result


def get_schedule(patient_id, schedule_id):
    query = f"""
SELECT 
    "medicine_schedule"."id",
    "medicine_schedule"."cycle_start",
    "medicine_schedule"."cycle_end",
    "medicine_schedule"."frequency"
FROM "medicine_schedule"
    INNER JOIN "medicine_cure" ON (
        "medicine_schedule"."id" = "medicine_cure"."schedule_id"
    )
WHERE (
        "medicine_cure"."patient_id" = {patient_id}
        AND "medicine_schedule"."id" = {schedule_id}
    )
LIMIT 21;
    """

    with conn_cursor() as cur:
        cur.execute(query)
        records = cur.fetchall()

    if not records:
        return None

    timesheet = prefetch_related_timesheet(schedule_id)
    r = records[0]
    return Schedule(id=r[0], cycle_start=r[1], cycle_end=r[2], frequency=r[3], timesheet=timesheet)


def list_schedules(patient_id):
    query = f"""
SELECT 
    "medicine_schedule"."id",
    "medicine_schedule"."cycle_start",
    "medicine_schedule"."cycle_end",
    "medicine_schedule"."frequency"
FROM "medicine_schedule"
ORDER BY "medicine_schedule"."id"
    """

    with conn_cursor() as cur:
        cur.execute(query)
        records = cur.fetchall()

    result = list()

    timesheet = prefetch_related_timesheet()

    for r in records:
        schedule = Schedule(id=r[0], cycle_start=r[1], cycle_end=r[2], frequency=r[3],
                            timesheet=[t for t in timesheet if t.schedule_id == r[0]])
        result.append(schedule)

    return result


def delete_schedule(patient_id, schedule_id):
    query = f"""
BEGIN;
DELETE FROM "medicine_schedule_timesheet" WHERE "medicine_schedule_timesheet"."schedule_id" IN ({schedule_id});
DELETE FROM "medicine_schedule" WHERE "medicine_schedule"."id" = {schedule_id};
COMMIT;
    """

    with conn_cursor() as cur:
        cur.execute(query)


def update_schedule(patient_id, schedule_id, data):
    timesheet_ids = data.pop('timesheet')
    set_statement = get_set_items(data.items())
    query = f"""
UPDATE "medicine_schedule"
SET {set_statement}
WHERE "medicine_schedule"."id" = {schedule_id}
    """

    with conn_cursor() as cur:
        cur.execute(query)
        query = f"""
                DELETE FROM "medicine_schedule_timesheet" WHERE "medicine_schedule_timesheet"."schedule_id" IN ({schedule_id})
            """
        cur.execute(query)
        for time_id in timesheet_ids:
            query = f"""
                INSERT INTO "medicine_schedule_timesheet" ("schedule_id", "timetable_id")
                VALUES ({schedule_id}, {time_id})
            """
            cur.execute(query)


def create_schedule(data):
    timesheet_ids = data.pop('timesheet')
    create_values = get_create_values(data.values())
    create_keys = get_create_keys(data.keys())
    query = f"""
INSERT INTO "medicine_schedule" ({create_keys})
VALUES ({create_values})
RETURNING "medicine_schedule"."id"
    """

    with conn_cursor() as cur:
        cur.execute(query)
        records = cur.fetchall()

    schedule = Schedule(id=records[0][0])
    with conn_cursor() as cur:
        for time_id in timesheet_ids:
            query = f"""
                INSERT INTO "medicine_schedule_timesheet" ("schedule_id", "timetable_id")
                VALUES ({schedule.id}, {time_id})
            """
            cur.execute(query)

    return schedule
