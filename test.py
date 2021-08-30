import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QApplication, QPushButton
import os, time
os.system("python3 arpscan.py > arpscan.txt ")
results = open("arpscan.txt", "r")
lines=  results.readlines()[2:]
ip_list, mac_list, vendor_list = [],[],[]
os.system("ip route | grep default > gateway.txt")
gateway_result = open("gateway.txt", "r")
gateway = gateway_result.readline()[11:23].strip()

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
os.system("rm arpscan.txt")
info_dct = {}

for item in ip_list:
    num = ip_list.index(item)
    info_dct[item] = {"Vendor" : vendor_list[num] , "MAC Address" : mac_list[num]}
info_dct = dict(sorted(info_dct.items()))


class MainWindow(QMainWindow): 
    def __init__(self, x):                                         
        super().__init__()
        self.setGeometry(1,1,1920,1080)
        self.setWindowTitle("InfoNet")
        self.setStyleSheet("background-color: grey")
    
    def progess_bar(self):
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(0,0,1920,1080)
    def main(self):
        global x_axis
        x_axis = 10
        global y_axis
        y_axis = 10
        ip_list2 = ip_list
        ip_list2.sort()
        obj = 0
        for ip in ip_list2:
            self.btn = QtWidgets.QPushButton(self)
            vendor = info_dct[ip]["Vendor"]
            if obj == 2:
                x_axis = 10
                y_axis += 110
                obj = 0
            if ip == gateway:
                self.btn.setText(f"\n{ip}\n(Gateway)\n")
                self.btn.clicked.connect(lambda ch, vendor = info_dct[ip]["Vendor"] , mac = info_dct[ip]["MAC Address"] : print(vendor,mac))
                self.btn.move(900, 450)
                self.btn.setStyleSheet("border-radius : 20; border: 3px solid blue")
                self.btn.setFont(QFont("Comfortaa",15))
                self.btn.adjustSize()
                x_axis += 0
                y_axis += 0
            else:
                self.btn.setText(f"\n{ip}\n({vendor})\n")
                self.btn.clicked.connect(lambda ch, mac = info_dct[ip]["MAC Address"] : print(vendor,mac))
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
