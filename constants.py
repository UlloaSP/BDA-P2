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
7 - Ver todas as filas
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
VALID_OPTIONS = ('1', '2', '3', '4', '5', '6', '7')

DEFAULT_INPUT = 'Opción> '

USER_INFO_TEMPLATE = ("Id: {userid}, Nome: {name}, Correo: {email}, Contrasinal: {password}, "
                      "Data de rexistro: {registrationdate}")
