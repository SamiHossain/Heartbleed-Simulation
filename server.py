from OpenSSL import SSL
import socket
import struct

CERT_FILE = "server.crt"
KEY_FILE = "server.key"

def create_server_context():
    context = SSL.Context(SSL.TLSv1_2_METHOD)
    context.use_certificate_file(CERT_FILE)
    context.use_privatekey_file(KEY_FILE)
    return context

def vulnerable_heartbeat(conn):
    # Receive the Heartbeat request from the client.
    request = conn.recv(1024)
    if len(request) < 2:
        return
    # Extract heartbeat type and claimed payload length.
    heartbeat_type = request[0]
    claimed_length = request[1]
    
    # Simulated sensitive data (could be from multiple regions, etc.).
    sensitive_data = (b"SESSION_KEY=ABC123DEF;"
                      b"USERNAME=johndoe;"
                      b"EMAIL=john@example.com;"
                      b"PASSWORD=secret")
    
    # Simulate vulnerability by leaking more data than provided.
    leaked_data = sensitive_data[:claimed_length]
    payload = request[2:]
    response = struct.pack("!BB", heartbeat_type, claimed_length) + payload + leaked_data
    conn.send(response)

def run_server():
    context = create_server_context()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 4444))
    sock.listen(5)
    print("TLS vulnerable server running on 127.0.0.1:4444")
    
    while True:
        client_sock, addr = sock.accept()
        print(f"Connection from {addr}")
        conn = SSL.Connection(context, client_sock)
        try:
            conn.set_accept_state()
            conn.do_handshake()
            vulnerable_heartbeat(conn)
        except Exception as e:
            print("Error during handshake or heartbeat processing:", e)
        finally:
            try:
                conn.shutdown()
            except Exception:
                pass
            conn.close()

if __name__ == "__main__":
    run_server()
