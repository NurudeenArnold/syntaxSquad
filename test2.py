from datetime import datetime
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
import os
import random
import re
import smtplib
import string
import tempfile
import threading
import time
import tkinter as tk
from tkinter import PhotoImage, messagebox
from tkinter import filedialog
from tkinter import Canvas, Frame, messagebox, PhotoImage
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import customtkinter as ctk
from PIL import Image, ImageTk

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("themes/red.json")

class User:
    def __init__(self, email, password, account_number, contact, dob, balance):
        self.email = email
        self.password = password
        self.account_number = account_number
        self.contact = contact
        self.dob = dob
        self.balance = float(balance)
        self.transactions = []


class NexBank(ctk.CTk):
    def __init__(self, root):
        self.root = root
        self.root.title("NexBank")
        self.root.geometry("1200x950")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (1200 // 2)
        y = (screen_height // 2) - (950 // 2)
        self.root.geometry(f"1200x950+{x}+{y}")

        self.logged_in_user = None
        self.users = {}
        self.current_frame = None

        self.load_users()
        
        self.login_panel = LoginPanel(self)
        self.welcome_panel = WelcomePanel(self)
        self.register_panel = RegisterPanel(self)
        self.register_welcome_panel = RegisterWelcomePanel(self)
        self.dashboard_panel = CenteredPanel(self)

        self.login_panel.hide_panel()
        self.welcome_panel.hide_panel()
        self.register_panel.hide_panel()
        self.register_welcome_panel.hide_panel()
        self.dashboard_panel.hide_panel()

        self.main_window()

    def load_users(self):
        try:
            with open("UserData.txt", "r") as file:
                for line in file:
                    data = line.strip().split(",")
                    if len(data) == 6:
                        email, password, account_number, contact, dob, balance = data
                        print(f"Loading user: {email}, {password}, {account_number}, {contact}, {dob}, {balance}")
                        self.users[email] = User(email, password, account_number, contact, dob, balance)
                        self.users[email].balance = float(balance)
                    elif len(data) == 5:
                        email, password, account_number, contact, dob, balance = data
                        print(f"Loading user: {email}, {password}, {account_number}, {contact}, {dob}, {balance}")
                        self.users[email] = User(email, password, account_number, contact, dob, balance)
                    else:
                        print(f"Skipping invalid line: {line}")
                    self.load_transaction_history(email)
            print("Users loaded successfully:", self.users)  
        except FileNotFoundError:
            print("UserData.txt file not found")
        except Exception as e:
            print(f"Error loading users: {e}")

    def save_users(self):
        try:
            with open("UserData.txt", "w") as file:
                for user in self.users.values():
                    file.write(f"{user.email},{user.password},{user.account_number},{user.contact},{user.dob},{user.balance}\n")
        except Exception as e:
            print(f"Error saving users: {e}")

    def load_transaction_history(self, email):
        try:
            with open("Transactionlog.txt", "r") as file:
                if email in self.users:
                    self.users[email].transactions.clear()  
                    for line in file:
                        transaction_data = line.strip().split(",")
                        if len(transaction_data) >= 2 and transaction_data[0] == email:
                            transaction_details = ",".join(transaction_data[1:])
                            print(f"Adding transaction for {email}: {transaction_details}")
                            self.users[email].transactions.append(transaction_details)  
        except FileNotFoundError:
            print("Transactionlog.txt file not found")
        except Exception as e:
            print(f"Error loading transaction history for {email}: {e}")

    def save_transaction_log(self, email, transaction_details):
        with open("Transactionlog.txt", "a") as file:
            file.write(f"{email},{transaction_details}\n")

    def main_window(self):
        self.clear_window()

        self.root.update_idletasks()  
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        image_path = "background.jpeg"
        if not os.path.exists(image_path):
            print("Image file not found!")
        else:
            background_image = Image.open(image_path)
            background_image = background_image.resize((width, height), Image.LANCZOS)
            self.background_image_tk = ImageTk.PhotoImage(background_image)

            self.background_label = ctk.CTkLabel(self.root, image=self.background_image_tk, text="")
            self.background_label.image = self.background_image_tk  
            self.background_label.place(relx=0.5, rely=0.5, anchor="center")

        mainframe = ctk.CTkFrame(self.root, corner_radius=32)
        mainframe.pack(padx=50, pady=30)
    
        label_main = ctk.CTkLabel(self.root, text="Welcome to NexBank!", font=("Verdana", 25), text_color="#B22E2E")
        label_main.pack(pady=50)

        image = Image.open("nexbank2.png")
        resizedImage = image.resize((300, 300), Image.LANCZOS)
        img = ImageTk.PhotoImage(resizedImage)
        image_label = ctk.CTkLabel(self.root, image=img, text="")
        image_label.image = img
        image_label.pack(pady=20)

        button_login = ctk.CTkButton(self.root, text="Login", command=self.show_login_and_welcome, corner_radius=32)
        button_login.pack(pady=10)

        button_register = ctk.CTkButton(self.root, text="Register", command=self.open_registration_window, corner_radius=32)
        button_register.pack()

        button_quit = ctk.CTkButton(self.root, text="Quit", command=self.quit_application, corner_radius=32)
        button_quit.pack(pady=10)
    
    def open_dashboard(self):
        self.clear_window()

        image = PhotoImage(file="nexbank2.png")
        resizedImage = image.subsample(1, 1)

        self.image_label = ctk.CTkLabel(self.root, image=resizedImage, text="")
        self.image_label.image = resizedImage
        self.image_label.pack(pady=50)

        self.label_title = ctk.CTkLabel(self.root, text="Dashboard", font=("Helvetica", 25), text_color="#B22E2E")
        self.label_title.pack(pady=10)

        self.button_balance = ctk.CTkButton(self.root, text="View Balance", command=self.view_balance, corner_radius=32)
        self.button_balance.pack(pady=10)

        self.button_transfer = ctk.CTkButton(self.root, text="Transfer Money", command=self.transfer_money, corner_radius=32)
        self.button_transfer.pack(pady=10)

        self.button_statement = ctk.CTkButton(self.root, text="View Bank Statement",
                                                        command=self.view_statement, corner_radius=32)
        self.button_statement.pack(pady=10)

        self.button_loan = ctk.CTkButton(self.root, text="Take Loan/Overdraft", command=self.take_loan, corner_radius=32)
        self.button_loan.pack(pady=10)

        self.button_personal_details = ctk.CTkButton(self.root, text="View Personal Details",
                                                               command=self.view_personal_details, corner_radius=32)
        self.button_personal_details.pack(pady=10)

        self.button_logout = ctk.CTkButton(self.root, text="Logout", command=self.logout, corner_radius=32)
        self.button_logout.pack(pady=10)

    def logout(self):
        self.login_panel.show_panel()
        self.welcome_panel.show_panel()
        self.main_window()
        self.liftAll()

    def view_balance(self):
        self.dashboard_panel.show_panel()
        self.clear_panel()
        self.liftAll()

        image = PhotoImage(file="nexbank2.png")
        resizedImage = image.subsample(1, 1)
        self.image_label = ctk.CTkLabel(self.dashboard_panel.frame, image=resizedImage, text="")
        self.image_label.image = resizedImage
        self.image_label.pack(pady=20)

        label_balance = ctk.CTkLabel(self.dashboard_panel.frame, text=f"Your Balance: R{self.logged_in_user.balance:.2f}",
                                               font=("Helvetica", 20))
        label_balance.pack(pady=20)

        button_back = ctk.CTkButton(self.dashboard_panel.frame, text="Back", command=self.backDashboard, corner_radius=32)
        button_back.pack(pady=10)
    
    def backDashboard(self):
        self.dashboard_panel.hide_panel()

    def transfer_money(self):
        self.dashboard_panel.show_panel()
        self.clear_panel()
        self.liftAll()

        image = PhotoImage(file="nexbank2.png")
        resizedImage = image.subsample(1, 1)
        self.image_label = ctk.CTkLabel(self.dashboard_panel.frame, image=resizedImage, text="")
        self.image_label.image = resizedImage
        self.image_label.pack(pady=20)
        self.label_title = ctk.CTkLabel(self.dashboard_panel.frame, text="Transfer Money", font=("Helvetica", 25),
                                                  text_color="#B22E2E")
        self.label_title.pack(pady=10)

        transfer_frame = ctk.CTkFrame(self.dashboard_panel.frame)
        transfer_frame.pack(padx=10, pady=10)

        label_account_number = ctk.CTkLabel(transfer_frame, text="Recipient Account Number:")
        label_account_number.pack()

        self.entry_account_number = ctk.CTkEntry(transfer_frame)
        self.entry_account_number.pack()

        label_amount = ctk.CTkLabel(transfer_frame, text="Amount:")
        label_amount.pack()

        self.entry_amount = ctk.CTkEntry(transfer_frame)
        self.entry_amount.pack()

        self.error_label_transfer = ctk.CTkLabel(transfer_frame, text="", text_color="red")
        self.error_label_transfer.pack(padx=10)

        button_transfer = ctk.CTkButton(transfer_frame, text="Transfer", command=self.process_transfer, corner_radius=32)
        button_transfer.pack(pady=(5, 30), padx=100)

        button_back = ctk.CTkButton(transfer_frame, text="Back", command=self.backDashboard, corner_radius=32)
        button_back.pack(pady=(5, 30), padx=100)

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
                            )

    def view_statement(self):
        self.dashboard_panel.show_panel()
        self.clear_panel()
        self.liftAll()
        self.load_transaction_history(self.logged_in_user.email)

        image = PhotoImage(file="nexbank2.png")
        resizedImage = image.subsample(1, 1)
        self.image_label = ctk.CTkLabel(self.dashboard_panel.frame, image=resizedImage, text="")
        self.image_label.image = resizedImage
        self.image_label.pack(pady=20)

        label_title = ctk.CTkLabel(self.dashboard_panel.frame, text="Bank Statement", font=("Helvetica", 25),  text_color="#B22E2E")
        label_title.pack(pady=10, padx=100)

        canvas = Canvas(self.dashboard_panel.frame, borderwidth=0, highlightthickness=0)
        frame = Frame(canvas)
        vsb = tk.Scrollbar(self.dashboard_panel.frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)

        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        canvas.create_window((0, 0), window=frame, anchor="n", width=self.dashboard_panel.frame.winfo_width())

        frame.bind("<Configure>", lambda event, canvas=canvas: self.on_frame_configure(canvas))

        if not self.logged_in_user.transactions:
            no_transactions_label = ctk.CTkLabel(frame, text="No transactions made yet.", justify="center")
            no_transactions_label.pack(pady=10, padx=(30, 0))
        else:
            for transaction in self.logged_in_user.transactions:
                transaction_label = ctk.CTkLabel(frame, text=transaction, wraplength=600, justify="center")
                transaction_label.pack(pady=5, padx=(30, 0))

        self.error_label_pdf = ctk.CTkLabel(frame, text="", text_color="red")
        self.error_label_pdf.pack(padx=(30, 0))

        self.button_download = ctk.CTkButton(frame, text="Download as PDF",
                                                       command=self.start_download_thread, corner_radius=32)
        self.button_download.pack(pady=10, padx=(30, 0))

        self.button_email = ctk.CTkButton(frame, text="Email Statement",
                                                       command=self.start_emailPDF_thread, corner_radius=32)
        self.button_email.pack(pady=10, padx=(30, 0))

        button_back = ctk.CTkButton(frame, text="Back", command=self.backDashboard, corner_radius=32)
        button_back.pack(pady=10, padx=(30, 0))

    def start_download_thread(self):
        download_thread = threading.Thread(target=self.download_transaction_history)
        download_thread.start()

    def start_emailPDF_thread(self):
        self.button_email.configure(text="Sending\nPlease Wait...")

        forgot_thread = threading.Thread(target=self.send_pdf_via_email)
        forgot_thread.start()
    
    def enable_window(self):
        for widget in self.login_panel.frame.winfo_children():
            if isinstance(widget, (ctk.CTkButton, ctk.CTkEntry, ctk.CTkCheckBox)):
                self.enable_widget(widget)
            for child in widget.winfo_children():
                if isinstance(child, (ctk.CTkButton, ctk.CTkEntry, ctk.CTkCheckBox)):
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
        for widget in self.login_panel.frame.winfo_children():
            if isinstance(widget, (ctk.CTkButton, ctk.CTkEntry, ctk.CTkCheckBox)):
                self.disable_widget(widget)
            for child in widget.winfo_children():
                if isinstance(child, (ctk.CTkButton, ctk.CTkEntry, ctk.CTkCheckBox)):
                    self.disable_widget(child)  

    def send_pdf_via_email(self):
        if not self.logged_in_user.transactions:
            self.error_label_pdf.configure(text="Cannot send email if there are no transactions made yet.")
            self.button_email.configure(text="Email Statement")
            return

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        pdf_filename = temp_file.name
        temp_file.close()

        c = canvas.Canvas(pdf_filename, pagesize=letter)

        logo_path = "nexbank.png"
        c.drawImage(logo_path, 50, 650, width=100, height=100)

        c.setFont("Helvetica", 12)
        c.drawString(350, 730, "Account Number: " + self.logged_in_user.account_number)
        c.drawString(350, 715, "DOB (DD/MM/YYYY): " + self.logged_in_user.dob)
        c.drawString(350, 700, "Contact Number: " + self.logged_in_user.contact)
        c.drawString(350, 685, "Email: " + self.logged_in_user.email)

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
            self.button_email.configure(text="Email Statement")
        except Exception as e:
            print(f"Failed to send email: {e}")
            self.error_label_pdf.configure(text="Failed to send email.", text_color="red")
            self.button_email.configure(text="Email Statement")
        os.remove(pdf_filename)

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
        c.drawString(350, 730, "Account Number: " + self.logged_in_user.account_number)
        c.drawString(350, 715, "DOB (DD/MM/YYYY): " + self.logged_in_user.dob)
        c.drawString(350, 700, "Contact Number: " + self.logged_in_user.contact)
        c.drawString(350, 685, "Email: " + self.logged_in_user.email)

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
        self.dashboard_panel.show_panel()
        self.clear_panel()
        self.liftAll()

        image = PhotoImage(file="nexbank2.png")
        resizedImage = image.subsample(1, 1)
        self.image_label = ctk.CTkLabel(self.dashboard_panel.frame, image=resizedImage, text="")
        self.image_label.image = resizedImage
        self.image_label.pack(pady=20)

        self.label_title = ctk.CTkLabel(self.dashboard_panel.frame, text="Take Loan/Overdraft", font=("Helvetica", 25),
                                                  text_color="#B22E2E")
        self.label_title.pack(pady=10)

        loan_frame = ctk.CTkFrame(self.dashboard_panel.frame)
        loan_frame.pack(padx=10, pady=10)

        label_amount = ctk.CTkLabel(loan_frame, text="Loan Amount:")
        label_amount.pack()

        self.entry_loan_amount = ctk.CTkEntry(loan_frame)
        self.entry_loan_amount.pack()

        self.error_label_loan = ctk.CTkLabel(loan_frame, text="", text_color="red")
        self.error_label_loan.pack(padx=10)

        button_loan = ctk.CTkButton(loan_frame, text="Apply", command=self.process_loan, corner_radius=32)
        button_loan.pack(pady=(5, 30), padx=100)

        button_back = ctk.CTkButton(loan_frame, text="Back", command=self.backDashboard, corner_radius=32)
        button_back.pack(pady=(5, 30), padx=100)
    
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
        self.logged_in_user.transactions.append(transaction_details)
        self.save_users()
        self.save_transaction_log(self.logged_in_user.email, transaction_details)
        self.error_label_loan.configure(text="Loan approved and credited to your account.", text_color="green")
        self.create_popup("Loan Accepted", f"Loan of R{amount:.2f} received on {timestamp}.\nBank Charges: R{bank_charges:.2f}")


    def view_personal_details(self):
        self.dashboard_panel.show_panel()
        self.clear_panel()
        self.liftAll()

        image = PhotoImage(file="nexbank2.png")
        resizedImage = image.subsample(1, 1)
        self.image_label = ctk.CTkLabel(self.dashboard_panel.frame, image=resizedImage, text="")
        self.image_label.image = resizedImage
        self.image_label.pack(pady=20)

        label_title = ctk.CTkLabel(self.dashboard_panel.frame, text="Personal Details", font=("Helvetica", 25),
                                             text_color="#B22E2E")
        label_title.pack(pady=10)

        details_frame = ctk.CTkFrame(self.dashboard_panel.frame)
        details_frame.pack(padx=10, pady=10)

        label_email = ctk.CTkLabel(details_frame, text=f"Email: {self.logged_in_user.email}")
        label_email.pack()

        label_account_number = ctk.CTkLabel(details_frame,
                                                      text=f"Account Number: {self.logged_in_user.account_number}")
        label_account_number.pack()

        label_contact = ctk.CTkLabel(details_frame, text=f"Contact Number: {self.logged_in_user.contact}")
        label_contact.pack()

        label_dob = ctk.CTkLabel(details_frame, text=f"Date of Birth: {self.logged_in_user.dob}")
        label_dob.pack()

        label_balance = ctk.CTkLabel(details_frame, text=f"Balance: R{self.logged_in_user.balance:.2f}")
        label_balance.pack()

        button_back = ctk.CTkButton(details_frame, text="Back", command=self.backDashboard, corner_radius=32)
        button_back.pack(pady=10, padx=100)


    def show_login_and_welcome(self):
        self.login_panel.show_panel()
        self.welcome_panel.show_panel()
        self.liftAll()

    def quit_application(self):
        self.root.quit()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.forget()

    def clear_panel(self):
        for widget in self.dashboard_panel.frame.winfo_children():
            widget.forget()
        self.image_label = None

    def open_registration_window(self):
        self.register_panel.show_panel()
        self.register_welcome_panel.show_panel()
        self.liftAll()
        pass  

    def liftAll(self):
        self.login_panel.frame.lift()
        self.welcome_panel.frame.lift()
        self.register_panel.frame.lift()
        self.register_welcome_panel.frame.lift()
        self.dashboard_panel.frame.lift()

class LoginPanel:
    def __init__(self, parent):
        self.master = parent
        self.root = parent.root
        self.width = 0.45
        self.start_pos = 1.0
        self.end_pos = 0.5
        self.pos = self.start_pos
        self.in_start_pos = True

        self.frame = ctk.CTkFrame(self.root)
        self.frame.place(relx=self.start_pos, rely=0.05, relwidth=self.width, relheight=0.9)

        self.load_images()
        self.create_login_screen()

    def load_images(self):
        self.show_path = "eye.png"
        self.show = Image.open(self.show_path).resize((20, 20), Image.LANCZOS)
        self.imgShow = ImageTk.PhotoImage(self.show)

        self.hide_path = "eyeslash.png"
        self.hide = Image.open(self.hide_path).resize((20, 20), Image.LANCZOS)
        self.imgHide = ImageTk.PhotoImage(self.hide)

        self.imgEmail = ImageTk.PhotoImage(Image.open("email.png").resize((20, 20), Image.LANCZOS))
        self.imgPassword = ImageTk.PhotoImage(Image.open("password.png").resize((20, 20), Image.LANCZOS))

    def create_login_screen(self):
        login_frame = ctk.CTkFrame(self.frame, corner_radius=32)
        login_frame.pack(padx=50, pady=30)

        self.label_title = ctk.CTkLabel(login_frame, text="Login", font=("Helvetica", 40), text_color="#B22E2E", corner_radius=32)
        self.label_title.pack(pady=(30, 5))

        self.label_subtitle = ctk.CTkLabel(login_frame, text="Welcome Back! Please enter your details", font=("Helvetica", 15), text_color="grey50", corner_radius=32)
        self.label_subtitle.pack(pady=(5, 10))

        self.label_email = ctk.CTkLabel(login_frame, text="Email:")
        self.label_email.pack()

        email_frame = ctk.CTkFrame(login_frame, fg_color="transparent")
        email_frame.pack()

        self.email_visibility_button = ctk.CTkButton(email_frame, image=self.imgEmail,
                                                    text="", width=20, height=20,
                                                    fg_color="transparent", bg_color="transparent", hover=False)
        self.email_visibility_button.pack(side="left", padx=(0, 0))

        self.entry_email = ctk.CTkEntry(email_frame, width=250, height=40, font=("Helvetica", 15))
        self.entry_email.pack(side="left", padx=(0, 42))

        self.label_password = ctk.CTkLabel(login_frame, text="Password:")
        self.label_password.pack()

        password_frame = ctk.CTkFrame(login_frame, fg_color="transparent")
        password_frame.pack()

        self.password_button = ctk.CTkButton(password_frame, image=self.imgPassword,
                                            text="", width=20, height=20, fg_color="transparent",
                                            bg_color="transparent", hover=False)
        self.password_button.pack(side="left", padx=(0, 0))

        self.entry_password = ctk.CTkEntry(password_frame, show="*", width=250, height=40, font=("Helvetica", 15))
        self.entry_password.pack(side="left", padx=(0, 0))

        self.password_visibility_button = ctk.CTkButton(password_frame, image=self.imgShow,
                                                        command=self.toggle_password_visibility, text="",
                                                        width=20, height=20, fg_color="transparent",
                                                        bg_color="transparent", hover=False)
        self.password_visibility_button.pack(side="left", padx=(0, 0))

        self.button_forgot_password = ctk.CTkButton(login_frame, text="forgot password ?", command=self.start_forgot_thread, 
                                                    corner_radius=32, fg_color="transparent", 
                                                    text_color="red", hover_color="white",
                                                    font=("Helvetica", 12, "underline"))
        self.button_forgot_password.pack(pady=(0, 0))

        self.error_label = ctk.CTkLabel(login_frame, text="", text_color="red")
        self.error_label.pack(padx=5)

        self.button_login = ctk.CTkButton(login_frame, text="Login", command=self.login_user, corner_radius=32, font=("Helvetica", 20), width=250, height=40, text_color="white")
        self.button_login.pack(pady=(0, 10))

        self.button_back = ctk.CTkButton(login_frame, text="Back", command=self.hideLoginPanels, corner_radius=32, font=("Helvetica", 20), width=250, height=40, text_color="white")
        self.button_back.pack(pady=(0, 30))

        register_frame = ctk.CTkFrame(login_frame, fg_color="transparent")
        register_frame.pack(pady=(0, 30))

        self.label_sign_up = ctk.CTkLabel(register_frame, text="Don't have an account ?", 
                                                    fg_color="transparent", 
                                                    text_color="grey50",
                                                    font=("Helvetica", 12))
        self.label_sign_up.pack(padx=(60, 0), side="left")

        self.button_sign_up = ctk.CTkButton(register_frame, text="Sign up", command=self.SignUpButton,
                                                    fg_color="transparent", 
                                                    hover_color="white", text_color="red",
                                                    font=("Helvetica", 12, "underline"))
        self.button_sign_up.pack(padx=(0, 60), side="left")

    def SignUpButton(self):
        self.hideLoginPanels()
        self.showRegisterPanels()
    
    def showRegisterPanels(self):
        self.master.register_panel.show_panel()
        self.master.register_welcome_panel.show_panel()

    def start_forgot_thread(self):
        self.button_forgot_password.configure(text="Please Wait...")
        self.master.disable_window()
        forgot_thread = threading.Thread(target=self.forgot_password)
        forgot_thread.start()

    def handle_forgot_password_error(self, message):
        self.error_label.configure(text=message)
        self.reset_forgot_password_button()
        self.master.enable_window()

    def reset_forgot_password_button(self):
        self.root.after(0, lambda: self.button_forgot_password.configure(text="Forgot Password"))

    def forgot_password(self):
        email = self.entry_email.get().strip()

        if not email:
            self.handle_forgot_password_error("Please enter your email address.")
            return

        user = self.master.users.get(email)
        if not user:
            self.handle_forgot_password_error("Email address not found.")
            return

        new_password = self.generate_temporary_password()
        user.password = new_password

        self.send_reset_email(email, new_password)
        self.master.save_users()

        self.error_label.configure(text="A new password has been sent to your email.", text_color="green")
        self.reset_forgot_password_button()
        self.master.enable_window()

    def generate_temporary_password(self, length=8):
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

    def toggle_password_visibility(self):
        if self.entry_password.cget("show") == "":
            self.entry_password.configure(show="*")
            self.password_visibility_button.configure(image=self.imgShow)
        else:
            self.entry_password.configure(show="")
            self.password_visibility_button.configure(image=self.imgHide)

    def login_user(self):
        email = self.entry_email.get().strip().lower()
        password = self.entry_password.get()

        if not (email and password):
            self.error_label.configure(text="Please fill in all fields")
            return

        if email in self.master.users and self.master.users[email].password == password:
            self.master.logged_in_user = self.master.users[email]
            self.master.open_dashboard()
            self.hideLoginPanels()
            self.entry_email.delete(0, 'end')
            self.entry_password.delete(0, 'end')
        else:
            self.error_label.configure(text="Invalid email or password.")


    def show_panel(self):
        self.animate("forward")

    def hide_panel(self):
        self.animate("backward")

    def animate(self, direction):
        if direction == "forward" and self.in_start_pos:
            self.animate_forward()
        elif direction == "backward" and not self.in_start_pos:
            self.animate_backwards()

    def animate_forward(self):
        if self.pos > self.end_pos:
            self.pos -= 0.008
            self.frame.place(relx=self.pos, rely=0.05, relwidth=self.width, relheight=0.9)
            self.frame.after(10, self.animate_forward)
        else:
            self.in_start_pos = False

    def animate_backwards(self):
        if self.pos < self.start_pos:
            self.pos += 0.008
            self.frame.place(relx=self.pos, rely=0.05, relwidth=self.width, relheight=0.9)
            self.frame.after(10, self.animate_backwards)
        else:
            self.in_start_pos = True

    def hideLoginPanels(self):
        self.master.login_panel.hide_panel()
        self.master.welcome_panel.hide_panel()

class WelcomePanel:
    def __init__(self, parent):
        self.master = parent
        self.root = parent.root
        self.width = 0.45
        self.start_pos = -0.45
        self.end_pos = 0.05
        self.pos = self.start_pos
        self.in_start_pos = True

        self.frame = ctk.CTkFrame(self.root)
        self.frame.place(relx=self.start_pos, rely=0.05, relwidth=self.width, relheight=0.9)

        self.create_welcome_message()

    def create_welcome_message(self):
        self.frame.update_idletasks()  
        width = self.frame.winfo_width()
        height = self.frame.winfo_height()

        image_path = "background.jpeg"
        if not os.path.exists(image_path):
            print("Image file not found!")
        else:
            background_image = Image.open(image_path)
            background_image = background_image.resize((width, height), Image.LANCZOS)
            self.background_image_tk = ImageTk.PhotoImage(background_image)

            self.background_label = ctk.CTkLabel(self.frame, image=self.background_image_tk, text="")
            self.background_label.image = self.background_image_tk  
            self.background_label.place(relx=0.5, rely=0.5, anchor="center")

    def show_panel(self):
        self.animate("forward")

    def hide_panel(self):
        self.animate("backward")

    def animate(self, direction):
        if direction == "forward" and self.in_start_pos:
            self.animate_forward()
        elif direction == "backward" and not self.in_start_pos:
            self.animate_backwards()

    def animate_forward(self):
        if self.pos < self.end_pos:
            self.pos += 0.008
            self.frame.place(relx=self.pos, rely=0.05, relwidth=self.width, relheight=0.9)
            self.frame.after(10, self.animate_forward)
        else:
            self.in_start_pos = False

    def animate_backwards(self):
        if self.pos > self.start_pos:
            self.pos -= 0.008
            self.frame.place(relx=self.pos, rely=0.05, relwidth=self.width, relheight=0.9)
            self.frame.after(10, self.animate_backwards)
        else:
            self.in_start_pos = True

# Define RegisterPanel class
class RegisterPanel:
    def __init__(self, parent):
        self.master = parent
        self.root = parent.root
        self.width = 0.45
        self.start_pos = -0.45
        self.end_pos = 0.05
        self.pos = self.start_pos
        self.in_start_pos = True

        self.frame = ctk.CTkFrame(self.root)
        self.frame.place(relx=self.start_pos, rely=0.05, relwidth=self.width, relheight=0.9)

        self.load_images()
        self.create_registration_form()

    def load_images(self):
        self.imgUser = ImageTk.PhotoImage(Image.open("user.png").resize((20, 20), Image.LANCZOS))
        self.imgPhone = ImageTk.PhotoImage(Image.open("phone.png").resize((20, 20), Image.LANCZOS))
        self.imgEmail = ImageTk.PhotoImage(Image.open("email.png").resize((20, 20), Image.LANCZOS))
        self.imgPassword = ImageTk.PhotoImage(Image.open("password.png").resize((20, 20), Image.LANCZOS))
        self.imgShow = ImageTk.PhotoImage(Image.open("eye.png").resize((20, 20), Image.LANCZOS))
        self.imgHide = ImageTk.PhotoImage(Image.open("eyeslash.png").resize((20, 20), Image.LANCZOS))

    def create_registration_form(self):
        registration_frame = ctk.CTkFrame(self.frame, corner_radius=32)
        registration_frame.pack(padx=50, pady=30)

        self.label_register = ctk.CTkLabel(registration_frame, text="Register", font=("Helvetica", 40), text_color="#B22E2E", corner_radius=32)
        self.label_register.pack(pady=(30, 5))

        self.label_subtitle = ctk.CTkLabel(registration_frame, text="Welcome! Please enter your details", font=("Helvetica", 15), text_color="grey50", corner_radius=32)
        self.label_subtitle.pack(pady=(5, 10))

        self.label_DOB = ctk.CTkLabel(registration_frame, text="DOB (DD/MM/YYYY):")
        self.label_DOB.pack()

        DOB_frame = ctk.CTkFrame(registration_frame, fg_color="transparent")
        DOB_frame.pack()

        self.DOB_visibility_button = ctk.CTkButton(DOB_frame, image=self.imgUser, text="", width=20, height=20, fg_color="transparent", bg_color="transparent", hover=False)
        self.DOB_visibility_button.pack(side="left", padx=(0, 0))

        self.entry_DOB = ctk.CTkEntry(DOB_frame, width=250, height=40, font=("Helvetica", 15))
        self.entry_DOB.pack(side="left", padx=(0, 42))

        self.label_contact = ctk.CTkLabel(registration_frame, text="Contact Number:")
        self.label_contact.pack()

        contact_frame = ctk.CTkFrame(registration_frame, fg_color="transparent")
        contact_frame.pack()

        self.contact_visibility_button = ctk.CTkButton(contact_frame, image=self.imgPhone, text="", width=20, height=20, fg_color="transparent", bg_color="transparent", hover=False)
        self.contact_visibility_button.pack(side="left", padx=(0, 0))

        self.entry_contact = ctk.CTkEntry(contact_frame, width=250, height=40, font=("Helvetica", 15))
        self.entry_contact.pack(side="left", padx=(0, 42))

        self.label_email = ctk.CTkLabel(registration_frame, text="Email:")
        self.label_email.pack()

        email_frame = ctk.CTkFrame(registration_frame, fg_color="transparent")
        email_frame.pack()

        self.email_visibility_button = ctk.CTkButton(email_frame, image=self.imgEmail, text="", width=20, height=20, fg_color="transparent", bg_color="transparent", hover=False)
        self.email_visibility_button.pack(side="left", padx=(0, 0))

        self.entry_email = ctk.CTkEntry(email_frame, width=250, height=40, font=("Helvetica", 15))
        self.entry_email.pack(side="left", padx=(0, 42))

        self.label_password = ctk.CTkLabel(registration_frame, text="Password:")
        self.label_password.pack()

        password_frame = ctk.CTkFrame(registration_frame, fg_color="transparent")
        password_frame.pack()

        self.password_button = ctk.CTkButton(password_frame, image=self.imgPassword, command=self.toggle_password_visibility, text="", width=20, height=20, fg_color="transparent", bg_color="transparent", hover=False)
        self.password_button.pack(side="left", padx=(0, 0))

        self.entry_password = ctk.CTkEntry(password_frame, show="*", width=250, height=40, font=("Helvetica", 15))
        self.entry_password.pack(side="left", padx=(0, 0))

        self.password_visibility_button = ctk.CTkButton(password_frame, image=self.imgShow, command=self.toggle_password_visibility, text="", width=20, height=20, fg_color="transparent", bg_color="transparent", hover=False)
        self.password_visibility_button.pack(side="left", padx=(0, 0))

        self.label_confirmPassword = ctk.CTkLabel(registration_frame, text="Confirm Password:")
        self.label_confirmPassword.pack()

        confirm_password_frame = ctk.CTkFrame(registration_frame, fg_color="transparent")
        confirm_password_frame.pack()

        self.confirm_password_visibility_button = ctk.CTkButton(confirm_password_frame, image=self.imgPassword, text="", width=20, height=20, fg_color="transparent", bg_color="transparent", hover=False)
        self.confirm_password_visibility_button.pack(side="left", padx=(0, 0))

        self.entry_confirmPassword = ctk.CTkEntry(confirm_password_frame, show="*", width=250, height=40, font=("Helvetica", 15))
        self.entry_confirmPassword.pack(side="left", padx=(0, 0))

        self.confirm_password_visibility_button2 = ctk.CTkButton(confirm_password_frame, image=self.imgShow, command=self.toggle_password_visibility2, text="", width=20, height=20, fg_color="transparent", bg_color="transparent", hover=False)
        self.confirm_password_visibility_button2.pack(side="left", padx=(0, 0))

        self.var_generate_password = ctk.BooleanVar()
        self.checkbutton_generate_password = ctk.CTkCheckBox(registration_frame, text="Generate password", variable=self.var_generate_password, command=self.toggle_password_entry)
        self.checkbutton_generate_password.pack(pady=(10), padx=10)

        self.error_label_reg = ctk.CTkLabel(registration_frame, text="", text_color="red")
        self.error_label_reg.pack(padx=10)

        confirm_TandC_frame = ctk.CTkFrame(registration_frame, fg_color="transparent")
        confirm_TandC_frame.pack()

        self.var_terms_conditions = ctk.BooleanVar()
        self.checkbutton_terms_conditions = ctk.CTkCheckBox(confirm_TandC_frame, text="I agree to the", variable=self.var_terms_conditions)
        self.checkbutton_terms_conditions.pack(side="left", pady=(0, 10), padx=(0, 0))
        self.checkbutton_terms_conditions.configure(state="disabled")

        self.link_terms = ctk.CTkLabel(confirm_TandC_frame, text="Terms & Conditions", text_color="red", cursor="hand2")
        self.link_terms.pack(side="left", pady=(0, 10), padx=(0, 0))
        self.link_terms.bind("<Button-1>", self.create_TandC)

        self.button_register = ctk.CTkButton(registration_frame, text="Register", command=self.start_register_thread, corner_radius=32, font=("Helvetica", 20), width=250, height=40, text_color="white")
        self.button_register.pack(pady=(0, 10))

        self.button_back = ctk.CTkButton(registration_frame, text="Back", command=self.hideRegisterPanels, corner_radius=32, font=("Helvetica", 20), width=250, height=40, text_color="white")
        self.button_back.pack(pady=(0, 30))

        signup_frame = ctk.CTkFrame(registration_frame, fg_color="transparent")
        signup_frame.pack(pady=(0, 30))

        self.label_sign_up = ctk.CTkLabel(signup_frame, text="Already have an account ?", 
                                                    fg_color="transparent", 
                                                    text_color="grey50",
                                                    font=("Helvetica", 12))
        self.label_sign_up.pack(padx=(60, 0), side="left")

        self.button_sign_up = ctk.CTkButton(signup_frame, text="Log in", command=self.LogInButton,
                                                    fg_color="transparent", 
                                                    hover_color="white", text_color="red",
                                                    font=("Helvetica", 12, "underline"))
        self.button_sign_up.pack(padx=(0, 60), side="left")

    def LogInButton(self):
        self.hideRegisterPanels()
        self.showLoginPanels()

    def hideRegisterPanels(self):
        self.master.register_panel.hide_panel()
        self.master.register_welcome_panel.hide_panel()

    def showLoginPanels(self):
        self.master.login_panel.show_panel()
        self.master.welcome_panel.show_panel()

    def toggle_password_visibility(self):
        if self.entry_password.cget("show") == "":
            self.entry_password.configure(show="*")
            self.password_visibility_button.configure(image=self.imgShow)
        else:
            self.entry_password.configure(show="")
            self.password_visibility_button.configure(image=self.imgHide)

    def toggle_password_visibility2(self):
        if self.entry_confirmPassword.cget("show") == "":
            self.entry_confirmPassword.configure(show="*")
            self.confirm_password_visibility_button2.configure(image=self.imgShow)
        else:
            self.entry_confirmPassword.configure(show="")
            self.confirm_password_visibility_button2.configure(image=self.imgHide)

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

    def create_TandC(self, event=None):
        self.TandC = tk.Toplevel(self.root)  
        self.TandC.title("Terms & Conditions")
        self.TandC.geometry("400x300")  
        self.TandC.iconbitmap("icon.ico")

        label_title = ctk.CTkLabel(
            self.TandC, text="Terms & Conditions", 
            font=("Helvetica", 25), text_color="red"
        )
        label_title.pack(pady=10, padx=30)

        label_message = ctk.CTkLabel(
            self.TandC, text="To keep the account open, the user needs to \nmaintain a minimum balance of R500.\n"
                         "Every transfer made will incur a charge of R10.\n"
                         "Every loan taken out will incur a charge of R50.\n"
                         "A user can only take out a loan if they have \na balance of R500 or more.", 
            font=("Helvetica", 12), text_color="black"
        )
        label_message.pack(pady=10, padx=30)

        button_ok = ctk.CTkButton(
            self.TandC, text="OK", 
            command=self.setYes, corner_radius=32
        )
        button_ok.pack(pady=10, padx=100)

        button_cancel = ctk.CTkButton(
            self.TandC, text="Cancel", 
            command=self.cancel, corner_radius=32
        )
        button_cancel.pack(pady=10, padx=100)

    def setYes(self):
        self.var_terms_conditions.set(True)
        self.checkbutton_terms_conditions.configure(state="normal")
        self.TandC.destroy()

    def cancel(self):
        self.checkbutton_terms_conditions.configure(state="normal")
        self.TandC.destroy()

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

    def enable_window(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, (ctk.CTkButton, ctk.CTkEntry, ctk.CTkCheckBox)):
                self.enable_widget(widget)
            for child in widget.winfo_children():
                if isinstance(child, (ctk.CTkButton, ctk.CTkEntry, ctk.CTkCheckBox)):
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
            if isinstance(widget, (ctk.CTkButton, ctk.CTkEntry, ctk.CTkCheckBox)):
                self.disable_widget(widget)
            for child in widget.winfo_children():
                if isinstance(child, (ctk.CTkButton, ctk.CTkEntry, ctk.CTkCheckBox)):
                    self.disable_widget(child)  

    def handle_error(self, message):
        self.error_label_reg.configure(text=message)
        self.reset_register_button()
        self.enable_window()

    def reset_register_button(self):
        self.root.after(0, lambda: self.button_register.configure(text="Register"))

    def register_user(self):
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        dob = self.entry_DOB.get().strip()
        contact = self.entry_contact.get().strip()
        confirmPassword = self.entry_confirmPassword.get()
        password = self.entry_password.get()
        email = self.entry_email.get().strip().lower()

        # Validation checks
        if not (dob and contact and email and password and confirmPassword):
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

        if not contact.isdigit():
            self.handle_error("Please enter a valid South African phone number")
            return

        if len(contact) != 10:
            self.handle_error("Please enter a 10-digit South African phone number.")
            return

        if not email:
            self.handle_error("Email cannot be empty.")
            return

        for user in self.master.users.values():
            if user.email == email:
                self.handle_error("Email already registered. Please try a different email.")
                return

        if not re.match(email_pattern, email):
            self.handle_error("Invalid email format.")
            return

        if self.var_generate_password.get():
            password = self.entry_password.get()
        else:
            if not self.is_strong_password(password):
                self.handle_error("Password is not strong. \nPlease include lowercase, uppercase, digits, and symbols.")
                return

        if password != confirmPassword:
            self.handle_error("Passwords do not match.")
            return
        
        if not self.var_terms_conditions.get():
            self.handle_error("Terms & Conditions is required to be accepted.")
            return

        balance = 500.0
        account_number = self.generate_account_number()
        new_user = User(email, password, account_number, contact, dob, balance)
        self.master.users[email] = new_user
        self.master.save_users()
        self.send_registration_email(email, password)
        self.create_popup("Register Successful",
                        "Please check your email for your credentials. \nYou will be able to login now.")
        self.hide_panel()
        self.master.register_welcome_panel.hide_panel()
        time.sleep(1) 
        self.master.login_panel.show_panel()
        self.master.welcome_panel.show_panel()

    def create_popup(self, title, message, text_color="black", page=""):
        popup = ctk.CTkFrame(self.root)
        popup.pack(padx=20, pady=20)

        label_title = ctk.CTkLabel(popup, text=title, font=("Helvetica", 25), text_color="red")
        label_title.pack(pady=10, padx=30)

        label_message = ctk.CTkLabel(popup, text=message, font=("Helvetica", 12), text_color=text_color)
        label_message.pack(pady=10, padx=30)

        button_ok = ctk.CTkButton(popup, text="OK", command=page, corner_radius=32)
        button_ok.pack(pady=10, padx=100)

    def start_register_thread(self):
        self.button_register.configure(text="Registering\nPlease Wait...")
        register_thread = threading.Thread(target=self.register_user)
        register_thread.start() 
        pass

    def create_main_window(self):

        pass

    def animate(self, direction):
        if direction == "forward" and self.in_start_pos:
            self.animate_forward()
        elif direction == "backward" and not self.in_start_pos:
            self.animate_backward()

    def animate_forward(self):
        self.pos += 0.008
        self.frame.place(relx=self.pos)
        if self.pos >= self.end_pos:
            self.in_start_pos = False
        else:
            self.frame.after(10, self.animate_forward)

    def animate_backward(self):
        self.pos -= 0.008
        self.frame.place(relx=self.pos)
        if self.pos <= self.start_pos:
            self.in_start_pos = True
        else:
            self.frame.after(10, self.animate_backward)

    def hide_panel(self):
        self.animate("backward")
    
    def show_panel(self):
        self.animate("forward")
    
    def hideRegisterPanels(self):
        self.master.register_panel.hide_panel()
        self.master.register_welcome_panel.hide_panel()

# Define Register Welcome Panel
class RegisterWelcomePanel:
    def __init__(self, parent):
        self.master = parent
        self.root = parent.root
        self.width = 0.45
        self.start_pos = 1.0  
        self.end_pos = 0.5
        self.pos = self.start_pos
        self.in_start_pos = True

        self.frame = ctk.CTkFrame(self.root)
        self.frame.place(relx=self.start_pos, rely=0.05, relwidth=self.width, relheight=0.9)

        self.create_welcome_message()

    def create_welcome_message(self):
        self.frame.update_idletasks()  
        width = self.frame.winfo_width()
        height = self.frame.winfo_height()

        image_path = "background.jpeg"
        if not os.path.exists(image_path):
            print("Image file not found!")
        else:
            background_image = Image.open(image_path)
            background_image = background_image.resize((width, height), Image.LANCZOS)
            self.background_image_tk = ImageTk.PhotoImage(background_image)

            self.background_label = ctk.CTkLabel(self.frame, image=self.background_image_tk, text="")
            self.background_label.image = self.background_image_tk  
            self.background_label.place(relx=0.5, rely=0.5, anchor="center")
        
    def animate(self, direction):
        if direction == "forward" and self.in_start_pos:
            self.animate_forward()
        elif direction == "backward" and not self.in_start_pos:
            self.animate_backwards()

    def animate_forward(self):
        if self.pos > self.end_pos:
            self.pos -= 0.008
            self.frame.place(relx=self.pos, rely=0.05, relwidth=self.width, relheight=0.9)
            self.frame.after(10, self.animate_forward)
        else:
            self.in_start_pos = False

    def animate_backwards(self):
        if self.pos < self.start_pos:
            self.pos += 0.008
            self.frame.place(relx=self.pos, rely=0.05, relwidth=self.width, relheight=0.9)
            self.frame.after(10, self.animate_backwards)
        else:
            self.in_start_pos = True

    def hide_panel(self):
        self.animate("backward")
    
    def show_panel(self):
        self.animate("forward")

class CenteredPanel:
    def __init__(self, parent):
        self.master = parent
        self.root = parent.root
        
        self.width = 0.6
        self.height = 0.9  
        self.start_pos = -0.9  
        self.end_pos = 0.04  
        self.pos = self.start_pos
        self.in_start_pos = True

        self.frame = ctk.CTkFrame(self.root)
        self.frame.place(relx=0.5, rely=self.start_pos, relwidth=self.width, relheight=self.height, anchor="n")

        self.create_content()

    def create_content(self):
        self.label_register_welcome = ctk.CTkLabel(self.frame, text="123 Welcome", font=("Helvetica", 25), text_color="#B22E2E")
        self.label_register_welcome.pack(pady=10)

    def animate(self, direction):
        if direction == "down" and self.in_start_pos:
            self.animate_down()
        elif direction == "up" and not self.in_start_pos:
            self.animate_up()

    def animate_down(self):
        if self.pos < self.end_pos:
            self.pos += 0.02  
            self.frame.place(relx=0.5, rely=self.pos, relwidth=self.width, relheight=self.height, anchor="n")
            self.frame.after(10, self.animate_down)
        else:
            self.in_start_pos = False

    def animate_up(self):
        if self.pos > self.start_pos:
            self.pos -= 0.02  
            self.frame.place(relx=0.5, rely=self.pos, relwidth=self.width, relheight=self.height, anchor="n")
            self.frame.after(10, self.animate_up)
        else:
            self.in_start_pos = True

    def hide_panel(self):
        self.animate("up")

    def show_panel(self):
        self.animate("down")

if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap("icon.ico")
    app = NexBank(root)
    root.mainloop()