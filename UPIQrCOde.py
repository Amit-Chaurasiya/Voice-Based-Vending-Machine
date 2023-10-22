import tkinter as tk
from PIL import Image, ImageTk
import qrcode
import time
import os

def generate_qr_code(myUPI, file_name):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(myUPI)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(file_name)

def close_window(root, file_name):
    root.destroy()
    os.remove(file_name)

def open_and_close_qr_code(file_name):
    root = tk.Tk()
    root.title("QR Code Viewer")

    qr_code_image = Image.open(file_name)
    qr_code_photo = ImageTk.PhotoImage(qr_code_image)

    label = tk.Label(root, image=qr_code_photo)
    label.pack()

    #root.after(1000, lambda: close_window(root, file_name))

    root.mainloop()

if __name__ == "__main__":
    myUPI = "upi://pay?pa=benroman1712345@okicici&pn=Amit%20Chaurasiya&am=10.00&tn=For%20Vending%20Machine&cu=INR"
    
    qr_code_file_name = "myUPIid.png"
    generate_qr_code(myUPI, qr_code_file_name)
    
    open_and_close_qr_code(qr_code_file_name)
