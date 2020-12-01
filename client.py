import sys
import socket
import platform
from functions.shared_functions import *

# Initiate a socket
# socket.AF_INET signifies that an IPv4 address is used
# socket.SOCK_STREAM signifies that the connection is a stream (TCP)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Map the client's request with a function
functions = {'get':recv_file, 'put':send_file, 'list':recv_listing}

operating_system = platform.system()
delimiters = {'Windows':'*','Linux':'/','Darwin':':'}
delimiter = delimiters[operating_system]

try:
    #Server's address is a tuple: (IP address, PORT number)
    server_address = (sys.argv[1],int(sys.argv[2]))
    server_address_string = str(server_address)
    request = sys.argv[3].lower() # Converting to lower means the request is case insensitive.
except Exception as e:
    sys.exit("Encountered an error: {exception}.".format(exception = e))

# Check if a request is valid.
if request not in ['get', 'put', 'list']:
    sys.exit("{request} is not a valid request.".format(request = request))

# Check if a filename is specified in the case of 'get' or 'put'.
request_requires_filename = False
if request in ['get','put']:
    request_requires_filename = True
    try:
        filename = sys.argv[4]
        if (filename not in os.listdir() and request == "put"):
            message = "does't exist"
            sys.exit(1)
        if (filename in os.listdir() and request == 'get'):
            message = "already exists and overwriting is denied"
            sys.exit(1)
    except SystemExit:
        sys.exit("Can't {request} '{file}' because it {message}.".format(request = request.upper(), file = filename, message = message))
    except:
        # If the request should've been followed with a filename, exit with an error and a message describing what happened.
        sys.exit("You must select a file to {request}".format(request = request.upper()))


# @request changes from string to function.
request_argv = sys.argv[3].lower()
request = functions[request_argv]


# Connect to a server with a given address in the form of (address,port).
# Let the server know delimiter it will use to identify the end of a file name or the request name.
# Log messages show the process of connecting to a server, its address and whether is successfuly did so.
try:
    print("Connecting to {server} ...".format(server = server_address_string))
    client_socket.connect(server_address)
    print("Successfuly connected to {server}.".format(server = server_address_string))
    client_socket.send(delimiter.encode()) # First things first let the server know about the delimiter.
except Exception as e:
    exit("Couldn't connect to {server} because of an illegal exception: \{exception}."\
        .format(server = server_address_string, exception = e))

try:
    # Set the arguments for the function to be the filename plus a character that signifies the end of the filename.
    # Try/Except --> If a filename wasn't specified in the case of 'list' then don't create an arguments variable.
    try:
        args = filename + delimiter
    except:
        args = ""
    
    # Send the type of request to the server
    client_socket.sendall(str.encode(request_argv + delimiter + args))
    # Check if the request requires additional parameter 'filename'.
    if request_requires_filename:
        request(client_socket, server_address_string, filename, client = True) 
    else:
        request(client_socket, server_address_string, client = True)

    #After the request is over, close the socket.
    client_socket.close()
    sys.exit(0) # 0 indicates an exit without errors.
    
except FileNotFoundError:
    # Explicitly inform, if it is the case, that a file was not found.
    sys.exit("Couldn't perform {request} because {file} doesn't exist."\
        .format(request = request, file = filename))
    client_socket.close()   

except Exception as e:
    # In case of exception, exit with an error and a message describing what happened.
    client_socket.close()
    sys.exit("Couldn't perform {request} because of an illegal exception: {exception}."\
        .format(request = request, exception = e))

