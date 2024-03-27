# translate_screen.py
import tkinter as tk
import random
from espCommunication import request_multimeter_data


class TranslateScreen:
    def __init__(self, master, num_nodes=0, connections=[]):
        self.master = master
        self.num_nodes = num_nodes
        self.connections = connections
        self.canvas = tk.Canvas(master, width=600, height=400)  # Adjusted width to make space for connections text
        self.canvas.pack()
        self.dot_colors = ['red', 'yellow', 'green']  # Colors for each column
        self.draw_grid()
        self.display_connections()
        # Add this after the `self.display_connections()` call in the `__init__` method
        self.dmm_button = tk.Button(self.master, text="Digital Multimeter", command=self.request_digital_multimeter)
        self.dmm_button.pack()
        self.update_multimeter_data_periodically()

        
    def draw_grid(self):
        self.dot_radius = 10
        self.small_dot_radius = 2
        self.grid_size = 100
        self.small_dot_distance = 15

        for i in range(3):
            for j in range(3):
                x = 100 + i * self.grid_size
                y = 100 + j * self.grid_size
                self.canvas.create_oval(x - self.dot_radius, y - self.dot_radius,
                                        x + self.dot_radius, y + self.dot_radius,
                                        fill='black', tags=('dot', f'dot_{i}_{j}'))

                # Create small dots aligned vertically
                for k in range(1, 5):
                    self.canvas.create_oval(x - self.small_dot_radius,
                                            y + k * self.small_dot_distance - self.small_dot_radius,
                                            x + self.small_dot_radius,
                                            y + k * self.small_dot_distance + self.small_dot_radius,
                                            fill='blue', tags=('small_dot'))

    def color_dots_based_on_nodes(self, num_nodes):
        # Ensure num_nodes is not greater than the total number of main dots
        num_nodes = min(num_nodes, 9)
        self.dots_to_color = random.sample(range(9), num_nodes)
        for dot_index in self.dots_to_color:
            i, j = divmod(dot_index, 3)  # Get the grid position from the index
            x = 100 + i * self.grid_size
            y = 100 + j * self.grid_size
            color = self.dot_colors[i]  # Color based on the column
            self.canvas.create_oval(x - self.dot_radius, y - self.dot_radius,
                                    x + self.dot_radius, y + self.dot_radius,
                                    fill=color, outline=color)

    

    def display_connections(self):
        if not self.connections:
            self.canvas.create_text(450, 200, text="No connections to display", fill="black")
        else:
            connections_text = "Connections:\n" + "\n".join(self.connections)
            self.canvas.create_text(450, 20, text=connections_text, anchor="nw", fill="black")
    
    def generate_matrix_for_esp(self):
        matrix = [["0" for _ in range(3)] for _ in range(3)]
        for dot_index in self.dots_to_color:
            i, j = divmod(dot_index, 3)
            matrix[j][i] = "1"
        return matrix
    
    def request_digital_multimeter(self):
        data = request_multimeter_data()
        print("Multimeter data received:", data)
        # Display the data on the screen or update a label with the received data
        self.update_multimeter_label(data)

    def update_multimeter_label(self, data):
        # Join the received data list into a single string to display
        multimeter_readings = "\n".join(data)
        if not hasattr(self, 'multimeter_label'):
            self.multimeter_label = tk.Label(self.master, text=multimeter_readings)
            self.multimeter_label.pack()
        else:
            self.multimeter_label.config(text=multimeter_readings)
    
    def update_multimeter_data_periodically(self):
        data = request_multimeter_data()
        self.update_multimeter_label(data)
        # Schedule the next call in 3000ms (3 seconds)
        self.master.after(3000, self.update_multimeter_data_periodically)

if __name__ == "__main__":
    root = tk.Tk()
    app = TranslateScreen(root)
    #app.color_dots_based_on_nodes(2)  # Example call; replace 2 with the actual number of nodes
    root.mainloop()
