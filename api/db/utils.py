import psycopg2
import contextlib


@contextlib.contextmanager
def conn_cursor():
    print('CUR opened')
    cur = conn.cursor()
    yield cur
    print('CUR closed')
    cur.close()


conn = psycopg2.connect(host='127.0.0.1',
                        user='postgres',
                        password='postgres',
                        port=5432,
                        database='postgres')
