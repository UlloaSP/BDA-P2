import psycopg2
from psycopg2 import errorcodes, extras

import constants
import userService


def find_todo_by_id(conn, control_tx=True):
    todoid = input(constants.FIND_TODO_BY_ID_INPUT)
    sql = constants.SQL_FIND_TODO_BY_ID

    retval = None

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        # cursor con diccionario para poder buscar los nombres de las columnas de la fila
        try:
            cur.execute(sql, (todoid,))
            row = cur.fetchone()  # devuelve la fila que ha encontrado en el select
            if row:  # if row is not None
                retval = {
                    'todoid': row['todoid'],
                    'title': row['title'],
                    'description': row['description'],
                    'creationDate': row['creationdate'],
                    'limitDate': row['limitdate'],
                    'status': row['status'],
                    'priority': row['priority'],
                }

                print(constants.TODO_INFO_TEMPLATE.format(
                    todoid=row['todoid'],
                    title=row['title'],
                    description=row['description'],
                    creationDate=row['creationdate'],
                    limitDate=row['limitdate'],
                    status=row['status'],
                    priority=row['priority']
                ))

            else:
                print(constants.NON_EXISTENT_TODO_SEARCH_BY_ID.format(
                    id=todoid
                ))
            conn.commit()
        except psycopg2.Error as e:
            print(constants.GLOBAL_ERROR.format(
                pgcode=str(e.pgcode),
                pgerror=str(e.pgerror)
            ))
            if control_tx:
                conn.rollback()
    return retval


def find_todo_by_title(conn, control_tx=True):
    title = input(constants.FIND_TODO_BY_TITLE_INPUT)
    sql = constants.SQL_FIND_TODO_BY_TITLE

    retval = None

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        # cursor con diccionario para poder buscar los nombres de las columnas de la fila
        try:
            cur.execute(sql, (title,))
            row = cur.fetchone()  # devuelve la fila que ha encontrado en el select
            if row:  # if row is not None
                retval = {
                    'todoid': row['todoid'],
                    'title': row['title'],
                    'description': row['description'],
                    'creationDate': row['creationdate'],
                    'limitDate': row['limitdate'],
                    'status': row['status'],
                    'priority': row['priority'],
                }

                print(constants.TODO_INFO_TEMPLATE.format(
                    todoid=row['todoid'],
                    title=row['title'],
                    description=row['description'],
                    creationDate=row['creationdate'],
                    limitDate=row['limitdate'],
                    status=row['status'],
                    priority=row['priority']
                ))

            else:
                print(constants.NON_EXISTENT_TODO_SEARCH_BY_TITLE.format(
                    title=title
                ))
            conn.commit()
        except psycopg2.Error as e:
            print(constants.GLOBAL_ERROR.format(
                pgcode=str(e.pgcode),
                pgerror=str(e.pgerror)
            ))
            if control_tx:
                conn.rollback()
    return retval


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
                print(constants.GLOBAL_ERROR.format(
                    pgcode=str(e.pgcode),
                    pgerror=str(e.pgerror)
                ))
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
                print(constants.GLOBAL_ERROR.format(
                    pgcode=str(e.pgcode),
                    pgerror=str(e.pgerror)
                ))
            conn.rollback()  # isto ocorre sempre que sucede unha excepción
