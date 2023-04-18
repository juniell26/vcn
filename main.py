import socket
from datetime import datetime
import segment1
import gateway

# Set the default buffer size
DEFAULT_BUFFER_SIZE = 4096

# Set the address and port of the proxy server
proxy_address = '192.168.56.1'
proxy_port = 8080

# Create a TCP/IP socket for the proxy server
proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to the address and port
proxy_socket.bind((proxy_address, proxy_port))

# Listen for incoming connections
proxy_socket.listen(5)

# Define a function to detect the size of the payload
def get_payload_size(request):
    
    # Parse the request to get the content length
    content_length = None
    lines = request.split(b"\r\n")
    for line in lines:
        if line.startswith(b"Content-Length:"):
            content_length = int(line.split(b":")[1].strip())
            break
    if content_length is None:
        return None
    
    # Return the payload size in bytes
    return content_length

# Define a function to get the buffer size based on the payload size
def get_buffer_size(payload_size):
    if payload_size is None:
        return DEFAULT_BUFFER_SIZE
    elif payload_size > 100000000:  # 100 MB
        return 32768
    elif 50000000 < payload_size <= 100000000:  # 50-100 MB
        return 32768
    elif 25000000 < payload_size <= 50000000:  # 25-50 MB
        return 16384
    elif 10000000 < payload_size <= 25000000:  # 10-25 MB
        return 8192
    elif 5000000 < payload_size <= 10000000:  # 5-10 MB
        return 4096
    elif 1000000 < payload_size <= 5000000:  # 1-5 MB
        return 2048
    elif 64000 < payload_size <= 1000000:  # 64 KB-1 MB
        return 1024
    elif 32000 < payload_size <= 64000:  # 32-64 KB
        return 512
    elif 16000 < payload_size <= 32000:  # 16-32 KB
        return 256
    elif 8000 < payload_size <= 16000:  # 8-16 KB
        return 128
    else:
        return DEFAULT_BUFFER_SIZE

# Define a function to get the buffer
def get_buffer(request, buffer_size):
    buffer = b""
    while len(buffer) < buffer_size:
        data = request.recv(buffer_size - len(buffer))
        if not data:
            break
        buffer += data
    return buffer

# Define a function to send the response back to the client
def send_response(client_socket, response_data):
    # Send the response data back to the client
    client_socket.sendall(response_data)

# Define a function to process the packet
def process_packet(request, buffer_size):
    payload_size = get_payload_size(request)
    processed_packet = segment1.process_packet(request, payload_size, buffer_size)
    return processed_packet

# Loop forever, accepting incoming connections
while True:
    # Accept a connection
    client_socket, client_address = proxy_socket.accept()
    print('A client has connected')

    # Print the client IP address
    print("Client connected from:", client_address[0])

    # Read the incoming request from the client
    request = client_socket.recv(DEFAULT_BUFFER_SIZE)
    
    # Read the request into a buffer
    buffer = bytearray(request)

    # Determine the size of the payload
    payload_size = get_payload_size(request)

    # Get the buffer size based on the payload size
    buffer_size = get_buffer_size(payload_size)
    
    # Read the payload from the buffer
    payload = buffer[:payload_size]
    
    # Pass the entire request to segment1
    segment1.process_packet(request, buffer_size)
        
    # Wait for the response from the gateway
    response_data = gateway.received_response()

    # Send the response data back to the client
    send_response(client_socket, response_data)

    # Close the client socket
    client_socket.close()

    
