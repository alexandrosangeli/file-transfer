# File Transferring
This is a client-server based file transfer system. A client can upload/download files from a server that runs on its local network.

## How it works
- Both the server and the client must run over the same netowork.
- When ```server.py``` is running over the network, ```client.py``` can also run, assuming the correct arguments have been set (*see "How to use"*).
- A TCP connection is established and then based on the service that client chose (this is set before running the python file), the server serves the client.
- Client has the three services to choose from: `GET`, `PUT`, `LIST`.
- `GET`: Downloads the specified file from the server if it exists.
- `PUT`: Uploads the specified file from the server if it exists.
- `LIST`: Requests a list that displays all files that exist on the server.

## How to use
- In order to work, the server must first run and then client should follow.
- ```server.py``` requires a port number. That's the port that client will use to reach the server.
- Run ```server.py``` using ```python server.py PORT``` where ```port``` is the port number.
- ```client.py``` requires an address, a port number and if the service is either `GET` or `PUT`, it also requires a filename.
- Run ```client.py``` using ```python client.py localhost PORT SERVICE FILENAME``` where ```localhost``` is the network the script runs over (can leave it as `localhost`), ```PORT``` is the port number to connect to the server and ```FILENAME``` is the name of the file to transfer (optional since LIST doesn't require a filename).

### Example
`$ python3 server.py 2000` followed by `$ python3 client.py localhost 2000 GET filename`.

## Tips
- Both ```server.py``` and ```client.py``` include ```from functions.shared_functions import *``` as they are supposed to run on different directories because the system doesn't allow overwrites and running both of them over the same directory will cause a runtime error. ```"functions"``` in this case is a directory that exists on the parent directory of ```server.py``` and ```client.py```.
## Note
- I would strongy discourage anyone from using the code for any academic related coursework. This action is against most scools' policy and it will probably be considered as plagiarism.
- The code is entirely written by me.

Copyright © 2020 Alexandros Angeli
