import tkinter as tk

fenster = tk.Tk()
fenster.title("Test")
fenster.geometry("300x200")

label = tk.Label(fenster, text="Hallo, mein Dashboard!", font=("Arial", 14))
label.pack(pady=50)

fenster.mainloop()