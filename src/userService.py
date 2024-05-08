import psycopg2
from psycopg2 import extras, errorcodes

import constants
import todoService


def insert_user(conn):
    name = input(constants.NAME_INPUT)
    email = input(constants.EMAIL_INPUT)
    password = input(constants.PASSWORD_INPUT)
    sql = constants.SQL_INSERT_USER

    with conn.cursor() as cur:
        try:
            cur.execute(sql, {'name': name, 'email': email, 'password': password})
            conn.commit()
            print(constants.INSERT_USER_SUCCESS)
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION:
                print(e.diag.column_name)
                if e.diag.column_name == 'name':
                    print(constants.INSERT_USER_DUPLICATED_NAME.format(name=name))
                if e.diag.column_name == 'email':
                    print(constants.INSERT_USER_DUPLICATED_EMAIL.format(email=email))
            elif e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                if e.diag.column_name == 'name':
                    print(constants.INSERT_USER_DUPLICATED_NAME)
                if e.diag.column_name == 'email':
                    print(constants.INSERT_USER_DUPLICATED_EMAIL)
                if e.diag.column_name == 'password':
                    print(constants.NOT_NULL_PASSWORD)
            else:
                print(constants.GLOBAL_ERROR.format(
                    pgcode=str(e.pgcode),
                    pgerror=str(e.pgerror)
                ))
            conn.rollback()


def find_users(conn):
    sql = constants.SQL_FIND_USERS
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        try:
            cur.execute(sql)
            row = cur.fetchone()
            while row:
                print(constants.USER_INFO_TEMPLATE.format(
                    userid=row['userid'],
                    name=row['name'],
                    email=row['email'],
                    password=row['password'],
                    registrationdate=row['registrationdate']
                ))
                row = cur.fetchone()
            print(constants.FIND_USERS_SUCCESS.format(number=cur.rowcount))
            conn.commit()
        except psycopg2.Error as e:
            print(constants.GLOBAL_ERROR.format(
                pgcode=str(e.pgcode),
                pgerror=str(e.pgerror)
            ))
            conn.rollback()  # isto ocorre sempre que sucede unha excepción


def find_user_by_name(conn):  # Si no se pasa control_tx entonces toma el valor True
    name = input(constants.NAME_INPUT)

    sql = constants.SQL_FIND_USER_BY_NAME

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        # cursor con diccionario para poder buscar los nombres de las columnas de la fila
        try:
            cur.execute(sql, {'name': name})
            row = cur.fetchone()  # devuelve la fila que ha encontrado en el select
            if row:  # if row is not None
                print(constants.USER_INFO_TEMPLATE.format(
                    userid=row['userid'],
                    name=row['name'],
                    email=row['email'],
                    password=row['password'],
                    registrationdate=row['registrationdate']
                ))
            else:
                print(constants.NON_EXISTENT_USER_SEARCH_BY_NAME.format(name=name))
            conn.commit()
        except psycopg2.Error as e:
            print(constants.GLOBAL_ERROR.format(
                pgcode=str(e.pgcode),
                pgerror=str(e.pgerror)
            ))
            conn.rollback()  # isto ocorre sempre que sucede unha excepción


def find_user_by_email(conn, control_tx=True, email=None):
    if not email:
        email = input(constants.EMAIL_INPUT)

    sql = constants.SQL_FIND_USER_BY_EMAIL
    retval = None

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        # cursor con diccionario para poder buscar los nombres de las columnas de la fila
        try:
            cur.execute(sql, (email,))
            row = cur.fetchone()  # devuelve la fila que ha encontrado en el select
            if row:  # if row is not None
                retval = {'id': row['userid'], 'name': row['name'], 'email': row['email'],
                          'password': row['password'], 'registrationDate': row['registrationdate']}

                print(constants.USER_INFO_TEMPLATE.format(
                    userid=row['userid'],
                    name=row['name'],
                    email=row['email'],
                    password=row['password'],
                    registrationdate=row['registrationdate']
                ))

            else:
                print(constants.NON_EXISTENT_USER_SEARCH_BY_EMAIL.format(email=email))
            conn.commit()
        except psycopg2.Error as e:
            print(constants.GLOBAL_ERROR.format(
                pgcode=str(e.pgcode),
                pgerror=str(e.pgerror)
            ))
            if control_tx:
                conn.rollback()
    return retval


def delete_user(conn, email=None):
    if not email:
        email = input(constants.EMAIL_INPUT)

    sql = constants.SQL_DELETE_USER

    with conn.cursor() as cur:
        try:
            cur.execute(sql, {'email': email})
            if cur.rowcount == 0:
                print(constants.NON_EXISTENT_USER_SEARCH_BY_EMAIL.format(email=email))
            else:
                print(constants.DELETE_USER_SUCCESS)
        except psycopg2.Error as e:
            print(constants.GLOBAL_ERROR.format(
                pgcode=str(e.pgcode),
                pgerror=str(e.pgerror)
            ))
            conn.rollback()  # isto ocorre sempre que sucede unha excepción


def delete_user_complete(conn):
    user = find_user_by_email(conn)

    # Buca ids de Todos del usuario
    sql = constants.SQL_FIND_USER_BY_ID
    todos_id_list = []

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        # cursor con diccionario para poder buscar los nombres de las columnas de la fila
        try:
            cur.execute(sql, {'userid': user['id']})
            row = cur.fetchone()
            while row:
                todos_id_list.append(row['todoid'])
                row = cur.fetchone()
        except psycopg2.Error as e:
            print(constants.GLOBAL_ERROR.format(
                pgcode=str(e.pgcode),
                pgerror=str(e.pgerror)
            ))

    # Borra la entrada de UserTodo con ID=userId
    sql = constants.SQL_DELETE_USER_BY_ID
    with conn.cursor() as cur:
        try:
            cur.execute(sql, {'userid': user['id']})
            if cur.rowcount == 0:
                print(constants.NON_EXISTENT_USER_SEARCH_BY_ID.format(userid=user['id']))
            else:
                print(constants.DELETE_USER_SUCCESS)
        except psycopg2.Error as e:
            print(constants.GLOBAL_ERROR.format(
                pgcode=str(e.pgcode),
                pgerror=str(e.pgerror)
            ))
            conn.rollback()  # isto ocorre sempre que sucede unha excepción
    # ---------------------------------------------

    delete_user(conn, user['email'])

    # Buscar todos los Todos y (gracias a la lista de ids) borrarlos si no están en la relación
    sql = constants.SQL_FIND_TODOS_BY_USER

    sql_remove = constants.SQL_DELETE_TODO_BY_ID

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        # cursor con diccionario para poder buscar los nombres de las columnas de la fila
        try:
            for todoid in todos_id_list:
                cur.execute(sql, {'todoid': int(todoid)})
                row = cur.fetchone()
                print(row)
                if not row:
                    cur.execute(sql_remove, {'todoid': int(todoid)})
                else:
                    while row:
                        if cur.rowcount >= 0:
                            cur.execute(sql_remove, {'todoid': int(todoid)})
                            if cur.rowcount != 1:
                                print(constants.DELETE_TODO_ERROR.format(todoid=todoid))
                        row = cur.fetchone()
                conn.commit()
        except psycopg2.Error as e:
            print(constants.GLOBAL_ERROR.format(
                pgcode=str(e.pgcode),
                pgerror=str(e.pgerror)
            ))


def update_password(conn):
    user = find_user_by_email(conn, control_tx=False)

    if user is None:
        conn.rollback()
        return

    password = input(constants.NEW_PASSWORD_INPUT)
    if password == "":
        password = None

    sql = constants.SQL_UPDATE_PASSWORD

    with conn.cursor() as cur:
        try:
            cur.execute(sql, {'password': password, 'email': user['email']})
            conn.commit()
            print(constants.UPDATE_PASSWORD_SUCCESS)
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                print(constants.NOT_NULL_PASSWORD)
            else:
                print(constants.GLOBAL_ERROR.format(
                    pgcode=str(e.pgcode),
                    pgerror=str(e.pgerror)
                ))
            conn.rollback()  # isto ocorre sempre que sucede unha excepción
