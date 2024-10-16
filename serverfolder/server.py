import socket

def receive_file(conn):
    file = conn.recv(1024).decode() # grab filename
    conn.send("filename".encode()) # send acknowledgement we got filename
    print("received filename: "+ file)
    with open(file, 'w') as f: # make and open the filename in server folder
        data = conn.recv(1024).decode()
        f.write(data)
    print('Received successfully!\n New filename is:', file)

def send_file(conn):
    filename = input("Enter the filename you would like to send:\n")
    try: 
        # check if file exists
        fi = open(filename, "r") 
        data = fi.read() 
        if not data:
            print("no data in file")
        else:
            # send file, acutal filename then wait for filename back
            conn.send("filename".encode())
            conn.send(filename.encode())
            while conn.recv(1024).decode() != "filename":
                pass # wait for filename 
            print("filename successfully received from server\nSending file data...")
            while data: 
                conn.send(str(data).encode()) 
                data = fi.read() 
            # File is closed after data is sent 
            fi.close()
    except IOError: 
        print('You entered an invalid filename!\nPlease enter a valid name')

def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        if str(data) == "filename": # receive filename 
            receive_file(conn)

        print("from connected user: " + str(data))
        data = input(' -> ')
        if data.lower().strip() == 'send file':
            send_file(conn)
            data = ""
            continue
        conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()