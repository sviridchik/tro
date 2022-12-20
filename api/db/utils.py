import psycopg2
import contextlib


@contextlib.contextmanager
def conn_cursor():
    conn = psycopg2.connect(host='127.0.0.1',
                            user='postgres',
                            password='postgres',
                            port=5432,
                            database='postgres')
    cur = conn.cursor()
    yield cur
    cur.close()
    conn.commit()
    conn.close()


def get_create_values(values):
    res = []
    for val in values:
        if isinstance(val, str):
            res.append(f"'{val}'")
        elif isinstance(val, int):
            res.append(str(val))
        else:
            TypeError(val)

    return ', '.join(res)

def get_create_keys(keys):
    return ', '.join(f'"{k}"' for k in keys)

def get_set_items(items):
    res = []
    for k, val in items:
        item = ''
        if isinstance(val, str):
            item_val = f"'{val}'"
        elif isinstance(val, int):
            item_val = str(val)
        else:
            TypeError(val)
        item = f'"{k}" = {item_val}'
        res.append(item)

    return ', '.join(res)
