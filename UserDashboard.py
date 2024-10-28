#  Importing Libraies

import tkinter as tk
import customtkinter as ctk
from PIL import ImageTk, Image
from customtkinter import FontManager
from tkinter import font

ctk.set_appearance_mode("dark")

# Create the main window
root = ctk.CTk()
root.geometry("900x440")
root.title("MAIN")

label = ctk.CTkLabel(master=root, text="This is User DashBoard window", font=("DM Sans", 50, 'bold'))
label.pack()



root.mainloop()
