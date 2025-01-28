import heapq

def dijkstra(graph, start, end, is_disabled=False):
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
                # Use the lift only if it's on the same or lower floor
                if floors[current_node] >= floors[neighbor]:
                    distance += graph[current_node][neighbor].get('Weight', 0)  # Adjust distance for stairs
                else:
                    continue  # Skip the lift if it's on a higher floor
            else:
                distance += graph[current_node][neighbor].get('Weight', 0)  # No adjustment needed for non-stairs/non-lift nodes

            if distance < distances[neighbor]:
                # Update the tentative distance and previous node
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    
    # If no path is found
    return float('infinity'), []

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
                  'MainHall': {'Type': 'Hallway', 'Weight': 1}},
    'Hallway1-B': {'Stairs1-B': {'Type': 'Stairs', 'Weight': 1},
                  'Hallway1-C': {'Type': 'Hallway', 'Weight': 1}},
    'Hallway2-B': {'Stairs2-B': {'Type': 'Stairs', 'Weight': 1},
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
    'Canteen': {'MainHall': {'Type': 'Hallway', 'Weight': 1}}
}

## Add floor information to classrooms
floors = {
    'Classroom1-3-B': 3,
    'Classroom2-3-B': 3,
    'Classroom3-3-B': 3,
    'Classroom4-3-B': 3,
    'Classroom5-3-B': 3,
    'Classroom6-3-B': 3,
    'Classroom7-3-B': 3,
    'Classroom8-3-B': 3,
    'Classroom1-3-C': 3,
    'Classroom2-3-C': 3,
    'Classroom3-3-C': 3,
    'Classroom4-3-C': 3,
    'Classroom5-3-C': 3,
    'Classroom6-3-C': 3,
    'Classroom7-3-C': 3,
    'Classroom8-3-C': 3,
    'Hallway0-B': 0,
    'Hallway1-B': 1,
    'Hallway2-B': 2,
    'Hallway3-B': 3,
    'Stairs0-B': 0,
    'Stairs1-B': 1,
    'Stairs2-B': 2,
    'Stairs3-B': 3,
    'Hallway0-C': 0,
    'Hallway1-C': 1,
    'Hallway2-C': 2,
    'Hallway3-C': 3,
    'Stairs0-C': 0,
    'Stairs1-C': 1,
    'Stairs2-C': 2,
    'Stairs3-C': 3,
    'Lift': 0,
    'Lift': 1,
    'Lift': 2,
    'Lift': 3,
    'MainHall': 0,
    'Canteen': 0
}

# Specify whether the user is disabled or able
is_disabled_user = False  # Change to False if the user is able

# Find the shortest path from a classroom to any end node considering user ability
start_node = 'Hallway0-C'  # Replace with the actual starting classroom
end_node = 'Hallway3-B'  # Replace with the actual end node

shortest_distance, path = dijkstra(school_map, start_node, end_node, is_disabled=is_disabled_user)

if shortest_distance == float('infinity'):
    print(f"There is no path from {start_node} to {end_node}.")
else:
    user_ability = "Disabled" if is_disabled_user else "Able"
    print(f"The user is {user_ability}.")
    print(f"The shortest distance from {start_node} to {end_node} is {shortest_distance} units.")
    print("The path is:", " -> ".join(path))
