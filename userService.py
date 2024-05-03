import psycopg2
from psycopg2 import extras, errorcodes


def insert_user(conn):
    name = input("Nome: ")
    email = input("Email: ")
    password = input("Contrasinal: ")

    sql = """
        insert into "User" (name, email, password, registrationDate)
        values(%(name)s, %(email)s, %(password)s, CURRENT_TIMESTAMP)
    """

    with conn.cursor() as cur:
        try:
            cur.execute(sql, {'name': name, 'email': email, 'password': password})
            conn.commit()
            print("O usuario foi insertado con éxito.")
        except psycopg2.Error as e:
            print("No commit")
            if e.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION:
                print(e.diag.column_name)
                if e.diag.column_name == 'name':
                    print(f"Xa existe un usuario co nome {name}")
                if e.diag.column_name == 'email':
                    print(f"Xa existe un usuario co email {email}")
            elif e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                if e.diag.column_name == 'mame':
                    print(f"Debe especificarse un nome de usuario")
                if e.diag.column_name == 'email':
                    print(f"Debe especificarse un correo electrónico")
                if e.diag.column_name == 'password':
                    print(f"Debe especificarse un contranisal")
            else:
                print(f"Erro: {e.pgcode} - {e.pgerror}")
            conn.rollback()  # isto ocorre sempre que sucede unha excepción


def find_users(conn):
    sql = """
        select *
        from "User"
        """
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        # cursor con diccionario para poder buscar los nombres de las columnas de la fila
        try:
            cur.execute(sql)
            row = cur.fetchone()  # devuelve las filas que ha encontrado en el select
            while row:
                print(f"Id: {row['userid']}, Nome: {row['name']}, Correo: {row['email']}, "
                      f"Contrasinal: {row['password']}, Data de rexistro: {row['registrationdate']}")
                row = cur.fetchone()
            print(f"Atopáronse {cur.rowcount} usuarios")
            conn.commit()
        except psycopg2.Error as e:
            print(f"Erro: {e.pgcode} - {e.pgerror}")
            conn.rollback()  # isto ocorre sempre que sucede unha excepción


def find_user_by_name(conn):  # Si no se pasa control_tx entonces toma el valor True
    name = input("Nome: ")

    sql = """
        select *
        from "User"
        where name = %s
        """

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        # cursor con diccionario para poder buscar los nombres de las columnas de la fila
        try:
            cur.execute(sql, (name,))
            row = cur.fetchone()  # devuelve la fila que ha encontrado en el select
            if row:  # if row is not None
                print(f"Id: {row['userid']}, Nome: {row['name']}, Correo: {row['email']}, "
                      f"Contrasinal: {row['password']}, Data de rexistro: {row['registrationdate']}")
            else:
                print(f"O usuario con nome {name} non existe")
            conn.commit()
        except psycopg2.Error as e:
            print(f"Erro: {e.pgcode} - {e.pgerror}")
            conn.rollback()  # isto ocorre sempre que sucede unha excepción


def find_user_by_email(conn, control_tx=True):
    """
    :param conn: a conexión aberta á bd
    :param control_tx: Indica se a función fará control transaccional (commit/rollback)
    """
    email = input("Correo: ")

    sql = """
        select *
        from "User"
        where email = %s
        """
    retval = None
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        # cursor con diccionario para poder buscar los nombres de las columnas de la fila
        try:
            cur.execute(sql, (email,))
            row = cur.fetchone()  # devuelve la fila que ha encontrado en el select
            if row:  # if row is not None
                retval = {'id': row['userid'], 'name': row['name'], 'email': row['email'],
                          'password': row['password'], 'registrationDate': row['registrationdate']}
                print(f"Id: {row['userid']}, Nome: {row['name']}, Correo: {row['email']}, "
                      f"Contrasinal: {row['password']}, Data de rexistro: {row['registrationdate']}")
            else:
                print(f"O usuario co email {email} non existe")
            conn.commit()
        except psycopg2.Error as e:
            print(f"Erro: {e.pgcode} - {e.pgerror}")
            if control_tx:
                conn.rollback()
    return retval


def delete_user(conn):
    email = input("Correo: ")

    sql = """
        delete from "User" where email = %(email)s
    """
    with conn.cursor() as cur:
        try:
            cur.execute(sql, {'email': email})
            if cur.rowcount == 0:
                print(f"O usuario con correo {email} non existe")
            else:
                print("O usuario foi eliminado con éxito.")
        except psycopg2.Error as e:
            print(f"Erro: {e.pgcode} - {e.pgerror}")
            conn.rollback()  # isto ocorre sempre que sucede unha excepción


def update_password(conn):
    user = find_user_by_email(conn, control_tx=False)

    if user is None:
        conn.rollback()
        return

    password = input("Novo contrasinal: ")
    if password == "":
        password = None

    sql = """
        update "User"
        set password = %(password)s
        where email = %(email)s
        """

    with conn.cursor() as cur:
        try:
            cur.execute(sql, {'password': password, 'email': user['email']})
            conn.commit()
            print("Contrasinal actualizado")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                print("O contrasinal non pode ser nulo")
            else:
                print(f"Erro: {e.pgcode} - {e.pgerror}")
            conn.rollback()  # isto ocorre sempre que sucede unha excepción