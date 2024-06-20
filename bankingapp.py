import tkinter as tk
import customtkinter
from tkinter import messagebox, PhotoImage
import random
import string
from datetime import datetime


customtkinter.set_appearance_mode("Light")
customtkinter.set_default_color_theme("themes/red.json")

class User:
    def __init__(self, username, password, pin, account_number):
        self.username = username
        self.password = password
        self.pin = pin
        self.account_number = account_number
        self.balance = 0.0
        self.transactions = []

class BankingApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("NexBank")
        self.root.geometry("400x400")
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
                        username, password, pin, account_number = data
                        self.users[username] = User(username, password, pin, account_number)
        except FileNotFoundError:
            pass

    def save_users(self):
        with open("UserData.txt", "w") as file:
            for user in self.users.values():
                file.write(f"{user.username},{user.password},{user.pin},{user.account_number}\n")

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.root.geometry(f"{width}x{height}+{int(x)}+{int(y)}")

    def create_main_window(self):
        self.clear_current_frame()
        self.root.configure(bg="red")

        self.label_main = customtkinter.CTkLabel(self.root, text="Welcome to NexBank!", font=("Helvetica", 25), text_color= "red")
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

        self.center_window(self.root, 500, 550)

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

        self.label_username = customtkinter.CTkLabel(registration_frame, text="Username:")
        self.label_username.pack()

        self.entry_username = customtkinter.CTkEntry(registration_frame)
        self.entry_username.pack()

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

        self.label_username = customtkinter.CTkLabel(login_frame, text="Username:")
        self.label_username.pack()

        self.entry_username = customtkinter.CTkEntry(login_frame)
        self.entry_username.pack()

        self.label_password = customtkinter.CTkLabel(login_frame, text="Password:")
        self.label_password.pack()

        self.entry_password = customtkinter.CTkEntry(login_frame, show="*")
        self.entry_password.pack()

        self.error_label = customtkinter.CTkLabel(login_frame, text="", text_color="red")
        self.error_label.pack(padx=10)

        self.button_login = customtkinter.CTkButton(login_frame, text="Login", command=self.login_user)
        self.button_login.pack(pady=(5, 30), padx=100)

        self.button_back = customtkinter.CTkButton(login_frame, text="Back", command=self.create_main_window)
        self.button_back.pack(pady=(5, 30), padx=100)

        self.center_window(450, 550)

    def return_to_main_window(self):
        self.clear_current_frame()
        self.create_main_window()

    def register_ok(self):
        self.return_to_main_window()
        self.open_login_window()

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

    def register_user(self):
        pin = self.entry_pin.get()

        if not pin.strip():
            self.error_label_reg.configure(text="PIN cannot be empty.")
            return

        if not pin.isdigit():
            self.error_label_reg.configure(text="PIN must contain only numbers.")
            return

        if len(pin) != 4:
            self.error_label_reg.configure(text="PIN must be 4 digits long.")
            return
        
        username = self.entry_username.get()

        if not username.strip():
            self.error_label_reg.configure(text="Username cannot be empty.")
            return

        if len(username) < 5:
            self.error_label_reg.configure(text="Username must be at least 5 characters long.")
            return

        if username in self.users:
            self.error_label_reg.configure(text="Username already registered. Please try a different username.")
            return

        if self.var_generate_password.get():
            password = self.entry_password.get()
        else:
            password = self.entry_password.get()
            if not self.is_strong_password(password):
                self.error_label_reg.configure(text="Password is not strong. \nPlease include lowercase, uppercase, digits, and symbols.")
                return

        account_number = self.generate_account_number()
        user = User(username, password, pin, account_number)
        self.users[username] = user
        self.save_users()
        
        self.show_registration_success_window(password)

    def show_registration_success_window(self, generated_password):
        self.clear_current_frame()

        label_success = customtkinter.CTkLabel(self.root, text="Registration Successful!", font=("Helvetica", 20), text_color="green")
        label_success.pack(pady=10)

        label_password = customtkinter.CTkLabel(self.root, text=f"Your Password: {generated_password}", font=("Helvetica", 15))
        label_password.pack(pady=5)

        button_ok = customtkinter.CTkButton(self.root, text="OK", command=self.register_ok)
        button_ok.pack(pady=20)

    def login_user(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username in self.users and self.users[username].password == password:
            self.logged_in_user = self.users[username]
            self.open_dashboard()
        else:
            self.error_label.configure(text="Invalid username or password.")

    def open_dashboard(self):
        self.clear_current_frame()

        self.label_title = customtkinter.CTkLabel(self.root, text=f"Welcome, {self.logged_in_user.username}", font=("Helvetica", 25), text_color="red")
        self.label_title.pack(pady=10)

        self.button_balance = customtkinter.CTkButton(self.root, text="View Balance", command=self.view_balance)
        self.button_balance.pack(pady=10)

        self.button_transfer = customtkinter.CTkButton(self.root, text="Transfer Money", command=self.transfer_money)
        self.button_transfer.pack(pady=10)

        self.button_statement = customtkinter.CTkButton(self.root, text="View Bank Statement", command=self.view_statement)
        self.button_statement.pack(pady=10)

        self.button_loan = customtkinter.CTkButton(self.root, text="Take Loan/Overdraft", command=self.take_loan)
        self.button_loan.pack(pady=10)

        self.button_personal_details = customtkinter.CTkButton(self.root, text="View Personal Details", command=self.view_personal_details)
        self.button_personal_details.pack(pady=10)

        self.button_logout = customtkinter.CTkButton(self.root, text="Logout", command=self.create_main_window)
        self.button_logout.pack(pady=10)

        self.center_window(450, 650)

    def view_balance(self):
        self.clear_current_frame()

        label_balance = customtkinter.CTkLabel(self.root, text=f"Your Balance: ${self.logged_in_user.balance:.2f}", font=("Helvetica", 20))
        label_balance.pack(pady=20)

        button_back = customtkinter.CTkButton(self.root, text="Back", command=self.open_dashboard)
        button_back.pack(pady=10)

    def transfer_money(self):
        self.clear_current_frame()

        self.label_title = customtkinter.CTkLabel(self.root, text="Transfer Money", font=("Helvetica", 25), text_color="red")
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

        button_transfer = customtkinter.CTkButton(transfer_frame, text="Transfer", command=self.process_transfer)
        button_transfer.pack(pady=(5, 30), padx=100)

        button_back = customtkinter.CTkButton(transfer_frame, text="Back", command=self.open_dashboard)
        button_back.pack(pady=(5, 30), padx=100)

        self.center_window(450, 550)

    def process_transfer(self):
        account_number = self.entry_account_number.get()
        amount_str = self.entry_amount.get()

        if not amount_str.strip() or not amount_str.isdigit() or float(amount_str) <= 0:
            self.error_label_transfer.configure(text="Please enter a valid amount.")
            return

        amount = float(amount_str)

        if amount > self.logged_in_user.balance:
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

        self.logged_in_user.balance -= amount
        recipient.balance += amount

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.logged_in_user.transactions.append(f"Transferred ${amount:.2f} to {recipient.username} on {timestamp}")
        recipient.transactions.append(f"Received ${amount:.2f} from {self.logged_in_user.username} on {timestamp}")

        self.save_users()
        self.error_label_transfer.configure(text="Transfer successful.", text_color="green")

    def view_statement(self):
        self.clear_current_frame()

        label_title = customtkinter.CTkLabel(self.root, text="Bank Statement", font=("Helvetica", 25), text_color="red")
        label_title.pack(pady=10)

        statement_frame = customtkinter.CTkFrame(self.root)
        statement_frame.pack(padx=10, pady=10)

        for transaction in self.logged_in_user.transactions:
            label_transaction = customtkinter.CTkLabel(statement_frame, text=transaction)
            label_transaction.pack()

        button_back = customtkinter.CTkButton(statement_frame, text="Back", command=self.open_dashboard)
        button_back.pack(pady=10)

    def take_loan(self):
        self.clear_current_frame()

        self.label_title = customtkinter.CTkLabel(self.root, text="Take Loan/Overdraft", font=("Helvetica", 25), text_color="red")
        self.label_title.pack(pady=10)

        loan_frame = customtkinter.CTkFrame(self.root)
        loan_frame.pack(padx=10, pady=10)

        label_amount = customtkinter.CTkLabel(loan_frame, text="Loan Amount:")
        label_amount.pack()

        self.entry_loan_amount = customtkinter.CTkEntry(loan_frame)
        self.entry_loan_amount.pack()

        self.error_label_loan = customtkinter.CTkLabel(loan_frame, text="", text_color="red")
        self.error_label_loan.pack(padx=10)

        button_loan = customtkinter.CTkButton(loan_frame, text="Apply", command=self.process_loan)
        button_loan.pack(pady=(5, 30), padx=100)

        button_back = customtkinter.CTkButton(loan_frame, text="Back", command=self.open_dashboard)
        button_back.pack(pady=(5, 30), padx=100)

        self.center_window(450, 550)

    def process_loan(self):
        amount_str = self.entry_loan_amount.get()

        if not amount_str.strip() or not amount_str.isdigit() or float(amount_str) <= 0:
            self.error_label_loan.configure(text="Please enter a valid amount.")
            return

        amount = float(amount_str)
        self.logged_in_user.balance += amount

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.logged_in_user.transactions.append(f"Loan of ${amount:.2f} received on {timestamp}")

        self.save_users()
        self.error_label_loan.configure(text="Loan approved and credited to your account.", text_color="green")

    def view_personal_details(self):
        self.clear_current_frame()

        label_title = customtkinter.CTkLabel(self.root, text="Personal Details", font=("Helvetica", 25), text_color="red")
        label_title.pack(pady=10)

        details_frame = customtkinter.CTkFrame(self.root)
        details_frame.pack(padx=10, pady=10)

        label_username = customtkinter.CTkLabel(details_frame, text=f"Username: {self.logged_in_user.username}")
        label_username.pack()

        label_account_number = customtkinter.CTkLabel(details_frame, text=f"Account Number: {self.logged_in_user.account_number}")
        label_account_number.pack()

        label_balance = customtkinter.CTkLabel(details_frame, text=f"Balance: ${self.logged_in_user.balance:.2f}")
        label_balance.pack()

        button_back = customtkinter.CTkButton(details_frame, text="Back", command=self.open_dashboard)
        button_back.pack(pady=10)

    def generate_password(self):
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for i in range(10))

    def is_strong_password(self, password):
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in string.punctuation for c in password)
        return len(password) >= 8 and has_lower and has_upper and has_digit and has_special

if __name__ == "__main__":
    root = customtkinter.CTk()
    app = BankingApplication(root)
    root.mainloop()
