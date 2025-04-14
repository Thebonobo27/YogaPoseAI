import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess

def start_app():
    try:
        subprocess.Popen(["python", "DTI\\choice.py"])
        root.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"Unable to open next page.\n\n{e}")


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

# Calming font
font_family = "Lucida Sans"

# Welcome text with glow/shadow effect
canvas.create_text(252, 122, text="Welcome to Yoga_Pose 🧘", font=(font_family, 20, "bold"),
                   fill="#000000", anchor='center')
canvas.create_text(250, 120, text="Welcome to Yoga_Pose 🧘", font=(font_family, 20, "bold"),
                   fill="#ffffff", anchor='center')

# Start "button" as text (true floating effect)
start_text = canvas.create_text(
    250, 500,
    text="Start",
    font=(font_family, 16, "bold"),
    fill="white",
    anchor='center'
)

# Hover effect and click interaction
def on_start_click(event):
    start_app()

canvas.tag_bind(start_text, "<Button-1>", on_start_click)
canvas.tag_bind(start_text, "<Enter>", lambda e: canvas.itemconfig(start_text, fill="lightgray"))
canvas.tag_bind(start_text, "<Leave>", lambda e: canvas.itemconfig(start_text, fill="white"))

# Keep reference
canvas.image = bg_photo

# Run the app
root.mainloop()




