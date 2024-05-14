import tkinter as tk
from tkinter import messagebox
import random
import string

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class BankingApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Banking Application")
        self.root.geometry("300x200")

        self.logged_in_user = None
        self.balance = 0.0

        self.create_main_window()

    def create_main_window(self):
        self.label_main = tk.Label(self.root, text="Welcome to the Banking Application!")
        self.label_main.pack()

        self.button_register = tk.Button(self.root, text="Register", command=self.open_registration_window)
        self.button_register.pack()

        self.button_login = tk.Button(self.root, text="Login", command=self.open_login_window)
        self.button_login.pack()

        self.error_label = tk.Label(self.root, text="", fg="red")
        self.error_label.pack()

    def open_registration_window(self):
        self.root.withdraw()  # Hide main window
        registration_window = tk.Toplevel(self.root)
        registration_window.title("Register")
        registration_window.geometry("300x250")

        self.label_username = tk.Label(registration_window, text="Username:")
        self.label_username.pack()

        self.entry_username = tk.Entry(registration_window)
        self.entry_username.pack()

        self.label_password = tk.Label(registration_window, text="Password:")
        self.label_password.pack()

        self.entry_password = tk.Entry(registration_window, show="*")
        self.entry_password.pack()

        self.var_generate_password = tk.BooleanVar()
        self.checkbutton_generate_password = tk.Checkbutton(registration_window, text="Generate a random password", variable=self.var_generate_password)
        self.checkbutton_generate_password.pack()

        self.button_register = tk.Button(registration_window, text="Register", command=self.register_user)
        self.button_register.pack()

    def open_login_window(self):
        self.root.withdraw()  # Hide main window
        login_window = tk.Toplevel(self.root)
        login_window.title("Login")
        login_window.geometry("300x200")

        self.label_username = tk.Label(login_window, text="Username:")
        self.label_username.pack()

        self.entry_username = tk.Entry(login_window)
        self.entry_username.pack()

        self.label_password = tk.Label(login_window, text="Password:")
        self.label_password.pack()

        self.entry_password = tk.Entry(login_window, show="*")
        self.entry_password.pack()

        self.button_login = tk.Button(login_window, text="Login", command=self.login_user)
        self.button_login.pack()

    def user_already_registered_popup(self):
        popup_window = tk.Toplevel(self.root)
        popup_window.title("User Already Registered")
        popup_window.geometry("300x100")
        label_message = tk.Label(popup_window, text="Username already registered. Please login instead.", font=("Helvetica", 12))
        label_message.pack()
        button_ok = tk.Button(popup_window, text="OK", command=self.open_login_window)
        button_ok.pack()

    def register_user(self):
        username = self.entry_username.get()

        # Check if the username already exists
        with open("UserData.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")
                if len(data) != 2:
                    continue  # Skip lines that don't contain username and password
                stored_username, _ = data
                if username == stored_username:
                    self.user_already_registered_popup()
                    return

        # If the username doesn't exist, proceed with registration
        if self.var_generate_password.get():
            generated_password = self.generate_password()
            self.entry_password.delete(0, tk.END)
            self.entry_password.insert(0, generated_password)
            self.error_label.config(text=f"Generated Password: {generated_password}. Successfully registered.", fg="green")
        else:
            generated_password = self.entry_password.get()
            if not self.is_strong_password(generated_password):
                self.error_label.config(text="Password is not strong. Please include lowercase, uppercase, digits, and symbols.", fg="red")
                return
            else:
                self.error_label.config(text="Password created. Successfully registered.", fg="green")

        # Write user data to file
        user = User(username, generated_password)
        with open("UserData.txt", "a") as file:
            file.write(f"{user.username},{user.password}\n")
        
        # Display registration success window with generated password
        self.show_registration_success_window(generated_password)
        # Close success window after 3 seconds
        self.root.after(3000, self.close_registration_success_window)

    def show_registration_success_window(self, generated_password):
        registration_success_window = tk.Toplevel(self.root)
        registration_success_window.title("Registration Successful")
        registration_success_window.geometry("250x150")
        label_success = tk.Label(registration_success_window, text="Registration Successful!", font=("Helvetica", 12))
        label_success.pack()

        label_password = tk.Label(registration_success_window, text=f"Generated Password: {generated_password}", font=("Helvetica", 10))
        label_password.pack()

    def close_registration_success_window(self):
        self.open_login_window()  # Open login window after success window closes

    def login_user(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        user_found = False
        with open("UserData.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")
                if len(data) != 2:
                    continue  # Skip lines that don't contain username and password
                stored_username, stored_password = data
                if username == stored_username:
                    user_found = True
                    if self.logged_in_user and self.logged_in_user.password != password:
                        messagebox.showerror("Login Error", "Incorrect password. Please enter the generated password.")
                        return
                    elif self.logged_in_user and self.logged_in_user.password == password:
                        self.error_label.config(text="Login successful.", fg="green")
                        self.open_bank_operations_window()  # Open bank operations window
                        return
                    elif password == stored_password:
                        self.logged_in_user = User(username, password)
                        self.error_label.config(text="Login successful.", fg="green")
                        self.open_bank_operations_window()  # Open bank operations window
                        return
                    else:
                        self.error_label.config(text="Invalid password.", fg="red")
                        return
        if not user_found:
            self.error_label.config(text="Username not found. Please register first.", fg="red")

    def open_bank_operations_window(self):
        self.root.withdraw()  # Hide main window
        operations_window = tk.Toplevel(self.root)
        operations_window.title("Bank Operations")
        operations_window.geometry("300x200")

        self.label_balance = tk.Label(operations_window, text="Balance: $0.00")
        self.label_balance.pack()

        self.button_deposit = tk.Button(operations_window, text="Deposit", command=self.deposit)
        self.button_deposit.pack()

        self.button_withdraw = tk.Button(operations_window, text="Withdraw", command=self.withdraw)
        self.button_withdraw.pack()

        self.button_print_statement = tk.Button(operations_window, text="Print Statement", command=self.print_bank_statement)
        self.button_print_statement.pack()

    def deposit(self):
        deposit_window = tk.Toplevel(self.root)
        deposit_window.title("Deposit")
        deposit_window.geometry("300x100")

        label_amount = tk.Label(deposit_window, text="Enter the amount to deposit:")
        label_amount.pack()

        entry_amount = tk.Entry(deposit_window)
        entry_amount.pack()

        button_confirm = tk.Button(deposit_window, text="Confirm", command=lambda: self.process_deposit(entry_amount, deposit_window))
        button_confirm.pack()

    def withdraw(self):
        withdraw_window = tk.Toplevel(self.root)
        withdraw_window.title("Withdraw")
        withdraw_window.geometry("300x100")

        label_amount = tk.Label(withdraw_window, text="Enter the amount to withdraw:")
        label_amount.pack()

        entry_amount = tk.Entry(withdraw_window)
        entry_amount.pack()

        button_confirm = tk.Button(withdraw_window, text="Confirm", command=lambda: self.process_withdrawal(entry_amount, withdraw_window))
        button_confirm.pack()

    def process_deposit(self, entry_amount, window):
        amount = entry_amount.get()
        if amount.isdigit() and int(amount) > 0:
            amount = float(amount)
            self.balance += amount
            self.update_balance(amount)
            self.error_label.config(text=f"Deposit of ${amount:.2f} successful.", fg="green")
            self.update_balance_label()
            window.destroy()
        else:
            self.error_label.config(text="Invalid deposit amount. Please enter a positive number.", fg="red")

    def process_withdrawal(self, entry_amount, window):
        amount = entry_amount.get()
        if amount.isdigit() and int(amount) > 0:
            amount = float(amount)
            if amount > self.balance:
                self.error_label.config(text="Insufficient funds.", fg="red")
            else:
                self.balance -= amount
                self.update_balance(-amount)
                self.error_label.config(text=f"Withdrawal of ${amount:.2f} successful.", fg="green")
                self.update_balance_label()
                window.destroy()
        else:
            self.error_label.config(text="Invalid withdrawal amount. Please enter a positive number.", fg="red")

    def print_bank_statement(self):
        statement = f"Username: {self.logged_in_user.username}\n\n"
        try:
            with open(f"{self.logged_in_user.username}_TransactionLog.txt", "r") as file:
                statement += file.read()
        except FileNotFoundError:
            statement += "No transactions found."
        messagebox.showinfo("Bank Statement", statement)

    def update_balance(self, amount):
        with open(f"{self.logged_in_user.username}_BankData.txt", "w") as file:
            file.write(str(self.balance))

        with open(f"{self.logged_in_user.username}_TransactionLog.txt", "a") as file:
            file.write(f"Balance Adjustment: {amount}\n")

    def update_balance_label(self):
        self.label_balance.config(text=f"Balance: ${self.balance:.2f}")

    def generate_password(self):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(12))
        return password

    def is_strong_password(self, password):
        return any(char.islower() for char in password) and \
               any(char.isupper() for char in password) and \
               any(char.isdigit() for char in password) and \
               any(char in string.punctuation for char in password)

def main():
    root = tk.Tk()
    app = BankingApplication(root)
    root.mainloop()

if __name__ == "__main__":
    main()
