import tkinter as tk
import espCommunication
from tkinter import messagebox
try:
    from style import StyleButton  # Attempt to import a styled button from `style.py`
except ImportError:
    StyleButton = tk.Button  # Fallback to default Button if `style.py` is not found
    
class RealLife(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(bg="white")
        self.canvas = tk.Canvas(self, width=300, height=300, bg="white")
        self.canvas.grid(row=0, column=0, pady=(20, 0))
        self.grid_size = 3
        self.dot_radius = 10
        self.dot_spacing = 80
        self.occupied_dots = set()
        self.component_counter = {"R": 0, "C": 0, "W": 0, "P": 0, "G": 0}
        self.matrix = [["0" for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.first_click_dot = None
        self.selected_component = None
        self.created_items = []
        self.initialize_game()
        self.setup_buttons()

    def initialize_game(self):
        self.draw_grid()
    
    def setup_buttons(self):
        button_frame = tk.Frame(self, bg="white")
        button_frame.grid(row=1, column=0, pady=(10, 20))
        self.undo_button = StyleButton(button_frame, text="Undo", command=self.undo_last_action)
        self.undo_button.grid(row=0, column=0, padx=5)
        self.return_button = StyleButton(button_frame, text="Return to Editor", command=self.return_to_editor)
        self.return_button.grid(row=0, column=1, padx=5)
        self.translate_button = StyleButton(button_frame, text="Translate", command=self.translate)
        self.translate_button.grid(row=0, column=2, padx=5)

    def draw_grid(self):
        offset = (400 - (self.grid_size - 1) * self.dot_spacing) // 2
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x = col * self.dot_spacing + offset
                y = row * self.dot_spacing + offset
                dot_tag = f"dot_{row}_{col}"
                self.canvas.create_oval(x - self.dot_radius, y - self.dot_radius,
                                        x + self.dot_radius, y + self.dot_radius,
                                        fill='black', tags=("dot", dot_tag))
        self.canvas.tag_bind("dot", "<Button-1>", self.on_dot_click)

    def on_dot_click(self, event):
        clicked_items = self.canvas.find_withtag("current")
        if clicked_items:
            clicked_dot = clicked_items[0]
            dot_tags = self.canvas.gettags(clicked_dot)
            for tag in dot_tags:
                if tag.startswith("dot_") and tag not in self.occupied_dots:
                    self.show_selection_menu(event, tag)
                    break

    def show_selection_menu(self, event, dot_tag):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Wire", command=lambda: self.place_component("wire", dot_tag, "red"))
        menu.add_command(label="Resistor", command=lambda: self.place_component("resistor", dot_tag, "green"))
        menu.add_command(label="Capacitor", command=lambda: self.place_component("capacitor", dot_tag, "blue"))
        menu.add_command(label="Ground", command=lambda: self.place_component("ground", dot_tag, "black", single_dot=True))
        menu.add_command(label="Power Source", command=lambda: self.place_component("power_source", dot_tag, "purple", single_dot=True))
        menu.post(event.x_root, event.y_root)

    def place_component(self, component_type, dot_tag, color, single_dot=False):
        row, col = map(int, dot_tag.split('_')[1:])
        component_key = component_type[0].upper()  # Convert first character to uppercase to match dictionary keys

        if single_dot:
            self.matrix[row][col] = component_key + str(self.component_counter[component_key] + 1)
            self.component_counter[component_key] += 1
            # Drawing single dot component logic remains unchanged.
        else:
            if not self.first_click_dot:
                self.selected_component = component_type
                self.first_click_dot = dot_tag
                # Mark the first dot as occupied logic remains unchanged.
            else:
                start_row, start_col = map(int, self.first_click_dot.split('_')[1:])
                self.matrix[start_row][start_col] = self.matrix[row][col] = component_key + str(self.component_counter[component_key] + 1)
                self.component_counter[component_key] += 1
                # Drawing line between dots logic remains unchanged.


    def draw_component_between_dots(self, component_type, start_dot_tag, end_dot_tag, color):
        start_x, start_y = self.tag_to_coords(start_dot_tag)
        end_x, end_y = self.tag_to_coords(end_dot_tag)
        item_id = self.canvas.create_line(start_x, start_y, end_x, end_y, fill=color, width=2)
        self.created_items.append(item_id)
        self.occupied_dots.add(end_dot_tag)  # Mark the second dot as occupied

    def undo_last_action(self):
        if self.created_items:
            last_item_id = self.created_items.pop()
            self.canvas.delete(last_item_id)

    def return_to_editor(self):
        # Hide the current RealLife frame
        self.pack_forget()
        # Call the parent's method to switch back to the circuit editor view
        self.parent.switch_back_to_editor()
    
    def switch_back_to_editor(self):
        # Re-display the main frame with the circuit maker/editor UI components
        if hasattr(self, 'main_frame'):
            self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Remove the RealLife view
        if hasattr(self, 'realLifeView'):
            self.realLifeView.pack_forget()  # Or `destroy()` if you prefer to completely destroy the view
            del self.realLifeView  # Clean up
    
    def translate(self):
        # Print the matrix and component connections for verification
        for row in self.matrix:
            print(' '.join(row))
        print("Component connections and positions have been printed.")

        # Call the send_matrix function from espCommunication.py
        espCommunication.send_matrix(self.matrix)



    def tag_to_coords(self, dot_tag):
        _, row, col = dot_tag.split('_')
        offset = (400 - (self.grid_size - 1) * self.dot_spacing) // 2
        x = int(col) * self.dot_spacing + offset
        y = int(row) * self.dot_spacing + offset
        return x, y

