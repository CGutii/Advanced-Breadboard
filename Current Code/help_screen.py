# help_screen.py
import tkinter as tk
from tkinter import scrolledtext

class HelpScreen:
    def __init__(self, master):
        self.master = master
        self.master.title("Help")
        self.master.geometry("500x400")  # Set a larger size for the window

        # Initialize Text widget with a Scrollbar
        self.text_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=40, height=10)
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Pages content including placeholder for images and text
        self.pages = [
            "Welcome to our application! Here's how to get started.",
            "Lessons:\n\n" +
            "An electrical circuit is a path in which electrons from a voltage or current source flow. " +
            "Basic components include resistors, capacitors, and inductors. Circuits can be series, parallel, or a mix.\n\n" +
            "Series: Components are in a single path from one end of the battery to the other. " +
            "Current is the same through each component.\n\n" +
            "Parallel: Components are on separate branches, and voltage across each component is the same.\n\n" +
            "[Insert Lessons Images Here]",
            "Examples:\n\n" +
            "Here are examples of components in series and parallel configurations.\n\n" +
            "[Insert Examples Images Here]"
        ]

        self.current_page = 0
        self.update_text_area()

        self.prev_button = tk.Button(self.master, text="Previous", command=self.go_prev)
        self.prev_button.pack(side=tk.LEFT, padx=(20, 10), pady=10)

        self.next_button = tk.Button(self.master, text="Next", command=self.go_next)
        self.next_button.pack(side=tk.RIGHT, padx=(10, 20), pady=10)

        self.update_buttons()

    def update_text_area(self):
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.INSERT, self.pages[self.current_page])
        self.text_area.configure(state='disabled')  # Make the text area read-only

    def go_next(self):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            self.update_text_area()
            self.update_buttons()

    def go_prev(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_text_area()
            self.update_buttons()

    def update_buttons(self):
        if self.current_page == 0:
            self.prev_button.config(state=tk.DISABLED)
        else:
            self.prev_button.config(state=tk.NORMAL)

        if self.current_page == len(self.pages) - 1:
            self.next_button.config(state=tk.DISABLED)
        else:
            self.next_button.config(state=tk.NORMAL)
