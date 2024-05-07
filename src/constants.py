HOST = 'localhost'
USER = 'ulloa'
PASSWORD = '3821'
DB = 'bd'
SQL_CREATE_TABLES = 'CreateTables.sql'
MENU_TEXT = """
-- MENÚ --
1 - Insertar usuario
2 - Mostrar todos os usuarios
3 - Buscar usuario por nome
4 - Buscar usuario por email
5 - Ver fila
6 - Filas con prezo maior
7 - Insertar ToDo
8 - Buscar ToDo por Id
9 - Buscat ToDo por título
q - Saír
"""

TRY_CONNECTION = 'Conectando a PosgreSQL...'
SUCCESSFULL_CONNECTION = 'Conectado.'
FAILED_CONNECTION = 'Erro de conexión:'
TERMINATING_CONNECTION = 'Desconectando de PosgreSQL.'
TERMINATED_CONNECTION = 'Desconectado.'

CREATING_TABLES = 'Creando Taboas'
CREATED_TABLES = 'Taboas Creadas Correctamente'
DUPLICATED_TABLES = 'As taboas xa foron creadas anteriormente. Non se crean.'

ERROR = 'Erro: '
INVALID_OPTION = 'Opción no válida. Por favor, elige una opción del menú.'
VALID_OPTIONS = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
GLOBAL_ERROR = "Erro: {pgcode} - {pgerror}"

NON_EXISTENT_TODO_SEARCH_BY_ID = "O ToDo con id: {id} non existe."
NON_EXISTENT_TODO_SEARCH_BY_TITLE = "O ToDo con título: {title} non existe."
NON_EXISTENT_USER_SEARCH_BY_NAME = "O usuario con nome {name} non existe"
NON_EXISTENT_USER_SEARCH_BY_EMAIL = "O usuario con email {email} non existe"
DEFAULT_INPUT = 'Opción> '
FIND_TODO_BY_ID_INPUT = 'Id del ToDo: '
FIND_TODO_BY_TITLE_INPUT = 'Título del ToDo: '
NAME_INPUT = "Nome: "
EMAIL_INPUT = "Email: "
PASSWORD_INPUT = "Contrasinal: "

INSERT_USER_SUCCESS = "O usuario foi insertado con éxito."
INSERT_USER_DUPLICATED_NAME = "Xa existe un usuario co nome {name}"
INSERT_USER_DUPLICATED_EMAIL = "Xa existe un usuario co email {email}"
INSERT_USER_NOT_NULL_NAME = "Debe especificarse un nome de usuario"
INSERT_USER_NOT_NULL_EMAIL = "Debe especificarse un correo electrónico"
INSERT_USER_NOT_NULL_PASSWORD = "Debe especificarse un contranisal"

FIND_USERS_SUCCESS = "Atopáronse {number} usuario/s"

USER_INFO_TEMPLATE = ("Id: {userid}, Nome: {name}, Correo: {email}, Contrasinal: {password}, "
                      "Data de rexistro: {registrationdate}")

TODO_INFO_TEMPLATE = ("Id: {todoid}, Titulo: {title}, Descripción: {description}, Fecha de Creación: {creationDate},"
                      "Fecha Límite: {limitDate}, Estado: {status}, Prioridade: {priority}")

SQL_INSERT_USER = """
        insert into "User" (name, email, password, registrationDate)
        values(%(name)s, %(email)s, %(password)s, CURRENT_TIMESTAMP)
    """

SQL_FIND_USERS = """
        select *
        from "User"
        """

SQL_FIND_USER_BY_NAME = """
        select *
        from "User"
        where name = %s
        """

SQL_FIND_USER_BY_EMAIL = """
        select *
        from "User"
        where email = %s
        """

SQL_DELETE_USER = """
        delete from "User" where email = %(email)s
    """

SQL_UPDATE_PASSWORD = """
        update "User"
        set password = %(password)s
        where email = %(email)s
        """

SQL_INSERT_TODO = """
        insert into todo (title, description, limitdate, status, priority, creationdate)
        values(%(title)s, %(description)s, %(limitdate)s, %(status)s, %(priority)s, CURRENT_TIMESTAMP)
    """

SQL_INSERT_USER_TODO = """
        insert into usertodo (userid, todoid)
        values(%(userid)s, %(todoid)s)
        """

SQL_FIND_TODO_BY_ID = """
        select * from todo where todoid = %s
"""

SQL_FIND_TODO_BY_TITLE = """
        select * from todo where title = %s
"""