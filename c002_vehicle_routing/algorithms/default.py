from c002_vehicle_routing.challenge import Challenge
import numpy as np

def solveChallenge(challenge: Challenge, logIntermediateInteger=print) -> np.ndarray:
    # Seed the random number generator.
    np.random.seed(challenge.seed)
    # Try up to 1000 attempts to find a solution using a naive algorithm.
    for _ in range(1000):
        # Calculate random greedy routes.
        routes = []
        visited = np.zeros(challenge.difficulty.num_nodes, dtype=bool)
        visited[0] = True
        # Loop until all nodes are visited
        while not np.all(visited):
            route = [0] # start each route at depot
            current_node = 0
            capacity = challenge.max_capacity
            # Loop until no more nodes can be added to the current route
            while capacity > 0 and not np.all(visited):
                is_eligible = ~visited * (challenge.demands <= capacity)
                # If there are any eligible nodes, visit one of the top 3 closest (randomly chosen)
                if np.any(is_eligible):
                    distance_to_eligible_nodes = challenge.distance_matrix[current_node][is_eligible]
                    # get indexs of where is_eligible is true
                    eligible_nodes = np.where(is_eligible)[0]
                    # sort eligible nodes by distance, and take top 3
                    top_3_closest_nodes = eligible_nodes[np.argsort(distance_to_eligible_nodes)][:3]
                    # randomly pick one
                    random_node = int(np.random.choice(top_3_closest_nodes))
                    capacity -= challenge.demands[random_node]
                    route.append(random_node)
                    visited[random_node] = True
                    current_node = random_node
                else:
                    break  
            # end each route at depot          
            route.append(0)
            routes.append(route)
        # Log an intermediate integer that is near impossible to fake unless this algorithm is ran 
        logIntermediateInteger(int(np.random.rand() * 10e6))       
        # Check if the routes is a solution
        if challenge.verifySolution(routes):
            break
    return routes
