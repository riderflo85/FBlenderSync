import socket
from urllib.parse import urlparse, parse_qs


def create_socket(host: str, port: int) -> socket.socket:
    """Create a server socket to listen web request.

    Args:
        host (str): Host address
        port (int): Port listen

    Returns:
        socket.socket: socket instance
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    # Listen only one connection
    sock.listen(1)
    return sock
    

def wait_authorization_code(socket_proc: socket.socket) -> str:
    """Wait the Dropbox oauth2 authorization code.

    Args:
        socket_proc (socket.socket): socket.socket instance server
    
    Returns:
        str: Dropbox authorization code
    """
    conn, addr = socket_proc.accept()
    data = conn.recv(1024)

    # Get the url response
    url = data.decode().split(' ')[1]

    query = urlparse(url).query
    params = parse_qs(query)
    param_code = params.get('code', [])

    conn.sendall(b'HTTP/1.1 200 OK\nContent-Type: text/html\n\n<html><body><h1>Vous pouvez fermer cette page !</h1></body></html>')
    conn.close()
    return param_code
