import tkinter as tk
from tkinter import ttk
import subprocess
import os
import sys
import zipfile
from tkinter import filedialog
import requests
import json
import atexit



def check_if_running(script_name):
    for line in os.popen("ps -ef | grep " + script_name):
        if script_name in line:
            return True
    return False

class Launcher:
    def __init__(self):        
        self.button_name = "Download"
        self.root = tk.Tk()
        self.root.title("Android Redemption Launcher")
        self.root.geometry("800x600")
        self.root.minsize("800","600")
        self.root.maxsize("800","600")

        self.filename = ""
        self.new_folder_name = ""
        self.isRunning = False
        

    def exit_handler(self):
        print("Exiting program")
        subprocess.call(["pkill","-f","window_manager.py"])


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
        if self.isRunning == True:
            self.status_label.config(text="Already running")
            self.status_label.config(foreground="red")
        else:
            print(f"2. {self.new_folder_name}")
            if os.path.exists(self.new_folder_name):
                print(self.new_folder_name)
                source_code = f"{self.new_folder_name}Game/window_manager.py"
                print(source_code)
                subprocess.Popen(["python", source_code])
                self.isRunning = True
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

        result = subprocess.run(["pip", "install", "-r", f"{self.filename}/requirements.txt"])
        if result.returncode != 0:
            self.status_label.config(text="Error: Occured while installing the requirements.")
            self.status_label.config(foreground="red")
            return
        self.status_label.config(text="Requirements installed successfully.")
        self.status_label.config(foreground="green")

    def setup(self):
        # Download the repository

        response = requests.get("https://api.github.com/repos/CocoGroudon/Android-Redemption/releases/latest")
        if response.status_code == 200:
            release = response.json()
            download_url = release["zipball_url"]
            self.filename = release["tag_name"]
            
            r = requests.get(download_url)
            print(r.content)
            open(self.filename, "wb").write(r.content)
        else:
            print("Error:", response.status_code)

        if response.status_code != 200:
            self.status_label.config(text="Error: Occured while downloading the Game.")
            self.status_label.config(foreground="red")
            return
        self.status_label.config(text="Game downloaded successfully.")
        self.status_label.config(foreground="green")


        # extract_path = filedialog.askdirectory(initialdir = ".", title = "Select directory to extract to")
        # print(extract_path)
        with zipfile.ZipFile(self.filename, 'r') as zip_ref:
            self.new_folder_name = zip_ref.namelist()[0]
            print(self.new_folder_name)
        data = {"folder_name": self.new_folder_name}
        with zipfile.ZipFile(self.filename, "r") as zip_ref:
            zip_ref.extractall()
        with open("settings.json", "w") as json_file:
            json.dump(data, json_file)



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

        result = subprocess.run(["pip", "install", "-r", f"{self.new_folder_name}/requirements.txt"])
        if result.returncode != 0:
            self.status_label.config(text="Error: Occured while installing the requirements.")
            self.status_label.config(foreground="red")
            return
        self.status_label.config(text="Requirements installed successfully.")
        self.status_label.config(foreground="green")

        self.button_name = "Update"

    def start(self):
        if os.path.isfile("settings.json"):

            # JSON READING
            with open("settings.json") as json_file:
                data = json.load(json_file)
                self.new_folder_name = data["folder_name"]
                print(f'1. folder_name: {self.new_folder_name}')
        else:
            print("Die Datei settings.json existiert nicht.")

        if not os.path.exists("venv") and not os.path.exists(self.filename) :
            self.btn_text = "Download"
        else:
            self.btn_text = "Update"

        self.create_gui()
        if os.path.isfile("settings.json"):       
            self.btn_text = "Update"
            self.status_label.config(text="Ready to game")
            self.status_label.config(foreground="green")
        self.root.mainloop()
        if not os.path.exists("venv") and not os.path.exists(self.filename) :
            self.setup()
        atexit.register(self.exit_handler)

if __name__ == "__main__":
    launcher = Launcher()
    launcher.start()