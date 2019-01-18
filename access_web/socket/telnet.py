import socket
import sys

def get_data_from_server(server_url, cmd):
    """ Simulates a socket connection between client and server_url

        Args:
            (server_url): Server url with full path"
            (cmd): Command to run on the remote computer
    """
    if server_url is None or len(server_url) <= 0:
        print("server_url can not be empty/null")
        return
    if cmd is None or len(cmd) <= 0:
        print("cmd cannot be empty/null")
        return

    print(cmd)
    try:
        socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_connection.connect((server_url, 80))

        # Data needs to be serialized
        socket_connection.send(cmd.encode())
        while True:
            data = socket_connection.recv(512) #receive only 512 bytes
            print(data.decode())
            if len(data) < 1:
                print("Reached EOF...")
                break
            print(data.decode()) # Deserial the data back from binary

    except Exception as exp:
        print(exp.message)
        exit()
    finally:
        if not socket_connection:
            socket_connection.close()


if __name__ == '__main__':

    args = sys.argv
    if len(args) is not 3:
        print("Help python telnet.py <server> <cmd>")
        print("-" * 100)
        print("Example")
        print("-" * 100)
        print("python telnet.py data.pr4e.org  http://data.pr4e.org/romeo.txt")
    else:
        print(args[1])
        get_data_from_server(args[1],  "GET {addr} HTTP/1.0\r\n\r\n".format(addr=args[2]))
