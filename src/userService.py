import psycopg2
from psycopg2 import extras, errorcodes

import constants


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
                    print(constants.INSERT_USER_NOT_NULL_PASSWORD)
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
            cur.execute(sql, (name,))
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


def find_user_by_email(conn, control_tx=True):
    email = input("Correo: ")
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


def delete_user(conn):
    email = input("Correo: ")
    sql = constants.SQL_DELETE_USER

    with conn.cursor() as cur:
        try:
            cur.execute(sql, {'email': email})
            if cur.rowcount == 0:
                print(f"O usuario con correo {email} non existe")
            else:
                print("O usuario foi eliminado con éxito.")
        except psycopg2.Error as e:
            print(constants.GLOBAL_ERROR.format(
                pgcode=str(e.pgcode),
                pgerror=str(e.pgerror)
            ))
            conn.rollback()  # isto ocorre sempre que sucede unha excepción


def update_password(conn):
    user = find_user_by_email(conn, control_tx=False)

    if user is None:
        conn.rollback()
        return

    password = input("Novo contrasinal: ")
    if password == "":
        password = None

    sql = constants.SQL_UPDATE_PASSWORD

    with conn.cursor() as cur:
        try:
            cur.execute(sql, {'password': password, 'email': user['email']})
            conn.commit()
            print("Contrasinal actualizado")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                print("O contrasinal non pode ser nulo")
            else:
                print(constants.GLOBAL_ERROR.format(
                    pgcode=str(e.pgcode),
                    pgerror=str(e.pgerror)
                ))
            conn.rollback()  # isto ocorre sempre que sucede unha excepción
