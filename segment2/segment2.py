import segment3
import time

class RateLimiter:
    def __init__(self, rate_limit):
        self.rate_limit = rate_limit
        self.last_request_time = 0

    def get_wait_time(self):
        # Calculate the time since the last request
        time_since_last_request = time.monotonic() - self.last_request_time

        # Calculate the minimum time between requests based on the rate limit
        min_time_between_requests = 1 / self.rate_limit

        # If the minimum time between requests hasn't elapsed, return the remaining time
        if time_since_last_request < min_time_between_requests:
            return min_time_between_requests - time_since_last_request

        # Otherwise, no wait time is needed
        return 0

    def wait(self):
        wait_time = self.get_wait_time()
        if wait_time > 0:
            time.sleep(wait_time)

        # Update the last request time
        self.last_request_time = time.monotonic()

def process_data(packet, receiver_function):
    # implementation of process_data function
    processed_data = packet  # do some processing
    receiver_function(processed_data)  # pass the processed data to the receiver function
    
    return

def process_packet(packet):
    try:
        # Extract relevant information from the packet
        src_ip = packet.get("src_ip")
        dst_ip = packet.get("dst_ip")
        src_port = packet.get("src_port")
        dst_port = packet.get("dst_port")
        device = packet.get("device")
        handshake = packet.get("handshake")
        packet_location = packet.get("packet_location")
        user_agent = packet.get("user_agent")

        # Check if all the required keys are present and have the expected data types
        if not all(key in packet for key in ["src_ip", "dst_ip", "src_port", "dst_port", "device", "handshake", "user_agent"]) or \
            ("packet_location" in packet and not isinstance(packet["packet_location"], str)) or \
            not isinstance(packet["src_ip"], str) or not isinstance(packet["dst_ip"], str) or \
            not isinstance(packet["device"], str) or not isinstance(packet["handshake"], bool) or \
            not isinstance(packet["user_agent"], str) or not isinstance(packet["src_port"], int) or \
            not isinstance(packet["dst_port"], int):
            provisional = False

            # Process the packet data and get the processed data
            processed_data = process_data(packet)

            # Do something with the processed data
            provisional = True

            # Provision the packet to move to the next module
            segment3.provision_packet({
                "src_ip": src_ip,
                "dst_ip": dst_ip,
                "src_port": src_port,
                "dst_port": dst_port,
                "device": device,
                "handshake": handshake,
                "packet_location": packet_location,
                "user_agent": user_agent,
                "processed_data": processed_data
            })

    except Exception as e:
        print("Error in Segment 2:", e)
    
    return provisional
print("segment 2 is running")