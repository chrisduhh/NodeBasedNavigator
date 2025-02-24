import tkinter as tk
from tkinter import ttk
import heapq
import timeit
import tracemalloc

# Function to handle multiple selected sessions and find the route
def find_route_through_sessions():
    start_node = start_node_var.get()
    end_node = end_node_var.get()
    is_disabled_user = is_disabled_var.get()
    is_emergency_user = is_emergency_var.get()

    # Create a list of selected sessions (nodes)
    selected_sessions = []
    for dropdown in session_dropdowns:
        session_name = dropdown.get()
        if session_name:  # If a session is selected
            selected_sessions.append(session_name)

    # If no sessions are selected, just find the route to the end node
    if not selected_sessions:
        selected_sessions = [end_node]

    # Calculate the route: start -> selected sessions -> end -> start
    total_path = []
    total_distance = 0

    # Find the route from start to the first selected session
    current_start = start_node
    for session in selected_sessions:
        session_node = session_to_node.get(session)  # Get the actual node for the session
        if session_node is None:
            continue  # Skip if no node is associated with the session

        distance, path = dijkstra(school_map, current_start, session_node, is_disabled=is_disabled_user, is_emergency=is_emergency_user)
        total_distance += distance
        total_path.extend(path[:-1])  # Exclude the current session as it's the next start
        current_start = session_node

    # Finally, find the route from the last session to the end node
    distance, path = dijkstra(school_map, current_start, end_node, is_disabled=is_disabled_user, is_emergency=is_emergency_user)
    total_distance += distance
    total_path.extend(path)

    # Multiply the distance by 7 (the map is based on the floor plan blocks, which are 7 meters by 7 meters) and display the result
    distance_in_meters = total_distance * 7

    # Update the GUI with the result
    result_label.config(text=f"Shortest Distance: {distance_in_meters} meters")
    path_label.config(text=f"Shortest Path: {total_path}")

def find_path():
    try:
        print("Starting find_path function.")  # Debug: start van de functie

        # Start measuring time
        start_time = timeit.default_timer()

        # Start tracing memory
        tracemalloc.start()

        # Debug: na tracemalloc en timeit start
        print("Timers and memory tracking started.")

        # Variabelen ophalen
        start_node = start_node_var.get()
        end_node = end_node_var.get()
        is_disabled_user = is_disabled_var.get()
        is_emergency_user = is_emergency_var.get()
        print(f"Start Node: {start_node}, End Node: {end_node}, Disabled: {is_disabled_user}, Emergency: {is_emergency_user}")

        # Emergency-modus
        if is_emergency_user:
            end_node = "Safe"
            end_node_var.set(end_node)
            end_node_dropdown.config(state="disabled")  # Disable the end node dropdown
            print("Emergency mode enabled. End node set to 'Safe'.")
        else:
            end_node_dropdown.config(state="normal")  # Enable the end node dropdown
            print("Normal mode enabled.")

        # Sessions-check
        if session_dropdowns:
            print("Session dropdowns detected. Calculating session route.")
            find_route_through_sessions()
        else:
            print("No session dropdowns. Calculating direct route.")
            shortest_distance, path = dijkstra(
                school_map, start_node, end_node,
                is_disabled=is_disabled_user, is_emergency=is_emergency_user
            )
            print(f"Shortest Distance: {shortest_distance}, Path: {path}")
            distance_in_meters = shortest_distance * 7

            # Update result labels
            result_label.config(text=f"Shortest Distance: {distance_in_meters} meters")
            path_label.config(text=f"Shortest Path: {path}")

        # Stop measuring time
        elapsed_time = timeit.default_timer() - start_time

        # Stop tracing memory
        _, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print(f"Elapsed Time: {elapsed_time:.6f} seconds")  # Debug: tijd
        print(f"Peak Memory Usage: {peak_memory / 1024:.2f} KiB")  # Debug: geheugen

        # Update time and memory labels
        time_label.config(text=f"Elapsed Time: {elapsed_time:.6f} seconds")
        memory_label.config(text=f"Peak Memory Usage: {peak_memory / 1024:.2f} KiB")
        root.update()

    except Exception as e:
        print(f"Error in find_path: {e}")  # Log de fout

# Dijkstra's algorithm to calculate shortest path
def dijkstra(graph, start, end, is_disabled=False, is_emergency=False):
    priority_queue = [(0, start)]
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    previous = {node: None for node in graph}

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node == end:
            path = []
            while current_node is not None:
                path.insert(0, current_node)
                current_node = previous[current_node]
            return current_distance, path

        if current_distance > distances[current_node]:
            continue

        for neighbor in graph[current_node]:
            distance = current_distance + graph[current_node][neighbor].get('Weight', 0)

            # Check if the user is disabled and if there is a lift available
            if is_disabled and graph[current_node][neighbor].get('Type', '') == 'Stairs':
                continue
            elif not is_disabled and graph[current_node][neighbor].get('Type', '') == 'Lift':
                if distances[current_node] > distances[neighbor] or (not is_emergency and not graph[current_node][neighbor].get('Emergency', False)):
                    continue
            elif graph[current_node][neighbor].get('Type', '') == 'Safe':
                if not is_emergency:
                    continue
            elif graph[current_node][neighbor].get('Type', '') == 'EmergencyExit':
                if not is_emergency:
                    continue
            else:
                distance += graph[current_node][neighbor].get('Weight', 0)

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    return float('infinity'), []

# Define the mapping between sessions and their nodes
session_to_node = {
    'Workshop Algorithms': 'ClassroomB-3-107',
    'Workshop Machine Learning': 'ClassroomB-3-104',
    'Workshop Development': 'ClassroomB-3-217',
    'Lunchpauze 40 min': 'Kantine',
    # Add other sessions as needed
}

# Updated example graph representation with floor information, divisions, and corrected connections
# Format: {node: {neighbor1: {'Type': type1, 'Weight': weight1}, neighbor2: {...}, ...}}
school_map = {

# Parkeerplaatsen
    'Parkeerplaats 1 (Mobiliteitsproblemen)': {'HallwayC-0-2': {'Type': 'Hallway', 'Weight': 1}},
    'Parkeerplaats 2': {'MainHall': {'Type': 'Hallway', 'Weight': 1}},
    'Parkeerplaats 3': {'MainHall': {'Type': 'Hallway', 'Weight': 1}},
    'Openbaar vervoer en fietsenstalling ingang': {'MainHall': {'Type': 'Hallway', 'Weight': 1}},

# Verdieping 3
	'ClassroomB-3-221': {'HallwayB-3-1': {'Type': 'Hallway', 'Weight': 1}},
	'ClassroomB-3-222': {'HallwayB-3-1': {'Type': 'Hallway', 'Weight': 1}},
	'ClassroomB-3-223': {'HallwayB-3-1': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-3-225': {'HallwayB-3-1': {'Type': 'Hallway', 'Weight': 2}},

	'ClassroomB-3-210A': {'HallwayB-3-1B': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-3-300': {'HallwayB-3-1B': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-3-302': {'HallwayB-3-1B': {'Type': 'Hallway', 'Weight': 1}},
	'ClassroomB-3-304': {'HallwayB-3-1B': {'Type': 'Hallway', 'Weight': 1}},
	'ClassroomB-3-306': {'HallwayB-3-1B': {'Type': 'Hallway', 'Weight': 1}},
	'ClassroomB-3-308': {'HallwayB-3-1B': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-3-310': {'HallwayB-3-1B': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-3-311': {'HallwayB-3-1B': {'Type': 'Hallway', 'Weight': 3}},
	'ClassroomB-3-309': {'HallwayB-3-1B': {'Type': 'Hallway', 'Weight': 3}},
	'ClassroomB-3-307': {'HallwayB-3-1B': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-3-312': {'HallwayB-3-1B': {'Type': 'Hallway', 'Weight': 1}},
	'ClassroomB-3-305': {'HallwayB-3-1B': {'Type': 'Hallway', 'Weight': 2}},

    'ClassroomB-3-200': {'HallwayB-3-2': {'Type': 'Hallway', 'Weight': 3}},
	'ClassroomB-3-206': {'HallwayB-3-2': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-3-208': {'HallwayB-3-2': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-3-210': {'HallwayB-3-2': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-3-209': {'HallwayB-3-2': {'Type': 'Hallway', 'Weight': 3}},
	'ClassroomB-3-211': {'HallwayB-3-2': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-3-213': {'HallwayB-3-2': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-3-215': {'HallwayB-3-2': {'Type': 'Hallway', 'Weight': 1}},
	'ClassroomB-3-217': {'HallwayB-3-2': {'Type': 'Hallway', 'Weight': 2}},

	'ClassroomB-3-103': {'HallwayB-3-3': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-3-105': {'HallwayB-3-3': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-3-107': {'HallwayB-3-3': {'Type': 'Hallway', 'Weight': 3}},
    'ClassroomB-3-104': {'HallwayB-3-3': {'Type': 'Hallway', 'Weight': 3}},
    'ClassroomB-3-106': {'HallwayB-3-3': {'Type': 'Hallway', 'Weight': 3}},
	'ClassroomB-3-108': {'HallwayB-3-3': {'Type': 'Hallway', 'Weight': 3}},
	'ClassroomB-3-110': {'HallwayB-3-3': {'Type': 'Hallway', 'Weight': 4}},
	'ClassroomB-3-111': {'HallwayB-3-3': {'Type': 'Hallway', 'Weight': 5}},
	'ClassroomB-3-112': {'HallwayB-3-3': {'Type': 'Hallway', 'Weight': 6}},
	'ClassroomB-3-114': {'HallwayB-3-3': {'Type': 'Hallway', 'Weight': 6}},

    'ClassroomC-3-101': {'HallwayC-3-1': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomC-3-103': {'HallwayC-3-1': {'Type': 'Hallway', 'Weight': 1}},
	'ClassroomC-3-105': {'HallwayC-3-1': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomC-3-107': {'HallwayC-3-1': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomC-3-031': {'HallwayC-3-1': {'Type': 'Hallway', 'Weight': 1}},
	
	'ClassroomC-3-203': {'HallwayC-3-2': {'Type': 'Hallway', 'Weight': 1}},
	'ClassroomC-3-203A': {'HallwayC-3-2': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomC-3-Uitleen': {'HallwayC-3-2': {'Type': 'Hallway', 'Weight': 3}},

    'HallwayB-3-1': {
        'ClassroomB-3-221': {'Type': 'Hallway', 'Weight': 1},
        'ClassroomB-3-222': {'Type': 'Hallway', 'Weight': 1},
        'ClassroomB-3-223': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-3-225': {'Type': 'Hallway', 'Weight': 2},
		'StairsB-3': {'Type': 'Stairs', 'Weight': 2},
        'EmergencyExitB-3': {'Type': 'EmergencyExit', 'Weight': 2},
		'HallwayB-3-2': {'Type': 'Hallway', 'Weight': 1},
        'HallwayB-3-1B': {'Type': 'Hallway', 'Weight': 1},
    },
    'HallwayB-3-1B': {
        'ClassroomB-3-210A': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-3-300': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-3-302': {'Type': 'Hallway', 'Weight': 1},
        'ClassroomB-3-304': {'Type': 'Hallway', 'Weight': 1},
        'ClassroomB-3-306': {'Type': 'Hallway', 'Weight': 1},
        'ClassroomB-3-308': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-3-310': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-3-311': {'Type': 'Hallway', 'Weight': 3},
        'ClassroomB-3-309': {'Type': 'Hallway', 'Weight': 3},
        'ClassroomB-3-307': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-3-312': {'Type': 'Hallway', 'Weight': 1},
        'ClassroomB-3-305': {'Type': 'Hallway', 'Weight': 2},
		'HallwayB-3-1': {'Type': 'Hallway', 'Weight': 2},
    },
    'HallwayB-3-2': {
        'ClassroomB-3-200': {'Type': 'Hallway', 'Weight': 3},
        'ClassroomB-3-206': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-3-208': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-3-210': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-3-209': {'Type': 'Hallway', 'Weight': 3},
        'ClassroomB-3-211': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-3-213': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-3-215': {'Type': 'Hallway', 'Weight': 1},
        'ClassroomB-3-217': {'Type': 'Hallway', 'Weight': 2},
		'HallwayB-3-3': {'Type': 'Hallway', 'Weight': 1},
        'HallwayB-3-1': {'Type': 'Hallway', 'Weight': 1},
    },
    'HallwayB-3-3': {
        'ClassroomB-3-103': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-3-105': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-3-107': {'Type': 'Hallway', 'Weight': 3},
        'ClassroomB-3-104': {'Type': 'Hallway', 'Weight': 3},
        'ClassroomB-3-106': {'Type': 'Hallway', 'Weight': 3},
        'ClassroomB-3-108': {'Type': 'Hallway', 'Weight': 3},
        'ClassroomB-3-110': {'Type': 'Hallway', 'Weight': 4},
        'ClassroomB-3-111': {'Type': 'Hallway', 'Weight': 5},
        'ClassroomB-3-112': {'Type': 'Hallway', 'Weight': 6},
        'ClassroomB-3-114': {'Type': 'Hallway', 'Weight': 6},
		'HallwayB-3-2': {'Type': 'Hallway', 'Weight': 1},
        'HallwayC-3-1': {'Type': 'Hallway', 'Weight': 1},
    },
    'HallwayC-3-1': {
        'ClassroomC-3-101': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomC-3-103': {'Type': 'Hallway', 'Weight': 1},
        'ClassroomC-3-105': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomC-3-107': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomC-3-031': {'Type': 'Hallway', 'Weight': 1},
		'StairsC-3-1': {'Type': 'Stairs', 'Weight': 2},
        'EmergencyExitC-3': {'Type': 'EmergencyExit', 'Weight': 2},
		'HallwayB-3-3': {'Type': 'Hallway', 'Weight': 3},
        'HallwayC-3-2': {'Type': 'Hallway', 'Weight': 3},
    },
    'HallwayC-3-2': {
        'ClassroomC-3-203': {'Type': 'Hallway', 'Weight': 1},
        'ClassroomC-3-203A': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomC-3-Uitleen': {'Type': 'Hallway', 'Weight': 3},
		'StairsC-3-2': {'Type': 'Stairs', 'Weight': 2},
        'EmergencyExitC-3': {'Type': 'EmergencyExit', 'Weight': 2},
        'HallwayC-3-1': {'Type': 'Hallway', 'Weight': 3},
		'Lift': {'Type': 'Lift', 'Weight': 1},
    },

#Verdieping 2

	'ClassroomB-2-221': {'HallwayB-2-1': {'Type': 'Hallway', 'Weight': 1}},
	'ClassroomB-2-222': {'HallwayB-2-1': {'Type': 'Hallway', 'Weight': 1}},
	'ClassroomB-2-223': {'HallwayB-2-1': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-2-225': {'HallwayB-2-1': {'Type': 'Hallway', 'Weight': 2}},

	'ClassroomB-2-210A': {'HallwayB-2-1B': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-2-300': {'HallwayB-2-1B': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-2-302': {'HallwayB-2-1B': {'Type': 'Hallway', 'Weight': 1}},
	'ClassroomB-2-304': {'HallwayB-2-1B': {'Type': 'Hallway', 'Weight': 1}},
	'ClassroomB-2-306': {'HallwayB-2-1B': {'Type': 'Hallway', 'Weight': 1}},
	'ClassroomB-2-308': {'HallwayB-2-1B': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-2-310': {'HallwayB-2-1B': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-2-311': {'HallwayB-2-1B': {'Type': 'Hallway', 'Weight': 3}},
	'ClassroomB-2-309': {'HallwayB-2-1B': {'Type': 'Hallway', 'Weight': 3}},
	'ClassroomB-2-307': {'HallwayB-2-1B': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-2-312': {'HallwayB-2-1B': {'Type': 'Hallway', 'Weight': 1}},
	'ClassroomB-2-305': {'HallwayB-2-1B': {'Type': 'Hallway', 'Weight': 2}},

    'ClassroomB-2-200': {'HallwayB-2-2': {'Type': 'Hallway', 'Weight': 3}},
	'ClassroomB-2-206': {'HallwayB-2-2': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-2-208': {'HallwayB-2-2': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-2-210': {'HallwayB-2-2': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-2-209': {'HallwayB-2-2': {'Type': 'Hallway', 'Weight': 3}},
	'ClassroomB-2-211': {'HallwayB-2-2': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-2-213': {'HallwayB-2-2': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-2-215': {'HallwayB-2-2': {'Type': 'Hallway', 'Weight': 1}},
	'ClassroomB-2-217': {'HallwayB-2-2': {'Type': 'Hallway', 'Weight': 2}},

	'ClassroomB-2-103': {'HallwayB-2-3': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-2-105': {'HallwayB-2-3': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-2-107': {'HallwayB-2-3': {'Type': 'Hallway', 'Weight': 3}},
    'ClassroomB-2-104': {'HallwayB-2-3': {'Type': 'Hallway', 'Weight': 3}},
	'ClassroomB-2-106': {'HallwayB-2-3': {'Type': 'Hallway', 'Weight': 3}},
	'ClassroomB-2-108': {'HallwayB-2-3': {'Type': 'Hallway', 'Weight': 3}},
	'ClassroomB-2-110': {'HallwayB-2-3': {'Type': 'Hallway', 'Weight': 4}},
	'ClassroomB-2-111': {'HallwayB-2-3': {'Type': 'Hallway', 'Weight': 5}},
	'ClassroomB-2-112': {'HallwayB-2-3': {'Type': 'Hallway', 'Weight': 6}},
	'ClassroomB-2-114': {'HallwayB-2-3': {'Type': 'Hallway', 'Weight': 6}},

    'ClassroomC-2-101': {'HallwayC-2-1': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomC-2-103': {'HallwayC-2-1': {'Type': 'Hallway', 'Weight': 1}},
	'ClassroomC-2-105': {'HallwayC-2-1': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomC-2-107': {'HallwayC-2-1': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomC-2-031': {'HallwayC-2-1': {'Type': 'Hallway', 'Weight': 1}},
	
	'ClassroomC-2-203': {'HallwayC-2-2': {'Type': 'Hallway', 'Weight': 1}},
	'ClassroomC-2-203A': {'HallwayC-2-2': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomC-2-Uitleen': {'HallwayC-2-2': {'Type': 'Hallway', 'Weight': 3}},

    'HallwayB-2-1': {
        'ClassroomB-2-221': {'Type': 'Hallway', 'Weight': 1},
        'ClassroomB-2-222': {'Type': 'Hallway', 'Weight': 1},
        'ClassroomB-2-223': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-2-225': {'Type': 'Hallway', 'Weight': 2},
		'StairsB-2': {'Type': 'Stairs', 'Weight': 2},
        'EmergencyExitB-3': {'Type': 'EmergencyExit', 'Weight': 2},
		'HallwayB-2-2': {'Type': 'Hallway', 'Weight': 1},
        'HallwayB-2-1B': {'Type': 'Hallway', 'Weight': 1},
    },
    'HallwayB-2-1B': {
        'ClassroomB-2-210A': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-2-300': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-2-302': {'Type': 'Hallway', 'Weight': 1},
        'ClassroomB-2-304': {'Type': 'Hallway', 'Weight': 1},
        'ClassroomB-2-306': {'Type': 'Hallway', 'Weight': 1},
        'ClassroomB-2-308': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-2-310': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-2-311': {'Type': 'Hallway', 'Weight': 3},
        'ClassroomB-2-309': {'Type': 'Hallway', 'Weight': 3},
        'ClassroomB-2-307': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-2-312': {'Type': 'Hallway', 'Weight': 1},
        'ClassroomB-2-305': {'Type': 'Hallway', 'Weight': 2},
		'HallwayB-2-1': {'Type': 'Hallway', 'Weight': 2},
    },
    'HallwayB-2-2': {
        'ClassroomB-2-200': {'Type': 'Hallway', 'Weight': 3},
        'ClassroomB-2-206': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-2-208': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-2-210': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-2-209': {'Type': 'Hallway', 'Weight': 3},
        'ClassroomB-2-211': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-2-213': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-2-215': {'Type': 'Hallway', 'Weight': 1},
        'ClassroomB-2-217': {'Type': 'Hallway', 'Weight': 2},
		'HallwayB-2-3': {'Type': 'Hallway', 'Weight': 1},
        'HallwayB-2-1': {'Type': 'Hallway', 'Weight': 1},
    },
    'HallwayB-2-3': {
        'ClassroomB-2-103': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-2-105': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-2-107': {'Type': 'Hallway', 'Weight': 3},
        'ClassroomB-2-104': {'Type': 'Hallway', 'Weight': 3},
        'ClassroomB-2-106': {'Type': 'Hallway', 'Weight': 3},
        'ClassroomB-2-108': {'Type': 'Hallway', 'Weight': 3},
        'ClassroomB-2-110': {'Type': 'Hallway', 'Weight': 4},
        'ClassroomB-2-111': {'Type': 'Hallway', 'Weight': 5},
        'ClassroomB-2-112': {'Type': 'Hallway', 'Weight': 6},
        'ClassroomB-2-114': {'Type': 'Hallway', 'Weight': 6},
		'HallwayB-2-2': {'Type': 'Hallway', 'Weight': 1},
        'HallwayC-2-1': {'Type': 'Hallway', 'Weight': 1},
    },
    'HallwayC-2-1': {
        'ClassroomC-2-101': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomC-2-103': {'Type': 'Hallway', 'Weight': 1},
        'ClassroomC-2-105': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomC-2-107': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomC-2-031': {'Type': 'Hallway', 'Weight': 1},
		'StairsC-2-1': {'Type': 'Stairs', 'Weight': 2},
        'EmergencyExitC-3': {'Type': 'EmergencyExit', 'Weight': 2},
		'HallwayB-2-3': {'Type': 'Hallway', 'Weight': 3},
        'HallwayC-2-2': {'Type': 'Hallway', 'Weight': 3},
    },
    'HallwayC-2-2': {
        'ClassroomC-2-203': {'Type': 'Hallway', 'Weight': 1},
        'ClassroomC-2-203A': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomC-2-Uitleen': {'Type': 'Hallway', 'Weight': 3},
		'StairsC-2-2': {'Type': 'Stairs', 'Weight': 2},
        'EmergencyExitC-3': {'Type': 'EmergencyExit', 'Weight': 2},
        'HallwayC-2-1': {'Type': 'Hallway', 'Weight': 3},
		'Lift': {'Type': 'Lift', 'Weight': 1},
    },

#Verdieping 1

	'ClassroomB-1-221': {'HallwayB-1-1': {'Type': 'Hallway', 'Weight': 1}},
	'ClassroomB-1-222': {'HallwayB-1-1': {'Type': 'Hallway', 'Weight': 1}},
	'ClassroomB-1-223': {'HallwayB-1-1': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-1-225': {'HallwayB-1-1': {'Type': 'Hallway', 'Weight': 2}},

	'ClassroomB-1-210A': {'HallwayB-1-1B': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-1-300': {'HallwayB-1-1B': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-1-302': {'HallwayB-1-1B': {'Type': 'Hallway', 'Weight': 1}},
	'ClassroomB-1-304': {'HallwayB-1-1B': {'Type': 'Hallway', 'Weight': 1}},
	'ClassroomB-1-306': {'HallwayB-1-1B': {'Type': 'Hallway', 'Weight': 1}},
	'ClassroomB-1-308': {'HallwayB-1-1B': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-1-310': {'HallwayB-1-1B': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-1-311': {'HallwayB-1-1B': {'Type': 'Hallway', 'Weight': 3}},
	'ClassroomB-1-309': {'HallwayB-1-1B': {'Type': 'Hallway', 'Weight': 3}},
	'ClassroomB-1-307': {'HallwayB-1-1B': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-1-312': {'HallwayB-1-1B': {'Type': 'Hallway', 'Weight': 1}},
	'ClassroomB-1-305': {'HallwayB-1-1B': {'Type': 'Hallway', 'Weight': 2}},

    'ClassroomB-1-200': {'HallwayB-1-2': {'Type': 'Hallway', 'Weight': 3}},
	'ClassroomB-1-206': {'HallwayB-1-2': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-1-208': {'HallwayB-1-2': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-1-210': {'HallwayB-1-2': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-1-209': {'HallwayB-1-2': {'Type': 'Hallway', 'Weight': 3}},
	'ClassroomB-1-211': {'HallwayB-1-2': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-1-213': {'HallwayB-1-2': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-1-215': {'HallwayB-1-2': {'Type': 'Hallway', 'Weight': 1}},
	'ClassroomB-1-217': {'HallwayB-1-2': {'Type': 'Hallway', 'Weight': 2}},

	'ClassroomB-1-103': {'HallwayB-1-3': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-1-105': {'HallwayB-1-3': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-1-107': {'HallwayB-1-3': {'Type': 'Hallway', 'Weight': 3}},
    'ClassroomB-1-104': {'HallwayB-1-3': {'Type': 'Hallway', 'Weight': 3}},
	'ClassroomB-1-106': {'HallwayB-1-3': {'Type': 'Hallway', 'Weight': 3}},
	'ClassroomB-1-108': {'HallwayB-1-3': {'Type': 'Hallway', 'Weight': 3}},
	'ClassroomB-1-110': {'HallwayB-1-3': {'Type': 'Hallway', 'Weight': 4}},
	'ClassroomB-1-111': {'HallwayB-1-3': {'Type': 'Hallway', 'Weight': 5}},
	'ClassroomB-1-112': {'HallwayB-1-3': {'Type': 'Hallway', 'Weight': 6}},
	'ClassroomB-1-114': {'HallwayB-1-3': {'Type': 'Hallway', 'Weight': 6}},

    'ClassroomC-1-101': {'HallwayC-1-1': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomC-1-103': {'HallwayC-1-1': {'Type': 'Hallway', 'Weight': 1}},
	'ClassroomC-1-105': {'HallwayC-1-1': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomC-1-107': {'HallwayC-1-1': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomC-1-031': {'HallwayC-1-1': {'Type': 'Hallway', 'Weight': 1}},
	
	'ClassroomC-1-203': {'HallwayC-1-2': {'Type': 'Hallway', 'Weight': 1}},
	'ClassroomC-1-203A': {'HallwayC-1-2': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomC-1-Uitleen': {'HallwayC-1-2': {'Type': 'Hallway', 'Weight': 3}},

    'HallwayB-1-1': {
        'ClassroomB-1-221': {'Type': 'Hallway', 'Weight': 1},
        'ClassroomB-1-222': {'Type': 'Hallway', 'Weight': 1},
        'ClassroomB-1-223': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-1-225': {'Type': 'Hallway', 'Weight': 2},
		'StairsB-1': {'Type': 'Stairs', 'Weight': 2},
        'EmergencyExitB-3': {'Type': 'EmergencyExit', 'Weight': 2},
		'HallwayB-1-2': {'Type': 'Hallway', 'Weight': 1},
        'HallwayB-1-1B': {'Type': 'Hallway', 'Weight': 1},
    },
    'HallwayB-1-1B': {
        'ClassroomB-1-210A': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-1-300': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-1-302': {'Type': 'Hallway', 'Weight': 1},
        'ClassroomB-1-304': {'Type': 'Hallway', 'Weight': 1},
        'ClassroomB-1-306': {'Type': 'Hallway', 'Weight': 1},
        'ClassroomB-1-308': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-1-310': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-1-311': {'Type': 'Hallway', 'Weight': 3},
        'ClassroomB-1-309': {'Type': 'Hallway', 'Weight': 3},
        'ClassroomB-1-307': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-1-312': {'Type': 'Hallway', 'Weight': 1},
        'ClassroomB-1-305': {'Type': 'Hallway', 'Weight': 2},
		'HallwayB-1-1': {'Type': 'Hallway', 'Weight': 2},
    },
    'HallwayB-1-2': {
        'ClassroomB-1-200': {'Type': 'Hallway', 'Weight': 3},
        'ClassroomB-1-206': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-1-208': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-1-210': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-1-209': {'Type': 'Hallway', 'Weight': 3},
        'ClassroomB-1-211': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-1-213': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-1-215': {'Type': 'Hallway', 'Weight': 1},
        'ClassroomB-1-217': {'Type': 'Hallway', 'Weight': 2},
		'HallwayB-1-3': {'Type': 'Hallway', 'Weight': 1},
        'HallwayB-1-1': {'Type': 'Hallway', 'Weight': 1},
    },
    'HallwayB-1-3': {
        'ClassroomB-1-103': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-1-105': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-1-107': {'Type': 'Hallway', 'Weight': 3},
        'ClassroomB-1-104': {'Type': 'Hallway', 'Weight': 3},
        'ClassroomB-1-106': {'Type': 'Hallway', 'Weight': 3},
        'ClassroomB-1-108': {'Type': 'Hallway', 'Weight': 3},
        'ClassroomB-1-110': {'Type': 'Hallway', 'Weight': 4},
        'ClassroomB-1-111': {'Type': 'Hallway', 'Weight': 5},
        'ClassroomB-1-112': {'Type': 'Hallway', 'Weight': 6},
        'ClassroomB-1-114': {'Type': 'Hallway', 'Weight': 6},
		'HallwayB-1-2': {'Type': 'Hallway', 'Weight': 1},
        'HallwayC-1-1': {'Type': 'Hallway', 'Weight': 1},
    },
    'HallwayC-1-1': {
        'ClassroomC-1-101': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomC-1-103': {'Type': 'Hallway', 'Weight': 1},
        'ClassroomC-1-105': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomC-1-107': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomC-1-031': {'Type': 'Hallway', 'Weight': 1},
		'StairsC-1-1': {'Type': 'Stairs', 'Weight': 2},
        'EmergencyExitC-3': {'Type': 'EmergencyExit', 'Weight': 2},
		'HallwayB-1-3': {'Type': 'Hallway', 'Weight': 3},
        'HallwayC-1-2': {'Type': 'Hallway', 'Weight': 3},
    },
    'HallwayC-1-2': {
        'ClassroomC-1-203': {'Type': 'Hallway', 'Weight': 1},
        'ClassroomC-1-203A': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomC-1-Uitleen': {'Type': 'Hallway', 'Weight': 3},
		'StairsC-1-2': {'Type': 'Stairs', 'Weight': 2},
        'EmergencyExitC-3': {'Type': 'EmergencyExit', 'Weight': 2},
        'HallwayC-1-1': {'Type': 'Hallway', 'Weight': 3},
		'Lift': {'Type': 'Lift', 'Weight': 1},
    },

# Verdieping 0

	'ClassroomB-0-221': {'HallwayB-0-1': {'Type': 'Hallway', 'Weight': 1}},
	'ClassroomB-0-222': {'HallwayB-0-1': {'Type': 'Hallway', 'Weight': 1}},
	'ClassroomB-0-223': {'HallwayB-0-1': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-0-225': {'HallwayB-0-1': {'Type': 'Hallway', 'Weight': 2}},

	'ClassroomB-0-210A': {'HallwayB-0-1B': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-0-300': {'HallwayB-0-1B': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-0-302': {'HallwayB-0-1B': {'Type': 'Hallway', 'Weight': 1}},
	'ClassroomB-0-304': {'HallwayB-0-1B': {'Type': 'Hallway', 'Weight': 1}},
	'ClassroomB-0-306': {'HallwayB-0-1B': {'Type': 'Hallway', 'Weight': 1}},
	'ClassroomB-0-308': {'HallwayB-0-1B': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-0-310': {'HallwayB-0-1B': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-0-311': {'HallwayB-0-1B': {'Type': 'Hallway', 'Weight': 3}},
	'ClassroomB-0-309': {'HallwayB-0-1B': {'Type': 'Hallway', 'Weight': 3}},
	'ClassroomB-0-307': {'HallwayB-0-1B': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-0-312': {'HallwayB-0-1B': {'Type': 'Hallway', 'Weight': 1}},
	'ClassroomB-0-305': {'HallwayB-0-1B': {'Type': 'Hallway', 'Weight': 2}},

    'ClassroomB-0-200': {'HallwayB-0-2': {'Type': 'Hallway', 'Weight': 3}},
	'ClassroomB-0-206': {'HallwayB-0-2': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-0-208': {'HallwayB-0-2': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-0-210': {'HallwayB-0-2': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-0-209': {'HallwayB-0-2': {'Type': 'Hallway', 'Weight': 3}},
	'ClassroomB-0-211': {'HallwayB-0-2': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-0-213': {'HallwayB-0-2': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-0-215': {'HallwayB-0-2': {'Type': 'Hallway', 'Weight': 1}},
	'ClassroomB-0-217': {'HallwayB-0-2': {'Type': 'Hallway', 'Weight': 2}},

	'ClassroomB-0-103': {'HallwayB-0-3': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-0-105': {'HallwayB-0-3': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomB-0-107': {'HallwayB-0-3': {'Type': 'Hallway', 'Weight': 3}},
    'ClassroomB-0-104': {'HallwayB-0-3': {'Type': 'Hallway', 'Weight': 3}},
	'ClassroomB-0-106': {'HallwayB-0-3': {'Type': 'Hallway', 'Weight': 3}},
	'ClassroomB-0-108': {'HallwayB-0-3': {'Type': 'Hallway', 'Weight': 3}},
	'ClassroomB-0-110': {'HallwayB-0-3': {'Type': 'Hallway', 'Weight': 4}},
	'ClassroomB-0-111': {'HallwayB-0-3': {'Type': 'Hallway', 'Weight': 5}},
	'ClassroomB-0-112': {'HallwayB-0-3': {'Type': 'Hallway', 'Weight': 6}},
	'ClassroomB-0-114': {'HallwayB-0-3': {'Type': 'Hallway', 'Weight': 6}},

    'ClassroomC-0-101': {'HallwayC-0-1': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomC-0-103': {'HallwayC-0-1': {'Type': 'Hallway', 'Weight': 1}},
	'ClassroomC-0-105': {'HallwayC-0-1': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomC-0-107': {'HallwayC-0-1': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomC-0-031': {'HallwayC-0-1': {'Type': 'Hallway', 'Weight': 1}},
	
	'ClassroomC-0-203': {'HallwayC-0-2': {'Type': 'Hallway', 'Weight': 1}},
	'ClassroomC-0-203A': {'HallwayC-0-2': {'Type': 'Hallway', 'Weight': 2}},
	'ClassroomC-0-Uitleen': {'HallwayC-0-2': {'Type': 'Hallway', 'Weight': 3}},

    'HallwayB-0-1': {
        'ClassroomB-0-221': {'Type': 'Hallway', 'Weight': 1},
        'ClassroomB-0-222': {'Type': 'Hallway', 'Weight': 1},
        'ClassroomB-0-223': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-0-225': {'Type': 'Hallway', 'Weight': 2},
		'StairsB-0': {'Type': 'Stairs', 'Weight': 2},
        'EmergencyExitB-3': {'Type': 'EmergencyExit', 'Weight': 2},
		'HallwayB-0-2': {'Type': 'Hallway', 'Weight': 1},
        'HallwayB-0-1B': {'Type': 'Hallway', 'Weight': 1},
    },
    'HallwayB-0-1B': {
        'ClassroomB-0-210A': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-0-300': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-0-302': {'Type': 'Hallway', 'Weight': 1},
        'ClassroomB-0-304': {'Type': 'Hallway', 'Weight': 1},
        'ClassroomB-0-306': {'Type': 'Hallway', 'Weight': 1},
        'ClassroomB-0-308': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-0-310': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-0-311': {'Type': 'Hallway', 'Weight': 3},
        'ClassroomB-0-309': {'Type': 'Hallway', 'Weight': 3},
        'ClassroomB-0-307': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-0-312': {'Type': 'Hallway', 'Weight': 1},
        'ClassroomB-0-305': {'Type': 'Hallway', 'Weight': 2},
		'HallwayB-0-1': {'Type': 'Hallway', 'Weight': 2},
    },
    'HallwayB-0-2': {
        'ClassroomB-0-200': {'Type': 'Hallway', 'Weight': 3},
        'ClassroomB-0-206': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-0-208': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-0-210': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-0-209': {'Type': 'Hallway', 'Weight': 3},
        'ClassroomB-0-211': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-0-213': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-0-215': {'Type': 'Hallway', 'Weight': 1},
        'ClassroomB-0-217': {'Type': 'Hallway', 'Weight': 2},
		'HallwayB-0-3': {'Type': 'Hallway', 'Weight': 1},
        'HallwayB-0-1': {'Type': 'Hallway', 'Weight': 1},
    },
    'HallwayB-0-3': {
        'ClassroomB-0-103': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-0-105': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomB-0-107': {'Type': 'Hallway', 'Weight': 3},
        'ClassroomB-0-104': {'Type': 'Hallway', 'Weight': 3},
        'ClassroomB-0-106': {'Type': 'Hallway', 'Weight': 3},
        'ClassroomB-0-108': {'Type': 'Hallway', 'Weight': 3},
        'ClassroomB-0-110': {'Type': 'Hallway', 'Weight': 4},
        'ClassroomB-0-111': {'Type': 'Hallway', 'Weight': 5},
        'ClassroomB-0-112': {'Type': 'Hallway', 'Weight': 6},
        'ClassroomB-0-114': {'Type': 'Hallway', 'Weight': 6},
		'HallwayB-0-2': {'Type': 'Hallway', 'Weight': 1},
        'HallwayC-0-1': {'Type': 'Hallway', 'Weight': 1},
    },
    'HallwayC-0-1': {
		'MainHall': {'Type': 'Hallway', 'Weight': 1},
        'ClassroomC-0-101': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomC-0-103': {'Type': 'Hallway', 'Weight': 1},
        'ClassroomC-0-105': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomC-0-107': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomC-0-031': {'Type': 'Hallway', 'Weight': 1},
		'StairsC-0-1': {'Type': 'Stairs', 'Weight': 2},
        'EmergencyExitC-3': {'Type': 'EmergencyExit', 'Weight': 2},
		'HallwayB-0-3': {'Type': 'Hallway', 'Weight': 3},
        'HallwayC-0-2': {'Type': 'Hallway', 'Weight': 3},
    },
    'HallwayC-0-2': {
		'MainHall': {'Type': 'Hallway', 'Weight': 1},
        'ClassroomC-0-203': {'Type': 'Hallway', 'Weight': 1},
        'ClassroomC-0-203A': {'Type': 'Hallway', 'Weight': 2},
        'ClassroomC-0-Uitleen': {'Type': 'Hallway', 'Weight': 3},
		'StairsC-0-2': {'Type': 'Stairs', 'Weight': 2},
        'EmergencyExitC-3': {'Type': 'EmergencyExit', 'Weight': 2},
        'HallwayC-0-1': {'Type': 'Hallway', 'Weight': 3},
        'Parkeerplaats 1 (Mobiliteitsproblemen)': {'Type': 'Hallway', 'Weight': 3},
		'Lift': {'Type': 'Lift', 'Weight': 1},
	},

# Liften, trappen, emergency en algemeen
	'Lift': {
		'HallwayC-0-2': {'Type': 'Lift', 'Weight': 1},
        'HallwayC-1-2': {'Type': 'Lift', 'Weight': 1},
		'HallwayC-2-2': {'Type': 'Lift', 'Weight': 1},
		'HallwayC-3-2': {'Type': 'Lift', 'Weight': 1},
	},
    'StairsB-0': {'HallwayB-0-1': {'Type': 'Hallway', 'Weight': 1},
                  'StairsB-1': {'Type': 'Stairs', 'Weight': 1}},
    'StairsB-1': {'HallwayB-1-1': {'Type': 'Hallway', 'Weight': 1},
                  'StairsB-2': {'Type': 'Stairs', 'Weight': 1},
                  'StairsB-0': {'Type': 'Stairs', 'Weight': 1}},
    'StairsB-2': {'HallwayB-2-1': {'Type': 'Hallway', 'Weight': 1},
                  'StairsB-3': {'Type': 'Stairs', 'Weight': 1},
                  'StairsB-1': {'Type': 'Stairs', 'Weight': 1}},
    'StairsB-3': {'HallwayB-3-1': {'Type': 'Hallway', 'Weight': 1},
                  'StairsB-2': {'Type': 'Stairs', 'Weight': 1}},

    'StairsC-0-1': {'HallwayC-0-1': {'Type': 'Hallway', 'Weight': 1},
                  'StairsC-1-1': {'Type': 'Stairs', 'Weight': 1}},
    'StairsC-1-1': {'HallwayC-1-1': {'Type': 'Hallway', 'Weight': 1},
                  'StairsC-2-1': {'Type': 'Stairs', 'Weight': 1},
                  'StairsC-0-1': {'Type': 'Stairs', 'Weight': 1}},
    'StairsC-2-1': {'HallwayC-2-1': {'Type': 'Hallway', 'Weight': 1},
                  'StairsC-3-1': {'Type': 'Stairs', 'Weight': 1},
                  'StairsC-1-1': {'Type': 'Stairs', 'Weight': 1}},
    'StairsC-3-1': {'HallwayC-3-1': {'Type': 'Hallway', 'Weight': 1},
                  'StairsC-2-1': {'Type': 'Stairs', 'Weight': 1}},

    'StairsC-0-2': {'HallwayC-0-2': {'Type': 'Hallway', 'Weight': 1},
                  'StairsC-1-2': {'Type': 'Stairs', 'Weight': 1}},
    'StairsC-1-2': {'HallwayC-1-2': {'Type': 'Hallway', 'Weight': 1},
                  'StairsC-2-2': {'Type': 'Stairs', 'Weight': 1},
                  'StairsC-0-2': {'Type': 'Stairs', 'Weight': 1}},
    'StairsC-2-2': {'HallwayC-2-2': {'Type': 'Hallway', 'Weight': 1},
                  'StairsC-3-2': {'Type': 'Stairs', 'Weight': 1},
                  'StairsC-1-2': {'Type': 'Stairs', 'Weight': 1}},
    'StairsC-3-2': {'HallwayC-3-2': {'Type': 'Hallway', 'Weight': 1},
                  'StairsC-2-2': {'Type': 'Stairs', 'Weight': 1}},

    'EmergencyExitB-0': {
		'HallwayB-0-1': {'Type': 'Hallway', 'Weight': 1},
		'EmergencyExitB-1': {'Type': 'EmergencyExit', 'Weight': 1},
		'Safe': {'Type': 'Safe', 'Weight': 1},
	},
    'EmergencyExitB-1': {
		'HallwayB-1-1': {'Type': 'Hallway', 'Weight': 1},
        'EmergencyExitB-2': {'Type': 'EmergencyExit', 'Weight': 1},
        'EmergencyExitB-0': {'Type': 'EmergencyExit', 'Weight': 1},
	},
    'EmergencyExitB-2': {
		'HallwayB-2-1': {'Type': 'Hallway', 'Weight': 1},
		'EmergencyExitB-3': {'Type': 'EmergencyExit', 'Weight': 1},
	    'EmergencyExitB-1': {'Type': 'EmergencyExit', 'Weight': 1},
	},
    'EmergencyExitB-3': {
		'HallwayB-3-1': {'Type': 'Hallway', 'Weight': 1},
		'EmergencyExitB-2': {'Type': 'EmergencyExit', 'Weight': 1},
	},

    'EmergencyExitC-0': {
        'HallwayC-0-1': {'Type': 'Hallway', 'Weight': 1},
		'HallwayC-0-2': {'Type': 'Hallway', 'Weight': 1},
        'EmergencyExitC-1': {'Type': 'EmergencyExit', 'Weight': 1},
        'Safe': {'Type': 'Safe', 'Weight': 1},
    },
    'EmergencyExitC-1': {
        'HallwayC-1-1': {'Type': 'Hallway', 'Weight': 1},
		'HallwayC-1-2': {'Type': 'Hallway', 'Weight': 1},
        'EmergencyExitC-2': {'Type': 'EmergencyExit', 'Weight': 1},
        'EmergencyExitC-0': {'Type': 'EmergencyExit', 'Weight': 1},
    },
    'EmergencyExitC-2': {
        'HallwayC-2-1': {'Type': 'Hallway', 'Weight': 1},
		'HallwayC-2-2': {'Type': 'Hallway', 'Weight': 1},
        'EmergencyExitC-3': {'Type': 'EmergencyExit', 'Weight': 1},
        'EmergencyExitC-1': {'Type': 'EmergencyExit', 'Weight': 1},
    },
    'EmergencyExitC-3': {
        'HallwayC-3-1': {'Type': 'Hallway', 'Weight': 1},
		'HallwayC-3-2': {'Type': 'Hallway', 'Weight': 1},
        'EmergencyExitC-2': {'Type': 'EmergencyExit', 'Weight': 1},
    },

    'MainHall': {
		'HallwayC-0-1': {'Type': 'Hallway', 'Weight': 1},
		'HallwayC-0-2': {'Type': 'Hallway', 'Weight': 1},
		'Kantine': {'Type': 'Hallway', 'Weight': 1},
        'Parkeerplaats 2': {'Type': 'Hallway', 'Weight': 1},
        'Parkeerplaats 3': {'Type': 'Hallway', 'Weight': 1},
        'Openbaar vervoer en fietsenstalling ingang': {'Type': 'Hallway', 'Weight': 1},
    },
    'Kantine': {'MainHall': {'Type': 'Hallway', 'Weight': 1}},
    'Safe': {'EmergencyExitB-0': {'Type': 'EmergencyExit', 'Weight': 1}},

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
start_node_var = tk.StringVar()
end_node_var = tk.StringVar()

# Create GUI elements
is_disabled_checkbox = tk.Checkbutton(mainframe, text="Mobiliteitsproblemen", variable=is_disabled_var)
is_emergency_checkbox = tk.Checkbutton(mainframe, text="Emergency", variable=is_emergency_var)

start_node_label = tk.Label(mainframe, text="Current location:")
start_node_dropdown = ttk.Combobox(mainframe, textvariable=start_node_var)
start_node_dropdown['values'] = tuple(school_map.keys())
end_node_label = tk.Label(mainframe, text="Manual end location:")
end_node_dropdown = ttk.Combobox(mainframe, textvariable=end_node_var)
end_node_dropdown['values'] = tuple(school_map.keys())

# Create session dropdowns dynamically
session_dropdowns = []
session_label = tk.Label(mainframe, text="Select sessions:")
session_label.grid(row=5, column=0, sticky=tk.W)

for i, session in enumerate(session_to_node.keys()):
    session_name_label = tk.Label(mainframe, text=f"Session {i+1}:")
    session_name_label.grid(row=6 + i, column=0, pady=(5, 0), sticky=tk.W)

    dropdown = ttk.Combobox(mainframe, values=list(session_to_node.keys()))
    dropdown.grid(row=6 + i, column=1, sticky=(tk.W, tk.E))
    session_dropdowns.append(dropdown)

# Result labels
result_label = ttk.Label(mainframe, text="", wraplength=300)
path_label = ttk.Label(mainframe, text="", wraplength=300)
time_label = ttk.Label(mainframe, text="Elapsed Time: Not measured yet")
memory_label = ttk.Label(mainframe, text="Peak Memory Usage: Not measured yet")

# Button to trigger the navigation
find_route_button = ttk.Button(mainframe, text="Start navigation through sessions", command=find_path)

# Arrange GUI elements in a grid
is_disabled_checkbox.grid(row=0, column=0, columnspan=2, sticky=tk.W)
is_emergency_checkbox.grid(row=1, column=0, columnspan=2, sticky=tk.W)
start_node_label.grid(row=2, column=0, sticky=tk.W)
start_node_dropdown.grid(row=2, column=1, sticky=(tk.W, tk.E))
end_node_label.grid(row=3, column=0, sticky=tk.W)
end_node_dropdown.grid(row=3, column=1, sticky=(tk.W, tk.E))
find_route_button.grid(row=4, column=0, columnspan=2, pady=(10, 0))
result_label.grid(row=7 + len(session_to_node), column=0, columnspan=2, pady=(10, 0))
path_label.grid(row=8 + len(session_to_node), column=0, columnspan=2, pady=(10, 0))
time_label.grid(row=9 + len(session_to_node), column=0, columnspan=2, pady=(10, 0))
memory_label.grid(row=10 + len(session_to_node), column=0, columnspan=2, pady=(10, 0))

# Run the Tkinter event loop
root.mainloop()