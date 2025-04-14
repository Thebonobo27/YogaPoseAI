import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess

def open_introvert():
    subprocess.Popen(["python", "introvert_page.py"])
    root.destroy()

def open_extrovert():
    subprocess.Popen(["python", "extrovert_page.py"])
    root.destroy()

# Create the main window
root = tk.Tk()
root.title("Yoga Poses")
root.geometry("500x600")

# Load and resize background image
bg_image = Image.open("C:\\grinding\\coding\\Game_Dev\\School_Project\\DTI\\521461.jpg").resize((500, 600))
bg_photo = ImageTk.PhotoImage(bg_image)

# Create canvas
canvas = tk.Canvas(root, width=500, height=600, highlightthickness=0)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor='nw')

# Center window on screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - 250
y = (screen_height // 2) - 300
root.geometry(f"+{x}+{y}")

# Font
font_family = "Lucida Sans"

# Welcome text
canvas.create_text(252, 122, text="Pick your choices", font=(font_family, 20, "bold"),
                   fill="#000000", anchor='center')
canvas.create_text(250, 120, text="Pick your choices", font=(font_family, 20, "bold"),
                   fill="#ffffff", anchor='center')

# "Introvert" option
intro_text = canvas.create_text(
    250, 460,
    text="Introvert",
    font=(font_family, 16, "bold"),
    fill="white",
    anchor='center'
)

# "Extrovert" option
extro_text = canvas.create_text(
    250, 510,
    text="Extrovert",
    font=(font_family, 16, "bold"),
    fill="white",
    anchor='center'
)

# Bind actions
canvas.tag_bind(intro_text, "<Button-1>", lambda e: open_introvert())
canvas.tag_bind(extro_text, "<Button-1>", lambda e: open_extrovert())

# Hover effects
canvas.tag_bind(intro_text, "<Enter>", lambda e: canvas.itemconfig(intro_text, fill="lightgray"))
canvas.tag_bind(intro_text, "<Leave>", lambda e: canvas.itemconfig(intro_text, fill="white"))

canvas.tag_bind(extro_text, "<Enter>", lambda e: canvas.itemconfig(extro_text, fill="lightgray"))
canvas.tag_bind(extro_text, "<Leave>", lambda e: canvas.itemconfig(extro_text, fill="white"))

# Keep reference
canvas.image = bg_photo

# Run the app
root.mainloop()
