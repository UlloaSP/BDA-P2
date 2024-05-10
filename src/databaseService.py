import sys

import psycopg2
from psycopg2 import errorcodes

import constants


def connect_db():
    try:

        conn = psycopg2.connect(
            host=input(constants.HOST),
            user=input(constants.USER),
            password=input(constants.PASSWORD),
            dbname=input(constants.DB)
        )
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE)

        print(constants.TRY_CONNECTION)

        conn.autocommit = False

        print(constants.SUCCESSFULL_CONNECTION)

        return conn

    except Exception as e:
        print(constants.FAILED_CONNECTION.format(e=e))
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


def drop_tables(conn):
    with conn.cursor() as cur:
        try:
            print(constants.DELETING_TABLES)
            cur.execute(constants.SQl_DROP_TABLES)
            conn.commit()
            print(constants.DELETED_TABLES)
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
                print(constants.NON_EXISTENT_TABLES)
            else:
                print(constants.GLOBAL_ERROR.format(
                    pgcode=str(e.pgcode),
                    pgerror=str(e.pgerror)
                ))
            conn.rollback()
