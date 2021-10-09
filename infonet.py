import sys, threading, socket, time, os
from time import sleep
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QApplication, QPushButton, QMessageBox
def redirect_output():
    sys.stdout = f = open("arpscan.txt", "w")
    import arpscan
    sys.stdout = sys.__stdout__
    f.close()

redirect_output()
os.system("clear")
ip_list, mac_list, vendor_list = [],[],[]
os.system("ip route | grep default > gateway.txt")
gateway_result = open("gateway.txt", "r")
gateway = gateway_result.readline()[11:23].strip()
gateway_result.close()

results = open("arpscan.txt","r")
lines = results.readlines()[2:]
for line in lines:
    if ":" in line:
        if "." in line:
            line2 = line.strip()
            for char in line2:
                time.sleep(0.015)
            line = line.split()
            mac_list.append(line[0])
            vendor_list.append(line[1])
            ip_list.append(line[2])
results.close()

os.system("rm arpscan.txt ; rm gateway.txt")
info_dct = {}
for item in ip_list:
    num = ip_list.index(item)
    info_dct[item] = {"Vendor" : vendor_list[num] , "MAC Address" : mac_list[num]}
info_dct = dict(sorted(info_dct.items()))
os.system("rm -r __pycache/")

class MainWindow(QMainWindow): 
    def __init__(self, x):                                         
        super().__init__()
        self.setGeometry(1,1,1920,1080)
        self.setWindowTitle("InfoNet")
        self.setStyleSheet("background-color: grey")
    
    def main(self):
        global x_axis
        x_axis = 10
        global y_axis
        y_axis = 10
        ip_list2 = ip_list
        ip_list2.sort()
        ports_dct = {}
        for ip_addr in ip_list2:
            ports_dct[ip_addr] = []
            def thread_function(port):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.2)
                result = s.connect_ex((ip_addr,port))
                if result == 0:
                    ports_dct[ip_addr].append(port)
                    s.close()
                    sleep(0.1)
            for i in range(49152):
                x = threading.Thread(target=thread_function, args=([i]))
                x.start()
        
        obj = 0
        for ip in ip_list2:
            self.btn = QtWidgets.QPushButton(self)
            ipv4 = ip
            def show_popup_gateway(self, vendor = info_dct[gateway]["Vendor"], ipv4 = ip ,ports_open = ports_dct[ipv4]):
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                mac = info_dct[gateway]["MAC Address"].upper()
                msg.setWindowTitle(vendor)
                if len(ports_open) > 0:
                    msg.setText(f"IP Address: {gateway} \nMAC Address: {mac} \nVendor: {vendor} \nOpen Ports: {','.join(str(x) for x in ports_open)}")
                elif len(ports_open) == 0:
                    msg.setText(f"IP Address: {ipv4} \nMAC Address: {mac} \nVendor: {vendor} \nOpen Ports: COULD NOT FIND ANY")
                x = msg.exec()
            ipv4 = ip
            def show_popup(self, vendor = info_dct[ip]["Vendor"], mac = info_dct[ip]["MAC Address"].upper(), ipv4 = ip, ports_open = ports_dct[ipv4]):
                msg2 = QMessageBox()
                msg2.setIcon(QMessageBox.Information)
                msg2.setWindowTitle(vendor)
                if len(ports_open) > 0:
	                msg2.setText(f"IP Address: {ipv4} \nMAC Address: {mac} \nVendor: {vendor} \nOpen Ports: {', '.join(str(x) for x in ports_open)}")
                elif len(ports_open) == 0:
                    msg2.setText(f"IP Address: {ipv4} \nMAC Address: {mac} \nVendor: {vendor} \nOpen Ports: COULD NOT FIND ANY")
                x2 = msg2.exec()

            if obj == 9:
                x_axis = 10
                y_axis += 110
                obj = 0
            if ip == gateway:
                self.btn.setText(f"\n{ip}\n(Gateway)\n")
                self.btn.clicked.connect(show_popup_gateway)
                self.btn.move(x_axis, y_axis)
                self.btn.setStyleSheet("border-radius : 20; border: 3px solid blue")
                self.btn.setFont(QFont("Comfortaa",15))
            else:
                vendor = info_dct[ip]["Vendor"]
                mac = info_dct[ip]["Vendor"]
                self.btn.setText(f"\n{ip}\n({vendor})\n")
                self.btn.clicked.connect(show_popup)
                self.btn.move(x_axis, y_axis)
                self.btn.setStyleSheet("border: 2px solid black; border-radius : 30 ")
            self.btn.setFont(QFont("Comfortaa",15))
            self.btn.adjustSize()
            x_axis += 190
            y_axis += 0
            obj += 1
		
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow(len(ip_list))                                            
    mainWin.main()
    mainWin.show()
    sys.exit( app.exec_() )
