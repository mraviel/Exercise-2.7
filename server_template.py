#   Heights sockets Ex. 2.7 template - server side
#   Author: Barak Gonen, 2017

import socket

IP = '0.0.0.0'
PORT = 8800


def receive_client_request(client_socket):
    """Receives the full message sent by the client

    Works with the protocol defined in the client's "send_request_to_server" function

    Returns:
        command: such as DIR, EXIT, SCREENSHOT etc
        params: the parameters of the command

    Example: 12DIR c:\cyber as input will result in command = 'DIR', params = 'c:\cyber'
    """
    data = client_socket.recv(1024)
    list_data = data.split()
    command = list_data[0]

    try:
        params = list_data[1]
        if len(list_data) > 2:
            params = ' '.join(list_data[1:])
    except IndexError:
        params = None

    return (command, params)


def check_client_request(command, params):
    """Check if the params are good.

    For example, the filename to be copied actually exists

    Returns:
        valid: True/False
        error_msg: None if all is OK, otherwise some error message
    """
    if params == None:
        valid = True
        error_msg = None
    else:
        valid = False
        error_msg = 'Eroor'
    return valid, error_msg


def handle_client_request(command, params):
    """Create the response to the client, given the command is legal and params are OK

    For example, return the list of filenames in a directory

    Returns:
        response: the requested data
    """

    return 'EveryThing Works GOOD!'


def send_response_to_client(response, client_socket):
    """Create a protocol which sends the response to the client

    The protocol should be able to handle short responses as well as files
    (for example when needed to send the screenshot to the client)
    """
    client_socket.send(response)



def main():
    # open socket with client
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(1)
    client_socket, address = server_socket.accept()

    # handle requests until user asks to exit
    done = False
    while not done:
        command, params = receive_client_request(client_socket)
        valid, error_msg = check_client_request(command, params)
        if valid:
            response = handle_client_request(command, params)
            send_response_to_client(response, client_socket)
        else:
            send_response_to_client(error_msg, client_socket)

        if command == 'EXIT':
            done = True

    client_socket.close()
    server_socket.close()

if __name__ == '__main__':
    main()