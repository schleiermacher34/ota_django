import socket
import ssl

try:
    # Use SSL context to ignore certificate validation temporarily
    context = ssl._create_unverified_context()
    sock = socket.create_connection(("vtiger.anatol.com", 443), timeout=10)
    ssl_sock = context.wrap_socket(sock, server_hostname="vtiger.anatol.com")
    print("Connection successful!")
    ssl_sock.close()
except socket.error as e:
    print(f"Connection failed: {e}")
