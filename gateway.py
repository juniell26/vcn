import socket
import http.server
import socketserver

def forward_to_server():
    # Define the IP address and port of the server
    server_ip = "example.com"  # Replace with the IP address or hostname of the server
    server_port = 80  # Replace with the appropriate port number for HTTP (typically 80)

    # Create a socket and connect to the server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip, server_port))

    # Send an HTTP GET request to the server
    request = "GET / HTTP/1.1\r\nHost: example.com\r\nConnection: close\r\n\r\n"
    sock.sendall(request.encode())

    # Receive the server's response
    response = ""
    while True:
        chunk = sock.recv(1024)
        if not chunk:
            break
        response += chunk.decode()

    # Close the socket
    sock.close()

    # Extract the response body from the response message
    response_body = response.split("\r\n\r\n", 1)[1]

    # Return the server response to send back to the main.py
    return response_body

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving directory at port {PORT}")
    httpd.serve_forever()
