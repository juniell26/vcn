from collections import deque
import time
import segment4

ip_request_counts = {}

class MaxClientsReached(Exception):
    pass

class TrafficControlled(Exception):
    pass

class RequestCount:
    def __init__(self, limit, window):
        self.limit = limit
        self.window = window
        self.requests = deque()
    
    def add_request(self):
        # Remove requests that are older than the window
        now = time.time()
        while self.requests and now - self.requests[0] > self.window:
            self.requests.popleft()
        
        # Add the current request time to the queue
        self.requests.append(now)
        
        # Check if the limit has been exceeded
        if len(self.requests) > self.limit:
            raise TrafficControlled("Source IP address has exceeded the request limit")

def process_data(packet, client_counter):
    try:
        # Increment the client counter
        client_counter += 1

        # Check if the maximum number of clients has been reached
        if client_counter > 1000:
            raise MaxClientsReached("Maximum number of clients reached")

        # Check if the source IP address has exceeded the request limit
        source_ip = packet.get("src_ip")
        if source_ip not in ip_request_counts:
            ip_request_counts[source_ip] = RequestCount(limit=10, window=60)
        ip_request_counts[source_ip].add_request()

        # Process the data received from the previous segment
        provision_traffic = "{} from segment 3".format(packet)

        # Pass the processed traffic to segment4
        processed_traffic, client_counter = segment4.process_data(provision_traffic, client_counter)

        # Print a message indicating that the segment is running
        print("Segment 3 running...")

        return processed_traffic, client_counter

    except MaxClientsReached as e:
        print("Error in Segment 3:", e)
        # Raise the exception to the previous segment
        raise e
    except TrafficControlled as e:
        print("Error in Segment 3:", e)
        # Raise the exception to the previous segment
        raise e
    except Exception as e:
        print("Error in Segment 3:", e)

# Initialize the IP request counts dictionary
ip_request_counts = {}

print('segment 3 is running')
