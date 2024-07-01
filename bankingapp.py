import os
import tempfile
import tkinter as tk
import customtkinter
from tkinter import Canvas, Frame, messagebox, PhotoImage
from PIL import Image, ImageTk
import random
import string
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
from tkinter import filedialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import threading
from email.mime.application import MIMEApplication
from email.utils import formataddr

customtkinter.set_appearance_mode("Light")
customtkinter.set_default_color_theme("themes/red.json")

class User:
    def __init__(self, email, password, account_number, contact, ID, dob):
        self.email = email
        self.password = password
        self.account_number = account_number
        self.balance = 500.0
        self.transactions = []
        self.contact = contact
        self.ID = ID
        self.dob = dob


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

        self.show_path = "eye.png"
        self.show = Image.open(self.show_path)
        self.show = self.show.resize((20, 20), Image.LANCZOS)
        self.imgShow = ImageTk.PhotoImage(self.show)

        self.hide_path = "eyeslash.png"
        self.hide = Image.open(self.hide_path)
        self.hide = self.hide.resize((20, 20), Image.LANCZOS)
        self.imgHide = ImageTk.PhotoImage(self.hide)

        self.user_path = "user.png"
        self.user = Image.open(self.user_path)
        self.user = self.user.resize((20, 20), Image.LANCZOS)
        self.imgUser = ImageTk.PhotoImage(self.user)

        self.phone_path = "phone.png"
        self.phone = Image.open(self.phone_path)
        self.phone = self.phone.resize((20, 20), Image.LANCZOS)
        self.imgPhone = ImageTk.PhotoImage(self.phone)

        self.email_path = "email.png"
        self.email = Image.open(self.email_path)
        self.email = self.email.resize((20, 20), Image.LANCZOS)
        self.imgEmail = ImageTk.PhotoImage(self.email)

        self.password_path = "password.png"
        self.password = Image.open(self.password_path)
        self.password = self.password.resize((20, 20), Image.LANCZOS)
        self.imgPassword = ImageTk.PhotoImage(self.password)

    def load_users(self):
        try:
            with open("UserData.txt", "r") as file:
                for line in file:
                    data = line.strip().split(",")
                    if len(data) == 7:
                        email, password, account_number, contact, ID, dob, balance = data
                        self.users[email] = User(email, password, account_number, contact, ID, dob)
                        self.users[email].balance = float(balance)
                    elif len(data) == 6:
                        email, password, account_number, contact, ID, dob = data
                        self.users[email] = User(email, password, account_number, contact, ID, dob)
                    self.load_transaction_history(email)
        except FileNotFoundError:
            pass

    def save_users(self):
        with open("UserData.txt", "w") as file:
            for user in self.users.values():
                file.write(
                    f"{user.email},{user.password},{user.account_number},{user.contact},{user.ID},{user.dob},{user.balance}\n")

    def load_transaction_history(self, email):
        try:
            with open("Transactionlog.txt", "r") as file:
                self.users[email].transactions.clear()
                for line in file:
                    transaction_data = line.strip().split(",")
                    if len(transaction_data) >= 2 and transaction_data[0] == email:
                        transaction_details = ",".join(transaction_data[1:])
                        if email in self.users:
                            self.users[email].transactions.append(transaction_details)
        except FileNotFoundError:
            pass

    def save_transaction_log(self, email, transaction_details):
        with open("Transactionlog.txt", "a") as file:
            file.write(f"{email},{transaction_details}\n")

    def process_transfer(self):
            account_number = self.entry_account_number.get()
            amount_str = self.entry_amount.get()

            if not amount_str.strip() or not amount_str.isdigit():
                self.error_label_transfer.configure(text="Please enter a valid amount.")
                return

            try:
                amount = float(amount_str)
                if amount <= 0:
                    self.error_label_transfer.configure(text="Please enter a valid positive amount.")
                    return
            except ValueError:
                self.error_label_transfer.configure(text="Please enter a valid numeric amount.")
                return

            if account_number == self.logged_in_user.account_number:
                self.error_label_transfer.configure(text="You cannot transfer to yourself. Nice try")
                return

            bank_charges = 10  

            total_deduction = amount + bank_charges

            if total_deduction > self.logged_in_user.balance:
                self.error_label_transfer.configure(text="Insufficient funds.")
                return

            recipient = None
            for user in self.users.values():
                if user.account_number == account_number:
                    recipient = user
                    break

            if not recipient:
                self.error_label_transfer.configure(text="Recipient account number not found.")
                return

            self.logged_in_user.balance -= total_deduction
            recipient.balance += amount

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.logged_in_user.transactions.append(
                f"Transferred R{amount:.2f} to {recipient.account_number} on {timestamp}, Bank Charges: R{bank_charges:.2f}")
            recipient.transactions.append(
                f"Received R{amount:.2f} from {self.logged_in_user.account_number} on {timestamp}")

            self.save_users()
            self.save_transaction_log(self.logged_in_user.email,
                                    f"Transferred R{amount:.2f} to {recipient.account_number} on {timestamp}, Bank Charges: R{bank_charges:.2f}")
            self.save_transaction_log(recipient.email,
                                    f"Received R{amount:.2f} from {self.logged_in_user.account_number} on {timestamp}")

            self.error_label_transfer.configure(text="Transfer successful.", text_color="green")
            self.create_popup("Transfer Successful",
                            f"Transferred R{amount:.2f} to {recipient.account_number} on {timestamp}. \n Bank charges: R{bank_charges:.2f}",
                            page=self.open_dashboard)


    def process_loan(self):
        amount_str = self.entry_loan_amount.get()

        if not amount_str.strip() or not amount_str.isdigit():
            self.error_label_loan.configure(text="Please enter a valid amount.")
            return

        try:
            amount = float(amount_str)
            if amount <= 0:
                self.error_label_loan.configure(text="Please enter a valid positive amount.")
                return
        except ValueError:
            self.error_label_loan.configure(text="Please enter a valid numeric amount.")
            return

        minimum_balance_required = 500  
        if self.logged_in_user.balance < minimum_balance_required:
            self.error_label_loan.configure(text="Insufficient balance to apply for a loan.")
            return

        bank_charges = 50  

        if self.logged_in_user.balance < bank_charges:
            self.error_label_loan.configure(text="Insufficient balance to cover bank charges.")
            return
        self.logged_in_user.balance -= bank_charges

        self.logged_in_user.balance += amount

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        transaction_details = f"Loan of R{amount:.2f} received on {timestamp}, Bank Charges: R{bank_charges:.2f}"

        self.logged_in_user.transactions.append(f"{self.logged_in_user.email}, {transaction_details}")

        self.save_users()
        self.save_transaction_log(self.logged_in_user.email, transaction_details)

        self.error_label_loan.configure(text="Loan approved and credited to your account.", text_color="green")
        self.create_popup("Loan Accepted", f"Loan of R{amount:.2f} received on {timestamp}.\nBank Charges: R{bank_charges:.2f}", page=self.open_dashboard)

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.root.geometry(f"{width}x{height}+{int(x)}+{int(y)}")

    def create_main_window(self):
        self.clear_current_frame()
        self.root.configure(bg="red")
        self.label_main = customtkinter.CTkLabel(self.root, text="Welcome to NexBank!", font=("Verdana", 25),
                                                 text_color="#B22E2E")
        self.label_main.pack(pady=20)

        image = PhotoImage(file="nexbank2.png")
        resizedImage = image.subsample(1, 1)
        self.image_label = customtkinter.CTkLabel(self.root, image=resizedImage, text="")
        self.image_label.image = resizedImage
        self.image_label.pack(pady=20)

        self.button_login = customtkinter.CTkButton(self.root, text="Login", command=self.open_login_window, corner_radius=32)
        self.button_login.pack(pady=10)

        self.button_register = customtkinter.CTkButton(self.root, text="Register",
                                                       command=self.open_registration_window, corner_radius=32)
        self.button_register.pack()

        self.button_quit = customtkinter.CTkButton(self.root, text="Quit", command=self.quit_application, corner_radius=32)
        self.button_quit.pack(pady=10)

        self.error_label = customtkinter.CTkLabel(self.root, text="", text_color="red")
        self.error_label.pack()

        self.center_window(450, 550)

    def clear_current_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def quit_application(self):
        if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
            self.root.destroy()

    def toggle_password_visibility(self):
        if self.entry_password.cget('show') == '':
            self.entry_password.configure(show='*')
            self.password_visibility_button.configure(image=self.imgShow)
        else:
            self.entry_password.configure(show='')
            self.password_visibility_button.configure(image=self.imgHide)

    def toggle_password_visibility2(self):
        if self.entry_confirmPassword.cget('show') == '':
            self.entry_confirmPassword.configure(show='*')
            self.confirm_password_visibility_button2.configure(image=self.imgShow)
        else:
            self.entry_confirmPassword.configure(show='')
            self.confirm_password_visibility_button2.configure(image=self.imgHide)

    def open_registration_window(self):
        self.clear_current_frame()

        self.label_title = customtkinter.CTkLabel(self.root, text="Register", font=("Helvetica", 25), text_color="#B22E2E")
        self.label_title.pack(pady=10)

        registration_frame = customtkinter.CTkFrame(self.root)
        registration_frame.pack(padx=10, pady=10)

        self.label_ID = customtkinter.CTkLabel(registration_frame, text="ID Number:")
        self.label_ID.pack()

        ID_frame = customtkinter.CTkFrame(registration_frame, fg_color="transparent")
        ID_frame.pack()

        self.ID_visibility_button = customtkinter.CTkButton(ID_frame, image=self.imgUser,
                                                                  text="",
                                                                  width=20, height=20, fg_color="transparent",
                                                                  bg_color="transparent", hover=False)
        self.ID_visibility_button.pack(side="left", padx=(0, 0))

        self.entry_ID = customtkinter.CTkEntry(ID_frame)
        self.entry_ID.pack(side="left", padx=(0, 35))

        self.label_DOB = customtkinter.CTkLabel(registration_frame, text="DOB (DD/MM/YYYY):")
        self.label_DOB.pack()

        DOB_frame = customtkinter.CTkFrame(registration_frame, fg_color="transparent")
        DOB_frame.pack()

        self.DOB_visibility_button = customtkinter.CTkButton(DOB_frame, image=self.imgUser,
                                                                  text="",
                                                                  width=20, height=20, fg_color="transparent",
                                                                  bg_color="transparent", hover=False)
        self.DOB_visibility_button.pack(side="left", padx=(0, 0))

        self.entry_DOB = customtkinter.CTkEntry(DOB_frame)
        self.entry_DOB.pack(side="left", padx=(0, 35))

        self.label_contact = customtkinter.CTkLabel(registration_frame, text="Contact Number:")
        self.label_contact.pack()

        contact_frame = customtkinter.CTkFrame(registration_frame, fg_color="transparent")
        contact_frame.pack()

        self.contact_visibility_button = customtkinter.CTkButton(contact_frame, image=self.imgPhone,
                                                                  text="",
                                                                  width=20, height=20, fg_color="transparent",
                                                                  bg_color="transparent", hover=False)
        self.contact_visibility_button.pack(side="left", padx=(0, 0))

        self.entry_contact = customtkinter.CTkEntry(contact_frame)
        self.entry_contact.pack(side="left", padx=(0, 35))

        self.label_email = customtkinter.CTkLabel(registration_frame, text="Email:")
        self.label_email.pack()

        email_frame = customtkinter.CTkFrame(registration_frame, fg_color="transparent")
        email_frame.pack()

        self.email_visibility_button = customtkinter.CTkButton(email_frame, image=self.imgEmail,
                                                                  text="",
                                                                  width=20, height=20, fg_color="transparent",
                                                                  bg_color="transparent", hover=False)
        self.email_visibility_button.pack(side="left", padx=(0, 0))

        self.entry_email = customtkinter.CTkEntry(email_frame)
        self.entry_email.pack(side="left", padx=(0, 35))

        self.label_password = customtkinter.CTkLabel(registration_frame, text="Password:")
        self.label_password.pack()

        password_frame = customtkinter.CTkFrame(registration_frame, fg_color="transparent")
        password_frame.pack()

        self.password_button = customtkinter.CTkButton(password_frame, image=self.imgPassword,
                                                                  command=self.toggle_password_visibility, text="",
                                                                  width=20, height=20, fg_color="transparent",
                                                                  bg_color="transparent", hover=False)
        self.password_button.pack(side="left", padx=(0, 0))

        self.entry_password = customtkinter.CTkEntry(password_frame, show="*")
        self.entry_password.pack(side="left", padx=(0, 0))

        self.password_visibility_button = customtkinter.CTkButton(password_frame, image=self.imgShow,
                                                                  command=self.toggle_password_visibility, text="",
                                                                  width=20, height=20, fg_color="transparent",
                                                                  bg_color="transparent", hover=False)
        self.password_visibility_button.pack(side="left", padx=(0, 0))

        self.label_confirmPassword = customtkinter.CTkLabel(registration_frame, text="Confirm Password:")
        self.label_confirmPassword.pack()

        confirm_password_frame = customtkinter.CTkFrame(registration_frame, fg_color="transparent")
        confirm_password_frame.pack()

        self.confirm_password_visibility_button = customtkinter.CTkButton(confirm_password_frame, image=self.imgPassword,
                                                                  text="",
                                                                  width=20, height=20, fg_color="transparent",
                                                                  bg_color="transparent", hover=False)
        self.confirm_password_visibility_button.pack(side="left", padx=(0, 0))

        self.entry_confirmPassword = customtkinter.CTkEntry(confirm_password_frame, show="*")
        self.entry_confirmPassword.pack(side="left", padx=(0, 0))

        self.confirm_password_visibility_button2 = customtkinter.CTkButton(confirm_password_frame, image=self.imgShow,
                                                                  command=self.toggle_password_visibility2, text="",
                                                                  width=20, height=20, fg_color="transparent",
                                                                  bg_color="transparent", hover=False)
        self.confirm_password_visibility_button2.pack(side="left", padx=(0, 0))

        self.var_generate_password = tk.BooleanVar()
        self.checkbutton_generate_password = customtkinter.CTkCheckBox(registration_frame, text="Generate password",
                                                                       variable=self.var_generate_password,
                                                                       command=self.toggle_password_entry)
        self.checkbutton_generate_password.pack(pady=(10), padx=10)

        self.error_label_reg = customtkinter.CTkLabel(registration_frame, text="", text_color="red")
        self.error_label_reg.pack(padx=10)

        self.button_register = customtkinter.CTkButton(registration_frame, text="Register", command=self.start_register_thread, corner_radius=32)
        self.button_register.pack(pady=(5, 30), padx=100)

        self.button_back = customtkinter.CTkButton(registration_frame, text="Back", command=self.create_main_window, corner_radius=32)
        self.button_back.pack(pady=(5, 30), padx=100)

        self.center_window(450, 650)

    def toggle_password_entry(self):
        if self.var_generate_password.get():
            generated_password = self.generate_password()

            self.entry_confirmPassword.configure(state='normal')
            self.entry_confirmPassword.delete(0, tk.END)
            self.entry_confirmPassword.insert(0, generated_password)
            self.entry_confirmPassword.configure(state='disabled')

            self.entry_password.configure(state='normal')
            self.entry_password.delete(0, tk.END)
            self.entry_password.insert(0, generated_password)
            self.entry_password.configure(state='disabled')
        else:
            self.entry_confirmPassword.configure(state='normal')
            self.entry_confirmPassword.delete(0, tk.END)

            self.entry_password.configure(state='normal')
            self.entry_password.delete(0, tk.END)

    def open_login_window(self):
        self.clear_current_frame()

        self.label_title = customtkinter.CTkLabel(self.root, text="Login", font=("Helvetica", 25), text_color="#B22E2E")
        self.label_title.pack(pady=10)

        login_frame = customtkinter.CTkFrame(self.root)
        login_frame.pack(padx=10, pady=10)

        self.label_email = customtkinter.CTkLabel(login_frame, text="Email:")
        self.label_email.pack()

        email_frame = customtkinter.CTkFrame(login_frame, fg_color="transparent")
        email_frame.pack()

        self.email_visibility_button = customtkinter.CTkButton(email_frame, image=self.imgEmail,
                                                                  text="",
                                                                  width=20, height=20, fg_color="transparent",
                                                                  bg_color="transparent", hover=False)
        self.email_visibility_button.pack(side="left", padx=(0, 0))

        self.entry_email = customtkinter.CTkEntry(email_frame)
        self.entry_email.pack(side="left", padx=(0, 35))

        self.label_password = customtkinter.CTkLabel(login_frame, text="Password:")
        self.label_password.pack()

        password_frame = customtkinter.CTkFrame(login_frame, fg_color="transparent")
        password_frame.pack()

        self.password_button = customtkinter.CTkButton(password_frame, image=self.imgPassword,
                                                                  command=self.toggle_password_visibility, text="",
                                                                  width=20, height=20, fg_color="transparent",
                                                                  bg_color="transparent", hover=False)
        self.password_button.pack(side="left", padx=(0, 0))

        self.entry_password = customtkinter.CTkEntry(password_frame, show="*")
        self.entry_password.pack(side="left", padx=(0, 0))

        self.password_visibility_button = customtkinter.CTkButton(password_frame, image=self.imgShow,
                                                                command=self.toggle_password_visibility, text="",
                                                                width=20, height=20, fg_color="transparent",
                                                                bg_color="transparent", hover=False)
        self.password_visibility_button.pack(side="left", padx=(0, 0))

        self.error_label = customtkinter.CTkLabel(login_frame, text="", text_color="red")
        self.error_label.pack(padx=10)

        self.button_login = customtkinter.CTkButton(login_frame, text="Login", command=self.login_user, corner_radius=32)
        self.button_login.pack(pady=(5, 30), padx=100)

        self.button_forgot_password = customtkinter.CTkButton(login_frame, text="Forgot Password", command=self.start_forgot_thread, corner_radius=32)
        self.button_forgot_password.pack(pady=(5, 30), padx=100)

        self.button_back = customtkinter.CTkButton(login_frame, text="Back", command=self.create_main_window, corner_radius=32)
        self.button_back.pack(pady=(5, 30), padx=100)

        self.center_window(450, 550)
        
    def handle_forgot_password_error(self, message):
        self.error_label.configure(text=message)
        self.reset_forgot_password_button()
        self.enable_window()

    def reset_forgot_password_button(self):
        self.root.after(0, lambda: self.button_forgot_password.configure(text="Forgot Password"))

    def forgot_password(self):
        email = self.entry_email.get().strip()

        if not email:
            self.handle_forgot_password_error("Please enter your email address.")
            return

        user = self.users.get(email)
        if not user:
            self.handle_forgot_password_error("Email address not found.")
            return

        new_password = self.generate_temporary_password()
        user.password = new_password

        self.send_reset_email(email, new_password)
        self.save_users()

        self.error_label.configure(text="A new password has been sent to your email.", text_color="green")
        self.reset_forgot_password_button()
        self.enable_window()

    def generate_temporary_password(self, length=8):
        import random
        import string

        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for i in range(length))

    def send_reset_email(self, recipient_email, new_password):
        sender_email = "sewparsad60@gmail.com"  
        sender_password = "xahk ahrn vvyl lgua"  
        subject = " NexBank Password Reset"

        message = MIMEMultipart()
        message['From'] =  "Nex Bank"
        message['To'] = recipient_email
        message['Subject'] = subject

        body = f"Dear NexBank Customer,\n\n Your new password is: {new_password}\n\nPlease apply your new password when logging in.\n\nBest regards,\nNexBank Team"
        message.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)  
            server.starttls()
            server.login(sender_email, sender_password)
            text = message.as_string()
            server.sendmail(sender_email, recipient_email, text)
            server.quit()
        except Exception as e:
            self.error_label.configure(text=f"Failed to send email: {str(e)}")

    def return_to_main_window(self):
        self.clear_current_frame()
        self.create_main_window()

    def register_ok(self):
        self.return_to_main_window()
        self.open_login_window()

    def send_registration_email(self, email, password):
        sender_email = "sewparsad60@gmail.com"
        sender_password = "xahk ahrn vvyl lgua"
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
            server.sendmail(sender_email, email, msg.as_string())
            server.quit()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send email: {str(e)}")

    def generate_account_number(self):
        return ''.join(random.choices(string.digits, k=10))

    def generate_password(self):
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for i in range(10))

    def is_strong_password(self, password):
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in string.punctuation for c in password)
        return len(password) >= 8 and has_lower and has_upper and has_digit and has_special

    def handle_error(self, message):
        self.error_label_reg.configure(text=message)
        self.reset_register_button()
        self.enable_window()

    def reset_register_button(self):
        self.root.after(0, lambda: self.button_register.configure(text="Register"))

    def register_user(self):
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        dob = self.entry_DOB.get().strip()
        ID = self.entry_ID.get().strip()
        contact = self.entry_contact.get().strip()
        confirmPassword = self.entry_confirmPassword.get()
        password = self.entry_password.get()
        email = self.entry_email.get()
        email = email.lower()

        if not (dob and ID and contact and email and password and confirmPassword):
            self.handle_error("Please fill in all fields")
            return

        if not re.match(r'\d{2}/\d{2}/\d{4}', dob):
            self.handle_error("Please enter Date of Birth in DD/MM/YYYY format.")
            return

        try:
            dob_date = datetime.strptime(dob, '%d/%m/%Y')
        except ValueError:
            self.handle_error("Invalid Date of Birth.")
            return

        today = datetime.today()
        age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))

        if age < 18:
            self.handle_error("You must be older than 18 years to register.")
            return

        if not ID.isdigit():
            self.handle_error("Please enter a valid ID Number")
            return

        if len(ID) != 13:
            self.handle_error("Please enter a 13-digit ID Number")
            return

        if not contact.isdigit():
            self.handle_error("Please enter a valid South African phone number")
            return

        if len(contact) != 10:
            self.handle_error("Please enter a 10-digit South African phone number.")
            return

        if not email.strip():
            self.handle_error("Email cannot be empty.")
            return

        for user in self.users.values():
            if user.ID == ID:
                self.handle_error("There is already an account with this ID Number.")
                return
            if user.email == email:
                self.handle_error("Email already registered. Please try a different email.")
                return

        if not re.match(email_pattern, email):
            self.handle_error("Invalid email format.")
            return

        if self.var_generate_password.get():
            password = self.entry_password.get()
        else:
            password = self.entry_password.get()
            if not self.is_strong_password(password):
                self.handle_error("Password is not strong. \nPlease include lowercase, uppercase, digits, and symbols.")
                return

        if password != confirmPassword:
            self.handle_error("Passwords do not match.")
            return

        account_number = self.generate_account_number()
        user = User(email, password, account_number, contact, ID, dob)
        self.users[email] = user
        self.save_users()
        self.send_registration_email(email, password)

        self.create_popup("Register Successful",
                          "Please check your email for your credentials. \nYou will be able to login now.",
                          page=self.open_login_window)

    def show_registration_success_window(self, generated_password):
        self.clear_current_frame()

        label_success = customtkinter.CTkLabel(self.root, text="Registration Successful!", font=("Helvetica", 20),
                                               text_color="green")
        label_success.pack(pady=10)

        label_password = customtkinter.CTkLabel(self.root, text=f"You will be able to login now.",
                                                font=("Helvetica", 15))
        label_password.pack(pady=5)

        button_ok = customtkinter.CTkButton(self.root, text="OK", command=self.register_ok, corner_radius=32)
        button_ok.pack(pady=20)

        self.center_window(450, 150)

    def login_user(self):
        email = self.entry_email.get()
        email = email.lower()
        password = self.entry_password.get()

        if not (email and password):
            self.error_label.configure(text="Please fill in all fields")
            return

        if email in self.users and self.users[email].password == password:
            self.logged_in_user = self.users[email]
            self.open_dashboard()
        else:
            self.error_label.configure(text="Invalid email or password.")

    def open_dashboard(self):
        self.clear_current_frame()
        image = PhotoImage(file="nexbank2.png")
        resizedImage = image.subsample(2, 2)
        self.image_label = customtkinter.CTkLabel(self.root, image=resizedImage, text="")
        self.image_label.image = resizedImage
        self.image_label.pack(pady=20)

        self.label_title = customtkinter.CTkLabel(self.root, text="Dashboard", font=("Helvetica", 25), text_color="#B22E2E")
        self.label_title.pack(pady=10)

        self.button_balance = customtkinter.CTkButton(self.root, text="View Balance", command=self.view_balance, corner_radius=32)
        self.button_balance.pack(pady=10)

        self.button_transfer = customtkinter.CTkButton(self.root, text="Transfer Money", command=self.transfer_money, corner_radius=32)
        self.button_transfer.pack(pady=10)

        self.button_statement = customtkinter.CTkButton(self.root, text="View Bank Statement",
                                                        command=self.view_statement, corner_radius=32)
        self.button_statement.pack(pady=10)

        self.button_loan = customtkinter.CTkButton(self.root, text="Take Loan/Overdraft", command=self.take_loan, corner_radius=32)
        self.button_loan.pack(pady=10)

        self.button_personal_details = customtkinter.CTkButton(self.root, text="View Personal Details",
                                                               command=self.view_personal_details, corner_radius=32)
        self.button_personal_details.pack(pady=10)

        self.button_logout = customtkinter.CTkButton(self.root, text="Logout", command=self.create_main_window, corner_radius=32)
        self.button_logout.pack(pady=10)

        self.center_window(450, 650)

    def view_balance(self):
        self.clear_current_frame()

        image = PhotoImage(file="nexbank2.png")
        resizedImage = image.subsample(2, 2)
        self.image_label = customtkinter.CTkLabel(self.root, image=resizedImage, text="")
        self.image_label.image = resizedImage
        self.image_label.pack(pady=20)

        label_balance = customtkinter.CTkLabel(self.root, text=f"Your Balance: R{self.logged_in_user.balance:.2f}",
                                               font=("Helvetica", 20))
        label_balance.pack(pady=20)

        button_back = customtkinter.CTkButton(self.root, text="Back", command=self.open_dashboard, corner_radius=32)
        button_back.pack(pady=10)

        self.center_window(450, 550)

    def transfer_money(self):
        self.clear_current_frame()

        image = PhotoImage(file="nexbank2.png")
        resizedImage = image.subsample(2, 2)
        self.image_label = customtkinter.CTkLabel(self.root, image=resizedImage, text="")
        self.image_label.image = resizedImage
        self.image_label.pack(pady=20)
        self.label_title = customtkinter.CTkLabel(self.root, text="Transfer Money", font=("Helvetica", 25),
                                                  text_color="#B22E2E")
        self.label_title.pack(pady=10)

        transfer_frame = customtkinter.CTkFrame(self.root)
        transfer_frame.pack(padx=10, pady=10)

        label_account_number = customtkinter.CTkLabel(transfer_frame, text="Recipient Account Number:")
        label_account_number.pack()

        self.entry_account_number = customtkinter.CTkEntry(transfer_frame)
        self.entry_account_number.pack()

        label_amount = customtkinter.CTkLabel(transfer_frame, text="Amount:")
        label_amount.pack()

        self.entry_amount = customtkinter.CTkEntry(transfer_frame)
        self.entry_amount.pack()

        self.error_label_transfer = customtkinter.CTkLabel(transfer_frame, text="", text_color="red")
        self.error_label_transfer.pack(padx=10)

        button_transfer = customtkinter.CTkButton(transfer_frame, text="Transfer", command=self.process_transfer, corner_radius=32)
        button_transfer.pack(pady=(5, 30), padx=100)

        button_back = customtkinter.CTkButton(transfer_frame, text="Back", command=self.open_dashboard, corner_radius=32)
        button_back.pack(pady=(5, 30), padx=100)

        self.center_window(450, 550)

    def view_statement(self):
        self.clear_current_frame()
        self.load_transaction_history(self.logged_in_user.email)

        image = PhotoImage(file="nexbank2.png")
        resizedImage = image.subsample(2, 2)
        self.image_label = customtkinter.CTkLabel(self.root, image=resizedImage, text="")
        self.image_label.image = resizedImage
        self.image_label.pack(pady=20)

        label_title = customtkinter.CTkLabel(self.root, text="Bank Statement", font=("Helvetica", 25),  text_color="#B22E2E")
        label_title.pack(pady=10, padx=100)

        canvas = Canvas(self.root, borderwidth=0, highlightthickness=0)
        frame = Frame(canvas)
        vsb = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)

        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        canvas.create_window((0, 0), window=frame, anchor="n", width=self.root.winfo_width())

        frame.bind("<Configure>", lambda event, canvas=canvas: self.on_frame_configure(canvas))

        if not self.logged_in_user.transactions:
            no_transactions_label = customtkinter.CTkLabel(frame, text="No transactions made yet.", justify="center")
            no_transactions_label.pack(pady=10, padx=(30, 0))
        else:
            for transaction in self.logged_in_user.transactions:
                transaction_label = customtkinter.CTkLabel(frame, text=transaction, wraplength=400, justify="center")
                transaction_label.pack(pady=5, padx=(30, 0))

        self.error_label_pdf = customtkinter.CTkLabel(frame, text="", text_color="red")
        self.error_label_pdf.pack(padx=(30, 0))

        self.button_download = customtkinter.CTkButton(frame, text="Download as PDF",
                                                       command=self.start_download_thread, corner_radius=32)
        self.button_download.pack(pady=10, padx=(30, 0))

        self.button_email = customtkinter.CTkButton(frame, text="Email Statement",
                                                       command=self.start_emailPDF_thread, corner_radius=32)
        self.button_email.pack(pady=10, padx=(30, 0))

        button_back = customtkinter.CTkButton(frame, text="Back", command=self.open_dashboard, corner_radius=32)
        button_back.pack(pady=10, padx=(30, 0))

        self.center_window(450, 550)

    def on_frame_configure(self, canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def download_transaction_history(self):
        if not self.logged_in_user.transactions:
            self.error_label_pdf.configure(text="Cannot download if there are no transactions made yet.")
            return

        root = tk.Tk()
        root.withdraw()  
        pdf_filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=f"{self.logged_in_user.account_number}_transaction_history.pdf"
        )
        if not pdf_filename:
            return  

        c = canvas.Canvas(pdf_filename, pagesize=letter)

        logo_path = "nexbank.png"
        c.drawImage(logo_path, 50, 650, width=100, height=100)

        c.setFont("Helvetica", 12)
        c.drawString(350, 730, "ID Number: " + self.logged_in_user.ID)
        c.drawString(350, 715, "Contact Number: " + self.logged_in_user.contact)
        c.drawString(350, 700, "DOB (DD/MM/YYYY): " + self.logged_in_user.dob)
        c.drawString(350, 685, "Account Number: " + self.logged_in_user.account_number)
        c.drawString(350, 670, "Email: " + self.logged_in_user.email)

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 600, "Transaction History")

        c.setFont("Helvetica", 12)
        c.drawString(50, 570, "-" * 70)

        y_position = 555
        max_y = 50

        for transaction in self.logged_in_user.transactions:
            transaction_parts = transaction.split(" on ")
            if len(transaction_parts) >= 2:
                transaction_info = transaction_parts[0].strip()
                timestamp = transaction_parts[1].strip()

                c.drawString(50, y_position, f"Transaction: {transaction_info}")
                c.drawString(50, y_position - 15, f"Timestamp: {timestamp}")
                c.drawString(50, y_position - 30, "-" * 70)
                y_position -= 45

                if y_position < max_y:
                    c.showPage()
                    logo_path = "nexbank.png"
                    c.drawImage(logo_path, 50, 650, width=100, height=100)
                    c.setFont("Helvetica-Bold", 16)
                    c.drawString(50, 600, "Continued Transaction History")
                    c.setFont("Helvetica", 12)
                    c.drawString(50, 570, "-" * 70)
                    y_position = 555

            else:
                print(f"Issue with transaction format: {transaction}")

        c.save()
        print(f"Transaction history saved to {pdf_filename}")

    def take_loan(self):
        self.clear_current_frame()

        image = PhotoImage(file="nexbank2.png")
        resizedImage = image.subsample(2, 2)
        self.image_label = customtkinter.CTkLabel(self.root, image=resizedImage, text="")
        self.image_label.image = resizedImage
        self.image_label.pack(pady=20)

        label_title = customtkinter.CTkLabel(self.root, text="Bank Statement", font=("Helvetica", 25), text_color="#B22E2E")
        label_title.pack(pady=10)
        self.label_title = customtkinter.CTkLabel(self.root, text="Take Loan/Overdraft", font=("Helvetica", 25),
                                                  text_color="#B22E2E")
        self.label_title.pack(pady=10)

        loan_frame = customtkinter.CTkFrame(self.root)
        loan_frame.pack(padx=10, pady=10)

        label_amount = customtkinter.CTkLabel(loan_frame, text="Loan Amount:")
        label_amount.pack()

        self.entry_loan_amount = customtkinter.CTkEntry(loan_frame)
        self.entry_loan_amount.pack()

        self.error_label_loan = customtkinter.CTkLabel(loan_frame, text="", text_color="red")
        self.error_label_loan.pack(padx=10)

        button_loan = customtkinter.CTkButton(loan_frame, text="Apply", command=self.process_loan, corner_radius=32)
        button_loan.pack(pady=(5, 30), padx=100)

        button_back = customtkinter.CTkButton(loan_frame, text="Back", command=self.open_dashboard, corner_radius=32)
        button_back.pack(pady=(5, 30), padx=100)

        self.center_window(450, 550)

    def view_personal_details(self):
        self.clear_current_frame()

        image = PhotoImage(file="nexbank2.png")
        resizedImage = image.subsample(2, 2)
        self.image_label = customtkinter.CTkLabel(self.root, image=resizedImage, text="")
        self.image_label.image = resizedImage
        self.image_label.pack(pady=20)

        label_title = customtkinter.CTkLabel(self.root, text="Personal Details", font=("Helvetica", 25),
                                             text_color="#B22E2E")
        label_title.pack(pady=10)

        details_frame = customtkinter.CTkFrame(self.root)
        details_frame.pack(padx=10, pady=10)

        label_email = customtkinter.CTkLabel(details_frame, text=f"Email: {self.logged_in_user.email}")
        label_email.pack()

        label_account_number = customtkinter.CTkLabel(details_frame,
                                                      text=f"Account Number: {self.logged_in_user.account_number}")
        label_account_number.pack()

        label_email = customtkinter.CTkLabel(details_frame, text=f"Contact Number: {self.logged_in_user.contact}")
        label_email.pack()

        label_email = customtkinter.CTkLabel(details_frame, text=f"ID Number: {self.logged_in_user.ID}")
        label_email.pack()

        label_email = customtkinter.CTkLabel(details_frame, text=f"Date of Birth: {self.logged_in_user.dob}")
        label_email.pack()

        label_balance = customtkinter.CTkLabel(details_frame, text=f"Balance: R{self.logged_in_user.balance:.2f}")
        label_balance.pack()

        button_back = customtkinter.CTkButton(details_frame, text="Back", command=self.open_dashboard, corner_radius=32)
        button_back.pack(pady=10, padx=100)

        self.center_window(450, 550)

    def generate_password(self):
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for i in range(10))

    def create_popup(self, title, message, text_color="black", page=""):
        self.clear_current_frame()
        popup = customtkinter.CTkFrame(self.root)
        popup.pack(padx=20, pady=20)

        label_title = customtkinter.CTkLabel(popup, text=title, font=("Helvetica", 25), text_color="red")
        label_title.pack(pady=10, padx=30)

        label_message = customtkinter.CTkLabel(popup, text=message, font=("Helvetica", 12), text_color=text_color)
        label_message.pack(pady=10, padx=30)

        button_ok = customtkinter.CTkButton(popup, text="OK", command=page, corner_radius=32)
        button_ok.pack(pady=10, padx=100)

        self.center_window(550, 300)

    def is_strong_password(self, password):
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in string.punctuation for c in password)
        return len(password) >= 8 and has_lower and has_upper and has_digit and has_special

    def start_download_thread(self):
        download_thread = threading.Thread(target=self.download_transaction_history)
        download_thread.start()

    def start_register_thread(self):
        self.button_register.configure(text="Registering\nPlease Wait...")
        self.disable_window()
        register_thread = threading.Thread(target=self.register_user)
        register_thread.start() 

    def start_forgot_thread(self):
        self.button_forgot_password.configure(text="Please Wait...")
        self.disable_window()
        forgot_thread = threading.Thread(target=self.forgot_password)
        forgot_thread.start()

    def start_emailPDF_thread(self):
        self.button_email.configure(text="Sending\nPlease Wait...")
        self.disable_window()
        forgot_thread = threading.Thread(target=self.send_pdf_via_email)
        forgot_thread.start()

    def enable_window(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, (customtkinter.CTkButton, customtkinter.CTkEntry, customtkinter.CTkCheckBox)):
                self.enable_widget(widget)
            for child in widget.winfo_children():
                if isinstance(child, (customtkinter.CTkButton, customtkinter.CTkEntry, customtkinter.CTkCheckBox)):
                    self.enable_widget(child)

    def enable_widget(self, widget):
        try:
            widget.configure(state='normal')
        except tk.TclError:
            pass

    def disable_widget(self, widget):
        try:
            widget.configure(state='disabled')
        except tk.TclError:
            pass

    def disable_window(self):
        print("window disabled")
        for widget in self.root.winfo_children():
            if isinstance(widget, (customtkinter.CTkButton, customtkinter.CTkEntry, customtkinter.CTkCheckBox)):
                self.disable_widget(widget)
            for child in widget.winfo_children():
                if isinstance(child, (customtkinter.CTkButton, customtkinter.CTkEntry, customtkinter.CTkCheckBox)):
                    self.disable_widget(child)  

    def send_pdf_via_email(self):
        if not self.logged_in_user.transactions:
            self.error_label_pdf.configure(text="Cannot send email if there are no transactions made yet.")
            return

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        pdf_filename = temp_file.name
        temp_file.close()

        c = canvas.Canvas(pdf_filename, pagesize=letter)

        logo_path = "nexbank.png"
        c.drawImage(logo_path, 50, 650, width=100, height=100)

        c.setFont("Helvetica", 12)
        c.drawString(350, 730, "ID Number: " + self.logged_in_user.ID)
        c.drawString(350, 715, "Contact Number: " + self.logged_in_user.contact)
        c.drawString(350, 700, "DOB (DD/MM/YYYY): " + self.logged_in_user.dob)
        c.drawString(350, 685, "Account Number: " + self.logged_in_user.account_number)
        c.drawString(350, 670, "Email: " + self.logged_in_user.email)

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 600, "Transaction History")

        c.setFont("Helvetica", 12)
        c.drawString(50, 570, "-" * 70)

        y_position = 555
        max_y = 50

        for transaction in self.logged_in_user.transactions:
            transaction_parts = transaction.split(" on ")
            if len(transaction_parts) >= 2:
                transaction_info = transaction_parts[0].strip()
                timestamp = transaction_parts[1].strip()

                c.drawString(50, y_position, f"Transaction: {transaction_info}")
                c.drawString(50, y_position - 15, f"Timestamp: {timestamp}")
                c.drawString(50, y_position - 30, "-" * 70)
                y_position -= 45

                if y_position < max_y:
                    c.showPage()
                    c.drawImage(logo_path, 50, 650, width=100, height=100)
                    c.setFont("Helvetica-Bold", 16)
                    c.drawString(50, 600, "Continued Transaction History")
                    c.setFont("Helvetica", 12)
                    c.drawString(50, 570, "-" * 70)
                    y_position = 555

            else:
                print(f"Issue with transaction format: {transaction}")

        c.save()
        print(f"Transaction history saved to {pdf_filename}")

        recipient_email = self.logged_in_user.email
        subject = "Your Transaction History"
        body = "Dear Customer,\n\nPlease find attached your transaction history.\n\nBest regards,\nNexBank Team"

        sender_email = "sewparsad60@gmail.com"  
        sender_password = "xahk ahrn vvyl lgua"

        message = MIMEMultipart()
        message['From'] = formataddr(('Nex Bank', sender_email))
        message['To'] = recipient_email
        message['Subject'] = subject

        message.attach(MIMEText(body, 'plain'))

        with open(pdf_filename, 'rb') as attachment:
            part = MIMEApplication(attachment.read(), Name=os.path.basename(pdf_filename))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(pdf_filename)}"'
        message.attach(part)

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient_email, message.as_string())
            print(f"Email sent to {recipient_email} with attachment {pdf_filename}.")
            self.error_label_pdf.configure(text="Email sent with transaction history.", text_color="green")
            self.button_email.configure(text="Email PDF Statement")
        except Exception as e:
            print(f"Failed to send email: {e}")
            self.error_label_pdf.configure(text="Failed to send email.", text_color="red")
            self.button_email.configure(text="Email PDF Statement")
        os.remove(pdf_filename)

if __name__ == "__main__":
    root = customtkinter.CTk()
    app = BankingApplication(root)
    root.mainloop()
