'''
A gopher server, by Nicole Binder and Will Gleason.

Written using starter code by:
Amy Csizmar Dalal
CS 331, Fall 2020
'''
import sys, socket, os

class TCPServer:
    def __init__(self, port=50000):
        self.port = port
        self.host = ""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)

        while True:
            clientSock, clientAddr = self.sock.accept()
            print ("Connection received from ",  clientSock.getpeername())
            while True:
                data = clientSock.recv(1024)
                if not len(data):
                    break

                #We get a CR LF message, list all we have
                if data.decode("ascii") == "\\r\\n":
                    with open("Content/links.txt") as links:
                        response = links.read()
                        response = response.encode("ascii")

                #Not a CR LF message, parse the selector
                else:
                    selector = data.decode("ascii")
                    selector = selector.replace("\\r\\n","")
                    fileType = selector[len(selector) - 3:]

                    try:
                        #They're asking for a specific file
                        if fileType in ["txt"]:
                            with open(os.path.join("Content", selector)) as chosenFile:
                                response = chosenFile.read()

                        #They're browsing a directory
                        else:
                            with open(os.path.join("Content", selector, "links.txt")) as links:
                                response = links.read()
                    except:
                        response = "Error: couldn't find that file or directory!"

                print ("Received message:  " + data.decode("ascii"))
                response = response + "\n."
                response = response.encode("ascii")
                clientSock.sendall(response)
            clientSock.close()



def main():
    # Create a server
    if len(sys.argv) > 1:
        try:
            server = TCPServer(int(sys.argv[1]))
        except ValueError as e:
            print ("Error in specifying port. Creating server on default port.")
            server = TCPServer()
    else:
        server = TCPServer()

    # Listen forever
    print ("Listening on port " + str(server.port))
    server.listen()

main()
