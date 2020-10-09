import socket
import threading
import traceback

class Server:
    def __init__(self, port):
        self.m_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = port

        self.m_socket.bind((self.host, self.port))
        print(f"Listening at {self.host}:{self.port}...")
        self.m_socket.listen()
        self.connection, self.address = self.m_socket.accept()
        print(f"Connected to {self.address}!")
        print("Type 'quit' to exit")

        self.receive_thread = threading.Thread(target=self.async_input)
        self.receive_thread.start()
        self.input_thread = threading.Thread(target=self.async_receive)     # Create the 2nd thread
        self.input_thread.start()                                           # and start it..

    def async_receive(self):        # This runs on the main thread
        print("receive thread started!")
        while True:
            try:
                print(self.connection.recv(1024))     # Blocking call. Waits for something to be read
            except Exception as e:
                print(traceback.format_exc())
                break

    def async_input(self):              # Runs on a second separate thread
        print("input thread started!")
        while True:
            text = input()                      # Blocking call. Waits for the input
            print(len(text.encode()))
            self.connection.send(text.encode())
            if text == 'quit':          # Close the connection if quit is typed
                self.connection.close()
                break


class Client:
    def __init__(self, port, hostname):
        self.hostname = hostname
        self.port = port
        self.m_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.m_socket.connect((hostname, port))
        print(f"Connected to {self.hostname}:{self.port}")
        self.receive_thread = threading.Thread(target=self.async_read)
        self.receive_thread.start()

        self.input_thread = threading.Thread(target=self.async_input)  # Create the 2nd thread
        self.input_thread.start()  # and start it..

    def async_read(self):        # This runs on the main thread
        while True:
            try:
                print(self.m_socket.recv(1024))     # Blocking call. Waits for something to be read
            except:
                break

    def async_input(self):              # Runs on a second separate thread
        print("input thread started!")
        while True:
            text = input()                      # Blocking call. Waits for the input
            self.m_socket.send(text.encode())
            if text == 'quit':
                self.m_socket.close()
                break



response = input("Press S to be a server, C to be a client")
if response == "S" or response == "s":
    port_no = int(input("Enter server port number"))
    server = Server(port_no)
elif response == "C" or response == "c":
    port_no = int(input("Enter client port number"))
    destination = input("Enter destination IP")
    client = Client(port_no, destination)
else:
    print("Enter either S or C")
