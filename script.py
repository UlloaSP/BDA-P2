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
1 - Crear táboa artigo    2 - Eliminar táboa artigo   3 - Insertar fila
4 - Eliminar fila         5 - Ver fila                6 - Filas con prezo maior
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


def show_all_users(conn):
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
                print(e.diag)
                if e.diag.column_name == 'userid':
                    print("user id")
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
            show_all_users(conn)


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
