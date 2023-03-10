import connection
import manager

def main():

    def line_extract(line: str, target_value):

        sym_number = line.find('=')
        if target_value == line[:sym_number]:
            return line[sym_number + 1:]
        else:
            return None

    CONFIG_FILE = './config.txt'
    print('Config initialization...')

    try:
        file = open(CONFIG_FILE, 'r')
        TOKEN = str(line_extract(file.readline().rstrip('\n'), 'token'))
        FOLDER = str(line_extract(file.readline(), 'folder'))

    except:
        print('Config reading error')
        return False

    finally:
        print(f'Token: ...{(TOKEN[40:])}')
        print(f'Directory: {FOLDER}')
        file.close()

    conn = connection.Connection(TOKEN, FOLDER)
    if conn.successfully:
        print("Successfully connected to YaDisk")
    else:
        print("Connection to YaDisk FAILED")
        return

    mgr = manager.Manager(conn)
    mgr.start_process()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('An error occurred while executing the program')
        print(e)
input("Enter to exit...")