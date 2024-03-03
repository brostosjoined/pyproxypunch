import socket
import struct
import sys
import time
import ipaddress
import threading

relayHost = ("delthas.fr:14764")
defaultPort = 41254
localIpv4 = ipaddress.ip_network('127.0.0.0/8', strict=False)
localIpv6 = ipaddress.ip_network('fc00::/7', strict=False)


def client(host, port):
    try:
        c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            c.bind(("", defaultPort))
        except:
            c.bind(("", 0))
        localPort = c.getsockname()[1]
        print("Listening, connect to 127.0.0.1 on port " + str(localPort))
        relayAddr = socket.getaddrinfo(*relayHost.split(':'), socket.AF_INET if '4' in 'udp4' else socket.AF_INET6, socket.SOCK_DGRAM)[0][4]
        remoteAddr = (host, port)
        chRelay = True
        def relay():
            relayPayload = struct.pack('>BB', port >> 8, port % 256) + socket.inet_aton(remoteAddr[0])
            while chRelay:
                c.sendto(relayPayload, relayAddr)
                time.sleep(0.5)
            else:
                return
        threading.Thread(target=relay,name=relay).start()
        buffer = bytearray(4096)
        while True:
            n, addr = c.recvfrom_into(buffer)
            if addr[0] != relayAddr[0] or addr[1] != relayAddr[1]:
                continue
            if n != 2:
                print("Error received packet of wrong size from relay. (size:"+str(n)+")", file=sys.stderr)
                continue
            remoteAddr = (remoteAddr[0], struct.unpack(">H", buffer[:2])[0])
            break
        chRelay= False
            
        chPunch = True
        def punch():
            punchPayload = bytearray(b'\xcd')
            while chPunch:
                c.sendto(punchPayload, remoteAddr)
                time.sleep(0.5)
        threading.Thread(target=punch, name="punch").start()
        foundPeer = False
        localAddr = None
        while True:
            n, addr = c.recvfrom_into(buffer[1:])
            if n > len(buffer)-1:
                print("Error received packet of wrong size from peer. (size:"+str(n)+")", file=sys.stderr)
                continue
            if addr == relayAddr:
                continue
            if addr == remoteAddr:
                if not foundPeer:
                    foundPeer = True
                    print("Connected to peer")
                if n != 0 and localAddr is not None and buffer[1] == 0xCC:
                    c.sendto(buffer[2:n+1], localAddr)
            elif localIpv4.contains(addr[0]) or localIpv6.contains(addr[0]):
                localAddr = addr
                buffer[0] = 0xCC
                c.sendto(buffer[:n+1], remoteAddr)
        chPunch = False
    except KeyboardInterrupt:
        chPunch = False
        c.close()
        sys.exit()
def server(port):
    try:
        c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        c.bind(("", 0))
        print("Listening, start hosting on port " + str(port))
        print("Connecting...")
        localAddr = ("127.0.0.1", port)
        relayAddr = socket.getaddrinfo(*relayHost.split(':'), socket.AF_INET if '4' in 'udp4' else socket.AF_INET6, socket.SOCK_DGRAM)[0][4]
        chRelay = True
        def relay():
            relayPayload = struct.pack('>BB', port >> 8, port % 256)
            while chRelay:
                c.sendto(relayPayload, relayAddr)
                time.sleep(0.5)
            else:
                return
        threading.Thread(target=relay, name="relay").start()
        
        buffer = bytearray(4096)
        receivedIp = False
        while True:
            n, addr = c.recvfrom_into(buffer)
            if addr[0] != relayAddr[0] or addr[1] != relayAddr[1]:
                continue
            if n == 4:
                if not receivedIp:
                    receivedIp = True
                    ip = socket.inet_ntop(socket.AF_INET, buffer[:4])
                    print("Connected. Ask your peer to connect to " + ip + " on port " + str(port) + " with proxypunch")
                continue
            if n != 6:
                print("Error received packet of wrong size from relay. (size:"+str(n)+")", file=sys.stderr)
                continue
            ip = buffer[2:6]
            remoteAddr = (socket.inet_ntop(socket.AF_INET, ip), struct.unpack(">H", buffer[:2])[0])
            break
        chRelay = False
        
        chPunch = True
        def punch():
            punchPayload = bytearray(b'\xcd')
            while chPunch:
                c.sendto(punchPayload, remoteAddr)
                time.sleep(0.5)
        threading.Thread(target=punch, name="punch").start()
        foundPeer = False
        while True:
            n, addr = c.recvfrom_into(buffer[1:])
            if n > len(buffer)-1:
                print("Error received packet of wrong size from peer. (size:"+str(n)+")", file=sys.stderr)
                continue
            if addr == relayAddr:
                continue
            if addr == remoteAddr:
                if not foundPeer:
                    foundPeer = True
                    print("Connected to peer")
                if n != 0 and buffer[1] == 0xCC:
                    c.sendto(buffer[2:n+1], localAddr)
            elif (localIpv4.contains(addr[0]) or localIpv6.contains(addr[0])) and addr[1] == port:
                buffer[0] = 0xCC
                c.sendto(buffer[:n+1], remoteAddr)
        chPunch = False
    except KeyboardInterrupt:
        chRelay = False
        c.close()
        sys.exit()

def main():
    print("proxypunch python port by brostos(Original by delthas- https://github.com/delthas/proxypunch)")
    print("Mode? s(erver) / c(lient)")

    try:
        mode = input()
        if mode == "s" or mode == "server":
            ("Port?")
            port = int(input())
            server(port)
        elif mode == "c" or mode == "client":
            print("Host?")
            host = input()
            print("port?")
            port = int(input())
            client(host, port)
        else:
            print("Retry and choose either s or c")
    except KeyboardInterrupt:
        sys.exit()
        
if __name__ == "__main__":
    main()


