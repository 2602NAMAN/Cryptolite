from cryptography.fernet import Fernet, InvalidToken
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
from tkinterdnd2 import DND_FILES, TkinterDnD
import tkinter as tk
import sv_ttk
import os
import random
import string
import pyperclip
import ctypes


try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  # DPI_AWARENESS_UNAWARE
except AttributeError:
    ctypes.windll.user32.SetProcessDPIAware()


def on_drop(event):

    file_list = event.data
    if file_list:
        # Concatenate characters to form the file path
        file_path = ''.join(file_list)
        # Remove any leading or trailing whitespace and curly braces
        file_path = file_path.strip('{}').strip()
        print("Dropped file path:", file_path)
        browseFiles.filename = file_path
        file_name = os.path.basename(file_path)
        drag_n_drop_label.configure(text=file_name, wraplength=150)


def browseFiles():

    browseFiles.filename = filedialog.askopenfilename()
    if browseFiles.filename:
        file_name = os.path.basename(browseFiles.filename)
        drag_n_drop_label.configure(text=file_name, wraplength=150)
    else:
        drag_n_drop_label.configure(text="Drag & Drop File")


def clear_file():

    password.delete(0, 'end')
    confirm_password.delete(0, 'end')
    save_entry.delete(0, 'end')
    browseFiles.filename = ""
    drag_n_drop_label.configure(text="Drag & Drop File")
    status_label.configure(text="Ready!")
    

def toggle_password_visibility(password_field, confirm_password_field):

    if password_field["show"] == "":
        password_field["show"] = "*"
        confirm_password_field["show"] = "*"
        show_password_button.config(text="Show")
    else:
        password_field["show"] = ""
        confirm_password_field["show"] = ""
        show_password_button.config(text="Hide")


def copy_password():

    generated_password = confirm_password.get()
    pyperclip.copy(generated_password)


def clear_password(password_field, confirm_password_field):

    password_field.delete(0, 'end')
    confirm_password_field.delete(0, 'end')


def generate_random_password(password_field, confirm_password_field):

    characters = string.ascii_letters + string.digits
    random_password = ''.join(random.choices(characters, k=24))
    password_field.delete(0, 'end')
    confirm_password_field.delete(0, 'end')
    password_field.insert(0, random_password)
    confirm_password_field.insert(0, random_password)


def browse_save_location(entry):

    save_location = filedialog.askdirectory()
    if save_location:
        entry.delete(0, tk.END)
        entry.insert(0, save_location)
        
    print("File save location:", save_location)


def encrypt_file(password, confirm_password):

    if not browseFiles.filename:
        status_label.configure(text="Please select a file!")
        return

    if not password.get():
        status_label.configure(text="Please enter a password!")
        return

    if not confirm_password.get():
        status_label.configure(text="Please confirm the password!")
        return

    if password.get() != confirm_password.get():
        status_label.configure(text="Your Passwords don't match!")
        return

    save_location = save_entry.get()
    if not save_location:
        status_label.configure(text="Please select a save location!")
        return

    temp_key = password.get()
    temp_key = ''.join(e for e in temp_key if e.isalnum())
    key = temp_key + ("s" * (43 - len(temp_key)) + "=")

    fernet = Fernet(key)

    if browseFiles.filename.endswith('.enc'):
        status_label.configure(text="File is already encrypted!")
        return

    with open(browseFiles.filename, 'rb') as file:  
        original = file.read()
    encrypted = fernet.encrypt(original)

    with open(os.path.join(save_location, os.path.basename(browseFiles.filename) + '.enc'), 'wb') as encrypted_file:    
        encrypted_file.write(encrypted)

    status_label.configure(text="Encrypted!")


def decrypt_file(password, confirm_password):

    if not browseFiles.filename:
        status_label.configure(text="Please select a file!")
        return

    if not password.get():
        status_label.configure(text="Please enter a password!")
        return

    if not confirm_password.get():
        status_label.configure(text="Please confirm the password!")
        return

    if password.get() != confirm_password.get():
        status_label.configure(text="Your Passwords don't match!")
        return

    save_location = save_entry.get()
    if not save_location:
        status_label.configure(text="Please select a save location!")
        return

    temp_key = password.get()
    temp_key = ''.join(e for e in temp_key if e.isalnum())
    key = temp_key + ("s" * (43 - len(temp_key)) + "=")

    fernet = Fernet(key)

    if not browseFiles.filename.endswith('.enc'):
        status_label.configure(text="File is not encrypted!")
        return

    with open(browseFiles.filename, 'rb') as enc_file:  
        encrypted = enc_file.read()
    try:
        decrypted = fernet.decrypt(encrypted)
    except InvalidToken:
        status_label.configure(text="Wrong Password!")
        return

    decrypted_file_path = os.path.join(save_location, os.path.basename(browseFiles.filename)[:-4])  # Remove '.enc' extension
    with open(decrypted_file_path, 'wb') as dec_file:  
        dec_file.write(decrypted)

    status_label.configure(text="Decrypted!")


window = TkinterDnD.Tk()

# Register drop target
window.drop_target_register(DND_FILES)
window.dnd_bind('<<Drop>>', on_drop)

window.title('Cryptolite')
window.geometry("300x480+800+250")
window.resizable(0,0)
window.iconbitmap('Images/Key.ico')

sv_ttk.set_theme("dark")

# Define a custom style for buttons with the desired font
custom_style = ttk.Style()
custom_style.configure("Custom.TButton", font=("Segoe UI", 10))

title_label = ttk.Label(window,text = "Cryptolite", font=("Segoe UI", 24, "italic"))
subtitle_label = ttk.Label(window, text="File Encryption Tool", font=("Segoe UI",10))

file_frame = ttk.Frame(window, style="Card.TFrame")
drag_n_drop_label = ttk.Label(window, text="Drag & Drop File", font=("Segoe UI",10))

addfile_img =ImageTk.PhotoImage(Image.open("Images/addfile.png"))
delete_img = ImageTk.PhotoImage(Image.open("Images/delete.png"))

browse_file_button = ttk.Button(window, text="Browse File", command=browseFiles, image=addfile_img)
clear_file_button = ttk.Button(window, text="Clear File", command=clear_file, image=delete_img)

password_label = ttk.Label(window, text="Password: ", font =("Segoe UI",10))
confirm_password_label = ttk.Label(window, text="Confirm Password: ", font =("Segoe UI",10))

password = tk.StringVar()   # Add a separate StringVar for password
confirm_password = tk.StringVar()  # Add a separate StringVar for confirm password

password = ttk.Entry(window, textvariable=password, show="*", font=("Segoe UI", 10))    # Use password variable
confirm_password = ttk.Entry(window, textvariable=confirm_password, show="*", font=("Segoe UI", 10))  # Use confirm_password variable

show_password_button = ttk.Button(window, text="Show", command=lambda: toggle_password_visibility(password, confirm_password), style="Custom.TButton")
copy_password_button = ttk.Button(window, text="Copy", command=copy_password, style="Custom.TButton")
clear_password_button = ttk.Button(window, text="Clear", command=lambda: clear_password(password, confirm_password), style="Custom.TButton")
create_password_button = ttk.Button(window, text="Create", command=lambda: generate_random_password(password, confirm_password), style="Custom.TButton")

save_label = ttk.Label(window, text="Save Location:", font=("Segoe UI", 10))
save_entry = ttk.Entry(window, font=("Segoe UI", 10))
browse_save_button = ttk.Button(window, text="Browse", command=lambda: browse_save_location(save_entry), style="Custom.TButton")

encrypt_button = ttk.Button(window, text="Encrypt",  command=lambda: encrypt_file(password, confirm_password), style="Custom.TButton")
decrypt_button = ttk.Button(window, text="Decrypt", command=lambda: decrypt_file(password, confirm_password), style="Custom.TButton")

status_label = ttk.Label(window, text="Ready!", font =("Segoe UI",10))


title_label.place(x=86, y=-2)
subtitle_label.place(x=94, y=41)

file_frame.place(x=15, y=75 ,width=270, height=90)
drag_n_drop_label.place(x=150, y=115, anchor="center")
browse_file_button.place(x=25, y=125)
clear_file_button.place(x=233, y=125)

password_label.place(x=15, y=172)
password.place(x=15, y=192, width=270)
confirm_password_label.place(x=15, y=230)
confirm_password.place(x=15, y=250, width=270)

show_password_button.place(x=15, y=290, width=62)
copy_password_button.place(x=84, y=290, width=62)
clear_password_button.place(x=153, y=290, width=62)
create_password_button.place(x=222, y=290)

save_label.place(x=15, y=335)
save_entry.place(x=15, y=355, width=190)
browse_save_button.place(x=213, y=355, width=71)

encrypt_button.place(x=15, y=410, width=127)
decrypt_button.place(x=157, y=410, width=127)

status_label.place(x=151, y=457, anchor="center")


window.mainloop()