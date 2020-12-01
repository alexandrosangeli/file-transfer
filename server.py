import sys
import socket
from functions.shared_functions import *

# Initiate a socket
# socket.AF_INET signifies that an IPv4 address is used
# socket.SOCK_STREAM signifies that the connection is a stream (TCP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Grab the port number from the command line.
try:
    port = int(sys.argv[1])
except IndexError:
    sys.exit("You must enter a port number.")
except Exception as e:
    sys.exit("Something unexpected happened: {exception}.".format(exception = e))

# Map the client's request with a function.
services = {'put':recv_file, 'get':send_file, 'list':send_listing}

# Bind to all available network interfaces on your host.
# Create a queue for incoming connection requests (size = 5)
# Catch any errors.
try:
    server_socket.bind(("0.0.0.0",port))
    server_socket.listen(5)
    print("Server up and running.")
except Exception as e:
    sys.exit("Operation has failed due to exception: {exception}".format(exception = e))

# Continusly listen for incoming connections.
# When a client connects, serve it and then loop back.
# Catch any errors during the process.
while True:
    try:
        while True:
            print("Waiting for a client...")
            # Accept the connection
            client_socket, client_address = server_socket.accept()
            client_address_string = str(client_address)
            print("Client {client} connected.".format(client = client_address_string))
            delimiter = client_socket.recv(1).decode() # Server receives the delimiter that will be used identify the end of filenames and request names.
            # Service will hold the client's request as string.
            service = ''
            request = bytearray(1)
            # Receive the name request to serve.
            # A special character will signify the end of the request type.
            while len(request) > 0 and delimiter not in request.decode():
                request = client_socket.recv(1)
                service += request.decode()
            # Remove the special character signifying the end of the request.   
            service = service.replace(delimiter,"")

            # Checks whether a filename is required for the given request.
            service_requires_filename = False
            if service in ['get', 'put']:
                service_requires_filename = True

            # Match the client's request with a function.
            service_function = services[service]

            # Receive the filename to operate on, if required.
            if service_requires_filename:
                filename = ''
                param = bytearray(1)
                while len(param) > 0 and delimiter not in param.decode():
                    param = client_socket.recv(1)
                    filename += param.decode()
                filename = filename.replace(delimiter,"")
                # Serve the client by calling function.
                service_function(client_socket, client_address_string, filename,server = True)
            else:
                service_function(client_socket, client_address_string, server = True)

            # When the client has been served, close the connection with it.
            client_socket.close()
                  
    except Exception as e:
        client_socket.close()
        print("The connection with {client} has been terminated due to an exception: {exception}.".format(exception = e, client = client_address_string))

