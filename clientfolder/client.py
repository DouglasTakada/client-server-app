import socket
import threading

def receive_file(conn):
    file = conn.recv(1024).decode() # grab filename
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
            print("filename successfully received from server\nSending file data...")
            while data: 
                client_socket.send(str(data).encode()) 
                data = fi.read() 
            # File is closed after data is sent 
            fi.close()
    except IOError: 
        print('You entered an invalid filename!\nPlease enter a valid name')

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

def receive(conn,stop):
    while conn and not stop.is_set():
        data = conn.recv(1024).decode()  # receive response
        if data == "filename":
            receive_file(conn)
        elif str(data) == "bye":
            conn.send("later gator!".encode())
            stop.set()
            break
        else:
            print('Received from server: ' + data)  # show in terminal

def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

        # Create two threads: one for sending and one for receiving
    stop_event = threading.Event()
    send_thread = threading.Thread(target=send, args=(client_socket,stop_event,))
    receive_thread = threading.Thread(target=receive, args=(client_socket,stop_event,))

    
    send_thread.start()
    receive_thread.start()

    send_thread.join()
    receive_thread.join()

    client_socket.close()  # close the connection

if __name__ == '__main__':
    client_program()