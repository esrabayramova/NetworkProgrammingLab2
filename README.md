# NetworkProgrammingLab2

## Description

This is a client-server-based console app called "text_service". The server and the client is created using object oriented approach. There are two modes that the server and the client can operate: change_text and encode_decode. After specifying the mode, client sends files to the server. In first case - change_text mode, client sends one text file and one JSON file to the server. Using this JSON file, server swaps the corresponding words and sends the result back to the client. In second case - encode_decode mode, the client sends two text files to the server - first one is the text file and the second file contains the key that will be used to XOR the content of the first file. After the server encodes the text with the given key, it sends the result back to the client. However, if the content of the file that the client sends to the server is already encoded, the server will decode it and send it to the client. After client gets the results, it will update the content of the previous files with what the results that the server sent.

## Installation

```
git clone https://github.com/esrabayramova/NetworkProgrammingLab2
```

## Usage


Firstly, two terminals are opened, one for the server and one for the client. After writing 'python3' and specifying the name of the file, the role must be shown - either client or server. The next thing is to type the hostname of the machine or the word 'localhost'. Another thing that is necessary for this program is the port number. However, in the code, the default port number is selected and it is not required to write. But if you want to use any particular port, you can write it by typing '-p' before this port number. Then, the mode is specified by typing --mode before - either "change_text" or "encode_decode" on the client terminal. If it is client terminal, then the names of two files (if they are not within the same directory, the path of the files) should be written. Then, you can check the content of the text file to see the results.

Here is the example:
```
python3 text_service.py server localhost
python3 text_service.py client localhost --mode text_change tfile.txt jfile.json
```

Client side terminates after receiving the message from the server, however, you should stop server by pressing Ctrl + C. As long as the server is running, it can make a connection with different clients. 
