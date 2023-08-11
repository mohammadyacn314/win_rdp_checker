import socket
from datetime import datetime
import threading
import ipaddress
import time , random


def generate_ip_range(s_ip, e_ip):
    start_ip = ipaddress.IPv4Address(s_ip)
    end_ip = ipaddress.IPv4Address(e_ip)
    ip_list = []
    current_ip = start_ip
    while current_ip <= end_ip:
        ip_list.append(str(current_ip))
        current_ip += 1    
    
    return ip_list


def scan_port(ip,fromport=1,toport=65536):
    try:
        print("-" * 50)
        global ip_founded_counter
        for port in range(fromport,toport):
            try:
                print(f"{ip}:{port}")
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)  # Set a timeout in seconds to avoid hanging
                s.connect((ip, port))
                s.sendall(b"\x03\x00\x00\x13\x0e\xe0\x00\x00\x00\x00\x00\x01\x00\x08\x00\x03\x00\x00\x00")
                data = s.recv(1024)  
                if data and b"\x03\x00\x00\x13\x0e\xd0\x00\x00\x124\x00\x02\x1f\x08\x00\x02\x00\x00\x00" in data:
                    print("++++++++++++ Open : "+ip+":"+str(port))
                    ip_founded_counter = ip_founded_counter+1
                    scanning_ips.remove(ip)
                    scanned_ips_port.append(ip+":"+str(port))   
                    with open("ok_ips.txt", "a") as file:
                        file.write(ip+":"+str(port)+"\n")  
                    return ip+":"+str(port)
                s.close()
            except Exception as e:
                pass
                #print("Error"+str(e))
        
    except Exception as e:
        #pass
        print("Error"+str(e))
    scanning_ips.remove(ip)
    return ""

scanning_ips = []
scanned_ips_port = []
if __name__ == "__main__":

    ip_counter = 0 
    ip_founded_counter = 0 
    target_ips = []
    max_threads = 100
    with open('ips.txt', 'r') as f:
        ranges = f.readlines()
        for range_i in ranges:        
            range_j = range_i.strip().split(':')[0]
            target_ips.append(range_j)


    for target_ip in target_ips:
        scanned_ips_port_txt = ""
        scanned_ips_port = []
        while len(scanning_ips) >= max_threads:
            time.sleep(0.1)
            print(f"Searched : {ip_counter}  || Founded : {ip_founded_counter}")
        ip_counter = ip_counter+1
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
        if len(scanning_ips) < max_threads:
            scanning_ips.append(target_ip)
            t = threading.Thread(target=scan_port, args=(target_ip,))
            t.start()
    


                    
            

