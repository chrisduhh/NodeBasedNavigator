import tkinter as tk
from tkinter import ttk
import heapq

def dijkstra(graph, start, end, is_disabled=False, is_emergency=False):
    # Priority queue to store nodes with their tentative distances
    priority_queue = [(0, start)]
    
    # Dictionary to store tentative distances
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    
    # Dictionary to store the previous node in the shortest path
    previous = {node: None for node in graph}
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node == end:
            # Reached the destination, reconstruct the path
            path = []
            while current_node is not None:
                path.insert(0, current_node)
                current_node = previous[current_node]
            return current_distance, path

        if current_distance > distances[current_node]:
            # Skip if the current distance is greater than the known distance
            continue

        for neighbor in graph[current_node]:
            distance = current_distance + graph[current_node][neighbor].get('Weight', 0)

            # Check if the user is disabled and if there is a lift available
            if is_disabled and graph[current_node][neighbor].get('Type', '') == 'Stairs':
                # Skip stairs if the user is disabled
                continue
            elif not is_disabled and graph[current_node][neighbor].get('Type', '') == 'Lift':
                # Skip lift if it's on the same or lower floor or not in emergency mode
                if distances[current_node] > distances[neighbor] or (not is_emergency and not graph[current_node][neighbor].get('Emergency', False)):
                    continue
            elif graph[current_node][neighbor].get('Type', '') == 'Safe':
                # Skip safe room if not in emergency mode
                if not is_emergency:
                    continue
            elif graph[current_node][neighbor].get('Type', '') == 'EmergencyExit':
                # Skip emergency exit if not in emergency mode
                if not is_emergency:
                    continue
            else:
                distance += graph[current_node][neighbor].get('Weight', 0)  # No adjustment needed for non-stairs/non-lift nodes

            if distance < distances[neighbor]:
                # Update the tentative distance and previous node
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    # If no path is found
    return float('infinity'), []

# Function to find the path and update the GUI
def find_path():
    start_node = start_node_var.get()
    is_disabled_user = is_disabled_var.get()
    is_emergency_user = is_emergency_var.get()

    # Check if the Coffee Break checkbox is pressed
    if is_coffee_break_var.get():
        end_node = "Hallway3-B"
        end_node_var.set(end_node)
        end_node_dropdown.config(state="disabled")  # Disable the end node dropdown
    # Check if the Lunch Break checkbox is pressed
    elif is_lunch_break_var.get():
        end_node = "Canteen"
        end_node_var.set(end_node)
        end_node_dropdown.config(state="disabled")  # Disable the end node dropdown
    # If in emergency mode, set the end node to "Safe"
    elif is_emergency_user:
        end_node = "Safe"
        end_node_var.set(end_node)
        end_node_dropdown.config(state="disabled")  # Disable the end node dropdown
    else:
        end_node = end_node_var.get()
        end_node_dropdown.config(state="normal")  # Enable the end node dropdown

    shortest_distance, path = dijkstra(school_map, start_node, end_node, is_disabled=is_disabled_user, is_emergency=is_emergency_user)

    # Display the result
    result_label.config(text=f"Shortest Distance: {shortest_distance}")
    path_label.config(text=f"Shortest Path: {path}")

# Updated example graph representation with floor information, divisions, and corrected connections
# Format: {node: {neighbor1: {'Type': type1, 'Weight': weight1}, neighbor2: {...}, ...}}
school_map = {
    'Classroom1-3-B': {'Hallway3-B': {'Type': 'Hallway', 'Weight': 1}},
    'Classroom2-3-B': {'Hallway3-B': {'Type': 'Hallway', 'Weight': 1}},
    'Classroom3-3-B': {'Hallway3-B': {'Type': 'Hallway', 'Weight': 1}},
    'Classroom4-3-B': {'Hallway3-B': {'Type': 'Hallway', 'Weight': 1}},
    'Classroom5-3-B': {'Hallway3-B': {'Type': 'Hallway', 'Weight': 1}},
    'Classroom6-3-B': {'Hallway3-B': {'Type': 'Hallway', 'Weight': 1}},
    'Classroom7-3-B': {'Hallway3-B': {'Type': 'Hallway', 'Weight': 1}},
    'Classroom8-3-B': {'Hallway3-B': {'Type': 'Hallway', 'Weight': 1}},
    'Classroom1-3-C': {'Hallway3-C': {'Type': 'Hallway', 'Weight': 1}},
    'Classroom2-3-C': {'Hallway3-C': {'Type': 'Hallway', 'Weight': 1}},
    'Classroom3-3-C': {'Hallway3-C': {'Type': 'Hallway', 'Weight': 1}},
    'Classroom4-3-C': {'Hallway3-C': {'Type': 'Hallway', 'Weight': 1}},
    'Classroom5-3-C': {'Hallway3-C': {'Type': 'Hallway', 'Weight': 1}},
    'Classroom6-3-C': {'Hallway3-C': {'Type': 'Hallway', 'Weight': 1}},
    'Classroom7-3-C': {'Hallway3-C': {'Type': 'Hallway', 'Weight': 1}},
    'Classroom8-3-C': {'Hallway3-C': {'Type': 'Hallway', 'Weight': 1}},
    'Hallway0-B': {'Stairs0-B': {'Type': 'Stairs', 'Weight': 1},
                  'EmergencyExit0-B': {'Type': 'EmergencyExit', 'Weight': 1},
                  'MainHall': {'Type': 'Hallway', 'Weight': 1}},
    'Hallway1-B': {'Stairs1-B': {'Type': 'Stairs', 'Weight': 1},
                  'EmergencyExit1-B': {'Type': 'EmergencyExit', 'Weight': 1},
                  'Hallway1-C': {'Type': 'Hallway', 'Weight': 1}},
    'Hallway2-B': {'Stairs2-B': {'Type': 'Stairs', 'Weight': 1},
                  'EmergencyExit2-B': {'Type': 'EmergencyExit', 'Weight': 1},
                  'Hallway2-C': {'Type': 'Hallway', 'Weight': 1}},                  
    'Hallway3-B': {'Classroom1-3-B': {'Type': 'Classroom', 'Weight': 1},
                  'Classroom2-3-B': {'Type': 'Classroom', 'Weight': 1},
                  'Classroom3-3-B': {'Type': 'Classroom', 'Weight': 1},
                  'Classroom4-3-B': {'Type': 'Classroom', 'Weight': 1},
                  'Classroom5-3-B': {'Type': 'Classroom', 'Weight': 1},
                  'Classroom6-3-B': {'Type': 'Classroom', 'Weight': 1},
                  'Classroom7-3-B': {'Type': 'Classroom', 'Weight': 1},
                  'Classroom8-3-B': {'Type': 'Classroom', 'Weight': 1},
                  'Stairs3-B': {'Type': 'Stairs', 'Weight': 1},
                  'EmergencyExit3-B': {'Type': 'EmergencyExit', 'Weight': 1},
                  'Hallway3-C': {'Type': 'Hallway', 'Weight': 1}},
    'Stairs0-B': {'Hallway0-B': {'Type': 'Hallway', 'Weight': 1},
                  'Stairs1-B': {'Type': 'Stairs', 'Weight': 1}},
    'Stairs1-B': {'Hallway1-B': {'Type': 'Hallway', 'Weight': 1},
                  'Stairs2-B': {'Type': 'Stairs', 'Weight': 1},
                  'Stairs0-B': {'Type': 'Stairs', 'Weight': 1}},
    'Stairs2-B': {'Hallway2-B': {'Type': 'Hallway', 'Weight': 1},
                  'Stairs3-B': {'Type': 'Stairs', 'Weight': 1},
                  'Stairs1-B': {'Type': 'Stairs', 'Weight': 1}},
    'Stairs3-B': {'Hallway3-B': {'Type': 'Hallway', 'Weight': 1},
                  'Stairs2-B': {'Type': 'Stairs', 'Weight': 1}},
    'EmergencyExit0-B': {'Hallway0-B': {'Type': 'Hallway', 'Weight': 1},
                  'EmergencyExit1-B': {'Type': 'EmergencyExit', 'Weight': 1},
                  'Safe': {'Type': 'Safe', 'Weight': 1}},
    'EmergencyExit1-B': {'Hallway1-B': {'Type': 'Hallway', 'Weight': 1},
                  'EmergencyExit2-B': {'Type': 'EmergencyExit', 'Weight': 1},
                  'EmergencyExit0-B': {'Type': 'EmergencyExit', 'Weight': 1}},
    'EmergencyExit2-B': {'Hallway2-B': {'Type': 'Hallway', 'Weight': 1},
                  'EmergencyExit3-B': {'Type': 'EmergencyExit', 'Weight': 1},
                  'EmergencyExit1-B': {'Type': 'EmergencyExit', 'Weight': 1}},
    'EmergencyExit3-B': {'Hallway3-B': {'Type': 'Hallway', 'Weight': 1},
                  'EmergencyExit2-B': {'Type': 'EmergencyExit', 'Weight': 1}},
    'Hallway0-C': {'Stairs0-C': {'Type': 'Stairs', 'Weight': 1},
                  'Lift': {'Type': 'Lift', 'Weight': 1},
                  'MainHall': {'Type': 'Hallway', 'Weight': 1}},
    'Hallway1-C': {'Stairs1-C': {'Type': 'Stairs', 'Weight': 1},
                  'Lift': {'Type': 'Lift', 'Weight': 1},
                  'Hallway1-B': {'Type': 'Hallway', 'Weight': 1}},
    'Hallway2-C': {'Stairs2-C': {'Type': 'Stairs', 'Weight': 1},
                  'Lift': {'Type': 'Lift', 'Weight': 1},
                  'Hallway2-B': {'Type': 'Hallway', 'Weight': 1}},
    'Hallway3-C': {'Classroom1-3-C': {'Type': 'Classroom', 'Weight': 1},
                  'Classroom2-3-C': {'Type': 'Classroom', 'Weight': 1},
                  'Classroom3-3-C': {'Type': 'Classroom', 'Weight': 1},
                  'Classroom4-3-C': {'Type': 'Classroom', 'Weight': 1},
                  'Classroom5-3-C': {'Type': 'Classroom', 'Weight': 1},
                  'Classroom6-3-C': {'Type': 'Classroom', 'Weight': 1},
                  'Classroom7-3-C': {'Type': 'Classroom', 'Weight': 1},
                  'Classroom8-3-C': {'Type': 'Classroom', 'Weight': 1},
                  'Stairs3-C': {'Type': 'Stairs', 'Weight': 1},
                  'Lift': {'Type': 'Lift', 'Weight': 1},
                  'Hallway3-B': {'Type': 'Hallway', 'Weight': 1}},
    'Stairs0-C': {'Hallway0-C': {'Type': 'Hallway', 'Weight': 1},
                  'Stairs1-C': {'Type': 'Stairs', 'Weight': 1}},
    'Stairs1-C': {'Hallway1-C': {'Type': 'Hallway', 'Weight': 1},
                  'Stairs2-C': {'Type': 'Stairs', 'Weight': 1},
                  'Stairs0-C': {'Type': 'Stairs', 'Weight': 1}},
    'Stairs2-C': {'Hallway2-C': {'Type': 'Hallway', 'Weight': 1},
                  'Stairs3-C': {'Type': 'Stairs', 'Weight': 1},
                  'Stairs1-C': {'Type': 'Stairs', 'Weight': 1}},
    'Stairs3-C': {'Hallway3-C': {'Type': 'Hallway', 'Weight': 1},
                  'Stairs2-C': {'Type': 'Stairs', 'Weight': 1}},
    'Lift': {'Hallway0-C': {'Type': 'Lift', 'Weight': 1},
                  'Hallway1-C': {'Type': 'Lift', 'Weight': 1},
                  'Hallway2-C': {'Type': 'Lift', 'Weight': 1},
                  'Hallway3-C': {'Type': 'Lift', 'Weight': 1}},
    'MainHall': {'Hallway0-B': {'Type': 'Hallway', 'Weight': 1},
                  'Hallway0-C': {'Type': 'Hallway', 'Weight': 1},
                  'Canteen': {'Type': 'Hallway', 'Weight': 1}},
    'Canteen': {'MainHall': {'Type': 'Hallway', 'Weight': 1}},
    'Safe': {'EmergencyExit0-B': {'Type': 'EmergencyExit', 'Weight': 1}}
}

# Create the main Tkinter window
root = tk.Tk()
root.title("School Map Navigation")

# Create a main frame
mainframe = ttk.Frame(root, padding="10")
mainframe.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Variables for GUI elements
is_disabled_var = tk.BooleanVar()
is_emergency_var = tk.BooleanVar()
is_coffee_break_var = tk.BooleanVar()
is_lunch_break_var = tk.BooleanVar()
start_node_var = tk.StringVar()
end_node_var = tk.StringVar()

# Create GUI elements
is_disabled_checkbox = tk.Checkbutton(mainframe, text="Disabled", variable=is_disabled_var)
is_emergency_checkbox = tk.Checkbutton(mainframe, text="Emergency", variable=is_emergency_var)
coffee_break_checkbox = tk.Checkbutton(mainframe, text="Coffee Break", variable=is_coffee_break_var)
lunch_break_checkbox = tk.Checkbutton(mainframe, text="12:00 - 13:00 Lunch Break", variable=is_lunch_break_var)
start_node_label = tk.Label(mainframe, text="Start Node:")
start_node_dropdown = ttk.Combobox(mainframe, textvariable=start_node_var)
start_node_dropdown['values'] = tuple(school_map.keys())
end_node_label = tk.Label(mainframe, text="End Node:")
end_node_dropdown = ttk.Combobox(mainframe, textvariable=end_node_var)
end_node_dropdown['values'] = tuple(school_map.keys())
find_path_button = ttk.Button(mainframe, text="Find Path", command=find_path)
result_label = ttk.Label(mainframe, text="")
path_label = ttk.Label(mainframe, text="")  # Added path_label

# Arrange GUI elements in a grid
is_disabled_checkbox.grid(row=0, column=0, columnspan=2, sticky=tk.W)
is_emergency_checkbox.grid(row=6, column=0, columnspan=2, pady=(10, 0), sticky=tk.W)
coffee_break_checkbox.grid(row=7, column=0, columnspan=2, pady=(10, 0), sticky=tk.W)
lunch_break_checkbox.grid(row=8, column=0, columnspan=2, pady=(10, 0), sticky=tk.W)
start_node_label.grid(row=1, column=0, sticky=tk.W)
start_node_dropdown.grid(row=1, column=1, sticky=(tk.W, tk.E))
end_node_label.grid(row=2, column=0, sticky=tk.W)
end_node_dropdown.grid(row=2, column=1, sticky=(tk.W, tk.E))
find_path_button.grid(row=3, column=0, columnspan=2, pady=(10, 0))
result_label.grid(row=4, column=0, columnspan=2, pady=(10, 0))
path_label.grid(row=5, column=0, columnspan=2, pady=(10, 0))  # Positioned path_label in the grid

# Run the Tkinter event loop
root.mainloop()
