import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageFilter, ImageDraw, ImageGrab
from tkinter import messagebox, filedialog
import sqlite3
import random
import smtplib
import os
from tkinter.filedialog import askopenfilename
import io
import re
from io import BytesIO
Image.MAX_IMAGE_PIXELS = None

# Show - hide password Func
def show_hide(pass_entry, button):
    # Check the current show option to toggle
    if pass_entry.cget('show') == '*':
        pass_entry.configure(show='')  # Show the password
        button.configure(image=ctk.CTkImage(Image.open(r"./assets/eye-solid.png"), size=(15, 15)))  # Change icon to eye open
    else:
        pass_entry.configure(show='*')  # Hide the password
        button.configure(image=ctk.CTkImage(Image.open(r"./assets/eye-slash-solid.png"), size=(15, 15)))  # Change icon to eye closed

# Setting up the Database
try:
    connection = sqlite3.connect("Database.db")
    cursor = connection.cursor()

    # Student Details Table
    student_table = """CREATE TABLE IF NOT EXISTS StudentDetails (
                        StudentID INTEGER PRIMARY KEY AUTOINCREMENT,
                        StudentName TEXT NOT NULL,
                        Gender TEXT,
                        Age INTEGER,
                        Contact INTEGER,
                        Course TEXT,
                        Email TEXT UNIQUE NOT NULL,
                        Pass TEXT NOT NULL DEFAULT 'user@123',
                        img BLOB
                    )"""

    # Admin Details Table
    admin_table = """CREATE TABLE IF NOT EXISTS AdminDetails (
                        AdminID TEXT PRIMARY KEY,
                        AdminName TEXT NOT NULL,
                        Email TEXT UNIQUE NOT NULL,
                        Pass TEXT NOT NULL,
                        img BLOB
                    )"""

    # connection.execute("DROP TABLE StudentDetails")
    # connection.execute("DROP TABLE AdminDetails")

    # Creating Table If table doesn't exist
    connection.execute(student_table)
    connection.execute(admin_table)

    # Fetching list of tables in the database
    cursor.execute("SELECT seq FROM sqlite_sequence WHERE name='StudentDetails'")
    result = cursor.fetchone()

    # Setting Autoincrement value as SQLite doesn't provide Autoincrement within the table 
    if result is None:
        connection.execute("INSERT INTO sqlite_sequence (name, seq) VALUES ('StudentDetails', 999);")

    # Inserting Dummy Data in Student Table
    cursor.execute("SELECT * FROM StudentDetails")
    record = cursor.fetchone()
    if not record:
        with open(r".\assets\profile_pic.png", 'rb') as read_data:
            pic_data = read_data.read()

        students = [
            ('DummyName1', 'DUMMY_GENDER', "20", "1234567890", 'C++', 'dummy1@gmail.com', '1234', pic_data),
            ('DummyName2', 'DUMMY_GENDER', "21", "1234567891", 'Python', 'dummy2@gmail.com', '1234', pic_data),
            ('DummyName3', 'DUMMY_GENDER', "22", "1234567892", 'Java', 'dummy3@gmail.com', '1234', pic_data),
        ]
        for values in students:
            query = """INSERT INTO StudentDetails (StudentName, Gender, Age, Contact, Course, Email, Pass, img) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
            cursor.execute(query, values)

    # Inserting Admin Data in Admin Table
    cursor.execute("SELECT * FROM AdminDetails")
    record = cursor.fetchone()
    if not record:
        pic_data = b''
        # Open the selected image
        img = Image.open(r".\assets\admin_pic.jpg").resize((135, 135))
        # Create a circular mask
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + img.size, fill=255)

        # Create a new image with transparency and apply the mask
        rounded_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
        rounded_img.paste(img, mask=mask)

        buffer = BytesIO()
        rounded_img.save(buffer, format='PNG')

         # Get the binary data directly from the buffer
        pic_data = buffer.getvalue()
        # with open(r".\assets\admin_pic.jpg", 'rb') as read_data:
        #     pic_data = read_data.read()
        cursor.execute("""INSERT INTO AdminDetails (AdminID, AdminName, Email, Pass, img) 
                        VALUES ("9891","Shivam Raj Gupta", "guptashivam25oct@gmail.com", "shivam@123", ?)""", (pic_data,))

    connection.commit()
except sqlite3.Error as e:
    messagebox.showerror("Email Error", f"Failed to send email: {e}")

finally:
    cursor.close()
    connection.close()

# generating OTP
def generate_otp(is_admin, user_id):
    #generating 4 digit random string
    otp = "".join([str(random.randint(0, 9)) for _ in range(4)])

    from_mail = os.environ.get("GMail_ID") # hid the senders mail in Environment variable
    password = os.environ.get("GMail_Pass") # hid the senders mail password in Environment variable

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            #print(from_mail)
            server.login(from_mail, password)

            message = f"Subject: OTP Verification\n\nYour OTP is: {otp}"
            server.sendmail(from_mail, user_id, message)

    except Exception as e:
        messagebox.showerror("Email Error", f"Failed to send OTP email: {str(e)}")

    return otp, is_admin

# Making widgets reuseable

#button
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

# other button 
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
#Entry
class CustomEntry(ctk.CTkEntry):
    def __init__(self, master=None, placeholder_text="", **kwargs):
        super().__init__(
            master=master,
            height=38,
            width=230,
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
        self.geometry("500x600+610+35")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")
        self.title("Login")
        self.iconbitmap(r'.\assets\window_icon.ico')

        # Setting Background Image
        background_image = ctk.CTkImage(
            light_image=Image.open(r".\assets\bg_img.png").filter(ImageFilter.GaussianBlur(6)), 
            size=(500, 600)
        )
        #placing Background Image
        self.bg_label = ctk.CTkLabel(master=self, image=background_image, text="")
        self.bg_label.pack()

        #credit
        # myLabel = ctk.CTkLabel(master=self, text="Made by: Shivam Raj Gupta",
        #                        font=("Bookman Old Style", 25,'bold', 'italic', 'underline'),
        #                        fg_color="#8FD3EE",
        #                        bg_color="#8FD3EE",
        #                        text_color='#113C4D')
        # myLabel.place(x=70,y=560)

        # Initialize the Window frame
        self.window_frame = Window(self.bg_label, self)

class Window(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(master=parent, width=320, height=350, fg_color="#2E2F33", bg_color="#BDE4F7", corner_radius=22)
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

        # Setting win img
        win_img = ctk.CTkImage(Image.open(r".\assets\window_img.png"), size=(80, 80))
        # Create a label widget to hold the win image
        win_img_label = ctk.CTkLabel(master=self, image=win_img, text="")
        win_img_label.place(x=160, y=90, anchor=tk.CENTER)

        create_account_button = CustomButton(master=self, text="Create Account", command=CreateAccountWindow)
        create_account_button.place(x=50, y=170)

        login_button = CustomButton(master=self, text="Login", command=loginAccountWindow)
        login_button.place(x=50, y=240)

        # Setting Cross Icon on frame
        delete_window_Img = ctk.CTkImage(light_image=Image.open(r".\assets\delete_window.png"), size=(30, 30))
        delete_window_Img_label = ctk.CTkLabel(master=self, image=delete_window_Img, text="", fg_color="#2E2F33", cursor= "hand2")
        delete_window_Img_label.bind("<Button-1>",DeleteWindow)
        delete_window_Img_label.place(x=300, y=50, anchor="se")
        # n, ne, e, se, s, sw, w, nw, or center

        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

class Add_account_Window(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(master=parent, width=320, height=350, fg_color="#2E2F33", bg_color="#BDE4F7", corner_radius=22)
        self.app = app

        def AddAdmin():
            self.place_forget()
            self.app.add_admin_account_frame = Add_admin_account(self.app.bg_label, self.app)
            self.app.add_admin_account_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        def AddUser():
            self.place_forget()
            self.app.add_user_account_frame = Add_user_account(self.app.bg_label, self.app)
            self.app.add_user_account_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        def BackToWindow():
            self.place_forget()
            self.app.window_frame = Window(self.app.bg_label, self.app)
            self.app.window_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Setting win img
        add_user_img = ctk.CTkImage(Image.open(r".\assets\Add_Account.png"), size=(80, 80))
        
        # Create a label widget to hold the win image
        add_user_img_label = ctk.CTkLabel(master=self, image=add_user_img, text="")
        add_user_img_label.place(x=170, y=90, anchor=tk.CENTER)


        add_admin_account_button = CustomButton(master=self, text="Create Account as Admin", command=AddAdmin)
        add_admin_account_button.place(x=50, y=170)

        add_user_account_button = CustomButton(master=self, text="Create Account as User", command=AddUser)
        add_user_account_button.place(x=50, y=240)

        BackToWindow = OtherButton(master=self, text="Back", cursor="hand2", command=BackToWindow)
        BackToWindow.place(x=163, y=305, anchor = tk.CENTER)

        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

class login_Window(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(master=parent, width=320, height=350, fg_color="#2E2F33", bg_color="#BDE4F7", corner_radius=22)
        self.app = app

        def Admin_Login():
            self.place_forget()
            self.app.admin_login_frame = AdminLogin(self.app.bg_label, self.app)
            self.app.admin_login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        def User_Login():
            self.place_forget()
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

        login_user_button = CustomButton(master=self, text="Login as Student", command=User_Login)
        login_user_button.place(x=50, y=240)

        BackToWindow = OtherButton(master=self, text="Back", cursor="hand2", command=BackToWindow)
        BackToWindow.place(x=163, y=305, anchor = tk.CENTER)

        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

class Add_admin_account(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(master=parent, width=320, height=510, fg_color="#2E2F33", bg_color="#BDE4F7", corner_radius=22)
        self.app = app

        pic_path = tk.StringVar()
        pic_path.set('')

        def open_pic():
            path = askopenfilename()

            if path:
                # Open and resize the image using PIL
                img = Image.open(path).resize((100, 100))

                # Create a circular mask
                mask = Image.new("L", img.size, 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0) + img.size, fill=255)

                # Create a new image with transparency (RGBA) and apply the mask
                rounded_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
                rounded_img.paste(img, mask=mask)

                # Convert the rounded image to CTkImage
                ctk_img = ctk.CTkImage(rounded_img, size=(100, 100))
                pic_path.set(path)

                # Update the button with the rounded CTkImage
                img_button.configure(image=ctk_img)
                img_button.image = ctk_img  # Bind the image to prevent garbage collection

        # Functions
        def create():
            pic_data = b''
            if pic_path.get() != '':
                # Open the selected image
                img = Image.open(pic_path.get()).resize((135, 135))

                # Create a circular mask
                mask = Image.new("L", img.size, 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0) + img.size, fill=255)

                # Create a new image with transparency and apply the mask
                rounded_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
                rounded_img.paste(img, mask=mask)

                buffer = BytesIO()
                rounded_img.save(buffer, format='PNG')

                # Get the binary data directly from the buffer
                pic_data = buffer.getvalue()
            else:
                # If no custom image, load the default profile picture
                with open(r".\assets\profile_pic.png", 'rb') as read_data:
                    pic_data = read_data.read()


            admin_code = self.AdminCode_entry.get().strip()
            admin_id = self.AdminID_entry.get().strip()
            admin_name = self.Name_entry.get().lower().strip()
            email = self.email_entry.get().lower().strip()
            password = self.createPass_entry.get().strip()
            pic_data = pic_data

            if admin_code == '' or admin_id == '' or admin_name == '' or email == '' or password =='':
                messagebox.showerror("Error!!","All fields are required")
            elif admin_code != '1234':
                messagebox.showerror("Error!","Wrong Admin Code")
            elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                messagebox.showerror(message="Enter Valid Email ID")
            else:
                try:
                    conn = sqlite3.connect("database.db")
                    cursor = conn.cursor()
                    # Query to check if the user exist
                    query = "SELECT * FROM AdminDetails WHERE AdminID = ? OR Email = ?"
                    values = (admin_id, email)
                    cursor.execute(query, values)
                    record = cursor.fetchone()
                    #print(record)
                    if record and record[0] == admin_id:
                        messagebox.showerror("User Exist!",message="User with same ID already exist")
                    elif record and record[2] == email:
                        messagebox.showerror("User Exist!",message="User with same EMail already Exist")
                    else:
                        query = "INSERT INTO AdminDetails (AdminID, AdminName, Email, Pass, img) VALUES (?, ?, ?, ?, ?)"
                        values = (admin_id, admin_name, email, password, pic_data)
                        cursor.execute(query, values)
                        conn.commit()
                        # Show success message
                        messagebox.showinfo("Success!", "Admin has been added successfully.")
                        # Close cursor and connection
                        cursor.close()
                        conn.close()
                        self.place_forget()
                        self.app.admin_login_frame = AdminLogin(self.app.bg_label, self.app)
                        self.app.admin_login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}")

        def back_to_window():
            response = messagebox.askyesno("Confirmation", "Are you Sure you want to exit this window?")
            if response:
                self.place_forget()
                self.app.window_frame = Window(self.app.bg_label, self.app)
                self.app.window_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            else:
                messagebox.showinfo("Cancelled", "The action was cancelled.")

        add_pic_frm = ctk.CTkFrame(master=self, width = 110, height = 110, corner_radius=50)
        add_pic_frm.place(x=100, y=12)
        img_button = ctk.CTkButton(master=add_pic_frm, image=ctk.CTkImage(Image.open(r".\assets\profile.png"), size=(100, 100)),
                                   text="", fg_color= "#2E2F33", bg_color="#2E2F33", hover=None, cursor = "hand2", command=open_pic)
        img_button.pack()

        self.AdminCode_entry = CustomEntry(master=self, placeholder_text="Admin Code")
        self.AdminCode_entry.place(x=50, y=130)

        self.AdminID_entry = CustomEntry(master=self, placeholder_text="Admin ID")
        self.AdminID_entry.place(x=50, y=185)

        self.Name_entry = CustomEntry(master=self, placeholder_text="Full Name")
        self.Name_entry.place(x=50, y=240)

        self.email_entry = CustomEntry(master=self, placeholder_text="Email")
        self.email_entry.place(x=50, y=295)

        self.createPass_entry = CustomEntry(master=self, placeholder_text="Create Password", show='*')
        self.createPass_entry.place(x=50, y=350)

        self.show_hide_button = ctk.CTkButton(master=self, image=ctk.CTkImage(Image.open(r".\assets\eye-slash-solid.png"), size=(15, 15)),
                                            text="",
                                            width=10,
                                            border_width=0,
                                            hover=None,
                                            fg_color='transparent',
                                            cursor="hand2",
                                            command=lambda: show_hide(self.createPass_entry, self.show_hide_button)
                                            )
        self.show_hide_button.place(x=280, y=355)

        create_button = CustomButton(master=self, text="Create Account", command=create)
        create_button.place(x=50, y=420)

        back_to_window_button = OtherButton(master=self, text="Back to Window", command=back_to_window)
        back_to_window_button.place(x=163, y=480, anchor=tk.CENTER)

        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

class Add_user_account(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(master=parent, width=480, height=520, fg_color="#2E2F33", bg_color="#BDE4F7", corner_radius=22)
        self.app = app

        pic_path = tk.StringVar()
        pic_path.set('')

        def open_pic():
            path = askopenfilename()
            if path:
                # Open and resize the image using PIL
                img = Image.open(path).resize((135, 135))

                # Create a circular mask
                mask = Image.new("L", img.size, 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0) + img.size, fill=255)

                # Create a new image with transparency (RGBA) and apply the mask
                rounded_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
                rounded_img.paste(img, mask=mask)

                # Convert the rounded image to CTkImage
                ctk_img = ctk.CTkImage(rounded_img, size=(135, 135))
                pic_path.set(path)

                # Update the button with the rounded CTkImage
                img_button.configure(image=ctk_img)
                img_button.image = ctk_img  # Bind the image to prevent garbage collection

        # Functions
        def create_user():
            pic_data = b''
            if pic_path.get() != '':
                # Open the selected image
                img = Image.open(pic_path.get()).resize((135, 135))

                # Create a circular mask
                mask = Image.new("L", img.size, 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0) + img.size, fill=255)

                # Create a new image with transparency and apply the mask
                rounded_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
                rounded_img.paste(img, mask=mask)

                buffer = BytesIO()
                rounded_img.save(buffer, format='PNG')

                # Get the binary data directly from the buffer
                pic_data = buffer.getvalue()
            else:
                # If no custom image, load the default profile picture
                with open(r".\assets\profile_pic.png", 'rb') as read_data:
                    pic_data = read_data.read()

            stud_name = self.stud_name_entry.get().lower().strip()
            gender = combobox_var.get()
            age = self.age_entry.get()
            phone_no = self.phone_entry.get().strip()
            course = course_var.get()
            email = self.email_entry.get().lower().strip()
            password = self.createPass_entry.get().strip()
            pic_data = pic_data

            if stud_name == '' or gender == "Gender" or age == '' or phone_no == '' or course =='Course' or email=='' or password == '':
                messagebox.showerror("Error!!","All fields are required")
            elif len(phone_no) != 10:
                messagebox.showerror(message="Enter Valid phone number length\nExclude 0 or +91")
            elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                messagebox.showerror(message="Enter Valid Email ID")
            else:
                try:
                    conn = sqlite3.connect("database.db")
                    cursor = conn.cursor()
                    # Query to check if the user exist
                    query = "SELECT * FROM StudentDetails WHERE Email = ?"
                    values = (email,)
                    cursor.execute(query, values)
                    record = cursor.fetchone()
                    #print(record)
                    if record and record[6] == email:
                        messagebox.showwarning("User Exist!",message="User Already Exist")
                    else:
                        query = """INSERT INTO StudentDetails (StudentName, Gender, Age, Contact, Course, Email, Pass, img) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
                        values = (stud_name, gender, age, phone_no, course, email, password, pic_data)
                        cursor.execute(query, values)
                        conn.commit()
                        # Show success message
                        messagebox.showinfo("Success!", "User has been added successfully.")
                        # Close cursor and connection
                        cursor.close()
                        conn.close()
                        self.place_forget()
                        self.app.studentCard_frame = StudentCard(self.app.bg_label, self.app, email)
                        self.app.studentCard_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}")

        def back_to_window():
            response = messagebox.askyesno("Confirmation", "Are you Sure you want to exit this window?")
            if response:
                self.place_forget()
                self.app.window_frame = Window(self.app.bg_label, self.app)
                self.app.window_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            else:
                messagebox.showinfo("Cancelled", "The action was cancelled.")

        add_pic_frm = ctk.CTkFrame(master=self, width = 110, height = 110, corner_radius=50)
        add_pic_frm.place(x=180, y=12)
        img_button = ctk.CTkButton(master=add_pic_frm, image=ctk.CTkImage(Image.open(r".\assets\man.png"), size=(135, 135)),
                                   text="", fg_color= "#2E2F33", bg_color="#2E2F33", hover=None, cursor="hand2", command=open_pic)
        img_button.pack()

        self.stud_name_entry = CustomEntry(master=self, placeholder_text="Full Name")
        self.stud_name_entry.place(x=10, y=160)

        combobox_var = ctk.StringVar(value="Gender")
        gender_comboBox = ctk.CTkComboBox(master=self, values=["Male", "Female", "Other"], 
                                                height=38,
                                                width=220,
                                                corner_radius=20,
                                                border_width=0,
                                                fg_color="white",
                                                button_color="#1F6AA5",
                                                button_hover_color="#144870",
                                                text_color="black",
                                                font=("Century Gothic", 12, 'bold'),
                                                state= 'readonly',
                                                variable=combobox_var)
        gender_comboBox.place(x=250, y=160)

        self.age_entry = CustomEntry(master=self, placeholder_text="Age")
        self.age_entry.place(x=10, y=220)
    
        self.phone_entry = CustomEntry(master=self, placeholder_text="Phone Number")
        self.phone_entry.place(x=250, y=220)

        course_var = ctk.StringVar(value="Course")
        course_comboBox = ctk.CTkComboBox(master=self, values=["Python", "C++", "Java"], 
                                                height=38,
                                                width=220,
                                                corner_radius=20,
                                                border_width=0,
                                                fg_color="white",
                                                button_color="#1F6AA5",
                                                button_hover_color="#144870",
                                                text_color="#A4A6AC",
                                                font=("Century Gothic", 12, 'bold'),
                                                state= 'readonly',
                                                variable=course_var)
        course_comboBox.place(x=10, y=280)

        self.email_entry = CustomEntry(master=self, placeholder_text="Email")
        self.email_entry.place(x=250, y=280)

        self.createPass_entry = CustomEntry(master=self, placeholder_text="Create Password", show='*')
        self.createPass_entry.place(x=130, y=350)

        self.show_hide_button = ctk.CTkButton(master=self, image=ctk.CTkImage(Image.open(r".\assets\eye-slash-solid.png"), size=(15, 15)),
                                            text="",
                                            width=10,
                                            border_width=0,
                                            hover=None,
                                            fg_color='transparent',
                                            cursor="hand2",
                                            command=lambda: show_hide(self.createPass_entry, self.show_hide_button)
                                            )
        self.show_hide_button.place(x=360, y=355)

        create_button =CustomButton(master=self, text="Create Account", command=create_user)
        create_button.place(x=130, y=420)

        back_to_window_button = OtherButton(master=self, text="Back to window", command=back_to_window)
        back_to_window_button.place(x=240, y=480, anchor=tk.CENTER)

        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Center the frame

# Student Card
class StudentCard(ctk.CTkFrame):
    def __init__(self, parent, app, email_id):
        super().__init__(master=parent, width=420, height=520, fg_color="#2E2F33")
        self.app = app
        self.email_id = email_id
        #functions

        def save_card():
            # Prompt user to select save location and file name
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
            if save_path:
                # Get the bounding box of the widget
                x, y, width, height = self.winfo_rootx(), self.winfo_rooty(), self.winfo_width(), self.winfo_height()
                # Capture the screen area of the widget and save
                ImageGrab.grab(bbox=(x, y, x + width, y + height)).save(save_path)
                messagebox.showinfo(message="Student card saved")

        def DeleteWindow(event):
            # self.app.destroy()
            self.place_forget()
            self.app.window_frame = Window(self.app.bg_label, self.app)
            self.app.window_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        heading_label = ctk.CTkLabel(master=self, text="Student Card", font=("Century Gothic", 28, 'bold'))
        heading_label.place(x=100, y=22)

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM StudentDetails WHERE Email = ?", (self.email_id,))
            record = cursor.fetchone()
        except sqlite3.Error as e:
            messagebox.showerror(message=f"Database Error: {e}")
            #print(e)
        
        stud_id, stud_name, stud_gender, stud_age, stud_phone, stud_course, stud_email, img_data = (
            record[0], record[1].capitalize(), record[2].capitalize(), record[3],
            record[4], record[5].capitalize(), record[6], record[8]
        )
        # Convert BLOB data to an image
        img = Image.open(io.BytesIO(img_data)).resize((150, 150), Image.LANCZOS)
        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(135, 135))  # Convert to CTkImage
        label = ctk.CTkLabel(master=self, image=ctk_img, text="", fg_color="transparent")  # Set transparent color
        label.place(x=145, y=65)

        id_label = ctk.CTkLabel(self, text="Student ID: ", font=("Century Gothic", 18, 'bold'))
        name_label = ctk.CTkLabel(self, text="Name: ", font=("Century Gothic", 18, 'bold'))
        gender_label = ctk.CTkLabel(self, text="Gender: ", font=("Century Gothic", 18, 'bold'))
        age_label = ctk.CTkLabel(self, text="Age: ", font=("Century Gothic", 18, 'bold'))
        phone_label = ctk.CTkLabel(self, text="Phone No.: ", font=("Century Gothic", 18, 'bold'))
        course_label = ctk.CTkLabel(self, text="Course: ", font=("Century Gothic", 18, 'bold'))
        email_label = ctk.CTkLabel(self, text="Email: ", font=("Century Gothic", 18, 'bold'))
        
        id = ctk.CTkLabel(self, text=f"{stud_id}", font=("Century Gothic", 18))
        name = ctk.CTkLabel(self, text=f"{stud_name}", font=("Century Gothic", 18))
        gender = ctk.CTkLabel(self, text=f"{stud_gender}", font=("Century Gothic", 18))
        age = ctk.CTkLabel(self, text=f"{stud_age}", font=("Century Gothic", 18))
        phone = ctk.CTkLabel(self, text=f"{stud_phone}", font=("Century Gothic", 18))
        course = ctk.CTkLabel(self, text=f"{stud_course}", font=("Century Gothic", 18))
        email = ctk.CTkLabel(self, text=f"{stud_email}", font=("Century Gothic", 18))
        
        id_label.place(x=15, y = 230)
        name_label.place(x=15, y = 258)
        gender_label.place(x=15, y = 288)
        age_label.place(x=15, y = 318)
        phone_label.place(x=15, y = 348)
        course_label.place(x=15, y = 378)
        email_label.place(x=15, y = 408)
        
        id.place(x=130, y = 230)
        name.place(x=130, y = 258)
        gender.place(x=130, y = 288)
        age.place(x=130, y = 318)
        phone.place(x=130, y = 348)
        course.place(x=130, y = 378)
        email.place(x=130, y = 408)

        save_card_button = CustomButton(master=self, text="Save Card", command=save_card)
        save_card_button.place(x=105, y=455)

        # Setting Cross Icon on frame
        delete_window_Img = ctk.CTkImage(light_image=Image.open(r".\assets\delete_window.png"), size=(30, 30))
        delete_window_Img_label = ctk.CTkLabel(master=self, image=delete_window_Img, text="", fg_color="#2E2F33", cursor= "hand2")
        delete_window_Img_label.bind("<Button-1>",DeleteWindow)
        delete_window_Img_label.place(x=390, y=50, anchor="se")
        # n, ne, e, se, s, sw, w, nw, or center

        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

class AdminLogin(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(master=parent, width=320, height=350, fg_color="#2E2F33", bg_color="#BDE4F7", corner_radius=22)
        self.app = app

        # Functions
        def login():
            username = self.user_entry.get().lower().strip()
            password = self.pass_entry.get()

            if username == '' or password == '':
                messagebox.showerror("Error!!","All fields are required")
            else:
                try:
                    conn = sqlite3.connect("Database.db")
                    cursor = conn.cursor()

                    # Query to check if the user exist
                    query = "SELECT * FROM AdminDetails WHERE AdminID = ? OR Email = ?"
                    values = (username, username)
                    cursor.execute(query, values)
                    record = cursor.fetchone()
                    if record:
                        query = "SELECT * FROM AdminDetails WHERE (AdminID = ? OR Email = ?) AND Pass = ?"
                        values = (username, username, password)
                        cursor.execute(query, values)
                        result = cursor.fetchone()
                        if result:
                            messagebox.showinfo("Success!", "Login is Successful")
                            cursor.close()
                            conn.close()
                            self.app.withdraw()
                            import AdminDashboard
                            AdminDashboard.DashboardWindow(self.app,username)
                        else:
                            messagebox.showerror("Error!!",'Wrong Credentials')
                    else:
                        messagebox.showerror(message="User doesn't Exist! or Wrong Username")
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

        # Setting win img
        admin_login_img = ctk.CTkImage(Image.open(r".\assets\Admin_Login.png"), size=(80, 80))
        
        # Create a label widget to hold the win image
        admin_login_img_label = ctk.CTkLabel(master=self, image=admin_login_img, text="")
        admin_login_img_label.place(x=160, y=60, anchor=tk.CENTER)

        l1= ctk.CTkLabel(master= self, text = "Login as Admin", font=("Times New Roman", 22))
        l1.place(x=160, y=120, anchor = tk.CENTER)

        self.user_entry = CustomEntry(master=self, placeholder_text="AdminID or Email")
        self.user_entry.place(x=50, y=150)

        self.pass_entry = CustomEntry(master=self, placeholder_text="Password", show='*')
        self.pass_entry.place(x=50, y=210)

        self.show_hide_button = ctk.CTkButton(master=self, image=ctk.CTkImage(Image.open(r".\assets\eye-slash-solid.png"), size=(15, 15)),
                                            text="",
                                            width=10,
                                            border_width=0,
                                            hover=None,
                                            fg_color='transparent',
                                            cursor="hand2",
                                            command=lambda: show_hide(self.pass_entry, self.show_hide_button)
                                            )
        self.show_hide_button.place(x=280, y=215)

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
        super().__init__(master=parent, width=320, height=350, fg_color="#2E2F33", bg_color="#BDE4F7", corner_radius=22)
        self.app = app

        # Functions
        def login():
            username = self.user_entry.get().lower().strip()
            password = self.pass_entry.get()

            if username == '' or password == '':
                messagebox.showerror("Error!!","All fields are required")
            else:
                try:
                    conn = sqlite3.connect("Database.db")
                    cursor = conn.cursor()

                    # Query to check if the user exist
                    query = "SELECT * FROM StudentDetails WHERE StudentID = ? OR Email = ?"
                    values = (username, username)
                    cursor.execute(query, values)
                    record = cursor.fetchone()
                    if record:
                        query = "SELECT * FROM StudentDetails WHERE (StudentID = ? OR Email = ?) AND Pass = ?"
                        values = (username, username, password)
                        cursor.execute(query, values)
                        result = cursor.fetchone()
                        if result:
                            messagebox.showinfo("Success!", "Login is Successful")
                            cursor.close()
                            conn.close()
                            self.app.withdraw()  # Hide login window
                            import UserDashboard  # Import here to avoid circular import
                            UserDashboard.DashboardWindow(self.app, username)  # Pass 'self.app' as argument
                        else:
                            messagebox.showerror("Error!!",'Wrong Credentials')
                    else:
                        messagebox.showinfo(message="Incorrect Id or User doesn't Exist!")
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

        l1= ctk.CTkLabel(master= self, text = "Login as Student", font=("Times New Roman", 22))
        l1.place(x=160, y=125, anchor = tk.CENTER)

        self.user_entry = CustomEntry(master=self, placeholder_text="Student ID or Email")
        self.user_entry.place(x=50, y=150)

        self.pass_entry = CustomEntry(master=self, placeholder_text="Password", show='*')
        self.pass_entry.place(x=50, y=210)

        self.show_hide_button = ctk.CTkButton(master=self, image=ctk.CTkImage(Image.open(r".\assets\eye-slash-solid.png"), size=(15, 15)),
                                            text="",
                                            width=10,
                                            border_width=0,
                                            hover=None,
                                            fg_color='transparent',
                                            cursor="hand2",
                                            command=lambda: show_hide(self.pass_entry, self.show_hide_button)
                                            )
        self.show_hide_button.place(x=280, y=215)

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
        super().__init__(master=parent, width=320, height=350, fg_color="#2E2F33", bg_color="#BDE4F7", corner_radius=22)
        self.app = app
        self.is_admin = is_admin

        def Continue():
            self.user_id = self.email_entry.get().lower().strip()
            if self.user_id =='':
                messagebox.showerror("Error!","Please Enter EMail-ID")
            elif not re.match(r"[^@]+@[^@]+\.[^@]+", self.user_id):
                messagebox.showerror("Error!","Please Enter Valid EMail-ID")
            else:
                try:
                    conn = sqlite3.connect("database.db")
                    cursor = conn.cursor()

                    if self.is_admin:
                        # Query to check if the user exist
                        query = "SELECT * FROM AdminDetails WHERE Email = ?"
                    else:
                        query = "SELECT * FROM StudentDetails WHERE Email = ?"
                    values = (self.user_id,)
                    cursor.execute(query, values)
                    record = cursor.fetchone()
                    if self.is_admin:
                        if record and record[2] == self.user_id:
                            cursor.close()
                            conn.close()
                            otp, is_admin = generate_otp(self.is_admin, self.user_id)
                            self.place_forget()
                            self.app.Otp_entry_frame = OTPEntry(self.app.bg_label, self.app, otp, self.user_id, is_admin)
                            self.app.Otp_entry_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
                        else:
                            messagebox.showerror("Invalid User","User not found or incorrect Username")
                    elif record and record[6] == self.user_id:
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
        super().__init__(master=parent, width=320, height=350, fg_color="#2E2F33", bg_color="#BDE4F7", corner_radius=22)
        self.app = app

        self.user_id = user_id
        self.otp = otp
        self.is_admin = is_admin

        def verify_otp():
            input_opt = self.otp_entry.get().strip()
            if input_opt == self.otp and self.is_admin:
                messagebox.showinfo(message="OTP Verified")
                self.place_forget()
                self.app.reset_pass_frame = ResetPassword(self.app.bg_label, self.app, self.user_id, is_admin)
                self.app.reset_pass_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            elif input_opt == self.otp and self.is_admin == False:
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
        super().__init__(master=parent, width=320, height=350, fg_color="#2E2F33", bg_color="#BDE4F7", corner_radius=22)
        self.app = app

        self.user_id = user_id
        self.is_admin = is_admin

        def reset_password():
            passwrd = self.newPass_entry1.get().strip()
            passwrd_repeat = self.newPass_entry2.get().strip()

            if passwrd == '' or passwrd_repeat == '':
                messagebox.showerror("Error!", "Field is required")
            elif passwrd == passwrd_repeat:
                try:
                    conn = sqlite3.connect("database.db")
                    cursor = conn.cursor()
                    if is_admin:
                        # Update password in the database
                        query = "UPDATE AdminDetails SET Pass = ? WHERE Email = ?"
                    else:
                        query = "UPDATE StudentDetails SET pass = ? WHERE Email = ?"
                    values = (passwrd, self.user_id)
                    cursor.execute(query, values)
                    conn.commit()

                    # Verify the password update
                    if is_admin:
                        query = "SELECT * FROM AdminDetails WHERE Email = ? AND Pass = ?"
                    else:
                        query = "SELECT * FROM StudentDetails WHERE Email = ? AND Pass = ?"
    
                    values = (user_id, passwrd)
                    cursor.execute(query, values)
                    result = cursor.fetchone()
                    if self.is_admin:
                        if result and result[2] == self.user_id and result[3] == passwrd:
                            messagebox.showinfo(message="Password Successfully reset")
                            cursor.close()
                            conn.close()
                            self.place_forget()
                            self.app.admin_login_frame = AdminLogin(self.app.bg_label, self.app)
                            self.app.admin_login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
                        else:
                            messagebox.showerror(message="Password reset failed. Please try again.")
                    elif result and result[6] == self.user_id and result[7] == passwrd:
                        messagebox.showinfo(message="Password Successfully reset")
                        cursor.close()
                        conn.close()
                        self.place_forget()
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
                self.place_forget()
                self.app.login_frame = login_Window(self.app.bg_label, self.app)
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

        self.show_hide_button1 = ctk.CTkButton(master=self, image=ctk.CTkImage(Image.open(r".\assets\eye-slash-solid.png"), size=(15, 15)),
                                            text="",
                                            width=10,
                                            border_width=0,
                                            hover=None,
                                            fg_color='transparent',
                                            cursor="hand2",
                                            command=lambda: show_hide(self.newPass_entry1, self.show_hide_button1)
                                            )
        self.show_hide_button1.place(x=278, y=165)

        self.show_hide_button2 = ctk.CTkButton(master=self, image=ctk.CTkImage(Image.open(r".\assets\eye-slash-solid.png"), size=(15, 15)),
                                            text="",
                                            width=10,
                                            border_width=0,
                                            hover=None,
                                            fg_color='transparent',
                                            cursor="hand2",
                                            command=lambda: show_hide(self.newPass_entry2, self.show_hide_button2)
                                            )
        self.show_hide_button2.place(x=278, y=215)

        reset_button = CustomButton(master=self, text="Reset Password", command=reset_password)
        reset_button.place(x=50, y=260)

        cancel_button = OtherButton(master=self, text="Cancel", command=cancel)  
        cancel_button.place(x=163, y=320, anchor=tk.CENTER)

        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Center the frame

if __name__ == "__main__":
    main()