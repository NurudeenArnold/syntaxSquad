import tkinter as tk
import customtkinter
from tkinter import messagebox, PhotoImage
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

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
            self.open_dashboard()
        else:
            self.error_label.configure(text="Invalid email or password.")

    def generate_account_number(self):
        return ''.join(random.choices(string.digits, k=10))

    def send_registration_email(self, email, password):
        sender_email = "sewparsad60@gmail.com"
        sender_password = "xahk ahrn vvyl lgua"  # Replace this with your app password
        subject = "NexBank Registration Successful"
        body = f"Dear User,\n\nThank you for registering with NexBank.\n\nYour login details are as follows:\nEmail: {email}\nPassword: {password}\n\nPlease keep this information secure.\n\nBest Regards,\nNexBank Team"

        msg = MIMEMultipart()
        msg['From'] = "Nex Bank"
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, msg.as_string())
            server.quit()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send email: {str(e)}")

    def open_dashboard(self):
        self.clear_current_frame()

        self.label_title = customtkinter.CTkLabel(self.root, text="Dashboard", font=("Helvetica", 25), text_color="red")
        self.label_title.pack(pady=10)

        dashboard_frame = customtkinter.CTkFrame(self.root)
        dashboard_frame.pack(padx=10, pady=10)

        self.label_welcome = customtkinter.CTkLabel(dashboard_frame, text=f"Welcome, {self.logged_in_user.email}!")
        self.label_welcome.pack()

        self.button_account_details = customtkinter.CTkButton(dashboard_frame, text="Account Details", command=self.open_account_window)
        self.button_account_details.pack(pady=5)

        self.button_deposit = customtkinter.CTkButton(dashboard_frame, text="Deposit", command=self.open_deposit_window)
        self.button_deposit.pack(pady=5)

        self.button_withdraw = customtkinter.CTkButton(dashboard_frame, text="Withdraw", command=self.open_withdraw_window)
        self.button_withdraw.pack(pady=5)

        self.button_transaction_history = customtkinter.CTkButton(dashboard_frame, text="Transaction History", command=self.open_transaction_history_window)
        self.button_transaction_history.pack(pady=5)

        self.button_logout = customtkinter.CTkButton(dashboard_frame, text="Logout", command=self.logout_user)
        self.button_logout.pack(pady=10)

        self.center_window(450, 450)

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

        self.button_back = customtkinter.CTkButton(account_frame, text="Back", command=self.open_dashboard)
        self.button_back.pack(pady=10)

    def open_deposit_window(self):
        self.clear_current_frame()

        self.label_title = customtkinter.CTkLabel(self.root, text="Deposit", font=("Helvetica", 25), text_color="red")
        self.label_title.pack(pady=10)

        deposit_frame = customtkinter.CTkFrame(self.root)
        deposit_frame.pack(padx=10, pady=10)

        self.label_amount = customtkinter.CTkLabel(deposit_frame, text="Amount to Deposit:")
        self.label_amount.pack()

        self.entry_amount = customtkinter.CTkEntry(deposit_frame)
        self.entry_amount.pack()

        self.button_deposit = customtkinter.CTkButton(deposit_frame, text="Deposit", command=self.deposit)
        self.button_deposit.pack(pady=10)

        self.button_back = customtkinter.CTkButton(deposit_frame, text="Back", command=self.open_dashboard)
        self.button_back.pack(pady=10)

    def deposit(self):
        try:
            amount = float(self.entry_amount.get())
            if amount <= 0:
                raise ValueError("Invalid amount")
            self.logged_in_user.balance += amount
            self.logged_in_user.transactions.append((datetime.now(), f"Deposited ${amount:.2f}"))
            self.save_users()
            messagebox.showinfo("Success", f"Deposited ${amount:.2f} successfully.")
            self.open_account_window()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")

    def open_withdraw_window(self):
        self.clear_current_frame()

        self.label_title = customtkinter.CTkLabel(self.root, text="Withdraw", font=("Helvetica", 25), text_color="red")
        self.label_title.pack(pady=10)

        withdraw_frame = customtkinter.CTkFrame(self.root)
        withdraw_frame.pack(padx=10, pady=10)

        self.label_amount = customtkinter.CTkLabel(withdraw_frame, text="Amount to Withdraw:")
        self.label_amount.pack()

        self.entry_amount = customtkinter.CTkEntry(withdraw_frame)
        self.entry_amount.pack()

        self.button_withdraw = customtkinter.CTkButton(withdraw_frame, text="Withdraw", command=self.withdraw)
        self.button_withdraw.pack(pady=10)

        self.button_back = customtkinter.CTkButton(withdraw_frame, text="Back", command=self.open_dashboard)
        self.button_back.pack(pady=10)

    def withdraw(self):
        try:
            amount = float(self.entry_amount.get())
            if amount <= 0 or amount > self.logged_in_user.balance:
                raise ValueError("Invalid amount")
            self.logged_in_user.balance -= amount
            self.logged_in_user.transactions.append((datetime.now(), f"Withdrew ${amount:.2f}"))
            self.save_users()
            messagebox.showinfo("Success", f"Withdrew ${amount:.2f} successfully.")
            self.open_account_window()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")

    def open_transaction_history_window(self):
        self.clear_current_frame()

        self.label_title = customtkinter.CTkLabel(self.root, text="Transaction History", font=("Helvetica", 25), text_color="red")
        self.label_title.pack(pady=10)

        transaction_frame = customtkinter.CTkFrame(self.root)
        transaction_frame.pack(padx=10, pady=10)

        for transaction in self.logged_in_user.transactions:
            date, desc = transaction
            label_transaction = customtkinter.CTkLabel(transaction_frame, text=f"{date}: {desc}")
            label_transaction.pack()

        self.button_back = customtkinter.CTkButton(transaction_frame, text="Back", command=self.open_dashboard)
        self.button_back.pack(pady=10)

        self.button_download = customtkinter.CTkButton(transaction_frame, text="Download as PDF", command=self.download_transaction_history)
        self.button_download.pack(pady=10)

    def download_transaction_history(self):
        file_name = f"Transaction_History_{self.logged_in_user.account_number}.pdf"
        c = canvas.Canvas(file_name, pagesize=letter)
        c.drawString(100, 750, f"Transaction History for Account: {self.logged_in_user.account_number}")
        c.drawString(100, 730, f"Email: {self.logged_in_user.email}")
        c.drawString(100, 710, "Date and Time                      Description")

        y_position = 690
        for transaction in self.logged_in_user.transactions:
            date, desc = transaction
            c.drawString(100, y_position, f"{date.strftime('%Y-%m-%d %H:%M:%S')}   {desc}")
            y_position -= 20

            if y_position < 50:
                c.showPage()
                y_position = 750

        c.save()
        messagebox.showinfo("Success", f"Transaction history downloaded as {file_name}")

    def logout_user(self):
        self.logged_in_user = None
        self.create_main_window()

if __name__ == "__main__":
    root = customtkinter.CTk()
    app = BankingApplication(root)
    root.mainloop()
