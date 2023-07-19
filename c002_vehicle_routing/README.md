# Capacitated Vehicle Routing

[The CVRP, or Capacitated Vehicle Routing Problem, is a well-studied optimisation problem in the field of operations research and transportation logistics](https://en.wikipedia.org/wiki/Vehicle_routing_problem). It involves the task of determining the optimal set of routes a fleet of vehicles should undertake in order to service a given set of customers, while meeting certain constraints.

In the CVRP, a fleet of identical vehicles based at a central depot must be routed to deliver goods to a set of geographically dispersed customers. Each vehicle has a fixed capacity, and each customer has a known demand for goods. The objective is to determine the minimum total distance that the fleet must travel to deliver goods to all customers and return to the depot, such that:

1. Each customer is visited by exactly one vehicle,
2. The total demand serviced by each vehicle does not exceed its capacity, and
3. Each vehicle starts and ends its route at the depot.

# Our Challenge

For our challenge, we use a version of the Capacitated Vehicle Routing problem with configurable difficulty, where the following two parameters can be adjusted in order to vary the diffculty of the challenge:

- Parameter 1: $num\_nodes$
- Parameter 2: $percent\_better\_than\_baseline$

$num\_nodes$ is the number of customers (plus 1 depot) which are uniformly at random placed on a grid of 500 by 500 with the depot at the center (250, 250). 

The demand of each customer is uniformly at random selected from the range [15, 30]. The maximimum capacity of each vehicle is set to 100.

We use a naive greedy algorithm to generate the baseline routes by iteratively selecting the closest unvisited node (returning to depot when necessary) until all drop-offs are made.

For a particular $percent\_better\_than\_baseline$, the objective is to find a set of routes such that the total distance travelled is $percent\_better\_than\_baseline$ shorter than the total distance of the baseline routes.

## Worked Example

Consider an example `Challenge` instance with `num_nodes=5`:

```
demands = [0, 25, 30, 40, 50] # a N array where index (i) is the demand at node i
distance_matrix = [ # a NxN symmetric matrix where index (i,j) is distance from node i to node j
    [0, 10, 20, 30, 40],
    [10, 0, 15, 25, 35],
    [20, 15, 0, 20, 30],
    [30, 25, 20, 0, 10],
    [40, 35, 30, 10, 0]
]
max_capacity = 100 # total demand for each route must not exceed this number 
max_total_distance = 140 # routes must have total distance under this number to be a solution 
```

The depot is the first node (node 0) with demand 0. The vehicle capacity is set to 100. In this example, routes must have a total distance of 140 or less to be a solution.

Now consider the following routes:

```
routes = [
  [0, 3, 4, 0], 
  [0, 1, 2, 0]
]
```

When evaluating these routes, each route has demand less than 100, and the total distance is shorter than 140, thereby these routes are a solution:

* Route 1: 
    * Depot -> 3 -> 4 -> Depot
    * Demand = 40 + 50 = 90
    * Distance = 30 + 10 + 40 = 80
* Route 2: 
    * Depot -> 1 -> 2 -> Depot
    * Demand = 25 + 30 = 55
    * Distance = 10 + 15 + 20 = 45
* Total Distance = 80 + 45 = 125