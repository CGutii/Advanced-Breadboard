# translate_screen.py
import tkinter as tk
import random

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


if __name__ == "__main__":
    root = tk.Tk()
    app = TranslateScreen(root)
    #app.color_dots_based_on_nodes(2)  # Example call; replace 2 with the actual number of nodes
    root.mainloop()
