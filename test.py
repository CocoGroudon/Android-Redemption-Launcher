import tkinter as tk
from tkinter import ttk
import subprocess
import os
import sys



def run_file1():
    	subprocess.run([sys.executable, "Android-Redemption\Game\window_manager.py"], shell=False, check=True)
#Android-Redemption\Game\window_manager.py

def update_game():
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
root.title("Android Redemption Launcher")
root.geometry("800x600")
root.minsize("800","600")
root.maxsize("800","600")
file1_button = ttk.Button(root, text="Starten", command=run_file1)
file1_button.place(x=100, y=225, width=225, height=150)

file2_button = ttk.Button(root, text="Update", command=update_game)
file2_button.place(x=475, y=225, width=225, height=150)

root.mainloop()

