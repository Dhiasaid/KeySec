from scapy.all import *

def replay_pcap(pcap_file, iface):
    packets = rdpcap(pcap_file)
    sendp(packets, iface=iface, verbose=True)

if __name__ == "__main__":
    pcap_file = "example.pcap"
    iface = "eth0"
    replay_pcap(pcap_file, iface)
