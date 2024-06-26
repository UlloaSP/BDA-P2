import constants
import databaseService
import todoService
import userService


def menu(conn):
    while True:
        print(constants.MENU_TEXT)
        opcion = input(constants.DEFAULT_INPUT)

        if opcion == 'q':
            break
        elif opcion in constants.VALID_OPTIONS:
            opcion = int(opcion)
            if opcion == 1:
                userService.insert_user(conn)
            elif opcion == 2:
                userService.find_users(conn)
            elif opcion == 3:
                userService.find_user_by_name(conn)
            elif opcion == 4:
                userService.find_user_by_email(conn)
            elif opcion == 5:
                userService.delete_user_complete(conn)
            elif opcion == 6:
                userService.update_password(conn)
            elif opcion == 7:
                todoService.insert_todo(conn)
            elif opcion == 8:
                todoService.find_todo_by_id(conn)
            elif opcion == 9:
                todoService.find_todo_by_title(conn)
            elif opcion == 10:
                todoService.add_line_description(conn)
            elif opcion == 11:
                todoService.insert_users_todo(conn)
            elif opcion == 12:
                todoService.update_date(conn)
        else:
            print(constants.INVALID_OPTION)
        input()


def main():
    try:
        conn = databaseService.connect_db()
        databaseService.create_tables(conn)
        while True:
            cond = input(constants.DELETE)
            if cond == 'True' or cond == 'False':
                break

            menu(conn)
            if cond == "True":
                databaseService.drop_tables(conn)
            databaseService.disconnect_db(conn)
    except KeyboardInterrupt:
        print(constants.USER_INTERRUPTION)


if __name__ == '__main__':
    main()
