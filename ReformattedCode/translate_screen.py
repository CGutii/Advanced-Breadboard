import tkinter as tk
#from circuit_simulator import CircuitSimulator  # Import the CircuitSimulator class
from help_screen import HelpScreen
import threading
import serial
import time
import random
import re

class TranslateScreen:
    def __init__(self, master, circuit_simulator_instance, num_nodes=0, connections=[]):
        self.master = master
        self.num_nodes = num_nodes
        self.connections = connections
        self.canvas = tk.Canvas(master, width=600, height=400)  # Adjusted width to make space for connections text
        self.canvas.pack()
        self.dot_colors = ['red', 'yellow', 'green']  # Colors for each column
        self.draw_grid()
        self.display_connections()
        self.sensor_data_btn = tk.Button(master, text="Get Sensor Data", command=self.update_sensor_data_and_warnings)
        self.sensor_data_btn.pack()
        self.sensor_data_label = tk.Label(master, text="Sensor Data: Not fetched yet")
        self.sensor_data_label.pack()
        self.warning_label = tk.Text(master, height=4, width=30)
        self.warning_label.pack()
        self.warning_label.configure(state='disabled')
        self.circuit_simulator = circuit_simulator_instance

        
        
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
    
    def display_sensor_data(self):
        sensor_data = self.circuit_simulator.get_sensor_data()  # Call the function from espCommunication.py
        self.sensor_data_label.config(text=f"Sensor Data: {sensor_data}")

    def update_sensor_data_and_warnings(self):
        # Fetch the latest sensor data
        sensor_data_str = self.circuit_simulator.get_sensor_data()

        # Parse the sensor data string using regular expressions
        match = re.match(r"Voltage:(\d+\.\d+) Current:(\d+\.\d+)", sensor_data_str)
        if match:
            voltage = float(match.group(1))
            current = float(match.group(2))
        else:
            print("Error: Unable to parse sensor data string")
            print("Received sensor data:", sensor_data_str)
            return

        # Update the sensor data label and warnings
        self.sensor_data_label.config(text=f"Sensor Data: Voltage={voltage}, Current={current}")
        short_circuit, open_circuit = self.getIntegerSensorData(voltage, current)
        self.update_warnings(short_circuit, open_circuit)


    def getIntegerSensorData(self, sensor_data):
        numbers = re.findall(r"[-+]?\d*\.\d+|\d+", sensor_data)
        if numbers:
            voltage, current = map(float, numbers[:2])
            short_circuit = voltage == 0
            open_circuit = current < 2
        else:
            short_circuit, open_circuit = False, False
        return short_circuit, open_circuit

    def update_warnings(self, short_circuit, open_circuit):
        warning_text = "Warning:"
        if short_circuit:
            warning_text += "\nPotential Short Circuit"
        if open_circuit:
            warning_text += "\nPotential Open Circuit"
        
        self.warning_label.configure(state='normal')
        self.warning_label.delete('1.0', tk.END)
        if warning_text == "Warning:":
            self.warning_label.insert(tk.END, "No warnings")
        else:
            self.warning_label.insert(tk.END, warning_text)
        self.warning_label.configure(state='disabled')


if __name__ == "__main__":
    root = tk.Tk()
    app = TranslateScreen(root, circuit_simulator_instance, num_nodes, connections)
    #app.color_dots_based_on_nodes(2)  # Example call; replace 2 with the actual number of nodes
    root.mainloop()
