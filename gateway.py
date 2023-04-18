import socket
import select

DEFAULT_BUFFER_SIZE = 4096
FAST_BUFFER_SIZE = 131072

def forward_to_server(request):
    # Define the IP address and port of the server
    server_ip = "192.168.56.1"  # Replace with the IP address or hostname of the server
    server_port = 80  # Replace with the appropriate port number for HTTP (typically 80)

    # Create a new socket and connect to the server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((server_ip, server_port))

    # Send the client's request to the server
    server_socket.sendall(request)

    # Receive the server's response
    received_response = b""
    buffer_size = DEFAULT_BUFFER_SIZE
    while True:
        # Check if there is data available to receive
        ready_to_read, _, _ = select.select([server_socket], [], [], 0.1)
        if ready_to_read:
            chunk = server_socket.recv(buffer_size)
            if not chunk:
                break
            received_response += chunk
            # If the response is larger than 5MB, increase the buffer size for faster receiving
            if len(received_response) > 5000000:
                buffer_size = FAST_BUFFER_SIZE

    # Close the socket
    server_socket.close()

    # Return the server response to send back to the main.py
    return received_response
