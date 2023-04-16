import socket
import main

DEFAULT_BUFFER_SIZE = 4096
FAST_BUFFER_SIZE = 131072

def forward_to_server(request):
    # Define the IP address and port of the server
    server_ip = "example.com"  # Replace with the IP address or hostname of the server
    server_port = 80  # Replace with the appropriate port number for HTTP (typically 80)

    # Create a socket and bind to the Ethernet interface
    interface_name = 'eth0' # Replace with the appropriate interface name
    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(3))
    sock.bind((interface_name, 0))

    # Send the client's request to the server
    sock.sendall(request)

    # Receive the server's response
    response = b""
    payload_size = 0
    buffer_size = DEFAULT_BUFFER_SIZE
    while True:
        chunk = sock.recv(buffer_size)
        if not chunk:
            break
        response += chunk
        payload_size += len(chunk)
        if payload_size > 5000000:
            buffer_size = FAST_BUFFER_SIZE

    # Close the socket
    sock.close()

    # Return the server response to send back to the main.py
    return response
