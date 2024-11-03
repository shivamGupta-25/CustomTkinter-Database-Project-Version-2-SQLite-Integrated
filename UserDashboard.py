import tkinter as tk
import customtkinter as ctk
from login_system import Window, UserLogin  # Import Window class from testinglogin.py
import sqlite3
from PIL import Image, ImageGrab, ImageDraw
import io
from tkinter import messagebox, filedialog
from tkinter.filedialog import askopenfilename
from io import BytesIO

def Data(user_id):
    username = user_id
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = "SELECT * FROM StudentDetails WHERE StudentID = ? OR  Email = ?"
    values = (username,username)
    cursor.execute(query, values)
    data = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return data

class CustomButton(ctk.CTkButton):
    def __init__(self, master, text, command=None, **kwargs):
        super().__init__(master, text=text, command=command, **kwargs)
        self.configure(
            font=("Century Gothic", 15, 'bold'),
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

class DashboardWindow(ctk.CTkToplevel):
    def __init__(self, app, username):
    #def __init__(self, app):
        super().__init__()
        self.app = app
        #self.userid = '1000'
        self.userid = username
        #print(self.userid)
        self.geometry("500x410+650+200") #500x410 #For Window # 500x440 if credit label is present
        self.title("Student Dashboard")
        self.resizable(False, False)
        #app.iconbitmap(r'.\assets\dashboard.ico')
        #print(font.families())

        # # Credit label
        # myLabel = ctk.CTkLabel(master=self, text="Made by: Shivam Raj Gupta",text_color="#C0E6F8", font=("Bookman Old Style", 25,'bold', 'italic', 'underline'))
        # myLabel.pack(side = tk.BOTTOM)

        self.active_button = None
        self.button_refs = {}  # Dictionary to store button references

        dashboard_frame = ctk.CTkFrame(master=self)
        dashboard_frame.pack(pady=5)
        dashboard_frame.pack_propagate(False)
        dashboard_frame.configure(width=480, height=400) #580

        options_frame = ctk.CTkFrame(master=dashboard_frame, width=150, height=390)
        options_frame.place(x=5, y=5)

        menu_label = ctk.CTkLabel(master=options_frame, text="Menu", font=("Century Gothic", 30, 'bold'))
        menu_label.place(x=30, y=20)

        # Navigation Buttons
        home_button = CustomButton(master=options_frame, text="Home", command=self.home_page)
        home_button.place(x=-4,y=80)
        self.button_refs["home"] = home_button  # Store reference

        student_card_button = CustomButton(master=options_frame, text="Student Card", command=self.studentCard_page)
        student_card_button.place(y=130)
        self.button_refs["student_card"] = student_card_button  # Store reference

        security_button = CustomButton(master=options_frame, text="Security", command=self.security_page)
        security_button.place(y=180)
        self.button_refs["security"] = security_button  # Store reference

        edit_data_button = CustomButton(master=options_frame, text="Edit Data", command=self.editData_page)
        edit_data_button.place(y=230)
        self.button_refs["edit_data"] = edit_data_button  # Store reference

        delete_account_button = CustomButton(master=options_frame, text="Delete Account", command=self.deleteAcc_page)
        delete_account_button.place(y=280)
        self.button_refs["delete_account"] = delete_account_button  # Store reference

        logout_button = ctk.CTkButton(master=options_frame,
                                      text="Logout",    
                                      font=("Century Gothic", 15, 'bold'),
                                      fg_color="#292929",
                                      #border_spacing=10,
                                      width=80, 
                                      height=50,
                                      corner_radius=50,
                                      hover_color="#242424",
                                      cursor="hand2",
                                      command=self.logout)

        logout_button.place(x=24,y=330)

        # Page frame where content will be displayed
        self.pages_frame = ctk.CTkFrame(master=dashboard_frame, width=318, height=390)
        self.pages_frame.place(x=158, y=5)

        # Bind the close button (X) to the close_app function
        self.protocol("WM_DELETE_WINDOW", self.close_app)

        self.home_page()

    def clear_page(self):
        for widget in self.pages_frame.winfo_children():
            widget.destroy()

    def set_active_button(self, button_key):
        if self.active_button:
            # Reset previous button text to normal (remove underline)
            self.active_button.configure(font=("Century Gothic", 15, 'bold'))
            
        # Set active button text to underlined
        self.active_button = self.button_refs[button_key]
        self.active_button.configure(font=("Century Gothic", 15, 'bold', 'underline'))

    
    def home_page(self):
        self.clear_page()
        self.set_active_button("home")  # Use the key to set the active button
        home_page_frame = ctk.CTkFrame(master=self.pages_frame, width=318, height=390, fg_color="transparent", bg_color="transparent", corner_radius=8)
        home_page_frame.pack()

        record = Data(self.userid)
        stud_id = record[0]
        stud_name = record[1].capitalize()
        stud_gender = record[2].capitalize()
        stud_age = record[3]
        stud_phone = record[4]
        stud_course = record[5].capitalize()
        stud_email = record[6]
        img_data = record[8]
        # Convert BLOB data to an image
        img = Image.open(io.BytesIO(img_data))
        img = img.resize((150, 150), Image.LANCZOS)  # Resize with LANCZOS for quality downsampling
        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(135, 135))  # Convert to CTkImage
        
        label = ctk.CTkLabel(master=home_page_frame, image=ctk_img, text="", fg_color="transparent")  # Set transparent color
        label.place(x=10, y=10)

        id_label = ctk.CTkLabel(master=home_page_frame, text="Student ID: ", font=("Century Gothic", 18, 'bold'))
        name_label = ctk.CTkLabel(master=home_page_frame, text="Hi!", font=("Century Gothic", 18, 'bold'))
        name_label2 = ctk.CTkLabel(master=home_page_frame, text="Name: ", font=("Century Gothic", 18, 'bold'))
        gender_label = ctk.CTkLabel(master=home_page_frame, text="Gender: ", font=("Century Gothic", 18, 'bold'))
        age_label = ctk.CTkLabel(master=home_page_frame, text="Age: ", font=("Century Gothic", 18, 'bold'))
        phone_label = ctk.CTkLabel(master=home_page_frame, text="Phone No.: ", font=("Century Gothic", 18, 'bold'))
        course_label = ctk.CTkLabel(master=home_page_frame, text="Course: ", font=("Century Gothic", 18, 'bold'))
        email_label = ctk.CTkLabel(master=home_page_frame, text="Email: ", font=("Century Gothic", 18, 'bold'))
        
        id = ctk.CTkLabel(master=home_page_frame, text=f"{stud_id}", font=("Century Gothic", 12))
        name = ctk.CTkLabel(master=home_page_frame, text=f"{stud_name}", font=("Century Gothic", 18, "bold", "italic", "underline"))
        name2 = ctk.CTkLabel(master=home_page_frame, text=f"{stud_name}", font=("Century Gothic", 12))
        gender = ctk.CTkLabel(master=home_page_frame, text=f"{stud_gender}", font=("Century Gothic", 12))
        age = ctk.CTkLabel(master=home_page_frame, text=f"{stud_age}", font=("Century Gothic", 12))
        phone = ctk.CTkLabel(master=home_page_frame, text=f"{stud_phone}", font=("Century Gothic", 12))
        course = ctk.CTkLabel(master=home_page_frame, text=f"{stud_course}", font=("Century Gothic", 12))
        email = ctk.CTkLabel(master=home_page_frame, text=f"{stud_email}", font=("Century Gothic", 12))
        
        
        id_label.place(x=15, y = 170)
        name_label.place(x=150, y= 50)
        name_label2.place(x=15, y= 200)
        gender_label.place(x=15, y = 230)
        age_label.place(x=15, y = 260)
        phone_label.place(x=15, y = 290)
        course_label.place(x=15, y = 320)
        email_label.place(x=15, y = 350)
        
        
        id.place(x=130, y = 170)
        name.place(x=150, y = 80)
        name2.place(x=130, y = 200)
        gender.place(x=130, y = 230)
        age.place(x=130, y = 260)
        phone.place(x=130, y = 290)
        course.place(x=130, y = 320)
        email.place(x=130, y = 350)


    def studentCard_page(self):
        self.clear_page()
        self.set_active_button("student_card")  # Use the key to set the active button
        student_card_frame = ctk.CTkFrame(master=self.pages_frame, width=318, height=390, fg_color="transparent", bg_color="transparent", corner_radius=8)
        student_card_frame.pack()
        # l1 = ctk.CTkLabel(master=student_card_frame, text="StudentCardPage")
        # l1.place(x=100, y=200)

        def save_card(event):
            # Prompt user to select save location and file name
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
            if save_path:
                # Get the bounding box of the parent frame
                x = self.pages_frame.winfo_rootx()
                y = self.pages_frame.winfo_rooty()
                width = self.pages_frame.winfo_width()
                height = self.pages_frame.winfo_height()
                
                # Capture the screen area of the parent frame
                img = ImageGrab.grab(bbox=(x, y, x + width, y + height))
                
                # Save the image
                img.save(save_path)
                messagebox.showinfo(message="Student card saved")


        # heading_label = ctk.CTkLabel(master=student_card_frame, text="Student Card", font=("Century Gothic",12))
        # heading_label.place(x=170, y=22)

        record = Data(self.userid)
        stud_id = record[0]
        stud_name = record[1].capitalize()
        stud_gender = record[2].capitalize()
        stud_age = record[3]
        stud_phone = record[4]
        stud_course = record[5].capitalize()
        stud_email = record[6]
        img_data = record[8]
        # Convert BLOB data to an image
        img = Image.open(io.BytesIO(img_data))
        img = img.resize((150, 150), Image.LANCZOS)  # Resize with LANCZOS for quality downsampling
        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(135, 135))  # Convert to CTkImage
        label = ctk.CTkLabel(master=student_card_frame, image=ctk_img, text="", fg_color="transparent")  # Set transparent color
        label.place(x=90, y=10)

        id_label = ctk.CTkLabel(master=student_card_frame, text="Student ID: ", font=("Century Gothic", 18, 'bold'))
        name_label = ctk.CTkLabel(master=student_card_frame, text="Name: ", font=("Century Gothic", 18, 'bold'))
        gender_label = ctk.CTkLabel(master=student_card_frame, text="Gender: ", font=("Century Gothic", 18, 'bold'))
        age_label = ctk.CTkLabel(master=student_card_frame, text="Age: ", font=("Century Gothic", 18, 'bold'))
        phone_label = ctk.CTkLabel(master=student_card_frame, text="Phone No.: ", font=("Century Gothic", 18, 'bold'))
        course_label = ctk.CTkLabel(master=student_card_frame, text="Course: ", font=("Century Gothic", 18, 'bold'))
        email_label = ctk.CTkLabel(master=student_card_frame, text="Email: ", font=("Century Gothic", 18, 'bold'))
        
        id = ctk.CTkLabel(master=student_card_frame, text=f"{stud_id}", font=("Century Gothic", 12))
        name = ctk.CTkLabel(master=student_card_frame, text=f"{stud_name}", font=("Century Gothic", 12))
        gender = ctk.CTkLabel(master=student_card_frame, text=f"{stud_gender}", font=("Century Gothic", 12))
        age = ctk.CTkLabel(master=student_card_frame, text=f"{stud_age}", font=("Century Gothic", 12))
        phone = ctk.CTkLabel(master=student_card_frame, text=f"{stud_phone}", font=("Century Gothic", 12))
        course = ctk.CTkLabel(master=student_card_frame, text=f"{stud_course}", font=("Century Gothic", 12))
        email = ctk.CTkLabel(master=student_card_frame, text=f"{stud_email}", font=("Century Gothic", 12))
        
        
        id_label.place(x=15, y = 170)

        name_label.place(x=15, y= 200)
        gender_label.place(x=15, y = 230)
        age_label.place(x=15, y = 260)
        phone_label.place(x=15, y = 290)
        course_label.place(x=15, y = 320)
        email_label.place(x=15, y = 350)
        
        
        id.place(x=130, y = 170)

        name.place(x=130, y = 200)
        gender.place(x=130, y = 230)
        age.place(x=130, y = 260)
        phone.place(x=130, y = 290)
        course.place(x=130, y = 320)
        email.place(x=130, y = 350)

        download_Img = ctk.CTkImage(light_image=Image.open(r".\assets\downloading.png"), size=(30, 30))
        download_Img_label = ctk.CTkLabel(master=student_card_frame, image=download_Img, text="", cursor= "hand2")
        download_Img_label.bind("<Button-1>",save_card)
        download_Img_label.place(x = 260, y=22,  anchor="nw")

    def security_page(self):
        self.clear_page()
        self.set_active_button("security")  # Use the key to set the active button
        security_page_frame = ctk.CTkFrame(master=self.pages_frame, width=318, height=390, fg_color="transparent", bg_color="transparent", corner_radius=8)
        security_page_frame.pack()
        l1 = ctk.CTkLabel(master=security_page_frame, text="Change Password", font=("Century Gothic", 22, 'bold', "underline"))
        l1.place(x=65, y=20)

        def ChangePassword():
            record = Data(self.userid)[7]
            currnt_pass = current_pass_entry.get().strip()
            new_pass = new_pass_entry.get().strip()
            if currnt_pass == '' or new_pass == '':
                messagebox.showerror(message="All Fields are required!")
            elif currnt_pass == record:
                #print("shivam")
                conn = sqlite3.connect('Database.db')
                cursor = conn.cursor()
                query = "UPDATE StudentDetails SET Pass = ? WHERE (StudentID = ? OR Email = ?)"
                values = (new_pass, self.userid, self.userid)
                cursor.execute(query, values)
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo(message="Password Changed!")
                self.destroy()  # Close the dashboard window
                self.app.deiconify()  # Show the main application window (login)
                UserLogin(self.app.bg_label, self.app)  # Reopen the login window
            else:
                messagebox.showerror(message="Current Pass doesn't Match")


        current_pass_entry = CustomEntry(master=security_page_frame, placeholder_text="Current Password")
        current_pass_entry.place(x=50, y=100)

        new_pass_entry = CustomEntry(master=security_page_frame, placeholder_text="New Password")
        new_pass_entry.place(x=50, y=180)

        change_pass_button = ctk.CTkButton(master=security_page_frame, text="Change Password",height=35, font=("Century Gothic", 12, 'bold'), command=ChangePassword)
        change_pass_button.place(x=90, y= 260)

    def editData_page(self):
        self.clear_page()
        self.set_active_button("edit_data")  # Use the key to set the active button
        edit_data_frame = ctk.CTkFrame(master=self.pages_frame, width=318, height=390, fg_color="transparent", bg_color="transparent", corner_radius=8)
        edit_data_frame.pack()
        # l1 = ctk.CTkLabel(master=edit_data_frame, text="Edit Data")
        # l1.place(x=100, y=200)

        record = Data(self.userid)
        #print(record)

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
        def update():
            stud_name = self.stud_name_entry.get().lower().strip()
            age = self.age_entry.get()
            phone_no = self.phone_entry.get().strip()
            gender = combobox_var.get()
            email = self.email_entry.get().lower().strip()

            if stud_name=='' or age =='' or phone_no=='' or gender=='' or email=='':
                messagebox.showerror(message="All fields are requied")
            elif not email.endswith("@gmail.com"):
                messagebox.showerror(message="Enter Valid EMailID")
            elif len(phone_no) != 10:
                messagebox.showerror(message="Enter Valid Phone Number")
            else:
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
                    pic_data = pic_data
                    conn = sqlite3.connect("database.db")
                    cursor = conn.cursor()
                    query = "UPDATE StudentDetails SET img = ? WHERE Email = ? OR StudentID = ?"
                    values = (pic_data, self.userid, self.userid)
                    cursor.execute(query, values)
                    conn.commit()
                    cursor.close()
                    conn.close()
                    # messagebox.showinfo(message="Data Added Successfully")

                conn = sqlite3.connect("database.db")
                cursor = conn.cursor()
                # query = "SELECT Email FROM StudentDetails where Email = ?"
                # values=(email,)
                # cursor.execute(query, values)
                record = cursor.fetchone()
                # print(record)
                # if record and record[0] == email:
                #     messagebox.showerror(message="Email already exist")
                # else:
                query = "UPDATE StudentDetails SET StudentName = ?, Gender = ?, Age = ?, Contact = ?, Email = ? WHERE Email = ? OR StudentID = ?"
                values = (stud_name, gender, age, phone_no, email, self.userid, self.userid)
                cursor.execute(query, values)
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo(message="Data Added Successfully")
                # print(stud_name)
                # print(age)
                # print(phone_no)
                # print(gender)
                # print(email)

        add_pic_frm = ctk.CTkFrame(master=edit_data_frame, width = 110, height = 110, corner_radius=50)
        add_pic_frm.place(y=12)
        img_button = ctk.CTkButton(master=add_pic_frm, image=ctk.CTkImage(Image.open(BytesIO(record[8])), size=(135, 135)),
                                   text="", fg_color= "#333333", bg_color="#333333", hover=None, cursor="hand2", command=open_pic)
        img_button.pack()

        self.stud_name_entry = CustomEntry(master=edit_data_frame, placeholder_text="Full Name")
        self.stud_name_entry.place(x = 5, y=155)
        self.stud_name_entry.insert(tk.END,record[1])

        self.age_entry = CustomEntry(master=edit_data_frame, placeholder_text="Age")
        self.age_entry.place(x=5, y=203)
        self.age_entry.insert(tk.END,record[3])
    
        self.phone_entry = CustomEntry(master=edit_data_frame, placeholder_text="Phone Number")
        self.phone_entry.place(x = 5, y=251)
        self.phone_entry.insert(tk.END,record[4])

        combobox_var = ctk.StringVar(value="Gender")
        gender_comboBox = ctk.CTkComboBox(master=edit_data_frame, values=["Male", "Female", "Other"], 
                                                height=38,
                                                width=220,
                                                corner_radius=20,
                                                border_width=0,
                                                fg_color="white",
                                                button_color="#1F6AA5",
                                                button_hover_color="#144870",
                                                text_color="black",
                                                font=("Century Gothic", 12, 'bold'),
                                                state='readonly',
                                                variable=combobox_var)
        gender_comboBox.place(x=5, y=299)
        combobox_var.set(record[2])

        self.email_entry = CustomEntry(master=edit_data_frame, placeholder_text="Email")
        self.email_entry.place(x = 5, y=347)
        self.email_entry.insert(tk.END,record[6])

        update_button = ctk.CTkButton(master=edit_data_frame, text="Update",font=("Century Gothic", 18, 'bold'),
                                      height=35, corner_radius=22, command=update)
        update_button.place(x=170,y=60)

    def deleteAcc_page(self):
        self.clear_page()
        self.set_active_button("delete_account")  # Use the key to set the active button
        delete_acc_frame = ctk.CTkFrame(master=self.pages_frame, width=318, height=390, fg_color="transparent", bg_color="transparent", corner_radius=8)
        delete_acc_frame.pack()

        def del_account():
            answer = messagebox.askquestion(message="Are you sure you want to delete your account?")
            if answer == "yes":
                conn = sqlite3.connect('Database.db')
                cursor = conn.cursor()
                query = "DELETE FROM StudentDetails WHERE StudentID = ? OR Email = ?"
                values = (self.userid, self.userid)
                cursor.execute(query, values)
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo(message="Account Deleted!")
                self.destroy()  # Close the dashboard window
                self.app.deiconify()  # Show the main application window (login)
                Window(self.app.bg_label, self.app)  # Reopen the login window
            else:
                messagebox.showinfo(message="Action Cancelled")
        l1 = ctk.CTkLabel(master=delete_acc_frame, text="⚠️ Delete Account",
                          #fg_color="#891818",
                          height=40,
                          width=40,
                          corner_radius=18, 
                          font=("Century Gothic", 22, 'bold', 'italic', 'underline'))
        l1.place(x=35, y=40)
        del_acc_button = ctk.CTkButton(master=delete_acc_frame, 
                                       fg_color="#9F1A1A",
                                       hover_color="#891818",
                                       text="Delete Account",height=45, width=40 ,corner_radius=22, font=("Century Gothic", 22, 'bold'), command=del_account)
        del_acc_button.place(x=50, y= 160)

    def logout(self):
        answer = messagebox.askquestion(message="Are you sure you want to logout?")
        if answer == 'yes':
            self.destroy()  # Close the dashboard window
            self.app.deiconify()  # Show the main application window (login)
            Window(self.app.bg_label, self.app)  # Reopen the login window

    def close_app(self):
        self.app.destroy()  # Close the main application completely

# if __name__ == "__main__":
#     # Initialize the main application root
#     app = ctk.CTk()  
#     app.withdraw()  # Hide the root window
    
#     # Show DashboardWindow directly
#     dashboard = DashboardWindow(app)
#     app.mainloop()
