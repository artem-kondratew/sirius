
import tkinter as tk
import socket
import time


TCP_IP = '192.168.4.1'
TCP_PORT = 80
server_addr = (TCP_IP, TCP_PORT)

BUFFER_SIZE = 1024

# socket - функция создания сокета
# Первый параметр socket_family может быть AF_INET или AF_UNIX
# Второй параметр socket_type может быть SOCK_STREAM (для TCP) или SOCK_DGRAM (для UDP)


def led_on():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.0)

    data = b'ledon'
    s.connect(server_addr)

    s.send(data)
    s.settimeout(1.0)
    try:
        data = s.recv(BUFFER_SIZE)
        if data == b'ledon':
            label_res["text"] = 'LED ON!'
        else:
            label_res["text"] = 'UNKNOWN RESPONSE'
    except socket.timeout:
        label_res["text"] = 'REQUEST TIMED OUT'


def led_off():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.0)

    data = b'ledoff'
    s.connect(server_addr)

    s.send(data)
    s.settimeout(1.0)
    try:
        data = s.recv(BUFFER_SIZE)
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
