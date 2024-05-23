import tkinter as tk
import customtkinter
from tkinter import messagebox, PhotoImage
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
        self.transaction_log_file = f"{username}_TransactionLog.txt"
        self.load_transaction_history()

    def load_transaction_history(self):
        try:
            with open(self.transaction_log_file, "r") as file:
                self.transaction_history = file.readlines()
        except FileNotFoundError:
            self.transaction_history = []

    def save_transaction_history(self):
        with open(self.transaction_log_file, "w") as file:
            file.writelines(self.transaction_history)

    def add_transaction(self, transaction):
        self.transaction_history.append(transaction)
        self.save_transaction_history()

class BankingApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Techatronics Bank")
        self.root.geometry("500x550")

        self.logged_in_user = None
        self.balance = 0.0
        self.current_window = None

        self.create_main_window()

    def create_main_window(self):
        self.destroy_current_window()
        self.root.deiconify()

        self.label_main = customtkinter.CTkLabel(self.root, text="Welcome to Techatronics Bank!", font=("Helvetica", 25),
                                                  text_color="#1E90FF")
        self.label_main.pack(pady=20)

        image = PhotoImage(file="banking.png")
        resizedImage = image.subsample(2, 2)

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

    def destroy_current_window(self):
        if self.current_window:
            self.current_window.destroy()
            self.current_window = None

    def quit_application(self):
        if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
            self.root.destroy()

    def open_registration_window(self):
        self.destroy_current_window()
        self.root.withdraw()
        registration_window = customtkinter.CTkToplevel(self.root)
        registration_window.title("Register")
        registration_window.geometry("500x650")
        menu = CTkMenuBar(registration_window)
        menu.add_cascade("Home", command=self.create_main_window)
        menu.add_cascade("Login", command=self.open_login_window)
        menu.add_cascade("Quit", command=self.quit_application)

        self.current_window = registration_window

        self.label_title = customtkinter.CTkLabel(registration_window, text="Register", font=("Helvetica", 25),
                                                   text_color="#1E90FF")
        self.label_title.pack(pady=10)

        registration_frame = customtkinter.CTkFrame(registration_window)
        registration_frame.pack(padx=10, pady=10)

        self.label_username = customtkinter.CTkLabel(registration_frame, text="Username:")
        self.label_username.pack()

        self.entry_username = customtkinter.CTkEntry(registration_frame)
        self.entry_username.pack()

        self.label_password = customtkinter.CTkLabel(registration_frame, text="Password:")
        self.label_password.pack()

        self.entry_password = customtkinter.CTkEntry(registration_frame, show="*")
        self.entry_password.pack()

        self.var_generate_password = tk.BooleanVar()
        self.checkbutton_generate_password = customtkinter.CTkCheckBox(registration_frame,
                                                                       text="Generate a random password",
                                                                       variable=self.var_generate_password)
        self.checkbutton_generate_password.pack(pady=(10), padx=10)

        self.error_label_reg = customtkinter.CTkLabel(registration_frame, text="", text_color="red")
        self.error_label_reg.pack(padx=10)

        self.button_register = customtkinter.CTkButton(registration_frame, text="Register", command=self.register_user)
        self.button_register.pack(pady=(5, 30), padx=100)

        registration_window.protocol("WM_DELETE_WINDOW", lambda: self.on_window_close(registration_window))

    def open_login_window(self):
        self.destroy_current_window()
        self.root.withdraw()
        login_window = customtkinter.CTkToplevel(self.root)
        login_window.title("Login")
        login_window.geometry("500x650")
        menu = CTkMenuBar(login_window)
        menu.add_cascade("Home", command=self.create_main_window)
        menu.add_cascade("Register", command=self.open_registration_window)
        menu.add_cascade("Quit", command=self.quit_application)

        self.current_window = login_window

        self.label_title = customtkinter.CTkLabel(login_window, text="Login", font=("Helvetica", 25), text_color="#1E90FF")
        self.label_title.pack(pady=10)

        login_frame = customtkinter.CTkFrame(login_window)
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

        login_window.protocol("WM_DELETE_WINDOW", lambda: self.on_window_close(login_window))

    def on_window_close(self, window):
        window.destroy()
        self.current_window = None
        self.root.deiconify()

    def return_to_main_window(self):
        self.destroy_current_window()
        self.create_main_window()

    def register_ok(self, username, generated_password):
        self.logged_in_user = User(username, generated_password)
        self.return_to_main_window()
        self.open_login_window()

    def register_user(self):
        username = self.entry_username.get()

        if not username.strip():
            self.error_label_reg.configure(text="Username cannot be empty.")
            return

        if len(username) < 5:
            self.error_label_reg.configure(text="Username must be at least 5 characters long.")
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
            self.entry_password.configure(state='disabled')
            self.error_label_reg.configure(
                text=f"Generated Password: {generated_password}. Successfully registered")
        else:
            generated_password = self.entry_password.get()
            if not self.is_valid_password(generated_password):
                self.error_label_reg.configure(
                    text="Password is not strong. \nPlease include lowercase, uppercase, digits, and symbols.")
                return
            else:
                self.error_label_reg.configure(text="Password created. Successfully registered.")

        user = User(username, generated_password)
        with open("UserData.txt", "a") as file:
            file.write(f"{user.username},{user.password}\n")

        self.show_registration_success_window(generated_password)


    def show_registration_success_window(self, generated_password):
        self.destroy_current_window()
        registration_success_window = customtkinter.CTkToplevel(self.root)
        registration_success_window.title("Registration Successful")
        registration_success_window.geometry("350x150")
        self.current_window = registration_success_window
        label_success = customtkinter.CTkLabel(registration_success_window, text="Registration Successful!",
                                                font=("Helvetica", 20), text_color="green")
        label_success.pack()

        label_password = customtkinter.CTkLabel(registration_success_window,
                                                 text=f"Generated Password: {generated_password}", font=("Helvetica", 15))
        label_password.pack()

        label_password = customtkinter.CTkLabel(registration_success_window, text="Please remember your password!",
                                                 font=("Helvetica", 15), text_color="red")
        label_password.pack()

        self.button_ok = customtkinter.CTkButton(registration_success_window, text="Ok", command=self.register_ok)
        self.button_ok.pack(pady=5, padx=100)

        registration_success_window.protocol("WM_DELETE_WINDOW", lambda: self.on_window_close(registration_success_window))

    def login_user(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        self.logged_in_user = User(username, password)
        self.logged_in_user.load_transaction_history() 
        user_found = False
        with open("UserData.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")
                if len(data) != 2:
                    continue
                stored_username, stored_password = data
                if username == stored_username:
                    user_found = True
                    if password == stored_password:
                        self.logged_in_user = User(username, password)
                        self.error_label.configure(text="Login successful.", text_color="green")
                        self.open_bank_operations_window()
                        return
                    else:
                        self.error_label.configure(text="Invalid password.")
                        return
        if not user_found:
            self.error_label.configure(text="Username not found. Please register first.")

    def open_bank_operations_window(self):
        self.destroy_current_window()
        operations_window = customtkinter.CTkToplevel(self.root)
        operations_window.title("Bank Operations")
        operations_window.geometry("350x400")

        menu = CTkMenuBar(operations_window)
        menu.add_cascade("Quit", command=self.quit_application)

        try:
            with open(f"{self.logged_in_user.username}_BankData.txt", "r") as file:
                self.balance = float(file.read())
        except FileNotFoundError:
            self.balance = 0.0

        bank_frame = customtkinter.CTkFrame(operations_window)
        bank_frame.pack(padx=10, pady=10)

        self.label_balance = customtkinter.CTkLabel(bank_frame, text=f"Balance: R{self.balance:.2f}", font=("Helvetica", 25))
        self.label_balance.pack(pady=50, padx=50)

        self.button_deposit = customtkinter.CTkButton(operations_window, text="Deposit", command=self.deposit)
        self.button_deposit.pack(pady=10)

        self.button_withdraw = customtkinter.CTkButton(operations_window, text="Withdraw", command=self.withdraw)
        self.button_withdraw.pack(pady=10)

        self.error_label_op = customtkinter.CTkLabel(operations_window, text="", text_color="red")
        self.error_label_op.pack(pady=5)

        self.button_print_statement = customtkinter.CTkButton(operations_window, text="Print Statement",
                                                               command=self.print_bank_statement)
        self.button_print_statement.pack(pady=5)

        operations_window.protocol("WM_DELETE_WINDOW", lambda: self.on_window_close(operations_window))

    def deposit(self):
        deposit_window = customtkinter.CTkToplevel(self.root)
        deposit_window.title("Deposit")
        deposit_window.geometry("300x150")

        label_amount = customtkinter.CTkLabel(deposit_window, text="Enter the amount to deposit:")
        label_amount.pack(pady=5)

        entry_amount = customtkinter.CTkEntry(deposit_window)
        entry_amount.pack(pady=5)

        button_confirm = customtkinter.CTkButton(deposit_window, text="Confirm",
                                                 command=lambda: self.process_deposit(entry_amount, deposit_window))
        button_confirm.pack(pady=5)

    def withdraw(self):
        withdraw_window = customtkinter.CTkToplevel(self.root)
        withdraw_window.title("Withdraw")
        withdraw_window.geometry("300x150")

        label_amount = customtkinter.CTkLabel(withdraw_window, text="Enter the amount to withdraw:")
        label_amount.pack(pady=5)

        entry_amount = customtkinter.CTkEntry(withdraw_window)
        entry_amount.pack(pady=5)

        button_confirm = customtkinter.CTkButton(withdraw_window, text="Confirm",
                                                  command=lambda: self.process_withdrawal(entry_amount, withdraw_window))
        button_confirm.pack(pady=5)

    def process_deposit(self, entry_amount, window):
        amount = entry_amount.get()
        if amount.replace('.', '', 1).isdigit() and float(amount) > 0:
            amount = float(amount)
            self.balance += amount
            self.logged_in_user.transaction_history.append(f"Deposited: R{amount:.2f}")
            self.update_balance(amount)
            self.error_label_op.configure(text=f"Deposit of R{amount:.2f} successful.", text_color="green")
            self.update_balance_label()
            window.destroy()
        else:
            self.error_label_op.configure(text="Invalid deposit amount. Please enter a positive number.", text_color="red")

    def process_withdrawal(self, entry_amount, window):
        amount = entry_amount.get()
        if amount.replace('.', '', 1).isdigit() and float(amount) > 0:
            amount = float(amount)
            if amount > self.balance:
                self.error_label_op.configure(text="Insufficient funds.", text_color="red")
            else:
                self.balance -= amount
                self.logged_in_user.transaction_history.append(f"Withdrew: R{amount:.2f}")
                self.update_balance(-amount)
                self.error_label_op.configure(text=f"Withdrawal of R{amount:.2f} successful.", text_color="green")
                self.update_balance_label()
                window.destroy()
        else:
            self.error_label_op.configure(text="Invalid withdrawal amount. Please enter a positive number.", text_color="red")

    def print_bank_statement(self):
        statement_window = tk.Toplevel(self.root)
        statement_window.title("Bank Statement")
        statement_window.geometry("300x300")

        statement_text = tk.Text(statement_window)
        statement_text.pack()

        statement_text.insert(tk.END, f"Username: {self.logged_in_user.username}\n")
        statement_text.insert(tk.END, "Transaction History:\n\n")
        for transaction in self.logged_in_user.transaction_history:
            statement_text.insert(tk.END, transaction)
        statement_text.insert(tk.END, f"\n\nCurrent Balance: R{self.balance:.2f}")

    def update_balance(self, amount):
        try:
            with open(f"{self.logged_in_user.username}_BankData.txt", "w") as file:
                file.write(str(self.balance + amount))
        except FileNotFoundError:
            with open(f"{self.logged_in_user.username}_BankData.txt", "w") as file:
                file.write(str(amount))

    def update_balance_label(self):
        self.label_balance.configure(text=f"Balance: R{self.balance:.2f}")

    def is_valid_username(self, username):
        return len(username) <= 10

    def is_valid_password(self, password):
        return len(password) == 12

    def generate_password(self):
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for i in range(12))


def main():
    root = customtkinter.CTk()
    app = BankingApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()
