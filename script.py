import sys
import psycopg2
import psycopg2.errorcodes
import psycopg2.extras

HOST = 'localhost'
USER = 'mon'
PASSWORD = 'clave'
DB = 'mon'
SQL_CREATE_TABLES = 'CreateTables.sql'
MENU_TEXT = """
-- MENÚ --
1 - Insertar usuario    2 - Mostrar todos os usuarios   3 - Buscar usuario por nome
4 - Buscar usuario por email         5 - Ver fila                6 - Filas con prezo maior
7 - Ver todas as filas    8 - Actualizar fila         9 - Actualizar prezo
q - Saír
"""


def create_tables(conn):
    with (open(SQL_CREATE_TABLES)) as archivo:
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
                print(f"Erro: {e.pgcode} - {e.pgerror}")  # esto o poñemos para os erros que non coñecemos
            conn.rollback()


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
                if e.diag.column_name == 'name':
                    print(f"Debe especificarse un nome de usuario")
                if e.diag.column_name == 'email':
                    print(f"Debe especificarse un correo electrónico")
                if e.diag.column_name == 'password':
                    print(f"Debe especificarse un contranisal")
            else:
                print(f"Erro: {e.pgcode} - {e.pgerror}")
            conn.rollback()  # isto ocorre sempre que sucede unha excepción


def insert_todo(conn):
    # TODO - cambiar transaccionalidad. Si falla el segundo insert, que se haga un rollback del primero
    userId = find_user_by_email(conn)['id']
    title = input("Título: ")
    description = input("Descripción: ")
    limitdate = input("Data límite: ")
    status = input("Estatus: ")
    priority = input("Prioridade: ")

    sql = """
        insert into todo (title, description, limitdate, status, priority, creationdate)
        values(%(title)s, %(description)s, %(limitdate)s, %(status)s, %(priority)s, CURRENT_TIMESTAMP)
    """

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

    sql = """
        insert into usertodo (userid, todoid)
        values(%(userid)s, %(todoid)s)
        """

    with conn.cursor() as cur:
        try:
            cur.execute(sql, {'userid': userId, 'todoid': 1})
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


def connect_db():
    try:
        conn = psycopg2.connect(host=HOST, user=USER, password=PASSWORD, dbname=DB)
        conn.autocommit = False
        return conn
    except Exception as e:
        print(f"Erro de conexión: {e}")
        sys.exit(1)  # Un programa sólo devuelve 0 en caso de éxito


## ------------------------------------------------------------
def disconnect_db(conn):
    conn.commit()
    # Si matamos la conexión cuando hemos hecho un insert. Confirmamos la última transacción antes de cerrar

    conn.close()


def menu(conn):
    """
    Imprime un menú de opcións, solicita a opción e executa a función asociada.
    'q' para saír.
    """
    while True:
        print(MENU_TEXT)
        tecla = input('Opción> ')
        if tecla == 'q':
            break
        elif tecla == '1':
            insert_user(conn)
        elif tecla == '2':
            find_users(conn)
        elif tecla == '3':
            find_user_by_name(conn)
        elif tecla == '4':
            find_user_by_email(conn)
        elif tecla == '5':
            delete_user(conn)
        elif tecla == '6':
            update_password(conn)
        elif tecla == '7':
            insert_todo(conn)
        input("Pulsa Enter...")


def main():
    """
    Función principal. Conecta á bd e executa o menú.
    Cando sae do menú, desconecta da bd e remata o programa
    """
    print('Conectando a PosgreSQL...')
    conn = connect_db()
    print(conn)
    print('Conectado.')
    create_tables(conn)
    menu(conn)
    disconnect_db(conn)


## ------------------------------------------------------------

if __name__ == '__main__':
    main()
