import tkinter as tk
import customtkinter as ctk
from login_system import Window  # Import Window class from testinglogin.py

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

class DashboardWindow(ctk.CTkToplevel):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.geometry("500x500")
        self.title("Dashboard")

        ctk.CTkLabel(self, text="User Dashboard").pack(pady=20)

        # Logout button
        CustomButton(self, text="Logout", command=self.logout).pack(pady=20)

        # Bind the close button (X) to the close_app function
        self.protocol("WM_DELETE_WINDOW", self.close_app)

    def logout(self):
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
