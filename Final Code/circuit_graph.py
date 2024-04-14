                                                                                                                                                                        
class CircuitGraph:
    def __init__(self):
        self.components = {}
        self.nodes = {}
        self.next_node_label = 'A'
        #self.components= {}

    def add_component(self, component):
        if component not in self.components:
            self.components[component] = []
    
    def reset_graph(self):
        self.components.clear()
        self.nodes.clear()
        self.next_node_label = 'A'
        print("All connections and components have been cleared from the graph.")
        

    def create_node(self, components):
        node_label = self.next_node_label
        self.next_node_label = chr(ord(node_label) + 1)
        self.nodes[node_label] = []
        for component in components:
            self._register_node_with_component(node_label, component)
        return node_label


    def find_or_create_node_for_junction(self, junction_components):
        all_related_nodes = set()
        for comp in junction_components:
            if comp in self.components:
                for node in self.components[comp]:
                    all_related_nodes.add(node)
        
        if all_related_nodes:
            primary_node_label = all_related_nodes.pop()
            while all_related_nodes:
                node_to_merge = all_related_nodes.pop()
                self._merge_nodes(primary_node_label, node_to_merge)
            return primary_node_label
        else:
            return self.create_node(junction_components)
    
    def _merge_nodes(self, primary_node_label, node_to_merge):
        for comp in self.nodes[node_to_merge]:
            if comp not in self.nodes[primary_node_label]:
                self.nodes[primary_node_label].append(comp)
                # Update the component's nodes list
                self.components[comp] = [primary_node_label if x == node_to_merge else x for x in self.components[comp]]
        del self.nodes[node_to_merge]

    
    def merge_nodes_by_junction(self):
        junctions_in_nodes = {}
        for node_label, components in list(self.nodes.items()):
            junctions = [comp for comp in components if getattr(comp, 'is_junction', False)]
            for junction in junctions:
                if junction.label not in junctions_in_nodes:
                    junctions_in_nodes[junction.label] = node_label
                else:
                    target_node = junctions_in_nodes[junction.label]
                    # Pass node_label directly without wrapping it in a list
                    self._merge_nodes(target_node, node_label)

        # Cleanup after merging
        self.cleanup_empty_nodes()
    
    def _register_node_with_component(self, node_label, component):
        if component not in self.components:
            self.components[component] = []
        if node_label not in self.components[component]:
            self.components[component].append(node_label)
        if component not in self.nodes[node_label]:
            self.nodes[node_label].append(component)


    def get_all_connections(self):
        connections_dict = {}
        for node_label, components in self.nodes.items():
            # Filter out the wires and only include components with a label attribute
            filtered_components = [comp for comp in components if hasattr(comp, 'label') and not hasattr(comp, 'end_x')]
            connections = [comp.label for comp in filtered_components]
            connections_dict[node_label] = connections
        return connections_dict

    def delete_wire(self, wire):
        for node_label, components in list(self.nodes.items()):
            if wire in components:
                components.remove(wire)
                if len(components) < 2:
                    del self.nodes[node_label]
                    for comp in list(components):
                        if comp in self.components and node_label in self.components[comp]:
                            self.components[comp].remove(node_label)
                break


    def print_connections(self):
        for node_label, components in self.nodes.items():
            print(f"Node \"{node_label}\" connections:")
            for comp in components:
                # Skip printing wires
                if not hasattr(comp, 'end_x') and hasattr(comp, 'label'):
                    print(f"- {comp.label}")


    def cleanup_empty_nodes(self):
        empty_nodes = [node for node, comps in self.nodes.items() if len(comps) < 2]
        for node in empty_nodes:
            del self.nodes[node]
