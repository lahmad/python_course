import socket
import re
URI="http://data.pr4e.org/intro-short.txt"
SERVER="data.pr4e.org"

def get_uri():
    """
    Retrieve the data from http://data.pr4e.org/intro-short.txt
    as an Http response and parse the response header.
    """
    params = dict()
    socket_object = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        socket_object.connect((SERVER, 80))
        cmd = "GET http://data.pr4e.org/intro-short.txt HTTP/1.0\r\n\r\n".format(URI).encode()
        socket_object.send(cmd)

        while True:
            data = socket_object.recv(512)
            if len(data) < 1:
                break
            print(data.decode())

    except IOError as error:
        print("Failed to open the socket error:")

    finally:
        if socket_object:
            socket_object.close()


if __name__ == "__main__":
    get_uri()
