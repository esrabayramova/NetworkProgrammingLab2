import argparse, socket, sys, os, json, pickle
from itertools import cycle

class server:
    MAX_BYTES = 65535

    def __init__(self, interface, port):
        self.interface = interface
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def run(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.interface, self.port))
        self.sock.listen(1)
        print("Server socket: ", self.sock.getsockname())

        while True:
            s, sockname = self.sock.accept()
            data = s.recv(self.MAX_BYTES)   #receive the data
            received = pickle.loads(data)   #process the data that the client sent
            mode = received[0]
            content_1 = received[1]   #main file
            content_2 = received[2]   #either key file or json file based on the mode

            if mode == "change_text":
                dctnry = json.loads(content_2)   #convert the content of the json file into dictionary
                for old, new in dctnry.items():
                    content_1 = content_1.replace(old, new)

                s.sendall(content_1.encode('ascii'))   #send back to the client
                print(content_1)

            elif mode == "encode_decode":
                key = content_2
                xor = [chr(ord(a)^ord(b)) for a, b in zip(content_1, cycle(key))]   #XOR the file content with the key
                coded = "".join(xor)

                s.sendall(coded.encode('ascii'))   #send back to the client
                print(coded)


class client:
        MAX_BYTES = 655535

        def __init__(self, hostname, port, mode):
            self.hostname = hostname
            self.port = port
            self.mode = mode
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        def run(self, file_1, file_2):
            self.sock.connect((self.hostname, self.port))
            print("Client socket: ", self.sock.getsockname())

            file1 = open(file_1, "r")
            content_1 = file1.read()   #content of the first file (main file)
            file1.close()

            file2 = open(file_2, "r")
            content_2 = file2.read()   #content of the second file (either key file or the json file)
            file2.close()

            data_to_send = []   #send the mode, contents of two files to the server as a list
            data_to_send.append(self.mode)
            data_to_send.append(content_1)
            data_to_send.append(content_2)

            tosend = pickle.dumps(data_to_send)   #process the list (data) before sending

            self.sock.sendall(tosend)   #send to the server

            final = self.sock.recv(self.MAX_BYTES)

            with open(file_1, "wb") as text_file:
                text_file.write(final)   #write the final result that the server sent to the main file

     
if __name__ == "__main__":
        parser = argparse.ArgumentParser(description = "sending data by TCP")
        choices = {"client": client, "server": server}
        #func = {"change_text": change_text, "encode_decode": encode_decode}
        parser.add_argument("role", choices = choices, help = "either server or client")
        parser.add_argument("host", help = "server interface")
        parser.add_argument("-p", metavar = 'PORT', type = int, default = 4337, help = "TCP port")

        if sys.argv[1] == "client":
            parser.add_argument("--mode", type=str, help = "which service do you choose? ")
            parser.add_argument("firstfile", help="name of the first file")
            parser.add_argument("secondfile", help="name of the second file")

        args = parser.parse_args()
        classname = choices[args.role]
        #endpoint = classname(args.host, args.p)
        
        if args.role == "client":
            endpoint = classname(args.host, args.p, args.mode)
            endpoint.run(args.firstfile, args.secondfile)

        elif args.role == "server":
            endpoint = classname(args.host, args.p)
            endpoint.run()
