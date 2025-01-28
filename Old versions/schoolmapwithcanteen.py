import heapq

def dijkstra(graph, start, end):
    # Priority queue to store nodes with their tentative distances
    priority_queue = [(0, start)]
    
    # Dictionary to store tentative distances
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if current_node == end:
            # Reached the destination, return the shortest distance
            return current_distance
        
        if current_distance > distances[current_node]:
            # Skip if the current distance is greater than the known distance
            continue
        
        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                # Update the tentative distance
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
    
    # If no path is found
    return float('infinity')

# Updated example graph representation with floor information and corrected connections
# Format: {node: [(neighbor1, weight1), (neighbor2, weight2), ...]}
school_map = {
    'Classroom1': [('Hallway', 1)],
    'Classroom2': [('Hallway', 1)],
    'Classroom3': [('Hallway', 1)],
    'Classroom4': [('Hallway', 1)],
    'Classroom5': [('Hallway', 1)],
    'Classroom6': [('Hallway', 1)],
    'Classroom7': [('Hallway', 1)],
    'Classroom8': [('Hallway', 1)],
    'Hallway': [('Classroom1', 1), ('Classroom2', 1), ('Classroom3', 1), ('Classroom4', 1),
                ('Classroom5', 1), ('Classroom6', 1), ('Classroom7', 1), ('Classroom8', 1),
                ('Stairs3', 1)],
    'Stairs3': [('Hallway', 1), ('Stairs2', 1)],
    'Stairs2': [('Stairs3', 1), ('Stairs1', 1)],
    'Stairs1': [('Stairs2', 1), ('MainHall', 1)],
    'MainHall': [('Stairs1', 1), ('Canteen', 1)],
    'Canteen': [('MainHall', 1)]
}

# Add floor information to classrooms
classroom_floors = {
    'Classroom1': 3,
    'Classroom2': 3,
    'Classroom3': 3,
    'Classroom4': 3,
    'Classroom5': 3,
    'Classroom6': 3,
    'Classroom7': 3,
    'Classroom8': 3,
    'Hallway': 3,
    'Stairs3': 3,
    'Stairs2': 2,
    'Stairs1': 1,
    'MainHall': 1,
    'Canteen': 1
}

# Find the shortest path from a classroom to the canteen
start_classroom = 'Classroom1'  # Replace with the actual starting classroom
end_canteen = 'Canteen'

shortest_distance = dijkstra(school_map, start_classroom, end_canteen)

if shortest_distance == float('infinity'):
    print(f"There is no path from {start_classroom} to {end_canteen}.")
else:
    print(f"The shortest distance from {start_classroom} to {end_canteen} is {shortest_distance} units.")
