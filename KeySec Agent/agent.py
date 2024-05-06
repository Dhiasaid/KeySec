import os
import requests
import logging
import time
import json
import tempfile
import subprocess
from scapy.all import sniff, wrpcap, rdpcap, IP, TCP

# Define the directory to monitor for PCAP files
PCAP_DIRECTORY = '/path/to/pcaps'

# Define the directory to store processed PCAP files
PROCESSED_DIRECTORY = '/path/to/processed'

# Define the Suricata log file name
SURICATA_LOG_FILE = '/path/to/suricata.log'

# Define the JSON log file name
JSON_LOG_FILE = '/path/to/network_traffic.json'

def handle_packet(packet):
    """Handles a single packet"""
    try:
        # Write packet to PCAP file
        wrpcap(PCAP_FILE, packet, append=True)

        # Extract packet information
        if IP in packet and TCP in packet:
            timestamp = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
            src_ip = packet[IP].src
            dest_ip = packet[IP].dst
            src_port = packet[TCP].sport
            dest_port = packet[TCP].dport
            protocol = packet[IP].proto

            # Example: Filter packets by protocol (e.g., TCP)
            if protocol == 6:  # TCP protocol
                # Example: Extract HTTP traffic and log URLs
                if packet[TCP].dport == 80:
                    http_payload = packet[TCP].payload
                    if http_payload:
                        url = extract_url(http_payload)
                        if url:
                            log_url(timestamp, src_ip, dest_ip, src_port, dest_port, url)

    except Exception as e:
        logging.error(f"Error handling packet: {e}")

def extract_url(payload):
    """Extracts URL from HTTP payload"""
    # Example: Extract URL from HTTP GET request
    payload_str = str(payload)
    start_index = payload_str.find("GET") + 4
    end_index = payload_str.find("HTTP/")
    if start_index != -1 and end_index != -1:
        return payload_str[start_index:end_index].strip()

def log_url(timestamp, src_ip, dest_ip, src_port, dest_port, url):
    """Logs URL information"""
    url_info = {
        "timestamp": timestamp,
        "src_ip": src_ip,
        "dest_ip": dest_ip,
        "src_port": src_port,
        "dest_port": dest_port,
        "url": url
    }

    # Write URL info to JSON log file
    with open(JSON_LOG_FILE, 'a') as f:
        f.write(json.dumps(url_info) + '\n')

def start_suricata():
    """Starts Suricata"""
    try:
        # Start Suricata with logging enabled
        subprocess.Popen(['suricata', '-c', 'suricata.yaml', '-l', '.', '-k', 'none', '-q', '-s', 'suricata.rules'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.info("Suricata started successfully.")
    except Exception as e:
        logging.error(f"Error starting Suricata: {e}")

def process_pcap_file(file_path):
    """Processes a PCAP file"""
    try:
        # Load packets from PCAP file
        packets = rdpcap(file_path)

        # Process each packet
        for packet in packets:
            handle_packet(packet)

        # After processing, move the file to the processed directory
        os.makedirs(PROCESSED_DIRECTORY, exist_ok=True)
        os.rename(file_path, os.path.join(PROCESSED_DIRECTORY, os.path.basename(file_path)))

    except Exception as e:
        logging.error(f"Error processing PCAP file: {e}")

def monitor_pcap_directory(directory):
    """Monitors a directory for PCAP files"""
    try:
        while True:
            # List files in directory
            files = os.listdir(directory)

            # Process each file
            for file_name in files:
                if file_name.endswith('.pcap'):
                    file_path = os.path.join(directory, file_name)
                    process_pcap_file(file_path)

            # Sleep for some time before checking again
            time.sleep(5)

    except KeyboardInterrupt:
        logging.info("Monitoring stopped due to keyboard interrupt.")

def send_post_request(url, data):
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()  # Return the response JSON data
    except requests.exceptions.RequestException as e:
        print(f"Error sending POST request: {e}")
        return None

# Example usage:
dashboard_url = "http://127.0.0.1:8000/api/"
file_data = {"filename": "example_file.txt", "status": "downloaded"}
response = send_post_request(dashboard_url, file_data)
if response:
    print("POST request successful:", response)
else:
    print("Failed to send POST request to the dashboard.")


def main():
    """Main function"""
    try:
        # Configure logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

        # Log startup message
        logging.info("Packet capture agent started.")

        # Start Suricata
        start_suricata()

        # Start monitoring PCAP directory
        monitor_pcap_directory(PCAP_DIRECTORY)

        # Start packet capture using Scapy
        sniff(prn=handle_packet, store=0)

    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
