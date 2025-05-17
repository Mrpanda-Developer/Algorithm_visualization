import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque

class FlowNetwork:
    def __init__(self):
        self.adj = {}
        self.flow = {}
        self.capacity = {}
    
    def add_vertex(self, vertex):
        self.adj[vertex] = []
    
    def add_edge(self, u, v, capacity):
        if u not in self.adj:
            self.add_vertex(u)
        if v not in self.adj:
            self.add_vertex(v)
        self.adj[u].append(v)
        self.adj[v].append(u)  # for residual graph
        self.capacity[(u, v)] = capacity
        self.capacity[(v, u)] = 0  # residual capacity
        self.flow[(u, v)] = 0
        self.flow[(v, u)] = 0
    
    def bfs(self, s, t, parent):
        """BFS for Edmonds-Karp algorithm"""
        visited = {v: False for v in self.adj}
        queue = deque()
        queue.append(s)
        visited[s] = True
        
        while queue:
            u = queue.popleft()
            
            for v in self.adj[u]:
                if not visited[v] and self.capacity[(u, v)] > self.flow[(u, v)]:
                    visited[v] = True
                    parent[v] = u
                    queue.append(v)
                    if v == t:
                        return True
        return False
    
    def dfs(self, u, t, visited, path):
        """DFS for Ford-Fulkerson algorithm"""
        if u == t:
            return path
        visited.add(u)
        for v in self.adj[u]:
            if v not in visited and self.capacity[(u, v)] > self.flow[(u, v)]:
                result = self.dfs(v, t, visited, path + [(u, v)])
                if result is not None:
                    return result
        return None
    
    def edmonds_karp(self, source, sink, visualize_callback=None):
        """Edmonds-Karp algorithm (BFS-based Ford-Fulkerson)"""
        parent = {}
        max_flow = 0
        
        while self.bfs(source, sink, parent):
            path_flow = float('inf')
            v = sink
            
            # Find minimum residual capacity of the path
            while v != source:
                u = parent[v]
                path_flow = min(path_flow, self.capacity[(u, v)] - self.flow[(u, v)])
                v = u
            
            # Update flow values
            v = sink
            while v != source:
                u = parent[v]
                self.flow[(u, v)] += path_flow
                self.flow[(v, u)] -= path_flow  # residual flow
                v = u
            
            max_flow += path_flow
            if visualize_callback:
                visualize_callback(f"Edmonds-Karp: Augmenting path found, flow = {path_flow}")
        
        if visualize_callback:
            visualize_callback(f"Edmonds-Karp: Final flow = {max_flow}")
        return max_flow
    
    def ford_fulkerson(self, source, sink, visualize_callback=None):
        """Ford-Fulkerson algorithm (DFS-based)"""
        max_flow = 0
        
        while True:
            path = self.dfs(source, sink, set(), [])
            if path is None:
                break
                
            # Find minimum residual capacity of the path
            path_flow = min(self.capacity[(u, v)] - self.flow[(u, v)] for (u, v) in path)
            
            # Update flow values
            for u, v in path:
                self.flow[(u, v)] += path_flow
                self.flow[(v, u)] -= path_flow  # residual flow
            
            max_flow += path_flow
            if visualize_callback:
                visualize_callback(f"Ford-Fulkerson: Augmenting path found, flow = {path_flow}")
        
        if visualize_callback:
            visualize_callback(f"Ford-Fulkerson: Final flow = {max_flow}")
        return max_flow
    
    def find_min_cut(self, source):
        """Find the min-cut after running max flow algorithm"""
        visited = set()
        queue = deque([source])
        visited.add(source)
        
        while queue:
            u = queue.popleft()
            for v in self.adj[u]:
                if v not in visited and self.capacity[(u, v)] > self.flow[(u, v)]:
                    visited.add(v)
                    queue.append(v)
        
        # Min-cut edges are those from visited to non-visited with capacity > 0
        min_cut_edges = []
        for u in visited:
            for v in self.adj[u]:
                if v not in visited and self.capacity[(u, v)] > 0:
                    min_cut_edges.append((u, v))
        
        return (visited, min_cut_edges)

class NetworkVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Max Flow Algorithm Visualizer")
        self.network = FlowNetwork()
        self.animation_speed = 500  # ms between steps
        self.animation_running = False
        self.current_algorithm = None
        
        # Create main frames
        self.control_frame = ttk.Frame(root, padding="10")
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        self.canvas_frame = ttk.Frame(root, padding="10")
        self.canvas_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        
        self.info_frame = ttk.Frame(root, padding="10")
        self.info_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Control panel
        ttk.Label(self.control_frame, text="Network Controls", font=('Helvetica', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=5)
        
        ttk.Button(self.control_frame, text="Add Node", command=self.add_node_dialog).grid(row=1, column=0, pady=5, sticky='ew')
        ttk.Button(self.control_frame, text="Add Edge", command=self.add_edge_dialog).grid(row=1, column=1, pady=5, sticky='ew')
        ttk.Button(self.control_frame, text="Clear Network", command=self.clear_network).grid(row=2, column=0, columnspan=2, pady=5, sticky='ew')
        
        ttk.Separator(self.control_frame, orient=tk.HORIZONTAL).grid(row=3, column=0, columnspan=2, pady=10, sticky='ew')
        
        ttk.Label(self.control_frame, text="Algorithm", font=('Helvetica', 12, 'bold')).grid(row=4, column=0, columnspan=2, pady=5)
        
        self.algorithm_var = tk.StringVar(value="edmonds_karp")
        ttk.Radiobutton(self.control_frame, text="Edmonds-Karp (BFS)", variable=self.algorithm_var, value="edmonds_karp").grid(row=5, column=0, columnspan=2, sticky='w')
        ttk.Radiobutton(self.control_frame, text="Ford-Fulkerson (DFS)", variable=self.algorithm_var, value="ford_fulkerson").grid(row=6, column=0, columnspan=2, sticky='w')
        
        ttk.Button(self.control_frame, text="Run Algorithm", command=self.run_algorithm).grid(row=7, column=0, columnspan=2, pady=10, sticky='ew')
        ttk.Button(self.control_frame, text="Step Algorithm", command=self.step_algorithm).grid(row=8, column=0, columnspan=2, pady=5, sticky='ew')
        
        ttk.Separator(self.control_frame, orient=tk.HORIZONTAL).grid(row=9, column=0, columnspan=2, pady=10, sticky='ew')
        
        self.speed_scale = ttk.Scale(self.control_frame, from_=100, to=2000, orient=tk.HORIZONTAL, 
                                    command=self.update_speed, value=self.animation_speed)
        self.speed_scale.grid(row=10, column=0, columnspan=2, pady=5, sticky='ew')
        ttk.Label(self.control_frame, text="Animation Speed").grid(row=11, column=0, columnspan=2)
        
        # Canvas for drawing
        self.canvas = tk.Canvas(self.canvas_frame, bg='white', width=600, height=400)
        self.canvas.pack(expand=True, fill=tk.BOTH)
        self.canvas.bind("<Configure>", self.draw_network)
        
        # Info panel
        self.info_text = tk.Text(self.info_frame, height=10, wrap=tk.WORD)
        self.info_text.pack(expand=True, fill=tk.BOTH)
        self.info_scroll = ttk.Scrollbar(self.info_frame, orient=tk.VERTICAL, command=self.info_text.yview)
        self.info_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.info_text.config(yscrollcommand=self.info_scroll.set)
        
        # Node positions for visualization
        self.node_positions = {}
        self.node_radius = 20
        self.highlighted_path = []
        self.min_cut_edges = []
        
        # Example network
        self.create_example_network()
    
    def update_speed(self, value):
        self.animation_speed = int(float(value))
    
    def log(self, message):
        self.info_text.insert(tk.END, message + "\n")
        self.info_text.see(tk.END)
        self.root.update()
    
    def add_node_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Node")
        
        ttk.Label(dialog, text="Node Name:").grid(row=0, column=0, padx=5, pady=5)
        node_entry = ttk.Entry(dialog)
        node_entry.grid(row=0, column=1, padx=5, pady=5)
        
        def add_node():
            name = node_entry.get().strip()
            if name:
                if name in self.network.adj:
                    messagebox.showerror("Error", f"Node '{name}' already exists!")
                else:
                    self.network.add_vertex(name)
                    self.draw_network()
                    dialog.destroy()
            else:
                messagebox.showerror("Error", "Node name cannot be empty!")
        
        ttk.Button(dialog, text="Add", command=add_node).grid(row=1, column=0, columnspan=2, pady=5)
        node_entry.focus()
    
    def add_edge_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Edge")
        
        ttk.Label(dialog, text="From Node:").grid(row=0, column=0, padx=5, pady=5)
        from_entry = ttk.Entry(dialog)
        from_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="To Node:").grid(row=1, column=0, padx=5, pady=5)
        to_entry = ttk.Entry(dialog)
        to_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Capacity:").grid(row=2, column=0, padx=5, pady=5)
        capacity_entry = ttk.Entry(dialog)
        capacity_entry.grid(row=2, column=1, padx=5, pady=5)
        
        def add_edge():
            u = from_entry.get().strip()
            v = to_entry.get().strip()
            capacity = capacity_entry.get().strip()
            
            if not u or not v:
                messagebox.showerror("Error", "Both nodes must be specified!")
                return
            
            try:
                capacity = int(capacity)
                if capacity <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Capacity must be a positive integer!")
                return
            
            if u not in self.network.adj or v not in self.network.adj:
                messagebox.showerror("Error", "One or both nodes don't exist!")
                return
            
            self.network.add_edge(u, v, capacity)
            self.draw_network()
            dialog.destroy()
        
        ttk.Button(dialog, text="Add", command=add_edge).grid(row=3, column=0, columnspan=2, pady=5)
        from_entry.focus()
    
    def clear_network(self):
        self.network = FlowNetwork()
        self.node_positions = {}
        self.highlighted_path = []
        self.min_cut_edges = []
        self.canvas.delete("all")
        self.info_text.delete(1.0, tk.END)
        self.log("Network cleared.")
    
    def create_example_network(self):
        self.clear_network()
        
        # Add edges (u, v, capacity)
        self.network.add_edge('s', 'a', 10)
        self.network.add_edge('s', 'b', 5)
        self.network.add_edge('a', 'b', 15)
        self.network.add_edge('a', 'c', 5)
        self.network.add_edge('b', 'c', 10)
        self.network.add_edge('b', 'd', 15)
        self.network.add_edge('c', 'd', 10)
        self.network.add_edge('d', 't', 10)
        self.network.add_edge('c', 't', 15)
        
        self.log("Example network loaded with nodes: s (source), a, b, c, d, t (sink)")
        self.draw_network()
    
    def calculate_node_positions(self, canvas_width, canvas_height):
        if not self.network.adj:
            return {}
        
        nodes = list(self.network.adj.keys())
        positions = {}
        
        # Special handling for source and sink
        if 's' in nodes:
            positions['s'] = (canvas_width * 0.2, canvas_height / 2)
            nodes.remove('s')
        if 't' in nodes:
            positions['t'] = (canvas_width * 0.8, canvas_height / 2)
            nodes.remove('t')
        
        # Position remaining nodes in layers
        num_nodes = len(nodes)
        for i, node in enumerate(nodes):
            x = canvas_width * 0.2 + (i+1) * (canvas_width * 0.6 / (num_nodes + 1))
            y = canvas_height / 2 + (i % 2) * (canvas_height * 0.3) - (canvas_height * 0.15)
            positions[node] = (x, y)
        
        return positions
    
    def draw_network(self, event=None):
        self.canvas.delete("all")
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if not self.node_positions or event:  # Recalculate positions if window was resized
            self.node_positions = self.calculate_node_positions(canvas_width, canvas_height)
        
        # Draw edges
        for u in self.network.adj:
            for v in self.network.adj[u]:
                if (u, v) in self.network.capacity and self.network.capacity[(u, v)] > 0:  # Only original edges
                    start_x, start_y = self.node_positions[u]
                    end_x, end_y = self.node_positions[v]
                    
                    # Calculate arrow position (don't draw on node circle)
                    angle = self.calculate_angle(start_x, start_y, end_x, end_y)
                    start_x += self.node_radius * 0.9 * angle[0]
                    start_y += self.node_radius * 0.9 * angle[1]
                    end_x -= self.node_radius * 0.9 * angle[0]
                    end_y -= self.node_radius * 0.9 * angle[1]
                    
                    # Draw edge
                    edge_color = "black"
                    width = 2
                    
                    # Highlight if in current path
                    if (u, v) in self.highlighted_path:
                        edge_color = "green"
                        width = 3
                    
                    # Highlight if in min cut
                    if (u, v) in self.min_cut_edges:
                        edge_color = "red"
                        width = 3
                    
                    self.canvas.create_line(start_x, start_y, end_x, end_y, 
                                          fill=edge_color, width=width, arrow=tk.LAST)
                    
                    # Draw flow/capacity label
                    mid_x = (start_x + end_x) / 2
                    mid_y = (start_y + end_y) / 2
                    label = f"{self.network.flow[(u, v)]}/{self.network.capacity[(u, v)]}"
                    self.canvas.create_text(mid_x, mid_y, text=label, fill="blue")
        
        # Draw nodes
        for node, (x, y) in self.node_positions.items():
            fill_color = "lightblue"
            if node == 's':
                fill_color = "lightgreen"
            elif node == 't':
                fill_color = "salmon"
            
            self.canvas.create_oval(x - self.node_radius, y - self.node_radius,
                                  x + self.node_radius, y + self.node_radius,
                                  fill=fill_color, outline="black")
            self.canvas.create_text(x, y, text=node)
    
    def calculate_angle(self, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        length = (dx**2 + dy**2)**0.5
        if length == 0:
            return (0, 0)
        return (dx/length, dy/length)
    
    def run_algorithm(self):
        if self.animation_running:
            return
        
        if not self.network.adj:
            messagebox.showerror("Error", "Network is empty!")
            return
        
        if 's' not in self.network.adj or 't' not in self.network.adj:
            messagebox.showerror("Error", "Network must have a source (s) and sink (t)!")
            return
        
        # Reset flow values
        for edge in self.network.flow:
            self.network.flow[edge] = 0
        
        self.highlighted_path = []
        self.min_cut_edges = []
        self.info_text.delete(1.0, tk.END)
        
        algorithm = self.algorithm_var.get()
        self.current_algorithm = algorithm
        
        if algorithm == "edmonds_karp":
            self.log("Running Edmonds-Karp algorithm (BFS-based)...")
            self.animate_algorithm(self.network.edmonds_karp, 's', 't')
        else:
            self.log("Running Ford-Fulkerson algorithm (DFS-based)...")
            self.animate_algorithm(self.network.ford_fulkerson, 's', 't')
    
    def step_algorithm(self):
        if self.animation_running:
            return
        
        if not self.current_algorithm:
            messagebox.showerror("Error", "Please run an algorithm first!")
            return
        
        # This is a simplified step-through for demonstration
        # In a real implementation, we would need to modify the algorithms to support stepping
        messagebox.showinfo("Info", "Stepping through algorithms requires more complex implementation.\nPlease use 'Run Algorithm' for full visualization.")
    
    def animate_algorithm(self, algorithm_func, source, sink):
        self.animation_running = True
        
        def algorithm_wrapper():
            max_flow = algorithm_func(source, sink, self.log)
            
            # After algorithm completes, show min-cut
            S, min_cut_edges = self.network.find_min_cut(source)
            self.min_cut_edges = min_cut_edges
            self.log(f"\nMinimum Cut:")
            self.log(f"S: {S}")
            self.log(f"T: {set(self.network.adj.keys()) - S}")
            self.log(f"Edges in min-cut: {min_cut_edges}")
            self.log(f"Capacity of min-cut: {sum(self.network.capacity[e] for e in min_cut_edges)}")
            self.log(f"Max flow: {max_flow}")
            
            self.draw_network()
            self.animation_running = False
        
        # Run algorithm in a separate thread to avoid freezing GUI
        import threading
        thread = threading.Thread(target=algorithm_wrapper)
        thread.daemon = True
        thread.start()

def main():
    root = tk.Tk()
    app = NetworkVisualizer(root)
    root.mainloop()

if __name__ == "__main__":
    main()