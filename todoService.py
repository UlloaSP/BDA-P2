import psycopg2
from psycopg2 import errorcodes

import constants
import userService


def insert_todo(conn):
    # TODO - cambiar transaccionalidad. Si falla el segundo insert, que se haga un rollback del primero
    userid = userService.find_user_by_email(conn)['id']
    title = input("Título: ")
    description = input("Descripción: ")
    limitdate = input("Data límite: ")
    status = input("Estatus: ")
    priority = input("Prioridade: ")

    sql = constants.SQL_INSERT_TODO

    with conn.cursor() as cur:
        try:
            cur.execute(sql, {'title': title, 'description': description, 'limitdate': limitdate,
                              'status': status, 'priority': priority})
            conn.commit()
        except psycopg2.Error as e:
            print("No commit")
            if e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                if e.diag.column_name == 'title':
                    print(f"Debe especificarse un título")
                if e.diag.column_name == 'description':
                    print(f"Debe especificarse unha descripción")
                if e.diag.column_name == 'limitdate':
                    print(f"Debe especificarse unha data límite")
                if e.diag.column_name == 'status':
                    print(f"Debe especificarse un estatus")
                if e.diag.column_name == 'priority':
                    print(f"Debe especificarse unha prioridade")
            else:
                print(f"Erro: {e.pgcode} - {e.pgerror}")
            conn.rollback()  # isto ocorre sempre que sucede unha excepción

    sql = constants.SQL_INSERT_TODO

    with conn.cursor() as cur:
        try:
            cur.execute(sql, {'userid': userid, 'todoid': 1})
            conn.commit()
            print("A tarefa foi creada correctamente.")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION:
                print(f"Este usuario xa ten esta tarefa.")
            if e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                if e.diag.column_name == 'userid':
                    print(f"Debe especificarse un usuario.")
                if e.diag.column_name == 'todoid':
                    print(f"Debe especificarse unha tarefa.")
            else:
                print(f"Erro: {e.pgcode} - {e.pgerror}")
            conn.rollback()  # isto ocorre sempre que sucede unha excepción
