import tkinter as tk
import random
from espCommunication import get_sensor_data

class TranslateScreen:
    def __init__(self, master, num_nodes=0, connections=[]):
        self.master = master
        self.num_nodes = num_nodes
        self.connections = connections
        self.canvas = tk.Canvas(master, width=600, height=400)
        self.canvas.pack()
        self.dot_colors = ['red', 'yellow', 'green']
        self.draw_grid()
        self.display_connections()
        self.sensor_data_display()
        self.fetch_sensor_data_btn = tk.Button(master, text="Fetch Sensor Data", command=self.fetch_sensor_data)
        self.fetch_sensor_data_btn.pack()
        self.sensor_data_label = tk.Label(master, text="Sensor Data: Not fetched yet")
        self.sensor_data_label.pack()
        
    def draw_grid(self):
        dot_radius = 10
        small_dot_radius = 2
        grid_size = 100
        small_dot_distance = 15
        for i in range(3):
            for j in range(3):
                x = 100 + i * grid_size
                y = 100 + j * grid_size
                self.canvas.create_oval(x - dot_radius, y - dot_radius, x + dot_radius, y + dot_radius, fill='black', tags=('dot', f'dot_{i}_{j}'))
                for k in range(1, 5):
                    self.canvas.create_oval(x - small_dot_radius, y + k * small_dot_distance - small_dot_radius, x + small_dot_radius, y + k * small_dot_distance + small_dot_radius, fill='blue', tags=('small_dot'))

    def color_dots_based_on_nodes(self, num_nodes):
        num_nodes = min(num_nodes, 9)
        dots_to_color = random.sample(range(9), num_nodes)
        for dot_index in dots_to_color:
            i, j = divmod(dot_index, 3)
            x = 100 + i * self.grid_size
            y = 100 + j * self.grid_size
            color = self.dot_colors[i]
            self.canvas.create_oval(x - self.dot_radius, y - self.dot_radius, x + self.dot_radius, y + self.dot_radius, fill=color, outline=color)

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

    def fetch_sensor_data(self):
        sensor_data = get_sensor_data()
        display_text = f"Voltage: {sensor_data.get('Voltage', 'N/A')} V, Current: {sensor_data.get('Current', 'N/A')} mA"
        self.sensor_data_label.config(text=display_text)

    def display_sensor_data(self):
        self.canvas.delete("sensor_data")
        sensor_data = get_sensor_data()
        voltage_text = f"Voltage: {sensor_data['Voltage']}V"
        current_text = f"Current: {sensor_data['Current']}mA"
        self.canvas.create_text(450, 350, text=voltage_text, fill="black", tags="sensor_data")
        self.canvas.create_text(450, 375, text=current_text, fill="black", tags="sensor_data")
        self.master.after(1000, self.display_sensor_data)

    def sensor_data_display(self):
        self.display_sensor_data()

if __name__ == "__main__":
    root = tk.Tk()
    app = TranslateScreen(master=root)
    root.mainloop()
