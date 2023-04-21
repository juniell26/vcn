import joblib
from sklearn.feature_extraction.text import CountVectorizer
from gateway import forward_to_server

# Load the machine learning model and vectorizer
clf = joblib.load("behavior_detection_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Create a set to store blocked IP addresses
blocked_ips = set()

def process_traffic(data, client_ip):
    # Check if the client's IP address has been blocked
    if client_ip in blocked_ips:
        print("Blocked traffic from", client_ip)
        return None

    # Use the vectorizer to transform the data into a feature vector
    data_vector = vectorizer.transform([data])

    # Use the machine learning model to predict if the traffic is malicious
    is_malicious = clf.predict(data_vector)[0]

    # If the traffic is malicious, block the client's IP address
    if is_malicious:
        print("Malicious traffic detected from", client_ip)
        blocked_ips.add(client_ip)
        return None

    # Process the data received from the previous segment
    processed_data = data + " from segment 4"
    
    # Forward the processed data to the gateway
    forward_to_server(processed_data)
    
# Print a message indicating that segment 4 is running
print('Segment 4 is running')
