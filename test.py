import socket, threading, time
from time import sleep
ip_list = ["localhost"]
for ip in ip_list:
    print(f"---------\nScanning {ip}\n----------------")
    def thread_function(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.1)
        results = s.connect_ex((ip, port))
        if results == 0:
            print(f"Port {port}: open")
            s.close()
            sleep(0.1)
        else:
            s.close()
            sleep(0.1)
        

    for i in range(65535):
       x = threading.Thread(target=thread_function, args=[i])
       x.start()

