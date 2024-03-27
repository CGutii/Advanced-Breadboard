import tkinter as tk
from tkinter import messagebox, simpledialog
from circuit_graph import CircuitGraph
from translate_screen import TranslateScreen
from help_screen import HelpScreen
from espCommunication import send_matrix
import threading


# Updated to track the count of each component type, now including 'Junction'
component_count = {"R": 0, "C": 0, "V": 0, "L": 0, "Ground": 0, "Junction": 0}

class Component:
    def __init__(self, canvas, x, y, label="", value=0, is_junction=False):  # Ensure this line is correct
        self.canvas = canvas
        self.x = x
        self.y = y
        self.label = label
        self.value = value
        self.id = []
        self.is_junction = is_junction

    def draw(self):
        pass

    def delete(self):
        for item_id in self.id:
            self.canvas.delete(item_id)
        self.id = []

    def edit(self):
        pass

    def redraw(self):
        self.delete()
        self.draw()

class Junction(Component):
    def __init__(self, canvas, x, y):
        global component_count
        component_count['Junction'] += 1
        super().__init__(canvas, x, y, f"J{component_count['Junction']}", 0, is_junction=True)  # This is correct

    def draw(self):
        self.id.append(self.canvas.create_oval(self.x-5, self.y-5, self.x+5, self.y+5, fill="red"))

class Resistor(Component):
    def __init__(self, canvas, x, y):
        global component_count
        component_count['R'] += 1
        super().__init__(canvas, x, y, f"R{component_count['R']}", 1)

    def draw(self):
        self.delete()
        self.id.append(self.canvas.create_rectangle(self.x-10, self.y-5, self.x+10, self.y+5, fill="gray"))
        self.id.append(self.canvas.create_text(self.x, self.y+20, text=f"{self.label}: {self.value}Ω"))

    def edit(self):
        new_label = simpledialog.askstring("Edit Label", "Enter new label:", initialvalue=self.label)
        if new_label:
            self.label = new_label
        new_value = simpledialog.askfloat("Edit Value", "Enter new value (Ohms):", initialvalue=self.value)
        if new_value is not None:
            self.value = new_value
        self.redraw()

class DCPowerSource(Component):
    def __init__(self, canvas, x, y):
        global component_count
        component_count['V'] += 1
        super().__init__(canvas, x, y, f"V{component_count['V']}", 5)

    def draw(self):
        self.delete()
        self.id.append(self.canvas.create_oval(self.x-10, self.y-15, self.x+10, self.y+15, outline="black", fill="yellow"))
        self.id.append(self.canvas.create_text(self.x, self.y+25, text=f"{self.label}: {self.value}V"))

    def edit(self):
        new_label = simpledialog.askstring("Edit Label", "Enter new label:", initialvalue=self.label)
        if new_label:
            self.label = new_label
        new_value = simpledialog.askfloat("Edit Value", "Enter new value (Volts):", initialvalue=self.value)
        if new_value is not None:
            self.value = new_value
        self.redraw()

class Ground(Component):
    def __init__(self, canvas, x, y):
        global component_count
        component_count['Ground'] += 1
        super().__init__(canvas, x, y, f"Ground{component_count['Ground']}", 0)

    def draw(self):
        self.delete()
        self.id.append(self.canvas.create_line(self.x-10, self.y, self.x+10, self.y, fill="green"))
        self.id.append(self.canvas.create_line(self.x-7, self.y+5, self.x+7, self.y+5, fill="green"))
        self.id.append(self.canvas.create_line(self.x-4, self.y+10, self.x+4, self.y+10, fill="green"))
        self.id.append(self.canvas.create_text(self.x, self.y+20, text=self.label))

    def edit(self):
        new_label = simpledialog.askstring("Edit Label", "Enter new label:", initialvalue=self.label)
        if new_label:
            self.label = new_label
        self.redraw()

class Inductor(Component):
    def __init__(self, canvas, x, y):
        global component_count
        component_count['L'] += 1
        super().__init__(canvas, x, y, f"L{component_count['L']}", 0.001)

    def draw(self):
        self.delete()
        self.id.append(self.canvas.create_line(self.x-15, self.y, self.x+15, self.y, fill="purple", arrow=tk.BOTH))
        self.id.append(self.canvas.create_text(self.x, self.y+20, text=f"{self.label}: {self.value}H"))

    def edit(self):
        new_label = simpledialog.askstring("Edit Label", "Enter new label:", initialvalue=self.label)
        if new_label:
            self.label = new_label
        new_value = simpledialog.askfloat("Edit Value", "Enter new value (Henrys):", initialvalue=self.value)
        if new_value is not None:
            self.value = new_value
        self.redraw()

class Capacitor(Component):
    def __init__(self, canvas, x, y):
        global component_count
        component_count['C'] += 1
        super().__init__(canvas, x, y, f"C{component_count['C']}", 0.000001)

    def draw(self):
        self.delete()
        self.id.append(self.canvas.create_line(self.x-5, self.y-10, self.x-5, self.y+10, fill="blue"))
        self.id.append(self.canvas.create_line(self.x+5, self.y-10, self.x+5, self.y+10, fill="blue"))
        self.id.append(self.canvas.create_text(self.x, self.y+20, text=f"{self.label}: {self.value}F"))

    def edit(self):
        new_label = simpledialog.askstring("Edit Label", "Enter new label:", initialvalue=self.label)
        if new_label:
            self.label = new_label
        new_value = simpledialog.askfloat("Edit Value", "Enter new value (Farads):", initialvalue=self.value)
        if new_value is not None:
            self.value = new_value
        self.redraw()


class Wire(Component):
    def __init__(self, canvas, start_x, start_y, start_comp=None, end_comp=None):
        super().__init__(canvas, start_x, start_y, "Wire", 0)
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = None
        self.end_y = None
        self.start_comp = start_comp
        self.end_comp = end_comp

    def draw(self, end_x=None, end_y=None):
        if end_x is not None and end_y is not None:
            self.end_x = end_x
            self.end_y = end_y
        if self.end_x is not None and self.end_y is not None:
            self.delete()
            self.id.append(self.canvas.create_line(self.x, self.y, self.end_x, self.end_y, fill="black"))


class CircuitSimulator:
    def __init__(self, master):
        self.master = master
        self.selected_component_type = None
        self.grid_size = 35
        self.is_drawing_wire = False
        self.is_delete_mode = False
        self.is_edit_mode = False
        self.wire_start_x = None
        self.wire_start_y = None
        self.component_objects = []
        self.occupied_positions = set()
        self.wire_connections = set()
        self.circuit_graph = CircuitGraph()
        self.setup_ui()

    def setup_ui(self):
        self.canvas = tk.Canvas(self.master, width=400, height=200, bg='white')
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.place_component_or_start_wire_or_delete)
        self.draw_grid()
        

        self.status_label = tk.Label(self.master, text="Status: Select an action", bg='white')
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

        # Organize the UI into Component, Tools, and Help sections
        components_frame = self.create_section("Components")
        tools_frame = self.create_section("Tools")
        help_frame = self.create_section("Help")

        # Add component buttons
        for comp in [Resistor, DCPowerSource, Ground, Inductor, Capacitor, Junction, Wire]:
            self.add_component_button(comp.__name__, comp, components_frame)

        # Add tool buttons
        self.add_tool_button("Delete", self.toggle_delete_mode, tools_frame)
        self.add_tool_button("Connections", self.print_connections, tools_frame)
        self.add_tool_button("Edit", self.enable_edit_mode, tools_frame)

        self.add_tool_button("Translate", self.open_translate_screen, help_frame)
        self.add_tool_button("Help", self.open_help_screen, help_frame)



    def create_section(self, title):
        label = tk.Label(self.master, text=title, anchor='center')
        frame = tk.Frame(self.master)
        label.pack(fill='x')
        frame.pack(fill='x')
        return frame
    
    def open_help_screen(self):
        help_window = tk.Toplevel(self.master)
        help_app = HelpScreen(help_window)

    def add_tool_button(self, name, command, frame):
        button = tk.Button(frame, text=name, command=command)
        button.pack(side=tk.LEFT)


    def add_help_button(self, name, frame):
        # Placeholder function for Help button
        button = tk.Button(frame, text=name, command=lambda: None)
        button.pack(side=tk.LEFT)
    
    def add_component_button(self, name, component_cls, frame):
        button = tk.Button(frame, text=name, command=lambda: self.select_component_type(component_cls))
        button.pack(side=tk.LEFT)

    def add_delete_button(self, frame):
        delete_button = tk.Button(frame, text="Delete", command=self.toggle_delete_mode)
        delete_button.pack(side=tk.LEFT)

    def add_connections_button(self, frame):
        connections_button = tk.Button(frame, text="Connections", command=self.print_connections)
        connections_button.pack(side=tk.LEFT)

    def add_edit_button(self, frame):
        edit_button = tk.Button(frame, text="Edit", command=self.enable_edit_mode)
        edit_button.pack(side=tk.LEFT)

    def add_translate_button(self, frame):
        translate_button = tk.Button(frame, text="Translate", command=self.open_translate_screen)
        translate_button.pack(side=tk.LEFT)
    
    # Add this method to the CircuitSimulator class in circuit_simulator.py
    def show_translate_screen(self):
        self.new_window = tk.Toplevel(self.master)
        self.app = TranslateScreen(self.new_window)


    def fixed_connections(self):
        self.circuit_graph.merge_nodes_by_junction()
        self.print_connections()

    # def get_all_connections(self):
    #     # This is a placeholder implementation
    #     # You need to adjust it to match your data structure
    #     connections = []
    #     for node in self.nodes:
    #         if node.connections:  # Assuming each node has a 'connections' attribute
    #             for connected_node in node.connections:
    #                 connections.append((node.id, connected_node.id))  # Adjust based on your structure
    #     return connections

    def open_translate_screen(self):
        self.circuit_graph.merge_nodes_by_junction()
        self.print_connections()

        num_nodes = len(self.circuit_graph.nodes)
        connections = self.circuit_graph.get_all_connections()

        translate_window = tk.Toplevel(self.master)
        translate_window.title("Translate Screen")
        translate_app = TranslateScreen(translate_window, num_nodes, connections)
        translate_app.color_dots_based_on_nodes(num_nodes)

        # Create a thread to send the matrix without blocking the GUI
        matrix = translate_app.generate_matrix_for_esp()
        send_thread = threading.Thread(target=send_matrix, args=(matrix,))
        send_thread.start()

        # Optional: print a message to the console
        print("Sending matrix to ESP...")



    
    def enable_edit_mode(self):
        self.is_edit_mode = True
        self.update_status("Edit", color='black')


    def canvas_click_handler(self, event):
        if self.is_edit_mode:
            self.handle_edit(event)
        else:
            self.place_component_or_start_wire_or_delete(event)

    def handle_edit(self, event):
        clicked_item = self.canvas.find_closest(event.x, event.y)[0]
        for component in self.component_objects:
            if clicked_item in component.id and not isinstance(component, Wire):
                component.edit()
                break

    def draw_grid(self):
        width = self.canvas.winfo_reqwidth()
        height = self.canvas.winfo_reqheight()
        for x in range(0, width, self.grid_size):
            for y in range(0, height, self.grid_size):
                self.canvas.create_oval(x-2, y-2, x+2, y+2, fill='gray')
    
    def add_component(self, component):
        self.component_objects.append(component)
        self.occupied_positions.add((component.x, component.y))
        component.draw()
        self.circuit_graph.add_component(component)


    def select_component_type(self, component_cls):
        self.is_delete_mode = False
        self.selected_component_type = component_cls
        self.is_drawing_wire = (component_cls == Wire)

    def toggle_delete_mode(self):
        self.is_delete_mode = not self.is_delete_mode
        self.update_status("Delete", color='black')


    def print_connections(self):
        # Merge nodes by junction to ensure the connections are up-to-date.
        self.circuit_graph.merge_nodes_by_junction()
        
        # Print the updated connections.
        self.circuit_graph.print_connections()

    
    def get_node_id(self, x, y):
        # A utility method to generate a unique identifier for a node based on its position
        return f"{x},{y}"
    
    def update_connections(self, start_x, start_y, end_x, end_y, wire):
        start_comp = self.find_component_at(start_x, start_y)
        end_comp = self.find_component_at(end_x, end_y)
        if start_comp and end_comp:
            # Adjusted to send a list of components including the wire
            components = [start_comp, end_comp, wire]
            self.circuit_graph.create_node(components)
    
    def update_status(self, status, color='black'):
        self.status_label.config(text=f"Status: {status}", fg=color)
    
    def select_component_type(self, component_cls):
        self.is_delete_mode = False
        self.selected_component_type = component_cls
        self.is_drawing_wire = (component_cls == Wire)

        # Map of component class names to their associated colors
        component_colors = {
            'Resistor': 'gray',
            'DCPowerSource': 'gold',
            'Ground': 'green',
            'Inductor': 'purple',
            'Capacitor': 'blue',
            'Junction': 'red',  # Assuming red for Junction, adjust if necessary
            'Wire': 'black'
        }
        
        # Get the color for the selected component, defaulting to black if not found
        color = component_colors.get(component_cls.__name__, 'black')
        
        self.update_status(component_cls.__name__, color=color)


    def find_component_at(self, x, y):
        for comp in self.component_objects:
            if comp.x == x and comp.y == y:
                return comp
        return None

    
    def place_component_or_start_wire_or_delete(self, event):
        grid_x, grid_y = round(event.x / self.grid_size) * self.grid_size, round(event.y / self.grid_size) * self.grid_size
        clicked_item = self.canvas.find_closest(event.x, event.y)[0]

        if self.is_edit_mode:
            self.handle_edit(event)
            self.is_edit_mode = False
            return
        elif self.is_delete_mode:
            component_to_delete = next((comp for comp in self.component_objects if clicked_item in comp.id), None)
            if component_to_delete:
                self.delete_component(component_to_delete)
        elif self.is_drawing_wire:
            if self.wire_start_x is None and (grid_x, grid_y) in self.occupied_positions:
                self.wire_start_x, self.wire_start_y = grid_x, grid_y
            elif self.wire_start_x is not None and (grid_x, grid_y) in self.occupied_positions:
                wire = Wire(self.canvas, self.wire_start_x, self.wire_start_y)
                wire.end_x, wire.end_y = grid_x, grid_y
                wire.draw()
                self.component_objects.append(wire)
                self.update_connections(self.wire_start_x, self.wire_start_y, grid_x, grid_y, wire)
                self.wire_start_x, self.wire_start_y = None, None
        else:
            if (grid_x, grid_y) not in self.occupied_positions:
                if self.selected_component_type:
                    component = self.selected_component_type(self.canvas, grid_x, grid_y)
                    self.add_component(component)
                    self.occupied_positions.add((grid_x, grid_y))
                    self.reconnect_components_if_applicable(grid_x, grid_y, component)



    def handle_wire_logic(self, grid_x, grid_y):
        if self.wire_start_x is not None and (grid_x, grid_y) in self.occupied_positions:
            wire = Wire(self.canvas, self.wire_start_x, self.wire_start_y)
            wire.end_x, wire.end_y = grid_x, grid_y
            wire.draw()
            self.add_component(wire)
            start_component = self.find_component_at(self.wire_start_x, self.wire_start_y)
            end_component = self.find_component_at(grid_x, grid_y)
            if start_component and end_component:
                node_label = self.circuit_graph.create_node(start_component, end_component, wire)
                print(f"Wire added to Node {node_label}")



    def delete_component(self, component_to_delete):
        if messagebox.askyesno("Confirm Delete", "Delete this component?"):
            self.circuit_graph.delete_component(component_to_delete)
            self.occupied_positions.discard((component_to_delete.x, component_to_delete.y))
            self.component_objects.remove(component_to_delete)
            component_to_delete.delete()

    
    def find_wires_for_component(self, component):
        connected_wires = []
        for wire in [comp for comp in self.component_objects if isinstance(comp, Wire)]:
            if hasattr(wire, 'start_comp') and hasattr(wire, 'end_comp'):
                if wire.start_comp == component or wire.end_comp == component:
                    connected_wires.append(wire)
        return connected_wires

    
    def delete_wire(self, wire):
        # First, remove the wire from the CircuitGraph
        self.circuit_graph.delete_wire(wire)
        # Then, remove it from the list of component objects
        self.component_objects.remove(wire)
        # Finally, delete the wire's drawing from the canvas
        wire.delete()
    
    def reconnect_components_if_applicable(self, x, y, new_component):
        connected_components = [comp for comp in self.find_components_connected_to_junction(x, y) if comp != new_component]
        if connected_components:
            node_label = self.circuit_graph.find_or_create_node_for_junction([new_component] + connected_components)
            for comp in connected_components:
                self.circuit_graph._register_node_with_component(node_label, comp)

    def find_components_connected_to_junction(self, x, y):
        connected_components = []
        for component in self.component_objects:
            if (component.x, component.y) == (x, y) and component != self:
                connected_components.append(component)
        return connected_components

    def remove_connections(self, wire):
        start_node = self.get_node_id(wire.x, wire.y)
        end_node = self.get_node_id(wire.end_x, wire.end_y)
        if start_node in self.node_connections:
            self.node_connections[start_node].remove(wire)
            if not self.node_connections[start_node]:
                del self.node_connections[start_node]
        if end_node in self.node_connections:
            self.node_connections[end_node].remove(wire)
            if not self.node_connections[end_node]:
                del self.node_connections[end_node]
        print(f"Disconnected wire between ({wire.x}, {wire.y}) and ({wire.end_x}, {wire.end_y})")


    def run(self):
        self.master.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = CircuitSimulator(root)
    app.run()
