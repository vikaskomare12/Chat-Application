import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog

HOST = '127.0.0.1'
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

window = tk.Tk()
window.title("Chat Application")
window.geometry("600x500")

chat_area = scrolledtext.ScrolledText(window)
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

message_entry = tk.Entry(window, width=50)
message_entry.pack(padx=10, pady=5)

def receive():
    while True:
        try:
            message = client.recv(1024).decode()
            chat_area.insert(tk.END, message + "\n")
            chat_area.see(tk.END)
        except:
            break

def send():
    message = message_entry.get()

    if message.strip() != "":
        client.send(message.encode())

    message_entry.delete(0, tk.END)

def upload_file():
    path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[
            ("Image Files", "*.png *.jpg *.jpeg *.gif"),
            ("All Files", "*.*")
        ]
    )

    if path:
        chat_area.insert(tk.END, f"Selected Image: {path}\n")
        chat_area.see(tk.END)

send_button = tk.Button(
    window,
    text="Send",
    command=send
)
send_button.pack(pady=5)

upload_button = tk.Button(
    window,
    text="Upload Image",
    command=upload_file
)
upload_button.pack(pady=5)

thread = threading.Thread(target=receive)
thread.daemon = True
thread.start()

window.mainloop()