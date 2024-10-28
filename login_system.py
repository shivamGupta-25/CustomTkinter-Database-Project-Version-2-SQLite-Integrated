import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageFilter
from tkinter import messagebox
import sqlite3
import random
import smtplib
from email.message import EmailMessage
import os


# Connect to database
conn = sqlite3.connect("data.db")
cursor = conn.cursor()

# Create tables if they do not exist
admin_table_create_query = """CREATE TABLE IF NOT EXISTS admin_users(
                    adminID TEXT PRIMARY KEY,
                    pass TEXT
                    )"""
user_table_create_query = """CREATE TABLE IF NOT EXISTS users(
                    userID TEXT PRIMARY KEY,
                    pass TEXT
                    )"""

conn.execute(admin_table_create_query)
conn.execute(user_table_create_query)

# conn.execute("""DELETE FROM admin_users""")
# conn.execute("""DELETE FROM users""")

# Username and password
username = os.environ.get("GMail_ID")
password = "shivam@123"

# Check if the user already exists in the admin_users table
query = "SELECT * FROM admin_users WHERE adminID = ?"
values = (username,)
cursor.execute(query, values)
record = cursor.fetchone()

# Insert only if user does not exist in the table
if not record:
    cursor.execute("INSERT INTO admin_users VALUES (?, ?)", (username, password))
    cursor.execute("INSERT INTO users VALUES (?, ?)", (username, password))

# Commit changes and close connection
conn.commit()
cursor.close()
conn.close()

def generate_otp(is_admin, user_id):
    otp = "".join([str(random.randint(0, 9)) for _ in range(4)])
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        from_mail = os.environ.get("GMail_ID")
        #print(from_mail)
        server.login(from_mail, os.environ.get("GMail_Pass For Sending Mail"))
        message = f"Subject: OTP Verification\n\nYour OTP is: {otp}"
        server.sendmail(from_mail, user_id, message)
        server.quit()
    except Exception as e:
        messagebox.showerror("Email Error", f"Failed to send OTP email: {str(e)}")
    if is_admin:
        #print("this is admin's: ",otp)
        return otp, is_admin
    else:
        #print("this is users: ",otp)
        return otp, is_admin

class CustomButton(ctk.CTkButton):
    def __init__(self, master, text, command=None, **kwargs):
        super().__init__(master, text=text, command=command, **kwargs)
        self.configure(
            font=("Century Gothic", 15, 'bold'),
            border_spacing=10,
            width=220, 
            corner_radius=18,
            cursor = "hand2"
        )

class OtherButton(ctk.CTkButton):
    def __init__(self, master, text, command=None, **kwargs):
        super().__init__(master, text=text, command=command, **kwargs)

        # Calculate the width based on text length
        font_size = 12  # Font size for the button text
        text_width = len(text) * font_size * 0.1  # Approximate text width calculation

        # Set the width based on text size and padding
        self.configure(
            font=('Century Gothic', font_size),
            fg_color="#2E2F33",
            hover=None,
            border_spacing=10,
            width=text_width,
            corner_radius=18,
            cursor="hand2",
        )

class CustomEntry(ctk.CTkEntry):
    def __init__(self, master=None, placeholder_text="", **kwargs):
        super().__init__(
            master=master,
            height=38,
            width=220,
            placeholder_text=placeholder_text,
            placeholder_text_color="#A4A6AC",
            fg_color="white",
            text_color="black",
            font=("Century Gothic", 12, 'bold'),
            border_width=0,
            corner_radius=20,
            **kwargs
        )

def main():
    app = Application()
    app.mainloop()

class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x440")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")
        self.title("Login")
        self.iconbitmap(r'.\assets\window_icon.ico')

        # Setting Background Image
        background_image = ctk.CTkImage(
            light_image=Image.open(r".\assets\background_img1.png").filter(ImageFilter.GaussianBlur(6)), 
            size=(600, 440)
        )
        self.bg_label = ctk.CTkLabel(master=self, image=background_image, text="")
        self.bg_label.pack()

        # Initialize the Login frame
        self.window_frame = Window(self.bg_label, self)

class Window(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(master=parent, width=320, height=350, fg_color="#2E2F33", bg_color="#676767", corner_radius=22)
        self.app = app

        #functions
        def DeleteWindow(event):
            self.app.destroy()

        def CreateAccountWindow():
            self.place_forget()
            self.app.add_account_window_frame = Add_account_Window(self.app.bg_label, self.app)
            self.app.add_account_window_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        def loginAccountWindow():
            self.place_forget()
            self.app.login_window_frame = login_Window(self.app.bg_label, self.app)
            self.app.login_window_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Setting login img
        win_img = ctk.CTkImage(Image.open(r".\assets\window_img.png"), size=(80, 80))
        
        # Create a label widget to hold the login image
        win_img_label = ctk.CTkLabel(master=self, image=win_img, text="")
        win_img_label.place(x=160, y=90, anchor=tk.CENTER)


        create_account_button = CustomButton(master=self, text="Create Account", command=CreateAccountWindow)
        create_account_button.place(x=50, y=170)

        login_button = CustomButton(master=self, text="Login", command=loginAccountWindow)
        login_button.place(x=50, y=240)

        delete_window_Img = ctk.CTkImage(light_image=Image.open(r".\assets\delete_window.png"), size=(30, 30))
        delete_window_Img_label = ctk.CTkLabel(master=self, image=delete_window_Img, text="", fg_color="#2E2F33", cursor= "hand2")
        delete_window_Img_label.bind("<Button-1>",DeleteWindow)
        delete_window_Img_label.place(x=300, y=50, anchor="se")
        # n, ne, e, se, s, sw, w, nw, or center

        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Center the frame

class Add_account_Window(ctk.CTkFrame):

    def __init__(self, parent, app):
        super().__init__(master=parent, width=320, height=350, fg_color="#2E2F33", bg_color="#676767", corner_radius=22)
        self.app = app

        def AddAdmin():
            self.app.add_admin_account_frame = Add_admin_account(self.app.bg_label, self.app)
            self.app.add_admin_account_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        def AddUser():
            self.app.add_user_account_frame = Add_user_account(self.app.bg_label, self.app)
            self.app.add_user_account_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        def BackToWindow():
            self.place_forget()
            self.app.window_frame = Window(self.app.bg_label, self.app)
            self.app.window_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Setting login img
        add_user_img = ctk.CTkImage(Image.open(r".\assets\Add_Account.png"), size=(80, 80))
        
        # Create a label widget to hold the login image
        add_user_img_label = ctk.CTkLabel(master=self, image=add_user_img, text="")
        add_user_img_label.place(x=170, y=90, anchor=tk.CENTER)


        add_admin_account_button = CustomButton(master=self, text="Create Account as Admin", command=AddAdmin)
        add_admin_account_button.place(x=50, y=170)

        add_user_account_button = CustomButton(master=self, text="Create Account as User", command=AddUser)
        add_user_account_button.place(x=50, y=240)

        BackToWindow = OtherButton(master=self, text="Back", cursor="hand2", command=BackToWindow)
        BackToWindow.place(x=163, y=305, anchor = tk.CENTER)

        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Center the frame

class login_Window(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(master=parent, width=320, height=350, fg_color="#2E2F33", bg_color="#676767", corner_radius=22)
        self.app = app

        def Admin_Login():
            self.app.admin_login_frame = AdminLogin(self.app.bg_label, self.app)
            self.app.admin_login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        def User_Login():
            self.app.user_login_frame = UserLogin(self.app.bg_label, self.app)
            self.app.user_login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        def BackToWindow():
            self.place_forget()
            self.app.window_frame = Window(self.app.bg_label, self.app)
            self.app.window_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Setting login img
        login_img = ctk.CTkImage(Image.open(r".\assets\enter.png"), size=(80, 80))
        
        # Create a label widget to hold the login image
        login_img_label = ctk.CTkLabel(master=self, image=login_img, text="")
        login_img_label.place(x=155, y=90, anchor=tk.CENTER)


        login_admin_button = CustomButton(master=self, text="Login as Admin", command=Admin_Login)
        login_admin_button.place(x=50, y=175)

        login_user_button = CustomButton(master=self, text="Login as User", command=User_Login)
        login_user_button.place(x=50, y=240)

        BackToWindow = OtherButton(master=self, text="Back", cursor="hand2", command=BackToWindow)
        BackToWindow.place(x=163, y=305, anchor = tk.CENTER)

        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Center the frame

class Add_admin_account(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(master=parent, width=320, height=350, fg_color="#2E2F33", bg_color="#676767", corner_radius=22)
        self.app = app

        # Functions
        def create():
            admin_code = self.AdminCode_entry.get()
            username = self.user_entry.get()
            password = self.createPass_entry.get()

            if username == '' or password == '' or admin_code == '':
                messagebox.showerror("Error!!","All fields are required")
            elif not username.endswith("@gmail.com"):
                messagebox.showerror(message="Enter Valid Email ID")
            elif admin_code != '1234':
                messagebox.showerror("Error!","Wrong Admin Code")
            else:
                try:
                    conn = sqlite3.connect("data.db")
                    cursor = conn.cursor()
                    # Query to check if the user exist
                    query = "SELECT * FROM admin_users WHERE adminID = ?"
                    values = (username,)
                    cursor.execute(query, values)
                    record = cursor.fetchone()
                    if record and record[0] == username:
                        messagebox.showwarning("User Exist!",message="Admin Already Exist")
                    else:
                        query = "INSERT INTO admin_users (adminID, pass) VALUES (?, ?)"
                        values = (username, password)
                        cursor.execute(query, values)
                        conn.commit()
                        # Show success message
                        messagebox.showinfo("Success!", "User has been added successfully.")
                        # Close cursor and connection
                        cursor.close()
                        conn.close()
                        self.app.login_window_frame = login_Window(self.app.bg_label, self.app)
                        self.app.login_window_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
                except Exception as e:
                    # More specific error handling
                    messagebox.showerror("Database Error", f"An error occurred: {e}")

        def back_to_window():
            response = messagebox.askyesno("Confirmation", "Are you Sure you want to exit this window?")
            if response:
                self.place_forget()
                self.app.window_frame = Window(self.app.bg_label, self.app)
                self.app.window_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            else:
                messagebox.showinfo("Cancelled", "The action was cancelled.")

        # Setting login img
        add_admin_img = ctk.CTkImage(Image.open(r".\assets\profile.png"), size=(80, 80))
        
        # Create a label widget to hold the login image
        add_admin_img_label = ctk.CTkLabel(master=self, image= add_admin_img, text="")
        add_admin_img_label.place(x=160, y=60, anchor=tk.CENTER)

        self.AdminCode_entry = CustomEntry(master=self, placeholder_text="Admin Code")
        self.AdminCode_entry.place(x=50, y=110)

        self.user_entry = CustomEntry(master=self, placeholder_text="Email")
        self.user_entry.place(x=50, y=160)

        self.createPass_entry = CustomEntry(master=self, placeholder_text="Create Password", show="*")
        self.createPass_entry.place(x=50, y=210)

        create_button = CustomButton(master=self, text="Create Account", command=create)
        create_button.place(x=50, y=260)

        back_to_window_button = OtherButton(master=self, text="Back to Window", command=back_to_window)
        back_to_window_button.place(x=163, y=320, anchor=tk.CENTER)

        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Center the frame

class Add_user_account(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(master=parent, width=320, height=350, fg_color="#2E2F33", bg_color="#676767", corner_radius=22)
        self.app = app

        # Functions
        def create_user():
            username = self.user_entry.get()
            password = self.createPass_entry.get()

            if username == '' or password == '':
                messagebox.showerror("Error!!","All fields are required")
            elif not username.endswith("@gmail.com"):
                messagebox.showerror(message="Enter Valid Email ID")
            else:
                try:
                    conn = sqlite3.connect("data.db")
                    cursor = conn.cursor()

                    # Query to check if the user exist
                    query = "SELECT * FROM users WHERE userID = ?"
                    values = (username,)
                    cursor.execute(query, values)
                    record = cursor.fetchone()
                    if record and record[0] == username:
                        messagebox.showwarning("User Exist!",message="User Already Exist")
                    else:
                        query = "INSERT INTO users (userID, pass) VALUES (?, ?)"
                        values = (username, password)
                        cursor.execute(query, values)
                        conn.commit()
                        # Show success message
                        messagebox.showinfo("Success!", "User has been added successfully.")
                        # Close cursor and connection
                        cursor.close()
                        conn.close()
                        self.app.login_window_frame = login_Window(self.app.bg_label, self.app)
                        self.app.login_window_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
                except Exception as e:
                    # More specific error handling
                    messagebox.showerror("Database Error", f"An error occurred: {e}")


        def back_to_window():
            response = messagebox.askyesno("Confirmation", "Are you Sure you want to exit this window?")
            if response:
                self.place_forget()
                self.app.window_frame = Window(self.app.bg_label, self.app)
                self.app.window_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            else:
                messagebox.showinfo("Cancelled", "The action was cancelled.")

        # Setting login img
        add_user_img = ctk.CTkImage(Image.open(r".\assets\man.png"), size=(80, 80))
        
        # Create a label widget to hold the login image
        add_user_img_label = ctk.CTkLabel(master=self, image=add_user_img, text="")
        add_user_img_label.place(x=170, y=60, anchor=tk.CENTER)


        self.user_entry = CustomEntry(master=self, placeholder_text="Email")
        self.user_entry.place(x=50, y=130)

        self.createPass_entry = CustomEntry(master=self, placeholder_text="Create Password", show='*')
        self.createPass_entry.place(x=50, y=190)

        create_button =CustomButton(master=self, text="Create Account", command=create_user)
        create_button.place(x=50, y=250)

        back_to_window_button = OtherButton(master=self, text="Back to window", command=back_to_window)
        back_to_window_button.place(x=163, y=310, anchor=tk.CENTER)

        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Center the frame

class AdminLogin(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(master=parent, width=320, height=350, fg_color="#2E2F33", bg_color="#676767", corner_radius=22)
        self.app = app

        # Functions
        def login():
            username = self.user_entry.get()
            password = self.pass_entry.get()

            if username == '' or password == '':
                messagebox.showerror("Error!!","All fields are required")
            else:
                try:
                    conn = sqlite3.connect("data.db")
                    cursor = conn.cursor()

                    # Query to check if the user exist
                    query = "SELECT * FROM admin_users WHERE adminID = ?"
                    values = (username,)
                    cursor.execute(query, values)
                    record = cursor.fetchone()
                    if record:
                        # Query to check if the user and password exist
                        query = "SELECT * FROM admin_users WHERE adminID = ? AND pass = ?"
                        values = (username, password)
                        cursor.execute(query, values)
                        result = cursor.fetchone()
                        if result:
                            messagebox.showinfo("Success!", "Login is Successful")
                            cursor.close()
                            conn.close()
                            self.app.withdraw()
                            import AdminDashboard
                        else:
                            messagebox.showerror("Error!!",'Wrong Credentials')
                    else:
                        messagebox.showinfo(message="User doesn't Exist!")
                except Exception as e:
                    messagebox.showerror("Connection", f"Database Connection not established! Error: {str(e)}")

        def frgt_pass():
            response = messagebox.askyesno("Confirmation", "Do you want to proceed to reset your password?")
            if response:
                self.place_forget()
                self.app.find_account_frame = FindAccount(self.app.bg_label, self.app, is_admin=True)
                self.app.find_account_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            else:
                messagebox.showinfo("Cancelled", "The action was cancelled.")

        def BackToWindow(event):
            self.place_forget()
            self.app.window_frame = Window(self.app.bg_label, self.app)
            self.app.window_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Setting login img
        admin_login_img = ctk.CTkImage(Image.open(r".\assets\Admin_Login.png"), size=(80, 80))
        
        # Create a label widget to hold the login image
        admin_login_img_label = ctk.CTkLabel(master=self, image=admin_login_img, text="")
        admin_login_img_label.place(x=160, y=60, anchor=tk.CENTER)

        l1= ctk.CTkLabel(master= self, text = "Login as Admin", font=("Times New Roman", 22))
        l1.place(x=160, y=120, anchor = tk.CENTER)

        self.user_entry = CustomEntry(master=self, placeholder_text="Email")
        self.user_entry.place(x=50, y=150)

        self.pass_entry = CustomEntry(master=self, placeholder_text="Password", show='*')
        self.pass_entry.place(x=50, y=210)

        login_button = CustomButton(master=self,  text="Login", command=login)
        login_button.place(x=50, y=268)

        frgt_button = OtherButton(master=self, text="Forget Password?", command=frgt_pass)
        frgt_button.place(x=163, y=325, anchor=tk.CENTER)

        BackToWindowImg = ctk.CTkImage(light_image=Image.open(r".\assets\delete.png"), size=(25, 25))
        bg_label = ctk.CTkLabel(master=self, image=BackToWindowImg, text="", fg_color="#2E2F33", cursor= "hand2")
        bg_label.bind("<Button-1>",BackToWindow)
        bg_label.place(x=300, y=50, anchor="se")
        # n, ne, e, se, s, sw, w, nw, or center

        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Center the frame

class UserLogin(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(master=parent, width=320, height=350, fg_color="#2E2F33", bg_color="#676767", corner_radius=22)
        self.app = app

        # Functions
        def login():
            username = self.user_entry.get()
            password = self.pass_entry.get()

            if username == '' or password == '':
                messagebox.showerror("Error!!","All fields are required")
            else:
                try:
                    conn = sqlite3.connect("data.db")
                    cursor = conn.cursor()

                    # Query to check if the user exist
                    query = "SELECT * FROM users WHERE userID = ?"
                    values = (username,)
                    cursor.execute(query, values)
                    record = cursor.fetchone()
                    if record:
                        # Query to check if the user and password exist
                        query = "SELECT * FROM users WHERE userID = ? AND pass = ?"
                        values = (username, password)
                        cursor.execute(query, values)
                        result = cursor.fetchone()
                        if result:
                            messagebox.showinfo("Success!", "Login is Successful")
                            cursor.close()
                            conn.close()
                            self.app.withdraw()
                            import UserDashboard
                        else:
                            messagebox.showerror("Error!!",'Wrong Credentials')
                    else:
                        messagebox.showinfo(message="User doesn't Exist!")
                except Exception as e:
                    messagebox.showerror("Connection", f"Database Connection not established! Error: {str(e)}")


        def frgt_pass():
            response = messagebox.askyesno("Confirmation", "Do you want to proceed to reset your password?")
            if response:
                self.place_forget()
                self.app.find_account_frame = FindAccount(self.app.bg_label, self.app, is_admin=False)
                self.app.find_account_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            else:
                messagebox.showinfo("Cancelled", "The action was cancelled.")

        def BackToWindow(event):
            self.place_forget()
            self.app.window_frame = Window(self.app.bg_label, self.app)
            self.app.window_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        user_login_img = ctk.CTkImage(Image.open(r".\assets\teamwork.png"), size=(80, 80))
        
        # Create a label widget to hold the login image
        user_login_img_label = ctk.CTkLabel(master=self, image=user_login_img, text="")
        user_login_img_label.place(x=160, y=60, anchor=tk.CENTER)

        l1= ctk.CTkLabel(master= self, text = "Login as User", font=("Times New Roman", 22))
        l1.place(x=160, y=125, anchor = tk.CENTER)

        self.user_entry = CustomEntry(master=self, placeholder_text="Email")
        self.user_entry.place(x=50, y=150)

        self.pass_entry = CustomEntry(master=self, placeholder_text="Password", show='*')
        self.pass_entry.place(x=50, y=210)

        login_button = CustomButton(master=self,  text="Login", command=login)
        login_button.place(x=50, y=268)

        frgt_button = OtherButton(master=self, text="Forget Password?", command=frgt_pass)
        frgt_button.place(x=163, y=325, anchor=tk.CENTER)

        BackToWindowImg = ctk.CTkImage(light_image=Image.open(r".\assets\delete.png"), size=(25, 25))
        bg_label = ctk.CTkLabel(master=self, image=BackToWindowImg, text="", fg_color="#2E2F33", cursor= "hand2")
        bg_label.bind("<Button-1>",BackToWindow)
        bg_label.place(x=300, y=50, anchor="se")
        # n, ne, e, se, s, sw, w, nw, or center

        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Center the frame

class FindAccount(ctk.CTkFrame):
    def __init__(self, parent, app, is_admin=False):
        super().__init__(master=parent, width=320, height=350, fg_color="#2E2F33", bg_color="#676767", corner_radius=22)
        self.app = app
        self.is_admin = is_admin

        def Continue():
            self.user_id = self.email_entry.get()
            if self.user_id =='':
                messagebox.showerror("Error!","Please Enter Username")
            else:
                try:
                    conn = sqlite3.connect("data.db")
                    cursor = conn.cursor()

                    if self.is_admin:
                        # Query to check if the user exist
                        query = "SELECT * FROM admin_users WHERE adminID = ?"
                    else:
                        query = "SELECT * FROM users WHERE userID = ?"
                    values = (self.user_id,)
                    cursor.execute(query, values)
                    record = cursor.fetchone()
                    if record and record[0] == self.user_id:
                        cursor.close()
                        conn.close()
                        otp, is_admin = generate_otp(self.is_admin, self.user_id)
                        self.place_forget()
                        self.app.Otp_entry_frame = OTPEntry(self.app.bg_label, self.app, otp, self.user_id, is_admin)
                        self.app.Otp_entry_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
                    else:
                        messagebox.showerror("Invalid User","User not found or incorrect Username")
                except Exception as e:
                    messagebox.showerror("Connection", f"Database Connection not established! Error: {str(e)}")
    

        def BackToLogin():
            self.place_forget()  # Hide the forgot password frame
            self.app.login_window_frame = login_Window(self.app.bg_label, self.app)  # Show the login frame again
            self.app.login_window_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        find_account_img = ctk.CTkImage(Image.open(r".\assets\error.png"), size = (80, 80))
        find_account_img_label=ctk.CTkLabel(master=self, image=find_account_img, text="")
        find_account_img_label.place(x=160, y=65, anchor = tk.CENTER)
        
        l1= ctk.CTkLabel(master= self, text = "Find your account", font=("Calibri Light", 25, 'bold'))
        l1.place(x=160, y=120, anchor = tk.CENTER)

        l2= ctk.CTkLabel(master= self, text = "Enter your username", font=("Candara", 12))
        l2.place(x=52, y=145)

        self.email_entry = CustomEntry(master = self, placeholder_text="Email")
        self.email_entry.place(x=50, y = 180)

        continue_button = CustomButton(master=self, text="Continue", command=Continue)
        continue_button.place(x=50, y=243)

        BackToWindow = OtherButton(master=self, text="Back to login", cursor="hand2", command=BackToLogin)
        BackToWindow.place(x=163, y=300, anchor = tk.CENTER)

        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Center the frame

class OTPEntry(ctk.CTkFrame):
    def __init__(self, parent, app, otp, user_id, is_admin = False):
        super().__init__(master=parent, width=320, height=350, fg_color="#2E2F33", bg_color="#676767", corner_radius=22)
        self.app = app

        self.user_id = user_id
        self.otp = otp
        self.is_admin = is_admin

        def verify_otp():
            input_opt = self.otp_entry.get()
            if input_opt == self.otp or self.is_admin:
                messagebox.showinfo(message="OTP Verified")
                self.place_forget()
                self.app.reset_pass_frame = ResetPassword(self.app.bg_label, self.app, self.user_id, is_admin)
                self.app.reset_pass_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            else:
                messagebox.showerror(message="Incorrect OTP")

        def cancel():
            self.place_forget()
            self.app.login_window_frame = login_Window(self.app.bg_label, self.app)
            self.app.login_window_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        otp_img = ctk.CTkImage(Image.open(r".\assets\one-time-password.png"), size = (80, 80))

        # Create a label widget to hold the OTP image
        otp_img_label=ctk.CTkLabel(master=self, image=otp_img, text="")
        otp_img_label.place(x=165, y=80, anchor = tk.CENTER)
        
        title_label = ctk.CTkLabel(master=self, text="Enter the code we sent to your Email", font=("Century Gothic", 12), fg_color="#2E2F33")
        title_label.place(x=160, y=150, anchor=tk.CENTER)

        self.otp_entry = CustomEntry(master = self, placeholder_text="Security Code", )
        self.otp_entry.place(x=50, y = 180)

        continue_button = CustomButton(master=self, text="Continue", command=verify_otp)
        continue_button.place(x=50, y=240)
        
        cancel_button = OtherButton(master=self, text="Cancel", command=cancel)  # Placeholder for now
        cancel_button.place(x=163, y=300, anchor=tk.CENTER)

        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Center the frame

class ResetPassword(ctk.CTkFrame):
    def __init__(self, parent, app, user_id, is_admin = False):
        super().__init__(master=parent, width=320, height=350, fg_color="#2E2F33", bg_color="#676767", corner_radius=22)
        self.app = app

        self.user_id = user_id
        self.is_admin = is_admin

        def reset_password():
            passwrd = self.newPass_entry1.get()
            passwrd_repeat = self.newPass_entry2.get()

            if passwrd == '' or passwrd_repeat == '':
                messagebox.showerror("Error!", "Field is required")
            elif passwrd == passwrd_repeat:
                try:
                    conn = sqlite3.connect("data.db")
                    cursor = conn.cursor()

                    verifier = None
                    if is_admin:
                        # Update password in the database
                        query = "UPDATE admin_users SET pass = ? WHERE adminID = ?"
                        verifier = "admin"
                    else:
                        query = "UPDATE users SET pass = ? WHERE userID = ?"
                    values = (passwrd, self.user_id)
                    cursor.execute(query, values)
                    conn.commit()

                    # Verify the password update
                    if verifier == "admin":
                        query = "SELECT * FROM admin_users WHERE adminID = ? AND pass = ?"
                    else:
                        query = "SELECT * FROM users WHERE userID = ? AND pass = ?"
    
                    values = (user_id, passwrd)
                    cursor.execute(query, values)
                    result = cursor.fetchone()

                    if result and result[0] == self.user_id and result[1] == passwrd:
                        messagebox.showinfo(message="Password Successfully reset")
                        cursor.close()
                        conn.close()
                        if self.is_admin:
                            self.app.admin_login_frame = AdminLogin(self.app.bg_label, self.app)
                            self.app.admin_login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
                        else:
                            self.app.user_login_frame = UserLogin(self.app.bg_label, self.app)
                            self.app.user_login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
                    else:
                        messagebox.showerror(message="Password reset failed. Please try again.")
                except Exception as e:
                    # More specific error handling
                    messagebox.showerror("Database Error", f"An error occurred: {e}")
            else:
                messagebox.showerror(message="Entered password is not the same.")

        def cancel():
            message = messagebox.askquestion(message="Do you want to cancel?")
            if message == "yes":
                self.app.login_frame = UserLogin(self.app.bg_label, self.app)
                self.app.login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Setting reset password img
        reset_pass_img = ctk.CTkImage(Image.open(r".\assets\reset-password.png"), size=(50, 50))
        
        # Create a label widget to hold the reset pass image
        reset_pass_img_label = ctk.CTkLabel(master=self, image=reset_pass_img, text="")
        reset_pass_img_label.place(x=160, y=35, anchor=tk.CENTER)

        # Labels
        l1 = ctk.CTkLabel(master=self, text="Create A Strong Password", font=("Calibri Light", 22, 'bold'))
        l1.place(x=160, y=75, anchor=tk.CENTER)

        l2 = ctk.CTkLabel(master=self, text="Your Password must be at least 6 characters", font=("Candara", 12))
        l3 = ctk.CTkLabel(master=self, text="and should include a combination of numbers,", font=("Candara", 12))
        l4 = ctk.CTkLabel(master=self, text="letters, and special character (!$@%)", font=("Candara", 12))

        l2.place(x=160, y=101, anchor=tk.CENTER)
        l3.place(x=160, y=120, anchor=tk.CENTER)
        l4.place(x=160, y=140, anchor=tk.CENTER)

        self.newPass_entry1 = CustomEntry(master=self, placeholder_text="New Password", show="*")
        self.newPass_entry1.place(x=50, y=160)

        self.newPass_entry2 = CustomEntry(master=self, placeholder_text="New Password, again", show="*")
        self.newPass_entry2.place(x=50, y=210)

        reset_button = CustomButton(master=self, text="Reset Password", command=reset_password)
        reset_button.place(x=50, y=260)

        cancel_button = OtherButton(master=self, text="Cancel", command=cancel)  
        cancel_button.place(x=163, y=320, anchor=tk.CENTER)

        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Center the frame


if __name__ == "__main__":
    main()