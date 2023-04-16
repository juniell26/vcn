import socket

# Set the proxy server address and port
proxy_address = '192.168.56.1'
proxy_port = 8080

# Create a TCP/IP socket for the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the proxy server
client_socket.connect((proxy_address, proxy_port))

# Send a GET request to a website through the proxy server
request = b"www.example.com"
client_socket.send(request)

# Receive the response from the proxy server
response = b""
while True:
    data = client_socket.recv(1024)
    if not data:
        break
    response += data

# Print the response
print(response)

# Clean up the socket
client_socket.close()
