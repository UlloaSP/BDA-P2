import psycopg2
from psycopg2 import errorcodes, extras

import constants
import userService


def find_todo_by_id(conn):
    while True:
        todoid = input(constants.FIND_TODO_BY_ID_INPUT)
        if todoid != "":
            break

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
            if e.pgcode == psycopg2.errorcodes.INVALID_TEXT_REPRESENTATION:
                print(constants.INVALID_ID_FORMAT)
            else:
                print(constants.GLOBAL_ERROR.format(
                    pgcode=str(e.pgcode),
                    pgerror=str(e.pgerror)
                ))
            conn.rollback()
    return retval


def find_todo_by_title(conn, title=None, control_tx=True):
    while not title or title == "":
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
    user = userService.find_user_by_email(conn, control_tx=False)
    if not user:
        conn.rollback()
        return

    title = input(constants.TITLE_INPUT)
    if title == "":
        title = None

    description = input(constants.DESCRIPTION_INPUT)
    if description == "":
        description = None

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
            # sabemos que todoid non dará problema porque a tarefa que buscamos existe. Nunca devolverá None
            todoid = find_todo_by_title(conn, title)['todoid']
            insert_users_todo(conn, user['id'], todoid, control_tx=False)
            conn.commit()
            print(constants.INSERT_TODO_SUCCESS)
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                if e.diag.column_name == 'title':
                    print(constants.NOT_NULL_TITLE)
                elif e.diag.column_name == 'description':
                    print(constants.NOT_NULL_DESCRIPTION)
                elif e.diag.column_name == 'limitdate':
                    print(constants.NOT_NULL_LIMIT_DATE)
                elif e.diag.column_name == 'status':
                    print(constants.NOT_NULL_STATUS)
                elif e.diag.column_name == 'priority':
                    print(constants.NOT_NULL_PRIORITY)
                else:
                    print(constants.GENERAL_NOT_NULL)
            elif e.pgcode == psycopg2.errorcodes.INVALID_DATETIME_FORMAT:
                print(constants.INVALID_DATETIME)
            elif e.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION:
                print(constants.INSERT_TODO_DUPLICATED_TITLE.format(title=title))
            elif e.pgcode == psycopg2.errorcodes.INVALID_TEXT_REPRESENTATION:
                if e.diag.column_name == 'status':
                    print(constants.INVALID_STATUS_FORMAT)
                elif e.diag.column_name == 'priority':
                    print(constants.INVALID_PRIORITY_FORMAT)
                else:
                    print(constants.GENERAL_INVALID_FORMAT)
            elif e.pgcode == psycopg2.errorcodes.DATETIME_FIELD_OVERFLOW:
                print(constants.OVERFLOW_DATETIME)
            elif e.pgcode == psycopg2.errorcodes.NUMERIC_VALUE_OUT_OF_RANGE:
                if e.diag.column_name == 'status':
                    print(constants.OUT_OF_RANGE_STATUS)
                elif e.diag.column_name == 'priority':
                    print(constants.OUT_OF_RANGE_PRIORITY)
                else:
                    print(constants.GENERAL_OUT_OF_RANGE)
            else:
                print(constants.GLOBAL_ERROR.format(
                    pgcode=str(e.pgcode),
                    pgerror=str(e.pgerror)
                ))
            conn.rollback()  # isto ocorre sempre que sucede unha excepción


def insert_users_todo(conn, userid=None, todoid=None, control_tx=True):
    if not userid:
        user = userService.find_user_by_email(conn, control_tx=False)
        if not user:
            conn.rollback()
            return
        userid = user['id']

    if not todoid:
        todo = find_todo_by_title(conn)
        if not todo:
            conn.rollback()
            return
        todoid = todo['todoid']

    sql = constants.SQL_INSERT_USER_TODO

    with conn.cursor() as cur:
        try:
            cur.execute(sql, {'userid': userid, 'todoid': todoid})
            conn.commit()
            print(constants.ADD_USER_TO_TODO_SUCCESS)
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION:
                print(constants.UNIQUE_USER_TODO)
            elif e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                if e.diag.column_name == 'userid':
                    print(constants.NOT_NULL_USER)
                elif e.diag.column_name == 'todoid':
                    print(constants.NOT_NULL_TODO)
                else:
                    print(constants.GENERAL_NOT_NULL)
            else:
                print(constants.GLOBAL_ERROR.format(
                    pgcode=str(e.pgcode),
                    pgerror=str(e.pgerror)
                ))
            if control_tx:
                conn.rollback()  # isto ocorre sempre que sucede unha excepción


def add_line_description(conn):
    todo = find_todo_by_title(conn)
    if todo is None:
        conn.rollback()
        return

    while True:
        additional_description = input(constants.UPDATE_DESCRIPTION_INPUT)
        if additional_description != "":
            break

    sql = constants.SQL_UPDATE_TODO_BY_DESCRIPTION

    with conn.cursor() as cur:
        try:
            cur.execute(sql, {'description': additional_description, 'todoid': todo['todoid']})
            conn.commit()
            print(constants.ADD_LINE_TO_DESCRIPTION_SUCCESS)
        except psycopg2.Error as e:
            print(constants.GLOBAL_ERROR.format(
                pgcode=str(e.pgcode),
                pgerror=str(e.pgerror)
            ))
            conn.rollback()  # isto ocorre sempre que sucede unha excepción


def update_date(conn):
    todo = find_todo_by_title(conn)
    if not todo:
        conn.rollback()
        return

    days = input(constants.UPDATE_DATE_INPUT)

    sql = constants.SQL_UPDATE_TODO_BY_DATE

    with conn.cursor() as cur:
        try:
            cur.execute(sql, {'days': days, 'todoid': todo['todoid']})
            conn.commit()
            print(constants.UPDATE_DATE_SUCCESS)
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.INVALID_DATETIME_FORMAT:
                print(constants.INVALID_DATETIME)
            else:
                print(constants.GLOBAL_ERROR.format(
                    pgcode=str(e.pgcode),
                    pgerror=str(e.pgerror)
                ))
            conn.rollback()  # isto ocorre sempre que sucede unha excepción
