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


def find_todo_by_title(conn, title=None, control_tx=True):
    if not title:
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
    user = userService.find_user_by_email(conn)
    if not user:
        conn.rollback()
        return

    title = input(constants.TITLE_INPUT)
    if title == "":
        title = None

    description = input(constants.DESCRIPTION_INPUT)
    limitdate = input(constants.LIMIT_DATE_INPUT)
    if limitdate == "":
        limitdate = None

    status = input(constants.STATUS_INPUT)
    if status == "":
        status = None

    priority = input(constants.PRIORITY_INPUT)
    if priority == "":
        priority = None

    sql = constants.SQL_INSERT_TODO

    with conn.cursor() as cur:
        try:
            cur.execute(sql, {'title': title, 'description': description, 'limitdate': limitdate,
                              'status': status, 'priority': priority})
            todoid = find_todo_by_title(conn, title)['todoid']
            insert_users_todo(conn, user['id'], todoid)
            conn.commit()
            print(constants.INSERT_TODO_SUCCESS)
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                if e.diag.column_name == 'title':
                    print(constants.NOT_NULL_TITLE)
                if e.diag.column_name == 'description':
                    print(constants.NOT_NULL_DESCRIPTION)
                if e.diag.column_name == 'limitdate':
                    print(constants.NOT_NULL_LIMIT_DATE)
                if e.diag.column_name == 'status':
                    print(constants.NOT_NULL_STATUS)
                if e.diag.column_name == 'priority':
                    print(constants.NOT_NULL_PRIORITY)
                if e.pgcode == psycopg2.errorcodes.INVALID_DATETIME_FORMAT:
                    print(constants.INVALID_DATETIME)
            else:
                print(constants.GLOBAL_ERROR.format(
                    pgcode=str(e.pgcode),
                    pgerror=str(e.pgerror)
                ))
            conn.rollback()  # isto ocorre sempre que sucede unha excepción


def insert_users_todo(conn, userid, todoid):
    sql = constants.SQL_INSERT_USER_TODO

    with conn.cursor() as cur:
        try:
            cur.execute(sql, {'userid': userid, 'todoid': todoid})
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION:
                print(constants.UNIQUE_USER_TODO)
            if e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                if e.diag.column_name == 'userid':
                    print(constants.NOT_NULL_USER)
                if e.diag.column_name == 'todoid':
                    print(constants.NOT_NULL_TODO)
            else:
                print(constants.GLOBAL_ERROR.format(
                    pgcode=str(e.pgcode),
                    pgerror=str(e.pgerror)
                ))
            conn.rollback()  # isto ocorre sempre que sucede unha excepción


def add_line_description(conn):
    todo = find_todo_by_title(conn)

    additional_description = input(constants.UPDATE_DESCRIPTION_INPUT)

    sql = constants.SQL_UPDATE_TODO_BY_DESCRIPTION

    with conn.cursor() as cur:
        try:
            cur.execute(sql, {'description': additional_description, 'todoid': todo['todoid']})
            conn.commit()
        except psycopg2.Error as e:
            print(constants.GLOBAL_ERROR.format(
                pgcode=str(e.pgcode),
                pgerror=str(e.pgerror)
            ))
            conn.rollback()  # isto ocorre sempre que sucede unha excepción


def update_date(conn):
    todo = find_todo_by_title(conn)

    days = input(constants.UPDATE_DATE_INPUT)

    sql = constants.SQL_UPDATE_TODO_BY_DATE

    with conn.cursor() as cur:
        try:
            cur.execute(sql, {'days': days, 'todoid': todo['todoid']})
            conn.commit()
        except psycopg2.Error as e:
            print(constants.GLOBAL_ERROR.format(
                pgcode=str(e.pgcode),
                pgerror=str(e.pgerror)
            ))
            conn.rollback()  # isto ocorre sempre que sucede unha excepción


def add_user_to_todo(conn):
    user = userService.find_user_by_email(conn)

    if not user:
        conn.rollback()
        return

    todo = find_todo_by_title(conn)

    if not todo:
        conn.rollback()
        return

    sql = constants.SQL_INSERT_USER_TODO
    with conn.cursor() as cur:
        try:
            cur.execute(sql, {'userid': user['id'], 'todoid': todo['todoId']})
            conn.commit()
            print(constants.ADD_USER_TO_TODO_SUCCESS)
        except psycopg2.Error as e:
            print(constants.GLOBAL_ERROR.format(
                pgcode=str(e.pgcode),
                pgerror=str(e.pgerror)
            ))
            conn.rollback()  # isto ocorre sempre que sucede unha excepción
