"""import socket

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
UDP_IP = '0.0.0.0'
UDP_PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)  # UDP socket
sock.bind((UDP_IP, UDP_PORT))

clients = {}


while True:
    data, addr = sock.recvfrom(1024)
    client_name =data.decode().rsplit(' ')[0]
    temp=data.decode().split()
    if(client_name not in clients.keys() and len(temp)==1):
        print(bcolors.OKBLUE, "welcome new client", client_name, " :) ", bcolors.ENDC)
        clients[client_name] = addr
        print(clients)
    else:
        name = data.decode().rsplit(' ')[0]
        if name not in clients.keys():
            sock.sendto('sorry, client no exist'.encode(), addr)
        else:
            sock.sendto(data, clients.get(name))"""


import socket

# Server configuration
UDP_IP = '0.0.0.0'
UDP_PORT = 9999
BUFFER_SIZE = 1024

# Users dictionary to store the mapping of usernames to their addresses
users = {}

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
print(f"Server running on IP: {UDP_IP}, port: {UDP_PORT}")

while True:
    data, addr = sock.recvfrom(BUFFER_SIZE)
    message = data.decode().strip()

    # Split the message to extract sender, recipient, and message
    parts = message.split(' ', 2)
    if len(parts) < 3:
        # Register or error in message format
        if len(parts) == 1 and parts[0] not in users:
            # New user registration
            users[parts[0]] = addr
            print(f"New user '{parts[0]}' added.")
        else:
            error_msg = "Invalid message format or user already registered."
            sock.sendto(error_msg.encode(), addr)
            print(error_msg)
        continue

    sender, recipient, msg = parts
    if recipient in users:
        # Include the sender's name in the message for the recipient
        forward_message = f"From {sender}: {msg}"
        sock.sendto(forward_message.encode(), users[recipient])
        print(f"Message from {sender} to {recipient}: {msg}")
    else:
        # Notify the sender that the recipient does not exist
        error_msg = "There is no such user."
        sock.sendto(error_msg.encode(), addr)
        print(f"Failed to send message from {sender}: {error_msg}")
