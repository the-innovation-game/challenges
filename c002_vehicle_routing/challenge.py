from typing import Union, Dict
from dataclasses import dataclass
import numpy as np

def calcBaselineRoutes(num_nodes: int, max_capacity: int, demands: np.ndarray, distance_matrix: np.ndarray) -> list:
    routes = []
    visited = np.zeros(num_nodes, dtype=bool)
    visited[0] = True

    # Loop until all nodes are visited
    while not np.all(visited):
        route = [0] # start each route at depot
        current_node = 0
        capacity = max_capacity

        # Loop until no more nodes can be added to the current route
        while capacity > 0 and not np.all(visited):
            eligible_nodes = ~visited * (demands <= capacity)

            # If there are any eligible nodes, visit the closest one
            if np.any(eligible_nodes):
                closest_node = int(np.where(eligible_nodes)[0][np.argsort(distance_matrix[current_node][eligible_nodes])][0])
                capacity -= demands[closest_node]
                route.append(closest_node)
                visited[closest_node] = True
                current_node = closest_node
            else:
                break
        
        route.append(0) # end each route at depot
        routes.append(route)

    return routes

def calcRoutesTotalDistance(num_nodes: int, max_capacity: int, demands: np.ndarray, distance_matrix: np.ndarray, routes: list) -> int:
    total_distance = 0
    visited = np.zeros(num_nodes, dtype=bool)
    visited[0] = True

    for route in routes:
        # always start each route at depot and with max capacity
        capacity = max_capacity
        current_node = 0 

        if len(route) <= 2 or route[0] != 0 or route[-1] != 0:
            raise Exception("Each route must start and end at node 0 (the depot), and visit at least one non-depot node")
        for node in route[1:-1]:
            if visited[node]:
                raise Exception("The same non-depot node cannot be visited more than once")
            if demands[node] > capacity:
                raise Exception("The total demand on each route must not exceed max capacity")
            visited[node] = True
            capacity -= demands[node]
            total_distance += distance_matrix[current_node, node]
            current_node = node

        total_distance += distance_matrix[current_node, 0]
    
    if not np.all(visited):
        raise Exception("All nodes must be visited")
    return total_distance

@dataclass
class Difficulty:
    # Number of nodes (including depot) for the vehicle routing problem
    num_nodes: int
    # The distance of your routes have to be this percentage shorter than routes found by a baseline algorithm
    percent_better_than_baseline: int

@dataclass
class Challenge:
    seed: int
    difficulty: Difficulty
    demands: np.ndarray
    distance_matrix: np.ndarray
    max_total_distance: int
    max_capacity: int = 100

    def verifySolution(self, solution: list):
        try:
            return calcRoutesTotalDistance(
                num_nodes=self.difficulty.num_nodes,
                max_capacity=self.max_capacity,
                demands=self.demands,
                distance_matrix=self.distance_matrix,
                routes=solution
            ) <= self.max_total_distance
        except Exception as e:
            raise Exception("Invalid solution") from e

    @classmethod
    def generateInstance(cls, seed: int, difficulty: Union[Difficulty, Dict[str, int]]) -> "Challenge":
        if isinstance(difficulty, dict):
            difficulty = Difficulty(**difficulty)
        np.random.seed(seed)
        node_positions = np.random.rand(difficulty.num_nodes, 2) * 500
        node_positions[0] = [250, 250] # depot is node 0, and in the center

        demands = np.random.randint(15, 30, size=difficulty.num_nodes)
        demands[0] = 0
        distance_matrix = np.linalg.norm(node_positions[:, None, :] - node_positions[None, :, :], axis=2).astype(int)
        baseline_routes = calcBaselineRoutes(difficulty.num_nodes, cls.max_capacity, demands, distance_matrix)
        baseline_routes_total_distance = calcRoutesTotalDistance(difficulty.num_nodes, cls.max_capacity, demands, distance_matrix, baseline_routes)
        max_total_distance = int(baseline_routes_total_distance * (100 - difficulty.percent_better_than_baseline) / 100)

        return cls(
            seed=seed,
            difficulty=difficulty,
            demands=demands,
            distance_matrix=distance_matrix,
            max_total_distance=max_total_distance
        )

    @classmethod
    def example(cls):
        return cls(
            seed=1234, # fake seed
            difficulty=Difficulty(
                num_nodes=5,
                percent_better_than_baseline=5
            ),
            demands=np.array([0, 25, 30, 20, 15], dtype=int),
            distance_matrix=np.array([
                [0, 10, 20, 30, 40],
                [10, 0, 15, 25, 35],
                [20, 15, 0, 20, 30],
                [30, 25, 20, 0, 10],
                [40, 35, 30, 10, 0]
            ], dtype=int),
            max_total_distance=140
        )


if __name__ == "__main__":
    import itertools
    import sys
    import json
    from datetime import datetime
    solveChallenge = getattr(__import__(f"c002_vehicle_routing.algorithms.{sys.argv[1]}").algorithms, sys.argv[1]).solveChallenge
    print("num_nodes,percent_better_than_baseline,total_seconds,num_attempts,num_solutions")
    for num_nodes, percent_better_than_baseline in itertools.product(
        [40, 60, 80, 100, 120, 140, 160],
        [25, 30, 35, 40, 45, 50]
    ):
        difficulty = Difficulty(num_nodes, percent_better_than_baseline)
        start = datetime.now()
        num_attempts = 0
        num_solutions = 0
        while (elapsed := (datetime.now() - start).total_seconds()) < 5:
            challenge = Challenge.generateInstance(num_attempts, difficulty)
            solution, solution_method_id = solveChallenge(challenge)
            try:
                json.dumps(solution)
            except:
                raise Exception("solution should be JSON serializable")
            try:
                int(solution_method_id)
            except:
                raise Exception("solution_method_id should be int")
            if challenge.verifySolution(solution):
                num_solutions += 1
            num_attempts += 1
        print(f"{num_nodes},{percent_better_than_baseline},{elapsed},{num_attempts},{num_solutions}")