import sys

import psycopg2
from psycopg2 import errorcodes

import constants


def connect_db():
    print(constants.TRY_CONNECTION)
    try:

        conn = psycopg2.connect(
            host=constants.HOST,
            user=constants.USER,
            password=constants.PASSWORD,
            dbname=constants.DB
        )

        conn.autocommit = False

        print(constants.SUCCESSFULL_CONNECTION)

        return conn

    except Exception as e:
        print(constants.FAILED_CONNECTION + f"{e}")
        sys.exit(1)


def disconnect_db(conn):
    conn.commit()
    print(constants.TERMINATING_CONNECTION)
    conn.close()
    print(constants.TERMINATED_CONNECTION)


def create_tables(conn):
    with (open(constants.SQL_CREATE_TABLES)) as archivo:
        sql = archivo.read()

    with conn.cursor() as cur:
        try:
            print(constants.CREATING_TABLES)
            cur.execute(sql)
            conn.commit()
            print(constants.CREATED_TABLES)
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.DUPLICATE_TABLE:
                print(constants.DUPLICATED_TABLES)
            else:
                print(constants.GLOBAL_ERROR.format(
                    pgcode=str(e.pgcode),
                    pgerror=str(e.pgerror)
                ))
            conn.rollback()
