import constants
import databaseService
import todoService
import userService


def menu(conn):
    while True:
        print(constants.MENU_TEXT)
        tecla = input('Opción> ')
        if tecla == 'q':
            break
        elif tecla == '1':
            userService.insert_user(conn)
        elif tecla == '2':
            userService.find_users(conn)
        elif tecla == '3':
            userService.find_user_by_name(conn)
        elif tecla == '4':
            userService.find_user_by_email(conn)
        elif tecla == '5':
            userService.delete_user(conn)
        elif tecla == '6':
            userService.update_password(conn)
        elif tecla == '7':
            todoService.insert_todo(conn)
        input("Pulsa Enter...")


def main():
    print('Conectando a PosgreSQL...')
    conn = databaseService.connect_db()
    print(conn)
    print('Conectado.')
    databaseService.create_tables(conn)
    menu(conn)
    databaseService.disconnect_db(conn)


if __name__ == '__main__':
    main()
