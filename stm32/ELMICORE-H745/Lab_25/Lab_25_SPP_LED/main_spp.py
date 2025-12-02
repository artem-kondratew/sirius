import tkinter as tk
import serial
import time

ser_port = 'COM7'
ser_baud = 115200
ser_timeout = 0.1

BUFFER_SIZE = 1024

ser = serial.Serial(port=ser_port, baudrate=ser_baud, timeout=ser_timeout)


def send_custom_text():
    text = entry.get().strip()
    if not text:
        label_res["text"] = "Please enter text to send"
        return
        
    data_w = text.encode('utf-8')
    ser.write(data_w)
    try:
        data_r = ser.read(BUFFER_SIZE).decode("utf-8", errors="ignore")
        print(f"Sent: {text}, Received: {data_r}")
        if data_r == text:
            label_res["text"] = f"Echo: {data_r}"
        else:
            label_res["text"] = f'Response: {data_r}'
    except serial.SerialTimeoutException:
        label_res["text"] = 'REQUEST TIMED OUT'


def callback():
    data = f'{15}'
    data_w = data.encode('utf-8')
    ser.write(data_w)
    try:
        data_r = ser.read(BUFFER_SIZE).decode("utf-8", errors="ignore")
        print(f"Sent: {data}, Received: {data_r}")
        if data_r == data:
            label_res["text"] = data_r
        else:
            label_res["text"] = f'Response: {data_r}'
    except serial.SerialTimeoutException:
        label_res["text"] = 'REQUEST TIMED OUT'


if __name__ == '__main__':
    window = tk.Tk()
    window.title("Serial Controller")
    window.geometry("350x250")

    input_frame = tk.Frame(window)
    input_frame.pack(pady=10)

    tk.Label(input_frame, text="Enter text:").pack()
    
    entry = tk.Entry(input_frame, width=30, font=("Arial", 10))
    entry.pack(pady=5)
    
    send_button = tk.Button(input_frame, text="Send Text", command=send_custom_text, width=10, height=1)
    send_button.pack(pady=5)

    label_res = tk.Label(window, text="-", font=("Arial", 12), wraplength=300, justify="left")
    label_res.pack(pady=10)

    window.bind('<Return>', lambda event: send_custom_text())

    window.mainloop()
    ser.close()