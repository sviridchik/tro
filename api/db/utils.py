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
