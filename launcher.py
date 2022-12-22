from tkinter import *
from tkinter import messagebox
import tkinter as tk
import subprocess

import  settings

class MainWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.window_width = settings.screen_width
        self.window_height = settings.screen_height
        self.title("Game Launcher")
        self.geometry(f"{self.window_width}x{self.window_height}")

        self.login_frame = LoginFrame(self)
        self.login_frame.pack(side="top", fill="both", expand=True)
        self.show_login_frame()

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_coordinate = (screen_width - self.window_width) // 2
        y_coordinate = (screen_height - self.window_height) // 2
        self.geometry(f"{self.window_width}x{self.window_height}+{x_coordinate}+{y_coordinate}")

    def show_login_frame(self):
        self.login_frame.pack(side="top", fill="both", expand=True)
        GameFrame(self).pack_forget()  # Remove the game widgets

    def show_game_frame(self):
        self.login_frame.pack_forget()
        self.game_frame = GameFrame(self)

class LoginFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.username_label = tk.Label(self, text="Username:")
        self.username_entry = tk.Entry(self)
        self.password_label = tk.Label(self, text="Password:")
        self.password_entry = tk.Entry(self, show="*")
        self.username_entry.bind("<Return>", lambda event: self.login())
        self.password_entry.bind("<Return>", lambda event: self.login())
        self.login_button = tk.Button(self, text="Login", command=self.login)
        self.username_label.pack()
        self.username_entry.pack()
        self.password_label.pack()
        self.password_entry.pack()
        self.login_button.pack()


    def login(self, event=None):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.check_credentials(username, password):
            self.parent.show_game_frame()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def check_credentials(self, username, password):
        # Replace this with your own code to check the username and password
        return username == "test" and password == "test"


class GameFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.pack(side="top", fill="both", expand=True)
        self.button = tk.Button(self, text="Start game", command=self.start_game)
        self.button.pack()

    def start_game(self):
        subprocess.run(["/path/to/game"])

Launcher = MainWindow()
Launcher.center_window()
Launcher.mainloop()
