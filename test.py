import tkinter as tk
from tkinter import ttk
import subprocess
import os
import ttkthemes




def run_file1():
    #add your code here
    pass

def run_file2():
    #add your code here
    pass 

def setup():
    # Download the repository
    subprocess.run(["git", "clone", "https://github.com/CocoGroudon/Android-Redemption.git"])

    # Create a virtual environment
    subprocess.run(["python", "-m", "venv", "venv"])

    # Activate the virtual environment
    os.system(r'venv\Scripts\activate.bat')

    # Install the requirements
    subprocess.run(["pip", "install", "-r", "Android-Redemption/requirements.txt"])

if not os.path.exists("venv") and not os.path.exists("Android-Redemption") :
    setup()

    root = tk.Tk()
    ttkthemes.set_theme("plastik")
    root.title("Python Launcher")
    file1_button = ttk.Button(root, text="Run File 1", command=run_file1, font=("Arial", 14), background="#2ecc71", foreground="white")
    file1_button.pack()

    file2_button = ttk.Button(root, text="Run File 2", command=run_file2, font=("Arial", 14), background="#2ecc71", foreground="white", )
    file2_button.pack()

    root.mainloop()

