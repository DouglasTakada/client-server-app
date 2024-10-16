import socket
import os

def receive_file(conn):
    file = conn.recv(1024).decode() # grab filename
    conn.send("filename".encode()) # send acknowledgement we got filename
    print("received filename: "+ file)
    with open(file, 'w') as f: # make and open the filename in server folder
        data = conn.recv(1024).decode()
        f.write(data)
    print('Received successfully!\n New filename is:', file)

def send_file(client_socket):
    filename = input("Enter the filename you would like to send:\n")
    try: 
        # check if file exists
        fi = open(filename, "r") 
        data = fi.read() 
        if not data:
            print("no data in file")
        else:
            # send file, acutal filename then wait for filename back
            client_socket.send("filename".encode())
            client_socket.send(filename.encode())
            while client_socket.recv(1024).decode() != "filename":
                pass # wait for filename 
            print("filename successfully received from server\nSending file data...")
            while data: 
                client_socket.send(str(data).encode()) 
                data = fi.read() 
            # File is closed after data is sent 
            fi.close()
    except IOError: 
        print('You entered an invalid filename!\nPlease enter a valid name')

def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = input(" -> ")  # take input

    while message.lower().strip() != 'bye':

        if message.lower().strip() == 'send file':
            send_file(client_socket)
            message = ""
            continue

        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response
        if data == "filename": # receive filename 
            receive_file(client_socket)

        print('Received from server: ' + data)  # show in terminal

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection

if __name__ == '__main__':
    client_program()