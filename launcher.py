from tkinter import *
from tkinter import messagebox
import tkinter as tk
import subprocess
from tkinter import ttk

import TKinterModernThemes as TKMT
from TKinterModernThemes.WidgetFrame import Widget

import database
import  settings

class MainWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.window_width = settings.screen_width
        self.window_height = settings.screen_height
        self.title("Game Launcher")
        self.geometry(f"{self.window_width}x{self.window_height}")

        self.style = ttk.Style(self)
                # radio button
        self.selected_theme = tk.StringVar()
        theme_frame = ttk.LabelFrame(self, text='Themes')
        theme_frame.grid(padx=10, pady=10, ipadx=20, ipady=20, sticky='w')

        for theme_name in self.style.theme_names():
            rb = ttk.Radiobutton(
                theme_frame,
                text=theme_name,
                value=theme_name,
                variable=self.selected_theme,
                command=self.change_theme)
            rb.pack(expand=True, fill='both')

    def change_theme(self):
        self.style.theme_use(self.selected_theme.get())


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
        self.username_label = ttk.Label(self, text="Username:")
        self.username_entry = ttk.Entry(self)
        self.password_label = ttk.Label(self, text="Password:")
        self.password_entry = ttk.Entry(self, show="*")
        self.username_entry.bind("<Return>", lambda event: self.login())
        self.password_entry.bind("<Return>", lambda event: self.login())
        self.login_button = ttk.Button(self, text="Login",style="C.TButton" , command=self.login)
        self.username_label.pack()
        self.username_entry.pack()
        self.password_label.pack()
        self.password_entry.pack()
        self.login_button.pack()


    def login(self, event=None):
        db = database.Database()
        username = self.username_entry.get()
        password = self.password_entry.get()
        if db.check_credentials(username, password):
            self.parent.show_game_frame()
        else:
            messagebox.showerror("Error", "Invalid username or password")


class GameFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.pack(side="top", fill="both", expand=True)
        self.button = ttk.Button(self, text="Start game", style="C.TButton" , command=self.start_game)
        self.button.pack()

    def start_game(self):
        subprocess.run(["/path/to/game"])



if __name__ == "__main__":
    Launcher = MainWindow()
    Launcher.center_window()
    Launcher.mainloop()
