
import tkinter as tk
import socket
import time

# Данные сервера
UDP_IP = '192.168.4.1'
UDP_PORT = 7
server_addr = (UDP_IP, UDP_PORT)

BUFFER_SIZE = 1024

# socket - функция создания сокета
# Первый параметр socket_family может быть AF_INET или AF_UNIX
# Второй параметр socket_type может быть SOCK_STREAM (для TCP) или SOCK_DGRAM (для UDP)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def led_on():
    data = b'ledon'

    s.settimeout(1.0)
    s.sendto(data, server_addr)
    try:
        data, addr = s.recvfrom(BUFFER_SIZE)
        if data == b'ledon':
            label_res["text"] = 'LED ON!'
        else:
            label_res["text"] = 'UNKNOWN RESPONSE'
    except socket.timeout:
        label_res["text"] = 'REQUEST TIMED OUT'


def led_off():
    data = b'ledoff'

    s.settimeout(1.0)
    s.sendto(data, server_addr)
    try:
        data, addr = s.recvfrom(BUFFER_SIZE)
        if data == b'ledoff':
            label_res["text"] = 'LED OFF!'
        else:
            label_res["text"] = 'UNKNOWN RESPONSE'
    except socket.timeout:
        label_res["text"] = 'REQUEST TIMED OUT'


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    window = tk.Tk()

    button_on = tk.Button(text="LED ON", command=led_on)
    button_off = tk.Button(text="LED OFF", command=led_off)
    label_res = tk.Label(text="-")

    button_on.pack()
    button_off.pack()
    label_res.pack()

    window.mainloop()

    s.close()
