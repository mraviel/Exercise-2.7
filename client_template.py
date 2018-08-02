#   Heights sockets Ex. 2.7 template - client side
#   Author: Barak Gonen, 2017


import socket

IP = '127.0.0.1'
PORT = 8800

commands_list = ['TAKE_SCREENSHOT', 'SEND_FILE', 'DIR', 'DELETE', 'COPY', 'EXECUTE', 'EXIT']

def valid_request(request):
    """Check if the request is valid (is included in the available commands)

    Return:
        True if valid, False if not
    """
    for command in commands_list:
        if request == command:
            return True
    return False

def send_request_to_server(my_socket, request):
    """Send the request to the server. First the length of the request (2 digits), then the request itself

    Example: '04EXIT'
    Example: '12DIR c:\cyber'
    """
    my_socket.send(request)


def handle_server_response(my_socket, request):
    """Receive the response from the server and handle it, according to the request

    For example, DIR should result in printing the contents to the screen,
    while SEND_FILE should result in saving the received file and notifying the user
    """
    data = my_socket.recv(1024)
    print data

def main():
    # open socket with the server
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((IP, PORT))

    # print instructions
    print('Welcome to remote computer application. Available commands are:\n')
    print('TAKE_SCREENSHOT\nSEND_FILE\nDIR\nDELETE\nCOPY\nEXECUTE\nEXIT')

    done = False
    # loop until user requested to exit
    while not done:
        request = raw_input("Please enter command:\n")
        if valid_request(request):
            send_request_to_server(my_socket, request)
            handle_server_response(my_socket, request)
            if request == 'EXIT':
                done = True
    my_socket.close()

if __name__ == '__main__':
    main()