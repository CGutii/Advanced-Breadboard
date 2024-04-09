import tkinter as tk
import espCommunication

class StyleButton(tk.Button):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.configure(
            bg="#f0f0f0",  # Button background color
            fg="black",  # Button text color
            bd=0,  # Border width
            font=("Arial", 10),  # Font and size
            padx=20,  # Horizontal padding
            pady=5,  # Vertical padding
            relief="flat"  # Flat relief to remove the border
        )
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['bg'] = '#e8e8e8'  # Lighten the button on hover

    def on_leave(self, e):
        self['bg'] = '#f0f0f0'  # Return to original color when not hovered
