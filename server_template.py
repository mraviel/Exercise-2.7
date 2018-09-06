import socket
import shutil
import os
import sys
import signal  # Allow socket destruction on Ctrl+C


class Server(object):
    """ The server class """

    def __init__(self, PORT=8800, IP='0.0.0.0'):
        self.PORT = PORT
        self.IP = IP
        self.commands_list = ['TAKE_SCREENSHOT', 'SEND_FILE', 'DIR', 'DELETE', 'COPY', 'EXECUTE', 'EXIT']

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            print ("The server is start on host:{0}:{1}").format(self.IP, self.PORT)
            server_socket.bind((self.IP, self.PORT))
            print ("Server started on port: {0}").format(self.PORT)

        except Exception as e:
            print("Error: Could not bind to port {0}".format(self.PORT))
            self.shutdown()
            sys.exit(1)

        self.main(server_socket)

    def shutdown(self):
        """ Shuts down the server """

        try:
            print ("Shuting down the server")
            Server.shutdown(socket.SHUT_RDWR)

        except Exception as e:
            pass  # Pass if socket is already closed

    def receive_client_request(self, client_socket):

        """ Receives the full message sent by the client """

        data = client_socket.recv(1024)
        list_data = data.split()
        command = [list_data[0]]  # the command from the self.commands_list (command = list of one command)

        try:  # check if there is params. (params = list of params)
            params = [list_data[1]]
            if len(list_data) > 2:
                params = list_data[1:]

        except IndexError:
            params = None

        return (command, params)

    def check_client_request(self, command, params):
        """ check if params are good. """

        command_str = ' '.join(command)  # str of command from self.commands_list

        valid = True  # defualt
        error_msg = None  # defualt

        if command_str == 'DIR':
            try:  # find the dir
                valid_dir = os.path.isdir(params[0])
                if valid_dir == False:
                    valid = False
                    error_msg = 'Error'

            except TypeError:
                valid = False
                error_msg = 'Error'
            return valid, error_msg

        elif command_str == 'DELETE':
            try:  # find the file
                valid_file = os.path.isfile(params[0])
                if valid_file == False:
                    valid = False
                    error_msg = 'Error'

            except TypeError:
                valid = False
                error_msg = 'Error'
            return valid, error_msg

        elif command_str == 'COPY':
            if params == None:
                return valid, error_msg

            for i in params:
                valid_dir = os.path.isdir(i)
                if valid_dir == False:  # check if it's dir
                    valid_file = os.path.isfile(i)
                    if valid_file == False:  # check if it's file
                        valid = False
                        error_msg = 'Error'
                    else:
                        valid = True
                        error_msg = None
            return valid, error_msg

        elif command_str == 'EXECUTE' or command_str == 'EXIT' or command_str == 'TAKE_SCREENSHOT':
            return valid, error_msg

    def handle_client_request(self, command, params):
        """ Create the response to the client, given the command is legal and params are OK """

        command_str = ' '.join(command)

        try:
            params_str = ' '.join(params)
        except TypeError:
            params_str = params

        if (command_str == 'TAKE_SCREENSHOT'):
            os.system("import -window root temp.png")
            return 'The image was taken!'

        elif (command_str == 'SEND_FILE'):
            pass

        elif (command_str == 'DIR'):
            list_dir = os.listdir(params_str)
            return str(list_dir)

        elif (command_str == 'DELETE'):
            os.remove(params_str)
            return 'The file in location: {0} is deleted'.format(params_str)

        elif (command_str == 'COPY'):
            try:
                shutil.copy(params[0], params[1])
                return "The file is copied"
            except TypeError:
                return "You need to give 2 arguments!"
            except IndexError:
                return "You need to give 2 arguments!"

        elif (command_str == 'EXECUTE'):
            try:
                os.system(params_str)
                return "tHe EXECUTE run perfectly"
            except TypeError:
                return "There is No argument!"

        elif (command_str == 'EXIT'):
            return 'Good bye'

    def send_response_to_client(self, response, client_socket):
        """ send respone to the client """
        client_socket.send(response)

    def main(self, server_socket):

        # open socket with client
        server_socket.listen(1)
        client_socket, address = server_socket.accept()

        # handle requests until user asks to exit
        done = False
        while not done:
            command, params = self.receive_client_request(client_socket)
            valid, error_msg = self.check_client_request(command, params)
            if valid:
                response = self.handle_client_request(command, params)
                self.send_response_to_client(response, client_socket)
            else:
                self.send_response_to_client(error_msg, client_socket)

            if command == 'EXIT':
                done = True

        client_socket.close()
        server_socket.close()


if __name__ == '__main__':

    my_server = Server()


    def shutdownServer(sig, unused):
        """
        Shutsdown server from a SIGINT recieved signal
        """
        my_server.shutdown()
        sys.exit(1)


    signal.signal(signal.SIGINT, shutdownServer)
    my_server.start()
    print("Press Ctrl+C to shut down server.")