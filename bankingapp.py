import tkinter as tk
import customtkinter
from tkinter import messagebox
from CTkMenuBar import *
import random
import string

customtkinter.set_ctk_parent_class(tk.Tk)
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue") 


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class BankingApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Techatronics Bank")
        self.root.geometry("350x200")
        menu = CTkMenuBar(root)
        menu.add_cascade("Login", command=self.open_login_window)
        menu.add_cascade("Register", command=self.open_registration_window)

        self.logged_in_user = None
        self.balance = 0.0

        self.create_main_window()

    def create_main_window(self):
        self.label_main = customtkinter.CTkLabel(self.root, text="Welcome to Techatronics Bank!", font=("Helvetica", 20))
        self.label_main.pack(pady=20)

        self.button_register = customtkinter.CTkButton(self.root, text="Register", command=self.open_registration_window)
        self.button_register.pack(pady=10)

        self.button_login = customtkinter.CTkButton(self.root, text="Login", command=self.open_login_window)
        self.button_login.pack()

        self.error_label = customtkinter.CTkLabel(self.root, text="", text_color="red")
        self.error_label.pack()


    def open_registration_window(self):
        self.root.withdraw()
        registration_window = customtkinter.CTkToplevel(self.root)
        registration_window.title("Register")
        registration_window.geometry("400x400")
        menu = CTkMenuBar(registration_window)
        menu.add_cascade("Login", command=self.open_login_window)
        menu.add_cascade("Register", command=self.open_registration_window)

        self.label_title = customtkinter.CTkLabel(registration_window, text="Register", font=("Helvetica", 35))
        self.label_title.pack(pady=10)

        registration_frame = customtkinter.CTkFrame(registration_window)
        registration_frame.pack(padx=10, pady=10)

        self.label_username = customtkinter.CTkLabel(registration_frame, text="Username:")
        self.label_username.pack()

        self.entry_username = customtkinter.CTkEntry(registration_frame)
        self.entry_username.pack(pady=(0, 5))

        self.label_password = customtkinter.CTkLabel(registration_frame, text="Password:")
        self.label_password.pack()

        self.entry_password = customtkinter.CTkEntry(registration_frame, show="*")
        self.entry_password.pack(pady=(0, 5))

        self.var_generate_password = tk.BooleanVar()
        self.checkbutton_generate_password = customtkinter.CTkCheckBox(registration_frame, text="Generate a random password", variable=self.var_generate_password)
        self.checkbutton_generate_password.pack(pady=(10), padx=10)

        self.error_label_reg = customtkinter.CTkLabel(registration_frame, text="", text_color="red")
        self.error_label_reg.pack()

        self.button_register = customtkinter.CTkButton(registration_frame, text="Register", command=self.register_user)
        self.button_register.pack(pady=10)


    def open_login_window(self):
        self.root.withdraw()
        login_window = customtkinter.CTkToplevel(self.root)
        login_window.title("Login")
        login_window.geometry("300x300")
        menu = CTkMenuBar(login_window)
        menu.add_cascade("Login", command=self.open_login_window)
        menu.add_cascade("Register", command=self.open_registration_window)

        self.label_title = customtkinter.CTkLabel(login_window, text="Login", font=("Helvetica", 35))
        self.label_title.pack(pady=10)

        self.label_username = customtkinter.CTkLabel(login_window, text="Username:")
        self.label_username.pack()

        self.entry_username = customtkinter.CTkEntry(login_window)
        self.entry_username.pack()

        self.label_password = customtkinter.CTkLabel(login_window, text="Password:")
        self.label_password.pack()

        self.entry_password = customtkinter.CTkEntry(login_window, show="*")
        self.entry_password.pack()

        self.error_label = customtkinter.CTkLabel(login_window, text="", text_color="red")
        self.error_label.pack()

        self.button_login = customtkinter.CTkButton(login_window, text="Login", command=self.login_user)
        self.button_login.pack()

    def register_ok(self):
        self.root.withdraw()
        self.open_login_window()

    def register_user(self):
        username = self.entry_username.get()

        if not username.strip():
            self.error_label_reg.configure(text="Username cannot be empty.")
            return

        with open("UserData.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")
                if len(data) != 2:
                    continue 
                stored_username, _ = data
                if username == stored_username:
                    self.error_label_reg.configure(text="Username already registered. Please try a different username.")
                    return

        if self.var_generate_password.get():
            generated_password = self.generate_password()
            self.entry_password.delete(0, tk.END)
            self.entry_password.insert(0, generated_password)
            self.entry_password.configure(state='disabled')  # Disable the password entry
            self.error_label.configure(text=f"Generated Password: {generated_password}. Successfully registered.")
        else:
            generated_password = self.entry_password.get()
            if not self.is_strong_password(generated_password):
                self.error_label_reg.configure(text="Password is not strong. \nPlease include lowercase, uppercase, digits, and symbols.")
                return
            else:
                self.error_label_reg.configure(text="Password created. Successfully registered.")

        user = User(username, generated_password)
        with open("UserData.txt", "a") as file:
            file.write(f"{user.username},{user.password}\n")
        
        self.show_registration_success_window(generated_password)
        self.root.after(3000, self.close_registration_success_window)


    def show_registration_success_window(self, generated_password):
        registration_success_window = customtkinter.CTkToplevel(self.root)
        registration_success_window.title("Registration Successful")
        registration_success_window.geometry("350x150")
        label_success = customtkinter.CTkLabel(registration_success_window, text="Registration Successful!", font=("Helvetica", 20), text_color="green")
        label_success.pack()

        label_password = customtkinter.CTkLabel(registration_success_window, text=f"Generated Password: {generated_password}", font=("Helvetica", 15))
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
                        self.error_label.configure(text="Login successful.")
                        self.open_bank_operations_window()  # Open bank operations window
                        return
                    elif password == stored_password:
                        self.logged_in_user = User(username, password)
                        self.error_label.configure(text="Login successful.", text_color="green")
                        self.open_bank_operations_window()  # Open bank operations window
                        return
                    else:
                        self.error_label.configure(text="Invalid password.")
                        return
        if not user_found:
            self.error_label.configure(text="Username not found. Please register first.")

    def open_bank_operations_window(self):
        self.root.withdraw() 
        operations_window = customtkinter.CTkToplevel(self.root)
        operations_window.title("Bank Operations")
        operations_window.geometry("300x200")

        self.label_balance = customtkinter.CTkLabel(operations_window, text="Balance: $0.00", font=("Helvetica", 25))
        self.label_balance.pack(pady=5)

        self.button_deposit = customtkinter.CTkButton(operations_window, text="Deposit", command=self.deposit)
        self.button_deposit.pack(pady=5)

        self.button_withdraw = customtkinter.CTkButton(operations_window, text="Withdraw", command=self.withdraw)
        self.button_withdraw.pack(pady=5)

        self.error_label_op = customtkinter.CTkLabel(operations_window, text="", text_color="red")
        self.error_label_op.pack(pady=5)

        self.button_print_statement = customtkinter.CTkButton(operations_window, text="Print Statement", command=self.print_bank_statement)
        self.button_print_statement.pack(pady=5)

    def deposit(self):
        deposit_window = customtkinter.CTkToplevel(self.root)
        deposit_window.title("Deposit")
        deposit_window.geometry("300x150")

        label_amount = customtkinter.CTkLabel(deposit_window, text="Enter the amount to deposit:")
        label_amount.pack(pady=5)

        entry_amount = customtkinter.CTkEntry(deposit_window)
        entry_amount.pack(pady=5)

        button_confirm = customtkinter.CTkButton(deposit_window, text="Confirm", command=lambda: self.process_deposit(entry_amount, deposit_window))
        button_confirm.pack(pady=5)

    def withdraw(self):
        withdraw_window = customtkinter.CTkToplevel(self.root)
        withdraw_window.title("Withdraw")
        withdraw_window.geometry("300x150")

        label_amount = customtkinter.CTkLabel(withdraw_window, text="Enter the amount to withdraw:")
        label_amount.pack(pady=5)

        entry_amount = customtkinter.CTkEntry(withdraw_window)
        entry_amount.pack(pady=5)

        button_confirm = customtkinter.CTkButton(withdraw_window, text="Confirm", command=lambda: self.process_withdrawal(entry_amount, withdraw_window))
        button_confirm.pack(pady=5)

    def process_deposit(self, entry_amount, window):
        amount = entry_amount.get()
        if amount.isdigit() and int(amount) > 0:
            amount = float(amount)
            self.balance += amount
            self.update_balance(amount)
            self.error_label_op.configure(text=f"Deposit of ${amount:.2f} successful.", text_color="green")
            self.update_balance_label()
            window.destroy()
        else:
            self.error_label.configure(text="Invalid deposit amount. Please enter a positive number.", text_color="red")

    def process_withdrawal(self, entry_amount, window):
        amount = entry_amount.get()
        if amount.isdigit() and int(amount) > 0:
            amount = float(amount)
            if amount > self.balance:
                self.error_label.configure(text="Insufficient funds.")
            else:
                self.balance -= amount
                self.update_balance(-amount)
                self.error_label_op.configure(text=f"Withdrawal of ${amount:.2f} successful.", text_color="green")
                self.update_balance_label()
                window.destroy()
        else:
            self.error_label.configure(text="Invalid withdrawal amount. Please enter a positive number.", text_color="red")

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
        self.label_balance.configure(text=f"Balance: ${self.balance:.2f}")

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
    root = customtkinter.CTk()
    app = BankingApplication(root)
    root.mainloop()

if __name__ == "__main__":
    main()
