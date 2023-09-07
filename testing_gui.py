import tkinter as tk

def button_clicked():
    label.config(text="Button Clicked")

root = tk.Tk()
root.title("Tkinter Example")

label = tk.Label(root, text="Hello, Tkinter!")
label.pack()

button = tk.Button(root, text="Click Me", command=button_clicked)
button.pack()

root.mainloop()
