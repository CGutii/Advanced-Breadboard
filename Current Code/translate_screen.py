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
        self.canvas = tk.Canvas(master, width=700, height=440)  # Adjusted width to make space for connections text
        self.canvas.pack()
        self.dots_to_color= []
        # Reference matrices for colors and values
        self.color_matrix = [['#F5F5DC', '#0000FF', '#006400'],
                             ['#FFA500', '#FF0000', '#90EE90'],
                             ['#FFFF00', '#FFFFFF', '#800080']]
        self.value_matrix = [[0, 0, 0],
                             [0, 0, 0],
                             [0, 0, 0]]
        self.draw_grid()
        self.display_connections()
        self.sensor_data_btn = tk.Button(master, text="Get Sensor Data", command=self.update_sensor_data_and_warnings)
        self.sensor_data_btn.pack()
        self.sensor_data_label = tk.Label(master, text="Sensor Data: Not fetched yet")
        self.sensor_data_label.pack()
        self.warning_label = tk.Text(master, height=10, width=15)
        self.warning_label.pack()
        self.warning_label.configure(state='disabled')
        self.circuit_simulator = circuit_simulator_instance

    def draw_grid(self):
        self.dot_radius = 10
        self.small_dot_radius = 3
        self.grid_size = 150
        self.small_dot_distance = 15

        for i in range(3):
            for j in range(3):
                x = 60 + i * self.grid_size
                y = 60 + j * self.grid_size
                color = 'black'  # Default color is black
                self.canvas.create_oval(x - self.dot_radius, y - self.dot_radius,
                                        x + self.dot_radius, y + self.dot_radius,
                                        fill=color, outline=color, tags=('dot', f'dot_{i}_{j}'))

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
        # Gather unique node labels from the connections
        available_labels = set()
        for node_label, components in self.connections.items():
            available_labels.add(node_label.lower())  # Assuming node labels are lowercase

        # Randomly assign labels to the turned-on nodes and update value_matrix
        self.value_matrix = [[0, 0, 0],
                             [0, 0, 0],
                             [0, 0, 0]]
        available_nodes = [(i, j) for i in range(3) for j in range(3)]
        assigned_labels = random.sample(list(available_labels), num_nodes)
        for label in assigned_labels:
            row, col = random.choice(available_nodes)
            available_nodes.remove((row, col))
            self.value_matrix[row][col] = label
            self.connections[label] = [(row, col)]

        # Color the dots based on the value_matrix
        for i in range(3):
            for j in range(3):
                x = 60 + i * self.grid_size
                y = 60 + j * self.grid_size
                color_index = self.value_matrix[j][i]
                color = self.color_matrix[j][i] if color_index else 'black'
                self.canvas.itemconfig(f"dot_{i}_{j}", fill=color, outline=color)
                if color_index:
                    self.canvas.create_rectangle(x - 5, y - 5, x + 5, y + 5, fill='black')
                    self.canvas.create_text(x, y, text=color_index.upper(), fill="white", tags=("dot_label", f"dot_{i}_{j}"))

    def display_connections(self):
        self.canvas.delete("connections")  # Delete previous connections text if any
        if not self.connections:
            self.canvas.create_text(450, 200, text="No connections to display", fill="black", tags="connections")
        else:
            connections_text = ""
            for node_label, components in self.connections.items():
                connections_text += f"Node \"{node_label}\" connections:\n" + "\n".join(f"- {comp}" for comp in components) + "\n\n"
            self.canvas.create_text(450, 20, text=connections_text.strip(), anchor="nw", fill="black", tags="connections")
        
            # Check for components in series or parallel
            parallel_components, series_components = self.find_series_parallel_components()
            warnings_text = ""
            if parallel_components:
                warnings_text += "Parallel components:\n"
                for p_comp in parallel_components:
                    warnings_text += f"- {p_comp}\n"
            if series_components:
                warnings_text += "Series components:\n"
                for s_comp in series_components:
                    warnings_text += f"- {s_comp}\n"
            # print("Parallel Components:", parallel_components)
            # print("Series Components:", series_components)
            # print("Displayed on canvas:", warnings_text.strip())

    def find_series_parallel_components(self):
        parallel_components = []
        series_components = []
        nodes_to_components = {}
        for node_label, components in self.connections.items():
            if node_label != 'j1':
                for comp in components:
                    if comp in nodes_to_components:
                        nodes_to_components[comp].append(node_label)
                    else:
                        nodes_to_components[comp] = [node_label]

        for component, nodes in nodes_to_components.items():
            if len(nodes) > 1:
                parallel_components.append(component)
        
        for node_label, components in self.connections.items():
            if node_label != 'j1' and len(components) == 2:
                node1, node2 = components
                if nodes_to_components[node1] != nodes_to_components[node2]:
                    series_components.append(node_label)
        
        return parallel_components, series_components

    # Other methods remain unchanged

        
    def generate_matrix_for_esp(self):
        matrix = [["0" for _ in range(3)] for _ in range(3)]
        for dot_index in self.dots_to_color:
            i, j = divmod(dot_index, 3)
            matrix[j][i] = "1"
        return matrix
    
    def matrix_to_serial_string(self, matrix):
        serial_string = ""
        for row in matrix:
            for element in row:
                serial_string += element
        serial_string += '\n'
        return serial_string.encode()
    

    def update_sensor_data_and_warnings(self):
        # Fetch the latest sensor data
        sensor_data_str = self.circuit_simulator.get_sensor_data()  # Call the function from espCommunication.py
    
        # Parse the sensor data string
        voltage, current = self.parse_sensor_data(sensor_data_str)
    
        # Update the sensor data label and warnings
        self.sensor_data_label.config(text=f"Sensor Data: Voltage={voltage}, Current={current}")
        short_circuit, open_circuit = self.getIntegerSensorData(voltage, current)
        self.update_warnings(short_circuit, open_circuit)

    def parse_sensor_data(self, sensor_data_str):
        # Split the sensor data string into voltage and current components
        voltage_str, current_str = sensor_data_str.split()
        
        voltage_str = voltage_str.rstrip('V')
        current_str = current_str.rstrip("mA")
    
        # Return the voltage and current values as floats
        return float(voltage_str), float(current_str)


    def getIntegerSensorData(self, voltage, current):
        #numbers = re.findall(r"[-+]?\d*\.\d+|\d+", sensor_data)
        short_circuit, open_circuit = False, False
        if voltage == 0:
            short_circuit = True
            
        if current < 2:
            open_circuit = True
            
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
