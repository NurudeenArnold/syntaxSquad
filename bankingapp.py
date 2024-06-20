import tkinter as tk
import customtkinter
from tkinter import messagebox, PhotoImage
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

customtkinter.set_appearance_mode("Light")
customtkinter.set_default_color_theme("themes/red.json")

class User:
    def __init__(self, email, password, pin, account_number):
        self.email = email
        self.password = password
        self.pin = pin
        self.account_number = account_number
        self.balance = 0.0
        self.transactions = []

class BankingApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("NexBank")
        self.root.geometry("500x500")
        self.root.configure(bg="blue")
        self.logged_in_user = None
        self.users = {}
        self.load_users()
        self.current_frame = None
        self.root.resizable(False, False)
        self.create_main_window()

    def load_users(self):
        try:
            with open("UserData.txt", "r") as file:
                for line in file:
                    data = line.strip().split(",")
                    if len(data) == 4:
                        email, password, pin, account_number = data
                        self.users[email] = User(email, password, pin, account_number)
        except FileNotFoundError:
            pass

    def save_users(self):
        with open("UserData.txt", "w") as file:
            for user in self.users.values():
                file.write(f"{user.email},{user.password},{user.pin},{user.account_number}\n")

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.root.geometry(f"{width}x{height}+{int(x)}+{int(y)}")

    def create_main_window(self):
        self.clear_current_frame()
        self.root.configure(bg="red")
        self.label_main = customtkinter.CTkLabel(self.root, text="Welcome to NexBank!", font=("Helvetica", 25), text_color="red")
        self.label_main.pack(pady=20)

        image = PhotoImage(file="Nex3.png")
        resizedImage = image.subsample(1, 1)
        self.image_label = customtkinter.CTkLabel(self.root, image=resizedImage, text="")
        self.image_label.image = resizedImage
        self.image_label.pack(pady=20)

        self.button_login = customtkinter.CTkButton(self.root, text="Login", command=self.open_login_window)
        self.button_login.pack(pady=10)

        self.button_register = customtkinter.CTkButton(self.root, text="Register", command=self.open_registration_window)
        self.button_register.pack()

        self.button_quit = customtkinter.CTkButton(self.root, text="Quit", command=self.quit_application)
        self.button_quit.pack(pady=10)

        self.error_label = customtkinter.CTkLabel(self.root, text="", text_color="red")
        self.error_label.pack()

    def clear_current_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def quit_application(self):
        if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
            self.root.destroy()

    def open_registration_window(self):
        self.clear_current_frame()

        self.label_title = customtkinter.CTkLabel(self.root, text="Register", font=("Helvetica", 25), text_color="red")
        self.label_title.pack(pady=10)

        registration_frame = customtkinter.CTkFrame(self.root)
        registration_frame.pack(padx=10, pady=10)

        self.label_email = customtkinter.CTkLabel(registration_frame, text="Email:")
        self.label_email.pack()

        self.entry_email = customtkinter.CTkEntry(registration_frame)
        self.entry_email.pack()

        self.label_password = customtkinter.CTkLabel(registration_frame, text="Password:")
        self.label_password.pack()

        self.entry_password = customtkinter.CTkEntry(registration_frame, show="*")
        self.entry_password.pack()

        self.label_pin = customtkinter.CTkLabel(registration_frame, text="PIN:")
        self.label_pin.pack()

        self.entry_pin = customtkinter.CTkEntry(registration_frame, show="*")
        self.entry_pin.pack()

        self.var_generate_password = tk.BooleanVar()
        self.checkbutton_generate_password = customtkinter.CTkCheckBox(registration_frame, text="Generate a random password", variable=self.var_generate_password, command=self.toggle_password_entry)
        self.checkbutton_generate_password.pack(pady=(10), padx=10)

        self.error_label_reg = customtkinter.CTkLabel(registration_frame, text="", text_color="red")
        self.error_label_reg.pack(padx=10)

        self.button_register = customtkinter.CTkButton(registration_frame, text="Register", command=self.register_user)
        self.button_register.pack(pady=(5, 30), padx=100)

        self.button_back = customtkinter.CTkButton(registration_frame, text="Back", command=self.create_main_window)
        self.button_back.pack(pady=(5, 30), padx=100)

        self.center_window(450, 650)

    def toggle_password_entry(self):
        if self.var_generate_password.get():
            generated_password = self.generate_password()
            self.entry_password.configure(state='normal')
            self.entry_password.delete(0, tk.END)
            self.entry_password.insert(0, generated_password)
            self.entry_password.configure(state='disabled')
        else:
            self.entry_password.configure(state='normal')
            self.entry_password.delete(0, tk.END)

    def open_login_window(self):
        self.clear_current_frame()

        self.label_title = customtkinter.CTkLabel(self.root, text="Login", font=("Helvetica", 25), text_color="red")
        self.label_title.pack(pady=10)

        login_frame = customtkinter.CTkFrame(self.root)
        login_frame.pack(padx=10, pady=10)

        self.label_email = customtkinter.CTkLabel(login_frame, text="Email:")
        self.label_email.pack()

        self.entry_email = customtkinter.CTkEntry(login_frame)
        self.entry_email.pack()

        self.label_password = customtkinter.CTkLabel(login_frame, text="Password:")
        self.label_password.pack()

        self.entry_password = customtkinter.CTkEntry(login_frame, show="*")
        self.entry_password.pack()

        self.button_login = customtkinter.CTkButton(login_frame, text="Login", command=self.login_user)
        self.button_login.pack(pady=10)

        self.button_back = customtkinter.CTkButton(login_frame, text="Back", command=self.create_main_window)
        self.button_back.pack()

        self.error_label = customtkinter.CTkLabel(login_frame, text="", text_color="red")
        self.error_label.pack()

        self.center_window(450, 450)

    def generate_password(self):
        length = 8
        letters_and_digits = string.ascii_letters + string.digits
        return ''.join(random.choice(letters_and_digits) for i in range(length))

    def register_user(self):
        email = self.entry_email.get()
        password = self.entry_password.get()
        pin = self.entry_pin.get()

        if not email or not password or not pin:
            self.error_label_reg.configure(text="All fields are required.")
            return

        if email in self.users:
            self.error_label_reg.configure(text="Email already registered.")
            return

        account_number = self.generate_account_number()
        self.users[email] = User(email, password, pin, account_number)
        self.save_users()

        # Send email with registration details
        self.send_registration_email(email, password)

        self.error_label_reg.configure(text="Registration successful.", text_color="green")

    def login_user(self):
        email = self.entry_email.get()
        password = self.entry_password.get()

        if email in self.users and self.users[email].password == password:
            self.logged_in_user = self.users[email]
            self.error_label.configure(text="")
            self.open_account_window()
        else:
            self.error_label.configure(text="Invalid email or password.")

    def generate_account_number(self):
        return ''.join(random.choices(string.digits, k=10))

    def send_registration_email(self, email, password):
        sender_email = "sewparsad60@gmail.com"
        sender_password = "xahk ahrn vvyl lgua"  # Replace this with your app password
        subject = "NexBank Registration Successful"
        body = f"Dear User,\n\nThank you for registering with NexBank.\n\nYour login details are as follows:\nEmail: {email}\nPassword: {password}\n\nPlease keep this information secure.\n\nBest regards,\nNexBank Team"

        msg = MIMEMultipart()
        msg['From'] = "Nex Bank"
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, email, text)
            server.quit()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send email: {str(e)}")

    def open_account_window(self):
        self.clear_current_frame()

        self.label_title = customtkinter.CTkLabel(self.root, text="Account Details", font=("Helvetica", 25), text_color="red")
        self.label_title.pack(pady=10)

        account_frame = customtkinter.CTkFrame(self.root)
        account_frame.pack(padx=10, pady=10)

        self.label_account_number = customtkinter.CTkLabel(account_frame, text=f"Account Number: {self.logged_in_user.account_number}")
        self.label_account_number.pack()

        self.label_balance = customtkinter.CTkLabel(account_frame, text=f"Balance: ${self.logged_in_user.balance:.2f}")
        self.label_balance.pack()

        self.button_logout = customtkinter.CTkButton(account_frame, text="Logout", command=self.logout_user)
        self.button_logout.pack(pady=10)

    def logout_user(self):
        self.logged_in_user = None
        self.create_main_window()

if __name__ == "__main__":
    root = customtkinter.CTk()
    app = BankingApplication(root)
    root.mainloop()
