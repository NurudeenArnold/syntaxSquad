from datetime import datetime
import random
import re
import string
import threading
import time
import customtkinter as ctk
from PIL import Image, ImageTk

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("themes/red.json")

class User:
    def __init__(self, email, password, account_number, contact, dob):
        self.email = email
        self.password = password
        self.account_number = account_number
        self.balance = 500.0
        self.transactions = []
        self.contact = contact
        self.dob = dob

window = ctk.CTk()
window.title('NexBank')
window.geometry('1000x800')
users = {}

def main_window():
    label_main = ctk.CTkLabel(window, text="Welcome to NexBank!", font=("Verdana", 25), text_color="#B22E2E")
    label_main.pack(pady=50)

    image = Image.open("nexbank2.png")
    resizedImage = image.resize((200, 200), Image.LANCZOS)
    img = ImageTk.PhotoImage(resizedImage)
    image_label = ctk.CTkLabel(window, image=img, text="")
    image_label.image = img
    image_label.pack(pady=20)

    button_login = ctk.CTkButton(window, text="Login", command=lambda: show_login_and_welcome(), corner_radius=32)
    button_login.pack(pady=10)

    button_register = ctk.CTkButton(window, text="Register", command=lambda: open_registration_window(), corner_radius=32)
    button_register.pack()

    button_quit = ctk.CTkButton(window, text="Quit", command=lambda: quit_application(), corner_radius=32)
    button_quit.pack(pady=10)

    error_label = ctk.CTkLabel(window, text="", text_color="red")
    error_label.pack()
main_window()

def show_dashboard():
    hide_widgets(window)

    image = Image.open("nexbank2.png")
    resizedImage = image.resize((200, 200), Image.LANCZOS)
    img = ImageTk.PhotoImage(resizedImage)
    
    image_label = ctk.CTkLabel(window, image=img, text="")
    image_label.image = img
    image_label.pack(pady=50)

    label_title = ctk.CTkLabel(window, text="Dashboard", font=("Helvetica", 25), text_color="#B22E2E")
    label_title.pack(pady=10)

    button_balance = ctk.CTkButton(window, text="View Balance", command=view_balance, corner_radius=32)
    button_balance.pack(pady=10)

    button_transfer = ctk.CTkButton(window, text="Transfer Money", command=transfer_money, corner_radius=32)
    button_transfer.pack(pady=10)

    button_statement = ctk.CTkButton(window, text="View Bank Statement", command=view_statement, corner_radius=32)
    button_statement.pack(pady=10)

    button_loan = ctk.CTkButton(window, text="Take Loan/Overdraft", command=take_loan, corner_radius=32)
    button_loan.pack(pady=10)

    button_personal_details = ctk.CTkButton(window, text="View Personal Details", command=view_personal_details, corner_radius=32)
    button_personal_details.pack(pady=10)

    button_logout = ctk.CTkButton(window, text="Logout", command=show_login_screen, corner_radius=32)
    button_logout.pack(pady=10)

def view_balance():
    pass

def transfer_money():
    pass

def view_statement():
    pass

def take_loan():
    pass

def view_personal_details():
    pass

def show_login_screen():
    time.sleep(1)
    login_panel.show_panel()
    welcome_panel.show_panel()
    hide_widgets(window)
    main_window()
    liftAll()

# Define LoginPanel class
class LoginPanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.width = 0.45
        self.start_pos = 1.0  
        self.end_pos = 0.5
        self.pos = self.start_pos
        self.in_start_pos = True

        self.place(relx=self.start_pos, rely=0.05, relwidth=self.width, relheight=0.9)

        self.load_images()
        self.create_login_screen()

    def load_images(self):
        self.show_path = "eye.png"
        self.show = Image.open(self.show_path)
        self.show = self.show.resize((20, 20), Image.LANCZOS)
        self.imgShow = ImageTk.PhotoImage(self.show)

        self.hide_path = "eyeslash.png"
        self.hide = Image.open(self.hide_path)
        self.hide = self.hide.resize((20, 20), Image.LANCZOS)
        self.imgHide = ImageTk.PhotoImage(self.hide)

        self.imgEmail = ImageTk.PhotoImage(Image.open("email.png").resize((20, 20), Image.LANCZOS))
        self.imgPassword = ImageTk.PhotoImage(Image.open("password.png").resize((20, 20), Image.LANCZOS))

    def create_login_screen(self):
        self.label_title = ctk.CTkLabel(self, text="Login", font=("Helvetica", 25), text_color="#B22E2E")
        self.label_title.pack(pady=10)

        login_frame = ctk.CTkFrame(self)
        login_frame.pack(padx=10, pady=10)

        self.label_email = ctk.CTkLabel(login_frame, text="Email:")
        self.label_email.pack()

        email_frame = ctk.CTkFrame(login_frame, fg_color="transparent")
        email_frame.pack()

        self.email_visibility_button = ctk.CTkButton(email_frame, image=self.imgEmail,
                                                     text="", width=20, height=20,
                                                     fg_color="transparent", bg_color="transparent", hover=False)
        self.email_visibility_button.pack(side="left", padx=(0, 0))

        self.entry_email = ctk.CTkEntry(email_frame)
        self.entry_email.pack(side="left", padx=(0, 35))

        self.label_password = ctk.CTkLabel(login_frame, text="Password:")
        self.label_password.pack()

        password_frame = ctk.CTkFrame(login_frame, fg_color="transparent")
        password_frame.pack()

        self.password_button = ctk.CTkButton(password_frame, image=self.imgPassword,
                                             text="", width=20, height=20, fg_color="transparent",
                                             bg_color="transparent", hover=False)
        self.password_button.pack(side="left", padx=(0, 0))

        self.entry_password = ctk.CTkEntry(password_frame, show="*")
        self.entry_password.pack(side="left", padx=(0, 0))

        self.password_visibility_button = ctk.CTkButton(password_frame, image=self.imgShow,
                                                        command=self.toggle_password_visibility, text="",
                                                        width=20, height=20, fg_color="transparent",
                                                        bg_color="transparent", hover=False)
        self.password_visibility_button.pack(side="left", padx=(0, 0))

        self.error_label = ctk.CTkLabel(login_frame, text="", text_color="red")
        self.error_label.pack(padx=10)

        self.button_login = ctk.CTkButton(login_frame, text="Login", command=self.login_user, corner_radius=32)
        self.button_login.pack(pady=(5, 30), padx=100)

        self.button_forgot_password = ctk.CTkButton(login_frame, text="Forgot Password", command=self.start_forgot_thread, corner_radius=32)
        self.button_forgot_password.pack(pady=(5, 30), padx=100)

        self.button_back = ctk.CTkButton(login_frame, text="Back", command=self.hideLoginPanels, corner_radius=32)
        self.button_back.pack(pady=(5, 30), padx=100)

    def toggle_password_visibility(self):
        if self.entry_password.cget("show") == "":
            self.entry_password.configure(show="*")
            self.password_visibility_button.configure(image=self.imgShow)
        else:
            self.entry_password.configure(show="")
            self.password_visibility_button.configure(image=self.imgHide)

    def login_user(self):
        email = self.entry_email.get()
        email = email.lower()
        password = self.entry_password.get()

        if not (email and password):
            self.error_label.configure(text="Please fill in all fields")
            return

        if email in users and users[email].password == password:
            self.logged_in_user = users[email]
            print("logged in")
        else:
            self.error_label.configure(text="Invalid email or password.")

    def start_forgot_thread(self):
        pass

    def animate(self, direction):
        if direction == "forward" and self.in_start_pos:
            self.animate_forward()
        elif direction == "backward" and not self.in_start_pos:
            self.animate_backwards()

    def animate_forward(self):
        if self.pos > self.end_pos:
            self.pos -= 0.008
            self.place(relx=self.pos, rely=0.05, relwidth=self.width, relheight=0.9)
            self.after(10, self.animate_forward)
        else:
            self.in_start_pos = False

    def animate_backwards(self):
        if self.pos < self.start_pos:
            self.pos += 0.008
            self.place(relx=self.pos, rely=0.05, relwidth=self.width, relheight=0.9)
            self.after(10, self.animate_backwards)
        else:
            self.in_start_pos = True

    def hide_panel(self):
        self.animate("backward")
    
    def show_panel(self):
        self.animate("forward")

    def hideLoginPanels(self):
        login_panel.hide_panel()
        welcome_panel.hide_panel()

# Define WelcomePanel class
class WelcomePanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.width = 0.45
        self.start_pos = -0.45 
        self.end_pos = 0.05
        self.pos = self.start_pos
        self.in_start_pos = True

        self.place(relx=self.start_pos, rely=0.05, relwidth=self.width, relheight=0.9)

        self.create_welcome_message()

    def create_welcome_message(self):
        self.label_welcome = ctk.CTkLabel(self, text="Welcome", font=("Helvetica", 25), text_color="#B22E2E")
        self.label_welcome.pack(pady=10)

    def animate(self, direction):
        if direction == "forward" and self.in_start_pos:
            self.animate_forward()
        elif direction == "backward" and not self.in_start_pos:
            self.animate_backwards()

    def animate_forward(self):
        if self.pos < self.end_pos:
            self.pos += 0.008
            self.place(relx=self.pos, rely=0.05, relwidth=self.width, relheight=0.9)
            self.after(10, self.animate_forward)
        else:
            self.in_start_pos = False

    def animate_backwards(self):
        if self.pos > self.start_pos:
            self.pos -= 0.008
            self.place(relx=self.pos, rely=0.05, relwidth=self.width, relheight=0.9)
            self.after(10, self.animate_backwards)
        else:
            self.in_start_pos = True

    def hide_panel(self):
        self.animate("backward")
    
    def show_panel(self):
        self.animate("forward")

# Define RegisterPanel class
class RegisterPanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.width = 0.45
        self.start_pos = -0.45  
        self.end_pos = 0.05
        self.pos = self.start_pos
        self.in_start_pos = True

        self.place(relx=self.start_pos, rely=0.05, relwidth=self.width, relheight=0.9)

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
        self.label_register = ctk.CTkLabel(self, text="Register", font=("Helvetica", 25), text_color="#B22E2E")
        self.label_register.pack(pady=10)

        registration_frame = ctk.CTkFrame(self)
        registration_frame.pack(padx=10, pady=10)

        self.label_DOB = ctk.CTkLabel(registration_frame, text="DOB (DD/MM/YYYY):")
        self.label_DOB.pack()

        DOB_frame = ctk.CTkFrame(registration_frame, fg_color="transparent")
        DOB_frame.pack()

        self.DOB_visibility_button = ctk.CTkButton(DOB_frame, image=self.imgUser,
                                                   text="",
                                                   width=20, height=20, fg_color="transparent",
                                                   bg_color="transparent", hover=False)
        self.DOB_visibility_button.pack(side="left", padx=(0, 0))

        self.entry_DOB = ctk.CTkEntry(DOB_frame)
        self.entry_DOB.pack(side="left", padx=(0, 35))

        self.label_contact = ctk.CTkLabel(registration_frame, text="Contact Number:")
        self.label_contact.pack()

        contact_frame = ctk.CTkFrame(registration_frame, fg_color="transparent")
        contact_frame.pack()

        self.contact_visibility_button = ctk.CTkButton(contact_frame, image=self.imgPhone,
                                                       text="",
                                                       width=20, height=20, fg_color="transparent",
                                                       bg_color="transparent", hover=False)
        self.contact_visibility_button.pack(side="left", padx=(0, 0))

        self.entry_contact = ctk.CTkEntry(contact_frame)
        self.entry_contact.pack(side="left", padx=(0, 35))

        self.label_email = ctk.CTkLabel(registration_frame, text="Email:")
        self.label_email.pack()

        email_frame = ctk.CTkFrame(registration_frame, fg_color="transparent")
        email_frame.pack()

        self.email_visibility_button = ctk.CTkButton(email_frame, image=self.imgEmail,
                                                     text="",
                                                     width=20, height=20, fg_color="transparent",
                                                     bg_color="transparent", hover=False)
        self.email_visibility_button.pack(side="left", padx=(0, 0))

        self.entry_email = ctk.CTkEntry(email_frame)
        self.entry_email.pack(side="left", padx=(0, 35))

        self.label_password = ctk.CTkLabel(registration_frame, text="Password:")
        self.label_password.pack()

        password_frame = ctk.CTkFrame(registration_frame, fg_color="transparent")
        password_frame.pack()

        self.password_button = ctk.CTkButton(password_frame, image=self.imgPassword,
                                              command=self.toggle_password_visibility, text="",
                                              width=20, height=20, fg_color="transparent",
                                              bg_color="transparent", hover=False)
        self.password_button.pack(side="left", padx=(0, 0))

        self.entry_password = ctk.CTkEntry(password_frame, show="*")
        self.entry_password.pack(side="left", padx=(0, 0))

        self.password_visibility_button = ctk.CTkButton(password_frame, image=self.imgShow,
                                                        command=self.toggle_password_visibility, text="",
                                                        width=20, height=20, fg_color="transparent",
                                                        bg_color="transparent", hover=False)
        self.password_visibility_button.pack(side="left", padx=(0, 0))

        self.label_confirmPassword = ctk.CTkLabel(registration_frame, text="Confirm Password:")
        self.label_confirmPassword.pack()

        confirm_password_frame = ctk.CTkFrame(registration_frame, fg_color="transparent")
        confirm_password_frame.pack()

        self.confirm_password_visibility_button = ctk.CTkButton(confirm_password_frame, image=self.imgPassword,
                                                                text="",
                                                                width=20, height=20, fg_color="transparent",
                                                                bg_color="transparent", hover=False)
        self.confirm_password_visibility_button.pack(side="left", padx=(0, 0))

        self.entry_confirmPassword = ctk.CTkEntry(confirm_password_frame, show="*")
        self.entry_confirmPassword.pack(side="left", padx=(0, 0))

        self.confirm_password_visibility_button2 = ctk.CTkButton(confirm_password_frame, image=self.imgShow,
                                                                 command=self.toggle_password_visibility2, text="",
                                                                 width=20, height=20, fg_color="transparent",
                                                                 bg_color="transparent", hover=False)
        self.confirm_password_visibility_button2.pack(side="left", padx=(0, 0))

        self.var_generate_password = ctk.BooleanVar()
        self.checkbutton_generate_password = ctk.CTkCheckBox(registration_frame, text="Generate password",
                                                             variable=self.var_generate_password,
                                                             command=self.toggle_password_entry)
        self.checkbutton_generate_password.pack(pady=(10), padx=10)

        self.error_label_reg = ctk.CTkLabel(registration_frame, text="", text_color="red")
        self.error_label_reg.pack(padx=10)

        confirm_TandC_frame = ctk.CTkFrame(registration_frame, fg_color="transparent")
        confirm_TandC_frame.pack()

        self.var_terms_conditions = ctk.BooleanVar()
        self.checkbutton_terms_conditions = ctk.CTkCheckBox(
            confirm_TandC_frame, text="I agree to the ", variable=self.var_terms_conditions
        )
        self.checkbutton_terms_conditions.pack(side="left", pady=(0, 10))
        self.checkbutton_terms_conditions.configure(state="disabled") 

        self.link_terms = ctk.CTkLabel(
            confirm_TandC_frame, text="Terms & Conditions", text_color="red", cursor="hand2"
        )
        self.link_terms.pack(side="left", pady=(0, 10))
        self.link_terms.bind("<Button-1>", self.create_TandC)

        self.button_register = ctk.CTkButton(registration_frame, text="Register", command=self.start_register_thread, corner_radius=32)
        self.button_register.pack(pady=(5, 30), padx=100)

        self.button_back = ctk.CTkButton(registration_frame, text="Back", command=self.hideRegisterPanels, corner_radius=32)
        self.button_back.pack(pady=(5, 30), padx=100)

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
            generated_password = 0 
            self.entry_password.delete(0, "end")
            self.entry_password.insert(0, generated_password)
            self.entry_confirmPassword.delete(0, "end")
            self.entry_confirmPassword.insert(0, generated_password)
        else:
            self.entry_password.delete(0, "end")
            self.entry_confirmPassword.delete(0, "end")
            self.entry_password.configure(show="*")
            self.entry_confirmPassword.configure(show="*")

    def create_TandC(self, event):
        pass

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
        contact = self.entry_contact.get().strip()
        confirmPassword = self.entry_confirmPassword.get()
        password = self.entry_password.get()
        email = self.entry_email.get()
        email = email.lower()

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

        if not email.strip():
            self.handle_error("Email cannot be empty.")
            return

        for user in self.users.values():
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
        
        if not self.var_terms_conditions.get():
            self.handle_error("Terms & Conditions is required to be accepted.")
            return

        account_number = self.generate_account_number()
        user = User(email, password, account_number, contact, dob)
        self.users[email] = user
        self.save_users()
        self.send_registration_email(email, password)

        self.create_popup("Register Successful",
                          "Please check your email for your credentials. \nYou will be able to login now.",
                          page=self.open_login_window)

    def start_register_thread(self):
        self.button_register.configure(text="Registering\nPlease Wait...")
        register_thread = threading.Thread(target=self.register_user)
        register_thread.start() 
        self.hide_panel()
        register_welcome_panel.hide_panel()
        time.sleep(1)
        login_panel.show_panel()
        welcome_panel.show_panel()
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
        self.place(relx=self.pos)
        if self.pos >= self.end_pos:
            self.in_start_pos = False
        else:
            self.after(10, self.animate_forward)

    def animate_backward(self):
        self.pos -= 0.008
        self.place(relx=self.pos)
        if self.pos <= self.start_pos:
            self.in_start_pos = True
        else:
            self.after(10, self.animate_backward)

    def hide_panel(self):
        self.animate("backward")
    
    def show_panel(self):
        self.animate("forward")
    
    def hideRegisterPanels(self):
        register_panel.hide_panel()
        register_welcome_panel.hide_panel()

# Define Register Welcome Panel
class RegisterWelcomePanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.width = 0.45
        self.start_pos = 1.0  
        self.end_pos = 0.5
        self.pos = self.start_pos
        self.in_start_pos = True

        self.place(relx=self.start_pos, rely=0.05, relwidth=self.width, relheight=0.9)

        self.create_welcome_message()

    def create_welcome_message(self):
        self.label_register_welcome = ctk.CTkLabel(self, text="Registration Welcome", font=("Helvetica", 25), text_color="#B22E2E")
        self.label_register_welcome.pack(pady=10)

    def animate(self, direction):
        if direction == "forward" and self.in_start_pos:
            self.animate_forward()
        elif direction == "backward" and not self.in_start_pos:
            self.animate_backwards()

    def animate_forward(self):
        if self.pos > self.end_pos:
            self.pos -= 0.008
            self.place(relx=self.pos, rely=0.05, relwidth=self.width, relheight=0.9)
            self.after(10, self.animate_forward)
        else:
            self.in_start_pos = False

    def animate_backwards(self):
        if self.pos < self.start_pos:
            self.pos += 0.008
            self.place(relx=self.pos, rely=0.05, relwidth=self.width, relheight=0.9)
            self.after(10, self.animate_backwards)
        else:
            self.in_start_pos = True

    def hide_panel(self):
        self.animate("backward")
    
    def show_panel(self):
        self.animate("forward")

# Global stuff
register_panel = RegisterPanel(window)
register_welcome_panel = RegisterWelcomePanel(window)

register_panel.hide_panel()
register_welcome_panel.hide_panel()

login_panel = LoginPanel(window)
welcome_panel = WelcomePanel(window)
register_panel = RegisterPanel(window)
register_welcome_panel = RegisterWelcomePanel(window)

login_panel.hide_panel()
welcome_panel.hide_panel()

def show_login_and_welcome():
    login_panel.show_panel()
    welcome_panel.show_panel()

def open_registration_window():
    register_panel.show_panel()
    register_welcome_panel.show_panel()

def quit_application():
    window.quit()

def hide_widgets(parent):
    for widget in parent.winfo_children():
        widget.pack_forget()

def liftAll():
    login_panel.lift()
    welcome_panel.lift()
    register_panel.lift()
    register_welcome_panel.lift()
    
window.mainloop()
