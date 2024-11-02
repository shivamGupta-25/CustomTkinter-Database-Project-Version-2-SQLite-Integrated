import customtkinter as ctk
from login_system import Window  # Import Window class from testinglogin.py
import sqlite3
from PIL import Image
import io
from tkinter import messagebox
import threading
import time
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from tkinter import ttk

def AdminData(user_id):
    username = user_id
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = "SELECT * FROM AdminDetails WHERE AdminID = ? OR  Email = ?"
    values = (username,username)
    cursor.execute(query, values)
    data = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return data

# Function to send an email
def send_email(subject, body, recipients):

    exclude_emails = ['dummy1@gmail.com', 'dummy2@gmail.com', 'dummy3@gmail.com']  # Replace with the emails you want to exclude
    # Filter out the excluded emails from recipients
    recipients = [recipient for recipient in recipients if recipient not in exclude_emails]

    sender_email = os.environ.get("GMail_ID")  # Replace with your email
    sender_password = os.environ.get("GMail_Pass For Sending Mail")  # Replace with your email password

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)

            for idx, recipient in enumerate(recipients):
                # Update status for progress bar
                status_label.configure(text=f"Sending to: {recipient}")  # Update status label
                progress_var.set(0)  # Reset progress for each email
                progress_window.update_idletasks()  # Refresh the GUI

                # Send email
                server.sendmail(sender_email, recipient, msg.as_string())

                # Update progress incrementally
                for progress in range(10, 101, 10):  # Increment in steps to visualize progress
                    progress_var.set(progress)  # Update progress to percentage
                    time.sleep(0.1)  # Short delay to visualize the progress
                    progress_window.update_idletasks()  # Refresh the GUI

        # Close the progress window after sending all emails
        progress_window.destroy()
        messagebox.showinfo("Success", "All announcements sent successfully!")

    except Exception as e:
        #print(f"Failed to send email: {e}")
        messagebox.showerror("Email Error", f"Failed to send email: {e}")
        progress_window.destroy()  # Close the progress window in case of error

class CustomButton(ctk.CTkButton):
    def __init__(self, master, text, command=None, **kwargs):
        super().__init__(master, text=text, command=command, **kwargs)
        self.configure(
            font=("Century Gothic", 25),
            border_spacing=10,
            width=90, 
            corner_radius=18,
            fg_color="transparent",
            hover=None,
            cursor="hand2"
        )

class OtherButton(ctk.CTkButton):
    def __init__(self, master, text, command=None, **kwargs):
        super().__init__(master, text=text, command=command, **kwargs)
        self.configure(
            font=("Century Gothic", 18, 'bold'),
            border_spacing=10,
            width=220, 
            corner_radius=18,
            cursor = "hand2"
        )

class CustomEntry(ctk.CTkEntry):
    def __init__(self, master=None, placeholder_text="", **kwargs):
        super().__init__(
            master=master,
            height=38,
            width=205,
            placeholder_text=placeholder_text,
            placeholder_text_color="#A4A6AC",
            fg_color="white",
            text_color="black",
            font=("Century Gothic", 12, 'bold'),
            border_width=0,
            corner_radius=20,
            **kwargs
        )

class DashboardWindow(ctk.CTkToplevel):
    #def __init__(self, app, username):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.userid = 'guptashivam25oct@gmail.com'
        #self.userid = username
        #print(self.userid)
        self.geometry("930x580+100+50")
        self.title("Student Dashboard")
        self.resizable(False, False)
        #app.iconbitmap(r'.\assets\dashboard.ico')

        self.active_button = None
        self.button_refs = {}  # Dictionary to store button references

        dashboard_frame = ctk.CTkFrame(master=self, 
                                       #fg_color='green',
                                       width=920, height=570)
        dashboard_frame.grid_propagate(False)
        dashboard_frame.grid(row=0, column =0,padx=5, pady=5)

        options_frame = ctk.CTkFrame(master=dashboard_frame, width=910, height=158, bg_color='transparent')
        options_frame.grid_propagate(False)
        options_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # myLabel = ctk.CTkLabel(master=options_frame, text="Made by: Shivam Raj Gupta",text_color="#C0E6F8", font=("Bookman Old Style", 22,'bold', 'italic', 'underline'))
        # myLabel.place(x=580, y=18)

        # Center-aligning frame in parent
        options_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)  # Add weight to columns
        options_frame.grid_rowconfigure(1, weight=1)  # Add weight to row

        # Menu Label
        menu_label = ctk.CTkLabel(master=options_frame, text="Menu", font=("Century Gothic", 50, 'bold'))
        menu_label.grid(row=0, column=0, columnspan=4, sticky="n")

        # Navigation Buttons
        home_button = CustomButton(master=options_frame, text="Home", command=self.home)
        home_button.grid(row=1, column=0, sticky="ew")
        self.button_refs["home"] = home_button  # Store reference

        manage_button = CustomButton(master=options_frame, text="Manage", command=self.manage)
        manage_button.grid(row=1, column=1, sticky="ew")
        self.button_refs["manage"] = manage_button  # Store reference

        announcement_button = CustomButton(master=options_frame, text="Announcement", command=self.announcement)
        announcement_button.grid(row=1, column=2, sticky="ew")
        self.button_refs["announcement"] = announcement_button  # Store reference

        logout_button = CustomButton(master=options_frame, text="Logout", command=self.logout)
        logout_button.grid(row=1, column=3, sticky="ew")

        #Page frame where content will be displayed
        self.pages_frame = ctk.CTkFrame(master=dashboard_frame, width=910, height=395,
                                        #fg_color='blue'
                                        )
        self.pages_frame.grid_propagate(False)
        self.pages_frame.grid(row=1, column = 0)

        # Bind the close button (X) to the close_app function
        self.protocol("WM_DELETE_WINDOW", self.close_app)

        self.home()

    def clear_page(self):
        for widget in self.pages_frame.winfo_children():
            widget.destroy()

    def set_active_button(self, button_key):
        # Remove underline from the previously active button
        if self.active_button:
            self.active_button.configure(font=("Century Gothic", 25))

        # Set the current active button with underline
        self.active_button = self.button_refs[button_key]
        self.active_button.configure(font=("Century Gothic", 25,'bold', 'underline'))


    def home(self):
        self.clear_page()
        self.set_active_button("home")
        
        home_page_frame = ctk.CTkFrame(master=self.pages_frame, width=910, height=395, fg_color="transparent", bg_color="transparent", corner_radius=8)
        home_page_frame.grid_propagate(False)
        home_page_frame.grid(row=0, column=0)

        record = AdminData(self.userid)
        id = record[0]
        name = record[1]
        email = record[2]
        img_data = record[4]

        info_frame = ctk.CTkFrame(master=home_page_frame, width=898, height=170, corner_radius=8)
        info_frame.grid_propagate(False)
        info_frame.grid(row=0, column=0, padx=5, pady=5)

        pic_frame = ctk.CTkFrame(master=info_frame, width=150, height=158, fg_color="transparent", bg_color="transparent", corner_radius=8)
        pic_frame.grid_propagate(False)
        pic_frame.grid(row=0, column=0, padx=5, pady=5)

        img = Image.open(io.BytesIO(img_data))
        img = img.resize((150, 150), Image.LANCZOS)
        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(135, 135))
        
        label = ctk.CTkLabel(master=pic_frame, image=ctk_img, text="", fg_color="transparent")
        label.grid(row=0, column=0, padx=10, pady=10)

        admin_detail_frame = ctk.CTkFrame(master=info_frame, width=725, height=140, fg_color="transparent", bg_color="transparent", corner_radius=8)
        admin_detail_frame.grid_propagate(False)
        admin_detail_frame.grid(row=0, column=1, padx=5, pady=5)

        admin_detail_frame.grid_rowconfigure(0, weight=1)
        admin_detail_frame.grid_rowconfigure(1, weight=1)
        admin_detail_frame.grid_columnconfigure(0, weight=1)
        admin_detail_frame.grid_columnconfigure(1, weight=1)
        admin_detail_frame.grid_columnconfigure(2, weight=1)

        id_label = ctk.CTkLabel(master=admin_detail_frame, text="Admin ID", font=("Century Gothic", 18, 'bold'))
        id_label.grid(row=0, column=0, padx=10, sticky="nsew")
        name_label = ctk.CTkLabel(master=admin_detail_frame, text="Name", font=("Century Gothic", 18, 'bold'))
        name_label.grid(row=0, column=1, padx=10, sticky="nsew")
        email_label = ctk.CTkLabel(master=admin_detail_frame, text="Email", font=("Century Gothic", 18, 'bold'))
        email_label.grid(row=0, column=2, padx=10, sticky="nsew")

        id_display = ctk.CTkLabel(master=admin_detail_frame, text=f"{id}", font=("Century Gothic", 22))
        id_display.grid(row=1, column=0, padx=10, pady=(2, 5), sticky="nsew")
        name_display = ctk.CTkLabel(master=admin_detail_frame, text=f"{name}", font=("Century Gothic", 22))
        name_display.grid(row=1, column=1, padx=10, pady=(2, 5), sticky="nsew")
        email_display = ctk.CTkLabel(master=admin_detail_frame, text=f"{email}", font=("Century Gothic", 22))
        email_display.grid(row=1, column=2, padx=10, pady=(2, 5), sticky="nsew")

        data_frame = ctk.CTkFrame(master=home_page_frame, width=898, height=205, corner_radius=8)
        data_frame.grid_propagate(False)
        data_frame.grid(row=1, column=0, padx=5, pady=5)

        data_frame.columnconfigure((0, 1, 2), weight=1)
        data_frame.rowconfigure(0, weight=1)

        l1 = ctk.CTkLabel(master=data_frame, text="Number of Student by Course", font=("Times New Roman", 30, 'bold', 'underline'))
        l1.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        query = "SELECT COUNT(*), Course FROM StudentDetails GROUP BY Course"
        cursor.execute(query)
        records = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()

        if not records:
            no_data_label = ctk.CTkLabel(master=data_frame, text="No records found", font=("Century Gothic", 22, 'bold'))
            no_data_label.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        else:
            for index, (count, course) in enumerate(records):
                course_label = ctk.CTkLabel(master=data_frame, text=f"{course}", font=("Century Gothic", 22, 'bold', 'italic'))
                course_label.grid(row=1, column=index, padx=10, pady=10, sticky="nsew")

                count_stud_label = ctk.CTkLabel(master=data_frame, text=f"{count}", font=("Century Gothic", 25, 'bold'))
                count_stud_label.grid(row=2, column=index, padx=10, pady=10, sticky="nsew")

#-------------------------------------------------------------------------------------

    def manage(self):
        self.clear_page()
        self.set_active_button("manage")  # Use the key to set the active button

        def treeview_data():
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM StudentDetails")
            data = cursor.fetchall()
            conn.commit()
            cursor.close()
            conn.close()
            tree.delete(*tree.get_children())
            for student in data:
                tree.insert('',"end",values=student)
        
        def selection(event):
            if tree.winfo_exists():  # Check if the Treeview widget still exists
                selected_item = tree.selection()
                if selected_item:
                    row = tree.item(selected_item)['values']
                    #print(row)
                    clear()
                    idEntry.insert(0,row[0])
                    nameEntry.insert(0, row[1])
                    gender_var.set(row[2])
                    ageEntry.insert(0,row[3])
                    phoneEntry.insert(0,row[4])
                    course_var.set(row[5])
                    emailEntry.insert(0,row[6])
        def delete_student():
            if tree.winfo_exists():  # Check if the Treeview widget still exists
                selected_item = tree.selection()
            if not selected_item:
                messagebox.showerror("Error", message="Select data to delete")
            else:
                id = idEntry.get()
                conn = sqlite3.connect("database.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM StudentDetails WHERE StudentID = ?", (id,))
                conn.commit()
                cursor.close()
                conn.close()
                treeview_data()
                clear()
                messagebox.showerror(message="Data is deleted")

        def clear(value=False):
            if value:
                tree.selection_remove(tree.focus())
            idEntry.delete(0,'end')
            nameEntry.delete(0,'end')
            gender_var.set('Gender')
            ageEntry.delete(0,'end')
            phoneEntry.delete(0,'end')
            course_var.set('Course')
            emailEntry.delete(0,'end')

        def delete_all():
            result = messagebox.askyesno("Confirm", message="Do you really want to delete all the records?")
            if result:
                conn = sqlite3.connect("database.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM StudentDetails")
                conn.execute("INSERT INTO sqlite_sequence (name, seq) VALUES ('StudentDetails', 999);")
                conn.commit()
                cursor.close()
                conn.close()
                treeview_data()
                clear()
                messagebox.showerror("Error",message="All Data Deleted")

        def show_all():
            treeview_data()
            searchEntry.delete(0,'end')
            search_box.set('Search By')

        def search_student():
            option = search_box.get()
            if option == "ID":
                option = "StudentID"
            elif option == "Name":
                option ="StudentName"
            elif option == "Phone":
                option ="Contact"
            value = searchEntry.get()
            if searchEntry.get() == '':
                messagebox.showerror("Error", "Enter value to search")
            elif search_box.get() == "Search By":
                messagebox.showerror("Error", "Please, Select search Option")
            else:
                conn = sqlite3.connect("database.db")
                cursor = conn.cursor()
                query = f"SELECT * FROM StudentDetails WHERE {option} = ?"
                values = (value,)
                cursor.execute(query, values)
                record = cursor.fetchall()
                conn.commit()
                cursor.close()
                conn.close()
                tree.delete(*tree.get_children())
                for student in record:
                    tree.insert('',"end",values=student)


        def update_student():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showerror("Error",message="Select data to update")
            else:
                id = idEntry.get().strip()
                name = nameEntry.get().strip()
                gender = gender_var.get()
                age = ageEntry.get().strip()
                phone = phoneEntry.get().strip()
                course = course_var.get()
                email = emailEntry.get().lower().strip()

                conn = sqlite3.connect("database.db")
                cursor = conn.cursor()
                query = """UPDATE StudentDetails SET StudentName = ?,
                        Gender = ?, Age = ?, Contact = ?, Course = ?, Email = ? 
                        WHERE StudentID = ?"""
                values = (name, gender, age, phone, course, email, id)
                cursor.execute(query, values)
                conn.commit()
                cursor.close()
                conn.close()
                treeview_data()
                clear()
                messagebox.showinfo("Update",message="Data updated successfully")


        def add_student():
            id = idEntry.get().strip()
            name = nameEntry.get().strip()
            gender = gender_var.get()
            age = ageEntry.get().strip()
            phone = phoneEntry.get().strip()
            course = course_var.get()
            email = emailEntry.get().lower().strip()

            if id == '' or name == '' or gender =='Gender' or age == '' or phone =='' or course =='Course' or email =='':
                messagebox.showerror("Error",message="All fields are required")
            elif not email.endswith("@gmail.com"):
                messagebox.showerror("Error",message="Enter Valid Email")
            elif len(phone) != 10:
                messagebox.showerror("Error",message="Enter Valid Phone Number")
            elif not id.isnumeric():
                messagebox.showerror(message="Enter numeric ID")
            else:
                conn = sqlite3.connect("database.db")
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM StudentDetails WHERE StudentID = ? OR Email = ?", (id,email))
                record = cursor.fetchone()
                if record:
                    messagebox.showerror(message="User Exists with this StudentID or Email")
                else:
                    # since admin can't set custom image, loading the default profile picture and inserting it
                    with open(r".\assets\profile_pic.png", 'rb') as read_data:
                        pic_data = read_data.read()
                    query = """INSERT INTO StudentDetails (StudentID, StudentName, Gender, Age, Contact, Course, Email, img) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
                    values = (id, name, gender, age, phone, course, email, pic_data)
                    cursor.execute(query, values)
                    cursor.execute("UPDATE sqlite_sequence SET seq = ? WHERE name = 'StudentDetails'", (id,))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    messagebox.showinfo(message="Student Added Successfully")
                    clear()
                    treeview_data()
            

        manage_frame = ctk.CTkFrame(master=self.pages_frame,  width=910, height=395, 
                                    #fg_color="red", 
                                    bg_color="transparent", corner_radius=8)
        manage_frame.grid_propagate(False)
        manage_frame.grid(row=0, column=0)
        # l1 = ctk.CTkLabel(master=manage_frame, text="manage")
        # l1.grid(row=1, column =1)
        leftFrame = ctk.CTkFrame(master=manage_frame)
        leftFrame.grid(row=0, column =0, padx=5, pady=5)

        idLabel = ctk.CTkLabel(master=leftFrame, text = "ID", font =('arial', 18, 'bold'))
        idLabel.grid(row=0, column=0, padx=10, pady=10, sticky = 'w')
        idEntry = CustomEntry(leftFrame)
        idEntry.grid(row=0, column=1, padx=10)

        nameLabel = ctk.CTkLabel(master=leftFrame, text = "Name", font =('arial', 18, 'bold'))
        nameLabel.grid(row=1, column=0, padx=10, pady=10, sticky = 'w')
        nameEntry = CustomEntry(leftFrame)
        nameEntry.grid(row=1, column=1, padx=10)

        genderLabel = ctk.CTkLabel(master=leftFrame, text = "Gender", font =('arial', 18, 'bold'))
        genderLabel.grid(row=2, column=0, padx=10, pady=10, sticky = 'w')
        gender_var = ctk.StringVar(value="Gender")
        gender_comboBox = ctk.CTkComboBox(master=leftFrame, values=["Male", "Female", "Other"], 
                                                height=38,
                                                width=205,
                                                corner_radius=20,
                                                border_width=0,
                                                fg_color="white",
                                                button_color="#1F6AA5",
                                                button_hover_color="#144870",
                                                text_color="black",
                                                font =('arial', 18, 'bold'),
                                                state= 'readonly',
                                                variable=gender_var)
        gender_comboBox.grid(row=2, column =1, padx=10)

        ageLabel = ctk.CTkLabel(master=leftFrame, text = "Age", font =('arial', 18, 'bold'))
        ageLabel.grid(row=3, column=0, padx=10, pady=10, sticky = 'w')
        ageEntry = CustomEntry(leftFrame)
        ageEntry.grid(row=3, column=1, padx=10)

        phoneLabel = ctk.CTkLabel(master=leftFrame, text = "Phone", font =('arial', 18, 'bold'))
        phoneLabel.grid(row=4, column=0, padx=10, pady=10, sticky = 'w')
        phoneEntry = CustomEntry(leftFrame)
        phoneEntry.grid(row=4, column=1, padx=10)

        courseLabel = ctk.CTkLabel(master=leftFrame, text = "Course", font =('arial', 18, 'bold'))
        courseLabel.grid(row=5, column=0, padx=10, pady=10, sticky = 'w')

        course_var = ctk.StringVar(value="Course")
        course_comboBox = ctk.CTkComboBox(master=leftFrame, values=["Python", "C++", "Java"], 
                                                height=38,
                                                width=205,
                                                corner_radius=20,
                                                border_width=0,
                                                fg_color="white",
                                                button_color="#1F6AA5",
                                                button_hover_color="#144870",
                                                text_color="black",
                                                font =('arial', 18, 'bold'),
                                                state= 'readonly',
                                                variable=course_var)
        course_comboBox.grid(row=5, column =1, padx=10)

        emailLabel = ctk.CTkLabel(master=leftFrame, text = "Email", font =('arial', 18, 'bold'))
        emailLabel.grid(row=6, column=0, padx=10, pady=10, sticky = 'w')
        emailEntry = CustomEntry(leftFrame)
        emailEntry.grid(row=6, column=1, padx=10)

        rightFrame = ctk.CTkFrame(master=manage_frame)
        rightFrame.grid(row=0, column =1)

        search_box = ctk.CTkComboBox(master=rightFrame, values=["ID", "Name","Gender", "Age", "Phone", "Course", "Email"], state='readonly')
        search_box.grid(row=0, column=0)
        search_box.set('Search By')

        searchEntry = ctk.CTkEntry(master=rightFrame)
        searchEntry.grid(row=0, column=1)

        search_button = ctk.CTkButton(rightFrame, text="Search", width=100, command=search_student)
        search_button.grid(row=0, column=2)

        showall_button = ctk.CTkButton(rightFrame, text="Show All", width=100, command=show_all)
        showall_button.grid(row=0, column=3, pady=5)

        tree = ttk.Treeview(rightFrame, height=13)
        tree.grid(row=1, column =0, columnspan=4)

        tree['columns'] = ('ID', 'Name', 'Gender', 'Age', 'Contact', 'Course', 'Email')
        tree.heading('ID', text='ID',anchor="center")
        tree.heading('Name', text='Name',anchor="center")
        tree.heading('Gender', text='Gender',anchor="center")
        tree.heading('Age', text='Age',anchor="center")
        tree.heading('Contact', text='Contact',anchor="center")
        tree.heading('Course', text='Course',anchor="center")
        tree.heading('Email', text='Email',anchor="center")

        tree.config(show='headings')
        tree.column('ID', width=70)
        tree.column('Name', width=110)
        tree.column('Gender', width=80)
        tree.column('Age', width=50)
        tree.column('Contact', width=120)
        tree.column('Course', width=100)
        tree.column('Email', width=310)
        style = ttk.Style()
        style.configure('Treeview.Heading', font = ('arial', 15, 'bold'))
        style.configure('Treeview', font = ('arial', 15, 'bold'), rowheight = 32)
        
        scrollbar = ttk.Scrollbar(rightFrame, orient="vertical", command=tree.yview)
        scrollbar.grid(row=1, column=4, sticky='ns')

        tree.config(yscrollcommand=scrollbar.set)

        treeview_data()

        self.bind('<ButtonRelease>',selection)

        button_frame = ctk.CTkFrame(master=manage_frame, fg_color='#2B2B2B')
        button_frame.grid(row=1, column=0, columnspan = 2)

        new_button = ctk.CTkButton(button_frame, text="New Student", font=('arial', 15, 'bold'), width =170, corner_radius=15, command=lambda:clear(True))
        new_button.grid(row=0, column=0,pady=5)

        addbutton = ctk.CTkButton(button_frame, text="Add Student", font=('arial', 15, 'bold'), width =170, corner_radius=15, command=add_student)
        addbutton.grid(row=0, column=1, pady=5, padx=5)

        updatebutton = ctk.CTkButton(button_frame, text="Update Student", font=('arial', 15, 'bold'), width =170, corner_radius=15, command=update_student)
        updatebutton.grid(row=0, column=2, pady=5, padx=5)

        deletebutton = ctk.CTkButton(button_frame, text="Delete Student", font=('arial', 15, 'bold'), width =170, corner_radius=15, command=delete_student)
        deletebutton.grid(row=0, column=3, pady=5, padx=5)

        deleteallbutton = ctk.CTkButton(button_frame, text="Delete All", font=('arial', 15, 'bold'), width =170, corner_radius=15, command=delete_all)
        deleteallbutton.grid(row=0, column=4, pady=5, padx=5)

    def announcement(self):
        self.clear_page()
        self.set_active_button("announcement")  # Use the key to set the active button
        announcement_frame = ctk.CTkFrame(master=self.pages_frame,  width=910, height=395, bg_color="transparent")
        announcement_frame.grid_propagate(False)
        announcement_frame.grid(row=0, column=0)

        def announce():
            subject = subject_entry.get().strip()
            body = text_area.get("0.0", "end").strip()

            if not subject or not body:
                messagebox.showwarning("Input Error", "Please fill in both subject and announcement body.")
                return
            
            selected_courses = [languages[idx][0] for idx, var in enumerate(language_vars) if var.get()]
            #print(selected_courses)
            if not selected_courses:
                messagebox.showwarning("No Course Selected", "Please select at least one course to announce.")
                return
            # Fetching emails
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            all_emails=[]
            for course in selected_courses:
                cursor.execute("SELECT Email FROM StudentDetails WHERE Course = ?", (course,))
                emails = cursor.fetchall()
                # print(emails)
                for email_tuple in emails:
                    all_emails.append(email_tuple[0])
            #print(all_emails)
            cursor.close()
            conn.close()

            if all_emails:
                # Create a new window for the progress bar
                global progress_window
                progress_window = ctk.CTkToplevel(self)
                progress_window.title("Sending Emails")
                progress_window.geometry("400x150")  # Increased size for better visibility
                progress_window.attributes('-topmost', True)  # Ensure it stays on top

                global progress_var
                progress_var = ctk.DoubleVar()
                
                global status_label
                status_label = ctk.CTkLabel(master=progress_window, text="Starting...", font=("Century Gothic", 16))
                status_label.pack(pady=(10, 0))  # Add label at the top

                progress_bar = ctk.CTkProgressBar(master=progress_window, variable=progress_var, width=300)
                progress_bar.pack(pady=20, padx=20)

                # Reset progress bar before sending emails
                progress_var.set(0)  

                # Start sending emails in a new thread to avoid freezing the GUI
                threading.Thread(target=send_email, args=(subject, body, all_emails)).start()

                # Reset the subject entry and checkboxes after sending
                subject_entry.delete(0, 'end')  # Clear the subject entry
                text_area.delete("0.0", "end")  # Clear the text area
                text_area.insert("0.0", "Write Announcement")  # Reset the text area to default text
                for var in language_vars:  # Uncheck all checkboxes
                    var.set(False)
            else:
                messagebox.showwarning("No Emails", "No email addresses found for the selected courses.")

        frame1 = ctk.CTkFrame(master=announcement_frame, width=898, height=90,
                                   #fg_color='green',
                                   corner_radius=8)
        frame1.grid_propagate(False)
        frame1.grid(row=0, column =0,padx=5, pady=5)

        # Configure the frame to allow centering of the label
        frame1.rowconfigure(0, weight=1)
        frame1.columnconfigure(0, weight=1)

        l1 = ctk.CTkLabel(master=frame1, text="Announcement",font=("Century Gothic", 50,'italic'))
        l1.grid(row=0, column =0,padx=10, pady=10)

        frame2 = ctk.CTkFrame(master=announcement_frame, width=898, height=285,
                                  #fg_color='blue',
                                   corner_radius=8)
        frame2.grid_propagate(False)
        frame2.grid(row=1, column =0, padx=5, pady=5)

        sectionframe1 = ctk.CTkFrame(master=frame2, width=449, height=275,
                                  #fg_color='green',
                                   corner_radius=8)
        sectionframe1.grid_propagate(False)
        sectionframe1.grid(row=0, column=0, padx=5, pady=5)

        # Configure the rows and columns for centering
        sectionframe1.rowconfigure(0, weight=1)
        sectionframe1.rowconfigure(1, weight=1)
        sectionframe1.columnconfigure(0, weight=1)

        subject_entry = CustomEntry(master=sectionframe1, placeholder_text="Subject")
        subject_entry.grid(row=0, column=0,padx=10, pady=10, sticky="nsew")

        text_area = ctk.CTkTextbox(master=sectionframe1,
                                    corner_radius=8,
                                    border_spacing=10,
                                    text_color="black",
                                    font=("Century Gothic", 18),
                                    fg_color='white',
                                    activate_scrollbars = True,
                                )
        text_area.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        text_area.insert("0.0", "Write Announcement")

        sectionframe2 = ctk.CTkFrame(master=frame2, width=425, height=275,
                                  #fg_color='green',
                                   corner_radius=8)
        sectionframe2.grid_propagate(False)
        sectionframe2.grid(row=0, column=1, padx=5, pady=5)

        l2 = ctk.CTkLabel(master=sectionframe2, text= "Select Course to Announce",
                          font=("Century Gothic", 22)
                          )
        l2.grid(row=0, column=0, padx=75, pady=10)

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        query = "SELECT DISTINCT(Course) FROM StudentDetails"
        cursor.execute(query)
        languages = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()

        language_vars = []
        for idx, language in enumerate(languages,start=1):
            var = ctk.BooleanVar()  # Create a BooleanVar for each checkbox
            language_vars.append(var)  # Store the BooleanVar for later use
            checkbox = ctk.CTkCheckBox(master=sectionframe2, text=language[0], variable=var, font=("Century Gothic", 18))
            checkbox.grid(row=idx, column=0, sticky="w", padx=30, pady=12)  # Use grid for positioning

        announce_btn = OtherButton(master=sectionframe2, text="Send Announcement", command=announce)
        announce_btn.grid(row=5, column=0, padx=75, pady=10)

    def logout(self):
        answer = messagebox.askquestion(message="Are you sure you want to logout?")
        if answer == 'yes':
            self.destroy()  # Close the dashboard window
            self.app.deiconify()  # Show the main application window (login)
            Window(self.app.bg_label, self.app)  # Reopen the login window

    def close_app(self):
        self.app.destroy()  # Close the main application completely

if __name__ == "__main__":
    # Initialize the main application root
    app = ctk.CTk()  
    app.withdraw()  # Hide the root window
    
    # Show DashboardWindow directly
    dashboard = DashboardWindow(app)
    app.mainloop()
