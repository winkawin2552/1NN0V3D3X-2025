import tkinter as tk

def start_detection():
    print("🔍 Detection started!")

root = tk.Tk()
root.title("Start Detection")

start_button = tk.Button(root, text="Start", command=start_detection, font=("Arial", 14), bg="green", fg="white")
start_button.pack(padx=100, pady=100)

root.mainloop()
