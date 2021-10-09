import scapy.all as scapy
# We need to create regular expressions to ensure that the input is correctly formatted.
import re
# Regular Expression Pattern to recognise IPv4 addresses.
ip_add_range = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]*$")
cidr = "192.168.0.1/24"
# Try ARPing the ip address range supplied by the user. 
# The arping() method in scapy creates a packet with an ARP message and sends it to the broadcast mac address ff:ff:ff:ff:ff:ff.
# If a valid ip address range was supplied the program will return the list of all results
arp_result = scapy.arping(cidr)
