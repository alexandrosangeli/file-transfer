import socket
import sys
import os

# A 100-character-long message acts as an identifier. When send over a socket it means an error has occured from the other side.
# It includes numbers, special characters, lower case and upper case letters making it improbable for a file to contain only this specific string of characters in this order.
# Another 100-character-long message to be sent in case no error was detected when trying to overwrite a file.

generated_message_code = "2c3Q73xo3tu5zw*z69oc60icdba0k'e^tc8&Af0v*q$4ft!grnfm5of7ujmr^f#fJnm#g63*9s*$i1yx7l8&zequtnnzz$m$shf!"
all_good_message = "0" * 100

"""
    Sends a file over a given socket.

    @socket The socket to send the file over.
    @address A string representation of the address associated with the socket.
    @filename The file to send.
    @server Signifies whether the function was called by the server or not.
    @client Signifies whether the function was called by the client or not.
"""
def send_file(socket, address, filename, server = False, client = False):

    # When a client tries to send a file, the server will always send a message code that will signify whether it can receive the file or not.
    # The client then receives the message code and decides wheter it can send the file or not.
    # The two messages are both 100-characters-long, therefore, the client will always receive 100 bytes that will hold the message code.
    if client:
        data = socket.recv(100)
        # If server can't receive a file, then let the client know and exit with an error.
        if data.decode() == generated_message_code:
            sys.exit("'{file}' already exists on the server {server}.".format(file = filename, server = address))
            return

    # If a server can receive the file or it is the client receiving the file, then proceed with sending it.
    try:
        f = open(filename, 'rb') # Encoding --> can read files with special characters
        # Read 1024 bytes of the file.
        # Send the data.
        # Repeat until there's no data left to read.
        data = f.read(1024)
        while data:
            socket.sendall(data)
            data = f.read(1024)
        # Close the stream with the file.
        f.close()
        if server:
            print("'{file}' was sent to client {client}.".format(file = filename, client = address))
        if client:
            print("'{file}' was sent to server {server}.".format(file = filename, server = address))

    except FileNotFoundError:
        # When a server tries to send a file that doesn't exist, send a message code instead that lets the client know that the file requested doesn't exist.
        if server:
            socket.sendall(generated_message_code.encode())  
            print("Client {client} tried to GET a file '{file}' which doesn't exist.".format(client = address, file = filename))  
    # End of function.


"""
    Receives a file over a given socket.

    @socket The socket to receive the file over.
    @address A string representation of the address associated with the socket.
    @filename The file to receive.
    @server Signifies whether the function was called by the server or not.
    @client Signifies whether the function was called by the client or not.
"""
def recv_file(socket, address, filename, server = False, client = False):
    # When a server tries to receive a file, check if it already exists to avoid overwriting.
    # If the file already exists, send a message code that represents that it tries to overwrite an existing file.
    # If the file doesn't exist, send a message code that represents that it can proceed with receiving the file.
    if server:
        if filename in os.listdir():
            socket.sendall(generated_message_code.encode())
            print("Client {client} tried to upload file '{file}' that already exists.".format(client = address, file = filename))
            return
        else:
            socket.sendall(all_good_message.encode())

    # Receive 100 bytes the first time to check if it match a message code.
    data = socket.recv(100)

    # Try/Except used because when the data received is not encoded string (e.g. in the case of an image), it will raise an exception.
    try:
        # If data received is a message code for when a client requests a file that doesn't exist, exit with an error.
        if client and data.decode() == generated_message_code:
            sys.exit("'{file}' was not found on the server {server}.".format(file = filename, server = address))
    # Catch a SystemExit exception and exit anyway.  
    except SystemExit:
            sys.exit("'{file}' was not found on the server {server}.".format(file = filename, server = address))
    except:
        pass
   
    # If the file the client tries to receive already exists locally, then append "New " before the name - Convenient way to identify the received file in case of a confusion.
    if client and filename in os.listdir():
        f = open("new " + filename, 'wb')
    else:
        # @appended_chars will be an empty string because it will be appended to the log message anyway in line 109 - avoids condition checking.
        appended_chars = ""
        f = open(filename, 'wb')
    # Keep receiving data until all of it has been received.
    while data:
        f.write(data)
        data = socket.recv(1024)
    # Close the stream with the file.
    f.close()
    # Report success.
    if client:
        print("'{file}' received from {server}".format(file = filename, server = address))
    if server:
        print("'{file}' received from {client}".format(file = filename, client = address))
    # End of function.


"""
    Sends a list with files and directories found in the directory the server runs in.

    @socket The socket to send the list over.
    @address A string representation of the address associated with the socket.
    @server Signifies whether the function was called by the server or not.
    @client Signifies whether the function was called by the client or not.
"""
def send_listing(socket, address, server = False, client = False):
    # Create a readable string with all the files in directory.
    data = ""
    number_of_directories = 0
    for i,file in enumerate(os.listdir()):
        if i != len(os.listdir())-1:
            data += "{filename},".format(filename = file)
        else:
            data += "{filename}".format(filename = file) # When on the last file, do not add ',' after the file name.   
    # Send all the data over the socket.
    socket.sendall(str.encode(data))
    if server:
        print("List sent to client {client}".format(client = address))
    # End of function.
    

"""
    Receives a list with files and directories found in the directory the server runs in.

    @socket The socket to receive the list over.
    @address A string representation of the address associated with the socket.
    @server Signifies whether the function was called by the server or not.
    @client Signifies whether the function was called by the client or not.
"""
def recv_listing(socket, address, server = False, client = False):
    
    items = ''
    data = bytearray(1)

    # Receive 2014 bytes over the socket.
    # Save that data to a string to format it later.
    # Repeat until all data is received.
    while len(data) > 0:
        data = socket.recv(1024)
        items += data.decode()
    items_list = items.split(',')
    # Print the list in a well-presented way.
    for f in items_list:
        print("> {file}".format(file = f))

    if client:
        print("List received from server {server}".format(server = address))
    # End of function.

