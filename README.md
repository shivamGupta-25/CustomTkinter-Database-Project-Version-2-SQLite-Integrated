# Student Desktop Application with User and Admin Dashboards

This GitHub repository contains the source code, assets, and resources for the project, along with a README file that provides an overview of its features and functionality.

## Table of Contents
- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Project Structure](#project-structure)
- [Features](#features)
  - [User Dashboard](#user-dashboard)
  - [Admin Dashboard](#admin-dashboard)
- [Tech Stack and Libraries](#tech-stack-and-libraries)
- [Code Modificaton You Need To Do Before Running The Code](#code-modificaton-you-need-to-do-before-running-the-code)
- [Project Demo](#project-demo)
  - [Part 1: Login System and User Dashboard Demonstration](#part-1-login-system-and-user-dashboard-demonstration)
  - [Part 2: Admin Dashboard Demonstration](#part-2-admin-dashboard-demonstration)
- [Screenshots](#screenshots)
  - [Login System and Password recovery](#login-system-and-password-recovery)
  - [Student Card](#student-card)
  - [Dashboard](#dashboard)
---

## Project Overview
This project is a Python-based desktop application featuring a secure login system with OTP authentication, user and admin dashboards, and an SQLite database for data management. The application provides a smooth, responsive interface for both students and administrators to manage data and perform essential tasks.

### Key Features
- **OTP-Based Password Recovery System**: Enhances security during password recovery for both User and Admin.
- **User Dashboard**: Allows students to access their profile, view their student card, update personal details and photo, manage security settings, and delete their account.
- **Admin Dashboard**: Empowers administrators to see summary of data, manage student data and send announcements.
- **SQLite Database Integration**: A local database setup, eliminating external dependencies and simplifying installation.
- **Responsive UI Transitions**: Seamless transitions between windows, avoiding common DPI and scaling issues.

---

## Project Structure
- **login_system.py**: Manages the login and OTP-based password reset functionality.
- **UserDashboard.py**: Contains user-specific functionalities such as profile viewing, downloading the student card, and security options.
- **AdminDashboard.py**: Provides admin tools for managing student data and sending announcements.

---

## Features

### User Dashboard
1. **Home**: View student details.
2. **Student Card**: Downloadable student card.
3. **Security**: Change password.
4. **Edit**: Edit profile information.
5. **Delete Account**: Permanently delete the account.
6. **Logout**: Log out of the dashboard.

### Admin Dashboard
1. **Home**: View a summary of no. of student in each Course.
2. **Manage**: Add, update, delete, and delete all student data with search functionalities.
3. **Announcement**: Send announcements to specific courses.
4. **Logout**: Log out of the admin dashboard.

---
## Tech Stack and Libraries
- **Python**
- **CustomTkinter**: For building the GUI.
- **SQLite**: For local database management.
- **smtplib**: To send OTP emails
- **random**: To generate OTPs for authentication.
- **tkinter.messagebox**: For pop-up messages.
- **tkinter.filedialog**: For saving files, such as downloading student cards.
---

---
## Code Modificaton You Need To Do Before Running The Code

**Replace:**  
from_mail : variable with your EmailID  
password : variable with your Email Password  
YouTube Video reference: https://youtu.be/IolxqkL7cD8?si=L-NxFHVgZeUUbvKQ
```
# login_system.py file

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

```

```
# AdminDashboard.py file

def send_email(subject, body, recipients):
    if not recipients:
        messagebox.showwarning("No Recipients", "No email addresses found for the selected courses.")
        return

    sender_email = os.environ.get("GMail_ID")
    sender_password = os.environ.get("GMail_Pass")

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    total_recipients = len(recipients)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)

            for idx, recipient in enumerate(recipients, start=1):
                # Reset progress bar for each email
                progress_var.set(0)
                status_label.configure(text=f"Sending to: {recipient}")

                # Send the email
                server.sendmail(sender_email, recipient, msg.as_string())

                # Update progress incrementally for each recipient
                progress_var.set((idx / total_recipients) * 100)
                time.sleep(0.05)  # Small delay for visualization
                progress_window.update_idletasks()

        progress_window.destroy()
        messagebox.showinfo("Success", "All announcements sent successfully!")

        # Reset UI elements after successful email sending
        subject_entry.delete(0, 'end')
        text_area.delete("0.0", "end")
        text_area.insert("0.0", "Write Announcement")
        for var in language_vars:
            var.set(False)
    except Exception as e:
        messagebox.showerror("Email Error", f"Failed to send email: {e}")
        progress_window.destroy()
```
---
## Project Demo
#### Part 1: Login System and User Dashboard Demonstration
https://www.linkedin.com/posts/shivam-raj-gupta_python-tkinter-sqlite-activity-7258851024658939904-38PY?utm_source=share&utm_medium=member_desktop

#### Part 2: Admin Dashboard Demonstration  
https://www.linkedin.com/posts/shivam-raj-gupta_python-tkinter-sqlite-activity-7259013994554769408-EaxW?utm_source=share&utm_medium=member_desktop

---

## Screenshots

### ***Login System and Password recovery:***  
![Login System and Password Recovery](https://github.com/user-attachments/assets/27d96077-608e-4d98-be82-dffb5d3ff7cd)


### ***Student Card:***  
![Student Card](https://github.com/user-attachments/assets/4daf16c7-0537-453a-a8f0-db3c1cf82975)

### ***Dashboard:***  
![Dashboard](https://github.com/user-attachments/assets/54e6a24b-eab3-4e20-825b-4f1f43e00820)



