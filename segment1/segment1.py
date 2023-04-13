import scapy.all as scapy
import os
import json
import segment2

PACKETS_FILE = "logs.json"

def is_duplicate_packet(packet_data, packet_dict):
    # Check if a packet with the same src/dst IP addresses, src/dst ports, and handshake flags already exists
    key = (packet_data["src_ip"], packet_data["dst_ip"], packet_data["src_port"], packet_data["dst_port"], packet_data["handshake"])
    return key in packet_dict

def process_packet(packet):
    # Extract relevant information from the packet
    src_ip = packet[scapy.IP].src
    dst_ip = packet[scapy.IP].dst
    src_port = packet[scapy.TCP].sport
    dst_port = packet[scapy.TCP].dport
    device = packet[scapy.RadioTap].notdecoded
    handshake = packet[scapy.TCP].flags
    packet_location = packet.getlayer(scapy.GPS).location if packet.haslayer(scapy.GPS) else None
    user_agent = ""

    # Check if the packet has an HTTP layer and extract the User-Agent header
    if packet.haslayer(scapy.HTTPRequest):
        headers = packet[scapy.HTTPRequest].fields.get('Headers')
        user_agent = headers.get('User-Agent', "")

    # Perform analysis on the packet data
    # ...
    # If an anomaly is detected, block the connection
    if len(packet[scapy.Raw].load) > 1000:
        # Create an iptables rule to drop all traffic to and from the source IP address
        os.system(f"iptables -A INPUT -s {src_ip} -j DROP")
        os.system(f"iptables -A OUTPUT -d {src_ip} -j DROP")
        print(f"Connection from {src_ip}:{src_port} blocked due to anomaly detected.")

    # Save the packet information to the JSON file if it's not a duplicate
    packet_data = {
        "src_ip": src_ip,
        "dst_ip": dst_ip,
        "src_port": src_port,
        "dst_port": dst_port,
        "device": device,
        "handshake": handshake,
        "packet_location": packet_location,
        "user_agent": user_agent
    }
    with open(PACKETS_FILE, "r") as f:
        packet_dict = {tuple(json.loads(line).values()) for line in f}
    if not is_duplicate_packet(packet_data, packet_dict):
        with open(PACKETS_FILE, "a") as f:
            json.dump(packet_data, f)
            f.write("\n")  # write a new line character to separate packets

def receive_packet(packet_handler):
    # Set up the packet capture filter

    capture_filter = "tcp and (dst port 80 or dst port 443)"  # capture HTTP and HTTPS traffic

    # Start capturing packets
    scapy.sniff(filter=capture_filter, prn=packet_handler)
    
    return

# Call the receive_packet function with process_packet function as an argument to process the packets
segment2.receive_packet(process_packet)

print('segment 1 is running')
