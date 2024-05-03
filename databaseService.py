import sys

import psycopg2
from psycopg2 import errorcodes

import constants


def connect_db():
    try:
        conn = psycopg2.connect(
            host=constants.HOST,
            user=constants.USER,
            password=constants.PASSWORD,
            dbname=constants.DB
        )

        conn.autocommit = False

        return conn

    except Exception as e:
        print(f"Erro de conexión: {e}")
        sys.exit(1)


def disconnect_db(conn):
    conn.commit()
    conn.close()


def create_tables(conn):
    with (open(constants.SQL_CREATE_TABLES)) as archivo:
        sql = archivo.read()

    with conn.cursor() as cur:
        try:
            cur.execute(sql)
            conn.commit()
            print("Táboas creadas")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.DUPLICATE_TABLE:
                print("As táboas xa existen. Non se crean.")
            else:
                print(f"Erro: {e.pgcode} - {e.pgerror}")
            conn.rollback()
