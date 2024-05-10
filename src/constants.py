HOST = 'Host: '
USER = 'Usuario: '
PASSWORD = 'Contraseña: '
DB = 'Base de Datos: '
SQL_CREATE_TABLES = './CreateTables.sql'
DELETE = "Desea que al terminar se eliminen las tablas de la BD? (True or False)"
MENU_TEXT = """
-- MENÚ --
01 - Insertar usuario               02 - Mostrar todos los usuarios 
03 - Buscar usuario por nombre      04 - Buscar usuario por email
05 - Eliminar usuario               06 - Actualizar contraseña                 
07 - Insertar tarea                 08 - Buscar tarea por id
09 - Buscar tarea por título        10 - Actualizar descripción de una tarea 
11 - Añadir usuario a una tareaa    12 - Actualizar fecha límite de tarea
q - Salir
"""

TRY_CONNECTION = 'Conectando a PosgreSQL...'
SUCCESSFULL_CONNECTION = 'Conectado.'
FAILED_CONNECTION = 'Error de conexión: {e}'
TERMINATING_CONNECTION = 'Desconectando de PosgreSQL.'
TERMINATED_CONNECTION = 'Desconectado.'
USER_INTERRUPTION = "\nOperación interrumpida por el usuario."

DELETING_TABLES = 'Eliminando Tablas'
DELETED_TABLES = 'Tablas Eliminadas Correctamente'
CREATING_TABLES = 'Creando Tablas'
CREATED_TABLES = 'Tablas Creadas Correctamente'
DUPLICATED_TABLES = 'Las tablas ya existen. No se crean'
NON_EXISTENT_TABLES = 'Las tablas no existen. No se eliminan'

ERROR = 'Error: '
INVALID_OPTION = 'Opción no válida. Por favor, elige una opción del menú.'
VALID_OPTIONS = ('01', '02', '03', '04', '05', '06', '07', '08', '09',
                 '1', '2', '3', '4', '5', '6', '7', '8', '9',
                 '10', '11', '12')
GLOBAL_ERROR = "Erro: {pgcode} - {pgerror}"

NON_EXISTENT_TODO_SEARCH_BY_ID = "La con id: {id} no existe."
NON_EXISTENT_TODO_SEARCH_BY_TITLE = "La tarea con título: {title} no existe."
NON_EXISTENT_USER_SEARCH_BY_ID = "El usuario con userId: {userid} no tiene tareas asignadas."
NON_EXISTENT_USER_SEARCH_BY_NAME = "El usuario con nombre {name} no existe"
NON_EXISTENT_USER_SEARCH_BY_EMAIL = "El usuario con email {email} no existe"

DELETE_TODO_ERROR = "Error al eliminar tarea con id = {todoid}"

DEFAULT_INPUT = 'Opción> '
FIND_TODO_BY_ID_INPUT = 'Id de la tarea: '
FIND_TODO_BY_TITLE_INPUT = 'Título de la tarea: '
NAME_INPUT = "Nombre: "
EMAIL_INPUT = "Email: "
PASSWORD_INPUT = "Contraseña: "
NEW_PASSWORD_INPUT = "Nueva Contraseña: "
TITLE_INPUT = "Título e la tarea: "
DESCRIPTION_INPUT = "Descripción: "
LIMIT_DATE_INPUT = "Fecha Límite: "
STATUS_INPUT = "Estado: "
PRIORITY_INPUT = "Prioridad: "
UPDATE_DESCRIPTION_INPUT = "Añade una linea a la descripción: "
UPDATE_DATE_INPUT = "Indique la cantidad de días en los que desea posponer la fecha límite: "
NUMERIC_VALUE_OUT_OF_RANGE = "El id proporcionado está fuera del rango permitido."
INSERT_TODO_SUCCESS = "La tarea fue creada correctamente."
INSERT_USER_SUCCESS = "El usuario fue insertado con éxito."
INSERT_USER_DUPLICATED_NAME = "Xa existe un usuario con el nombre {name}"
INSERT_USER_DUPLICATED_EMAIL = "Xa existe un usuario con el email {email}"
INSERT_USER_NOT_NULL_NAME = "Debe especificarse un nombre de usuario"
INSERT_USER_NOT_NULL_EMAIL = "Debe especificarse un correo electrónico"
NOT_NULL_PASSWORD = "Debe especificarse una contraseña"
NOT_NULL_TITLE = "Debe especificarse un título"
NOT_NULL_DESCRIPTION = "Debe especificarse una descripción"
NOT_NULL_LIMIT_DATE = "Debe especificarse una fecha límite"
NOT_NULL_STATUS = "Debe especificarse un estado"
NOT_NULL_PRIORITY = "Debe especificarse una prioridad"
NOT_NULL_USER = "Debe especificarse un usuario."
NOT_NULL_TODO = "Debe especificarse una tarea."
INVALID_STATUS_FORMAT = "El formato del estado no es válido."
INVALID_PRIORITY_FORMAT = "El formato de la prioridad no es válido."
OUT_OF_RANGE_PRIORITY = "La prioridad indicada está fuera de rango."
OUT_OF_RANGE_STATUS = "El estado indicado está fuera de rango."
UNIQUE_USER_TODO = "Este usuario ya tiene asignada esta tarea."
INVALID_DATETIME = "El formato de la fecha no es válido."
OVERFLOW_DATETIME = "La fecha proporcionada no es válida."
FIND_USERS_SUCCESS = "Se encontraron {number} usuario/s"
DELETE_USER_SUCCESS = "El usuario fue eliminado correctamente."
UPDATE_PASSWORD_SUCCESS = "Contraseña actualizada correctamente."
ADD_USER_TO_TODO_SUCCESS = "Usuario agregado correctamente a la tarea."
INVALID_ID_FORMAT = "El formato del id proporcionado no es válido."
INSERT_TODO_DUPLICATED_TITLE = "Ya existe una tarea con título {title}"
ADD_LINE_TO_DESCRIPTION_SUCCESS = "La descripción se ha actualizado correctamente."
UPDATE_DATE_SUCCESS = "La fecha se ha actualizado correctamente."

GENERAL_NOT_NULL = "Algún valor está vacio."
GENERAL_UNIQUE = "Algún campo no es válido porque ya figura en la BBDD (debe ser único)."
GENERAL_INVALID_FORMAT = "El formato de algún campo no es válido."
GENERAL_OUT_OF_RANGE = "Algún campo numérico está fuera de rango."


USER_INFO_TEMPLATE = ("Id: {userid}, Nombre: {name}, Correo: {email}, Contraseña: {password}, "
                      "Fehca de Alta: {registrationdate}")

TODO_INFO_TEMPLATE = ("Id: {todoid}, Titulo: {title}, Descripción: {description}, Fecha de Creación: {creationDate},"
                      "Fecha Límite: {limitDate}, Estado: {status}, Prioridad: {priority}")

SQL_INSERT_USER = """
        insert into "User" (name, email, password, registrationDate)
        values(%(name)s, %(email)s, %(password)s, CURRENT_TIMESTAMP)
    """

SQL_FIND_USERS = """
        select *
        from "User"
        """
SQL_FIND_TODOS_BY_USERID = """
    select todoId from UserTodo where userId = %(userid)s
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

SQL_DELETE_USERTODO_BY_USERID = """
    delete from UserTodo where userId = %(userid)s
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

SQL_UPDATE_TODO_BY_DATE = """
    UPDATE Todo
    SET limitdate = limitdate + INTERVAL %(days)s DAY
    WHERE todoid = %(todoid)s
    """

SQL_UPDATE_TODO_BY_DESCRIPTION = """
    UPDATE Todo SET description = CONCAT(description, %(description)s) WHERE todoid = %(todoid)s
    """

SQL_FIND_TODOS_BY_USER = """
    select * from UserTodo where todoid = %(todoid)s
    """

SQL_DELETE_TODO_BY_ID = """
    delete from Todo where todoid = %(todoid)s
    """

SQl_DROP_TABLES = """
    delete from UserTodo;
    drop table UserTodo;
    delete from Todo;
    drop table Todo;
    delete from "User";
    drop table "User";
"""
