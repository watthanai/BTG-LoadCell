import serial
import json
import keyboard
import csv
from datetime import datetime



# ser = serial.Serial(port='COM6',baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1)
ser = serial.Serial(
        port='COM8',
        baudrate=9600, 
        parity=serial.PARITY_NONE, 
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0)
print("Connected to"+ ser.portstr)
seq = []
receive =[]
count = 1
header_add = False

while True:
    
    for receive in ser.read():
        seq.append(chr(receive)) #convert from ANSII
        joined_seq = ''.join(str(v) for v in seq) #Make a string from array
        
        if chr(receive) == '\n':
            seq = []
            count += 1
            current_time = datetime.now()
            dt_string = current_time.strftime("%d/%m/%Y %H:%M:%S")
            Data={
                "Datetime":dt_string,
                "Header01":joined_seq[0:2],
                "Header02":joined_seq[3:5],
                "Weight":joined_seq[10:14],
                "Units":joined_seq[15:17]
            }
            
            print(Data)
            
            with open("Loadcell.csv","a",newline="") as f:
                if not header_add:
                    writer =csv.writer(f)
                    writer.writerow(['Datetime','Header01','Header02','Weight','Units'])
                    header_add = True
                writer =csv.writer(f)
                writer.writerow(
                    [dt_string,
                    joined_seq[0:2],
                    joined_seq[3:5],
                    joined_seq[10:14],
                    joined_seq[15:17]]
                )
                print(header_add)
                break

    if keyboard.is_pressed('q'):
        print("user need to quit the app")
        break  

ser.close()
