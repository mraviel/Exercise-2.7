import socket
import shutil
import os
import sys
import signal  # Allow socket destruction on Ctrl+C

class Client(object):
    """ The client class """

    def __init__(self, PORT=8800, IP='127.0.0.1'):

        self.PORT = PORT
        self.IP = IP
        self.commands_list = ['TAKE_SCREENSHOT', 'SEND_FILE', 'DIR', 'DELETE', 'COPY', 'EXECUTE', 'EXIT']

    def start(self):
        """ To start the client """

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            client_socket.connect((self.IP, self.PORT))

        except Exception as e:
            print("Error: Could not connect to port {0}".format(self.PORT))
            self.shutdown()
            sys.exit(1)

        self.main(client_socket)

    def shutdown(self):
        """ Shuts down the client """

        try:
            print ("Shuting down the client")
            Client.shutdown(socket.SHUT_RDWR)

        except Exception as e:
            pass  # Pass if socket is already closed

    def valid_request(self, request):
        """Check if the request is valid (is included in the available commands)"""

        for command in self.commands_list:
            if command in request:
                return True
        return False



    def send_request_to_server(self, my_socket, request):
        """Send the request to the server."""

        my_socket.send(request)


    def handle_server_response(self, my_socket, request):
        """Receive the response from the server and handle it, according to the request"""

        data = my_socket.recv(1024)
        print data

    def main(self, client_socket):
        """ The main in the class """

        # print instructions
        print('Welcome to remote computer application. Available commands are:\n')
        print('TAKE_SCREENSHOT\nSEND_FILE\nDIR\nDELETE\nCOPY\nEXECUTE\nEXIT')

        done = False
        # loop until user requested to exit
        while not done:
            request = raw_input("Please enter command:\n")
            if self.valid_request(request):
                self.send_request_to_server(client_socket, request)
                self.handle_server_response(client_socket, request)
                if request == 'EXIT':
                    done = True
        client_socket.close()


if __name__ == '__main__':

    my_client = Client()

    my_client.start()
    print("Press Ctrl+C to shut down server.")