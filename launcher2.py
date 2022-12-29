from tkinter import *
from TKinterModernThemes  import *

# Erstelle ein Fenster
window = tk()

# Setze das Theme

# Erstelle einen Button
button = Button(text="Click me!", command=lambda: print("Button clicked!"))
button.pack()

window.mainloop()