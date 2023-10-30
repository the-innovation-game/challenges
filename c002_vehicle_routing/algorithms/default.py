from c002_vehicle_routing.challenge import Challenge


def solveChallenge(challenge: Challenge) -> list:
    D = challenge.distance_matrix
    C = challenge.max_capacity
    N = challenge.difficulty.num_nodes
    # Clarke-Wright heuristic for node pairs based on their distances to depot
    # vs distance between each other 
    scores = sorted(
        (
            (D[i, 0] + D[0, j] - D[i, j], i, j)
            for i in range(1, N)
            for j in range(i + 1, N)
        ),
        reverse=True
    )    
    # create a route for every node
    routes = [[i] for i in range(N)]
    routes[0] = None
    route_demands = challenge.demands.tolist()
    # iterate through node pairs, starting from greatest score
    for s, i, j in scores:
        # stop if score is negative
        if s < 0:
            break        
        # skip if joining the nodes is not possible
        if (
            (left_route := routes[i]) is None or
            (right_route := routes[j]) is None or
            (left_startnode := left_route[0]) == (right_startnode := right_route[0]) or
            (merged_demand := (route_demands[left_startnode] + route_demands[right_startnode])) > C
        ):
            continue
        # left_route will have node i either at the start or the end
        # right_route will have node j either at the start or the end
        left_endnode = left_route[-1]
        right_endnode = right_route[-1]
        routes[left_startnode] = routes[right_startnode] = routes[left_endnode] = routes[right_endnode] = None
        # flip routes where necessary so that we can join node i and node j in the middle
        if left_startnode == i:
            left_route = left_route[::-1]
            left_startnode = left_endnode
        if right_endnode == j:
            right_route = right_route[::-1]
            right_endnode = right_startnode        
        # only the start and end nodes of routes are kept
        routes[left_startnode] = routes[right_endnode] = left_route + right_route
        route_demands[left_startnode] = route_demands[right_endnode] = merged_demand
    # each route needs to start and end at depot (node 0)
    return [
        [0] + routes[i] + [0] 
        for i in range(N) 
        if routes[i] is not None and routes[i][0] == i
    ]