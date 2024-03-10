import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import schemdraw
import schemdraw.elements as elm
import tempfile
import os
import io
from PIL import Image as PilImage, ImageTk
from wand.image import Image as WandImage
from wand.color import Color
from style import StyleButton  # Assuming style.py is in the same directory
import espCommunication

class CircuitMaker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Circuit Maker with Enhanced Features')
        self.originalSize = "800x500"  # Save the original size
        self.geometry(self.originalSize)
        self.drawing = schemdraw.Drawing(show=False)
        self.last_direction = None
        self.components_with_values = []
        self.setup_gui()

    def setup_gui(self):
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.menu_button = StyleButton(self.main_frame, text="Add Component", command=self.show_add_menu)
        self.menu_button.pack(side=tk.TOP, pady=10)
        
        self.real_life_button = StyleButton(self.main_frame, text="Real Life", command=self.switch_to_real_life)
        self.real_life_button.pack(side=tk.TOP, pady=10)
        
        self.done_button = StyleButton(self.main_frame, text="Done", command=self.print_connections)
        self.done_button.pack(side=tk.TOP, pady=10)
        
        self.circuit_display = tk.Label(self.main_frame)
        self.circuit_display.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    def show_add_menu(self):
        menu = tk.Menu(self.menu_button, tearoff=0)
        components = ['Resistor', 'Capacitor', 'SourceV', 'Wire', 'Ground']
        for comp in components:
            menu.add_command(label=comp, command=lambda c=comp: self.add_component_prompt(c))
        try:
            menu.tk_popup(self.menu_button.winfo_rootx(), self.menu_button.winfo_rooty() + self.menu_button.winfo_height())
        finally:
            menu.grab_release()


    def add_component_prompt(self, component_type):
        orientation = "right"  # Default orientation
        value = None  # Default value

        if component_type in ['Resistor', 'Capacitor', 'SourceV']:
            label = simpledialog.askstring("Label", "Enter label (max 5 chars, unique):", parent=self)
            if not label or len(label) > 5:
                messagebox.showerror("Error", "Invalid label.")
                return
            value = simpledialog.askstring("Value", "Enter value:", parent=self)
            orientation = simpledialog.askstring("Orientation", "Enter orientation (up, down, left, right):", parent=self)
        elif component_type == 'Wire':
            orientation = simpledialog.askstring("Direction", "Enter direction (up, down, left, right):", parent=self)

        if component_type != 'Wire':
            self.add_component(component_type, label, orientation, value)
        else:
            self.add_wire(orientation)
    
    def add_wire(self, direction):
        if self.is_opposite_direction(direction):
            messagebox.showerror("Error", "Cannot place in the opposite direction of current flow.")
            return
        wire = elm.Line().length(2)
        wire = getattr(wire, direction)()
        self.drawing += wire
        self.last_direction = direction
        self.update_circuit_display()


    def add_component(self, component_type, label, orientation, value=None):
        if self.is_opposite_direction(orientation):
            messagebox.showerror("Error", "Cannot place in the opposite direction of current flow.")
            return
        element = getattr(elm, component_type)()
        if label:
            element = element.label(f"{label}: {value}" if value else label)
        if orientation:
            element = getattr(element, orientation)()
            self.last_direction = orientation
        self.drawing += element
        if label:
            self.components_with_values.append((element, value))
        self.update_circuit_display()

    def print_connections(self):
        for element, value in self.components_with_values:
            print(f"Component: {type(element).__name__}, Value: {value}, Label: {element.label}, Direction: {self.last_direction}")

    def update_circuit_display(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.svg') as tmpfile_svg:
            self.drawing.save(tmpfile_svg.name)
            tmpfile_svg.close()
            with WandImage(filename=tmpfile_svg.name, format='svg') as img:
                img.format = 'png'
                png_blob = img.make_blob()
        img = PilImage.open(io.BytesIO(png_blob))
        photo = ImageTk.PhotoImage(img)
        self.circuit_display.config(image=photo)
        self.circuit_display.image = photo
        os.remove(tmpfile_svg.name)

    def switch_to_real_life(self):
        self.geometry("400x400")  # Smaller, compact size for RealLife view
        self.main_frame.pack_forget()  # Hide main UI components
        from real_life import RealLife
        self.realLifeView = RealLife(self)
        self.realLifeView.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)


    def switch_back_to_editor(self):
        self.geometry(self.originalSize)  # Reset to original size
        if hasattr(self, 'realLifeView'):
            self.realLifeView.pack_forget()
            self.realLifeView.destroy()
            del self.realLifeView
        self.setup_gui()  # Re-setup the GUI for the circuit maker/editor view

    def is_opposite_direction(self, direction):
        opposites = {'left': 'right', 'right': 'left', 'up': 'down', 'down': 'up'}
        return self.last_direction and opposites.get(self.last_direction) == direction

if __name__ == "__main__":
    app = CircuitMaker()
    app.mainloop()
