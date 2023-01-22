import tkinter as tk
from tkinter import ttk
import subprocess
import os
import sys
import zipfile
from tkinter import filedialog
import requests


class Launcher:
    def __init__(self):        
        self.button_name = "Download"
        self.root = tk.Tk()
        self.root.title("Android Redemption Launcher")
        self.root.geometry("800x600")
        self.root.minsize("800","600")
        self.root.maxsize("800","600")



        
    def create_gui(self):
        self.status_label = tk.Label(self.root, text="")
        self.status_label.place(x=100, y=450, width=600, height=50)

        file1_button = ttk.Button(self.root, text=self.btn_text, command=self.button_1)
        file1_button.place(x=100, y=225, width=225, height=150)

        file2_button = ttk.Button(self.root, text="Run", command=self.run_file1)
        file2_button.place(x=475, y=225, width=225, height=150)
    
    def button_1(self):
        if not os.path.exists("venv") and not os.path.exists("Android-Redemption") :
            self.setup()
            self.btn_text = "Update"
        else:
            self.update_game()

    def run_file1(self):
        if os.path.exists("Android-Redemption/Game/window_manager.py"):
            subprocess.run([sys.executable, "Android-Redemption/Game/window_manager.py"], shell=False, check=True)
        else:
            self.status_label.config(text="Error: window_manager.py not found.")
            self.status_label.config(foreground="red")

    def update_game(self):
        #add your code here
        #Android-Redemption
        result = subprocess.run(['git', '-C',"Android-Redemption" , 'pull'])
        if result.returncode != 0:
            self.status_label.config(text="Error: Occured while cloning the repository.")
            self.status_label.config(foreground="red")
            return
        self.status_label.config(text="Repository cloned successfully.")
        self.status_label.config(foreground="green")

        result = subprocess.run(["pip", "install", "-r", "Android-Redemption/requirements.txt"])
        if result.returncode != 0:
            self.status_label.config(text="Error: Occured while installing the requirements.")
            self.status_label.config(foreground="red")
            return
        self.status_label.config(text="Requirements installed successfully.")
        self.status_label.config(foreground="green")

    def setup(self):
        # Download the repository
        #https://github.com/CocoGroudon/Android-Redemption/archive/refs/tags/alpha.zip
        result = subprocess.run(["git", "clone", "https://github.com/CocoGroudon/Android-Redemption.git"])

        response = requests.get("https://api.github.com/repos/CocoGroudon/Android-Redemption/releases/latest")
        
        if response.status_code == 200:
            release = response.json()
            download_url = release["assets"][0]["browser_download_url"]
            filename = release["assets"][0]["name"]
            r = requests.get(download_url)
            open(filename, "wb").write(r.content)
        else:
            print("Error:", response.status_code)

        if result.returncode != 0:
            self.status_label.config(text="Error: Occured while downloading the Game.")
            self.status_label.config(foreground="red")
            return
        self.status_label.config(text="Game downloaded successfully.")
        self.status_label.config(foreground="green")


        extract_path = filedialog.askdirectory(initialdir = ".", title = "Select directory to extract to")

        with zipfile.ZipFile("Android-Redemption-alpha.zip", "r") as zip_ref:
            zip_ref.extractall(extract_path)


        # Create a virtual environment
        result = subprocess.run(["python", "-m", "venv", "venv"])
        if result.returncode != 0:
            self.status_label.config(text="Error:   Occured while creating virtual environment.")
            self.status_label.config(foreground="red")
            return
        self.status_label.config(text="Virtual environment created successfully.")
        self.status_label.config(foreground="green")
        # Activate the virtual environment
        os.system(r'venv\Scripts\activate.bat')
        # Install the requirements
        result = subprocess.run(["pip", "install", "-r", "Android-Redemption/requirements.txt"])
        if result.returncode != 0:
            self.status_label.config(text="Error: Occured while installing the requirements.")
            self.status_label.config(foreground="red")
            return
        self.status_label.config(text="Requirements installed successfully.")
        self.status_label.config(foreground="green")

        self.button_name = "Update"
        self.file1_button.config(text=self.button_name)

    def start(self):
        if not os.path.exists("venv") and not os.path.exists("Android-Redemption") :
            self.btn_text = "Download"
        else:
            self.btn_text = "Update"

        self.create_gui()
        self.root.mainloop()
        if not os.path.exists("venv") and not os.path.exists("Android-Redemption") :
            self.setup()
        else:
            self.btn_text = "Update"
            self.status_label.config(text="Ready to game")
            self.status_label.config(foreground="green")

if __name__ == "__main__":
    launcher = Launcher()
    launcher.start()