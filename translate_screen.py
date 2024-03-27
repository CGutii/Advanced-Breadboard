# translate_screen.py
import tkinter as tk
import random
import threading
import time
import serial 

# You need to establish serial connection once and keep it open
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

def get_sensor_data():
    ser.write(b"GET_SENSOR_DATA\n")  # Send command to ESP
    line = ser.readline().decode('utf-8').strip()  # Read the response from ESP
    if line.startswith("SENSOR_DATA"):
        parts = line.split(" ")
        if len(parts) == 4:
            return {
                "voltage": parts[1] + "V",
                "current": parts[2] + "mA",
                "power": parts[3] + "mW"
            }
    return {
        "voltage": "N/A",
        "current": "N/A",
        "power": "N/A"
    }

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
        self.multimeter_label = tk.Label(master, text="")
        self.multimeter_label.pack()
        self.update_sensor_data = True
        self.sensor_thread = threading.Thread(target=self.update_sensor_readings)
        self.sensor_thread.start()
    
        
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
    
    def update_sensor_readings(self):
        while self.update_sensor_data:
            sensor_data = get_sensor_data()
            display_text = "Voltage: {}\nCurrent: {}\nPower: {}".format(
                sensor_data["voltage"],
                sensor_data["current"],
                sensor_data["power"]
            )
            # Since Tkinter is not thread-safe, we use `after` to schedule an update
            self.master.after(0, self.update_multimeter_label, display_text)
            time.sleep(3)  # Refresh every 3 seconds
        
    
    def update_multimeter_label(self, text):
        self.multimeter_label.config(text=text)
    
    def stop_sensor_thread(self):
        self.update_sensor_data = False
        self.sensor_thread.join()
    
    def __del__(self):
        self.stop_sensor_thread()



if __name__ == "__main__":
    root = tk.Tk()
    app = TranslateScreen(root)
    root.mainloop()
    app.stop_sensor_thread()
