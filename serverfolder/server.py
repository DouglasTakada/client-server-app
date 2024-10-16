import socket
import threading

def receive_file(conn):
    file = conn.recv(1024).decode() # grab filename
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
            print("filename successfully received from server\nSending file data...")
            while data: 
                conn.send(str(data).encode()) 
                data = fi.read() 
            # File is closed after data is sent 
            fi.close()
    except IOError: 
        print('You entered an invalid filename!\nPlease enter a valid name')

def receive(conn,stop):
    # receive data stream. it won't accept data packet greater than 1024 bytes
    while not stop.is_set():
        data = conn.recv(1024).decode()
        if str(data) == "filename": # receive filename 
            receive_file(conn)
        elif str(data) == "bye":
            conn.send("later gator!".encode())
            stop.set()
            break
        else:
            print("from connected user: " + str(data))

def send(conn,stop):
    message = ""
    while message.lower().strip() != 'bye':
        message = input(" -> ")  # take input
        if message.lower().strip() == 'send file':
            send_file(conn)
            message = ""
            continue
        conn.send(message.encode())  # send message
    stop.set()

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

            # Create two threads: one for sending and one for receiving
    stop_event = threading.Event()
    send_thread = threading.Thread(target=send, args=(conn,stop_event,))
    receive_thread = threading.Thread(target=receive, args=(conn,stop_event,))

    send_thread.start()
    receive_thread.start()

    send_thread.join()
    receive_thread.join()

    conn.close()  # close the connection

if __name__ == '__main__':
    server_program()