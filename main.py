import sys #damit kann man Kommandozeilen-Argumente ausführen
import socket 
import threading
from datetime import datetime 

# Ziel definieren
if len(sys.argv) == 2:
    target = socket.gethostbyname(sys.argv[1]) #Hostname wird zur Ipv4-Adresse übersetzt
    port_anfang = 0
    port_ende = 1000

elif len(sys.argv) == 3:
    target = socket.gethostbyname(sys.argv[1])
    port_anfang = int(sys.argv[2])
    port_ende = port_anfang

elif len(sys.argv) == 4:
    target = socket.gethostbyname(sys.argv[1])
    port_anfang = int(sys.argv[2])
    port_ende = int(sys.argv[3])

else: 
    print("Kein gültiges Argument")
    print("Syntax: python3 scanner.py <ip/hostname> <port_anfang> <port_ende>")
    print("Falls Ports nicht gesetzt, p_a = 1, p_e = 1000")
    sys.exit()

print("-"*50)
print("Scannt Ziel: "+target)
print("Zeit Anfang: " +str(datetime.now()))
print("-"*50)

class PortThreading(threading.Thread):
    def __init__(self, target, port):
	threading.Thread.__init__(self)
	self.target = target
	self.port = port

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET stellt Ipv4 dar, SOCK_STREAM TCP
        socket.setdefaulttimeout(0.5)
        result = s.connect_ex((target, port))
        if result == 0:
            print("Port {}".format(port) +" ist offen.")
	if port == port_ende:
            print("-"*50)
	    print("Ziel "+target +" erfolgreich gescannt.")
    	    print("Zeit Ende: " +str(datetime.now()))
    	    print("-"*50)
        s.close()

try: 
    for port in range(port_anfang, port_ende+1):
        scan = PortThreading(target, port)
	scan.start()
         
except KeyboardInterrupt:
    sys.exit()

except socket.gaierror:
    print("Hostname konnte nicht aufgelöst werden.")
    sys.exit()

except socket.error:
    print("Konnte nicht zum Server verbinden.")
    sys.exit()

