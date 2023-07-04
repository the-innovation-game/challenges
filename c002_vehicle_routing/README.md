
# Challenge Background

The CVRP, or Capacitated Vehicle Routing Problem, is a well-studied optimisation problem in the field of operations research and transportation logistics. It involves the task of determining the optimal set of routes a fleet of vehicles should undertake in order to service a given set of customers, while meeting certain constraints.

In the CVRP, a fleet of identical vehicles based at a central depot must be routed to deliver goods to a set of geographically dispersed customers. Each vehicle has a fixed capacity, and each customer has a known demand for goods. The objective is to determine the minimum total distance that the fleet must travel to deliver goods to all customers and return to the depot, such that:

1. Each customer is visited by exactly one vehicle,
2. The total demand serviced by each vehicle does not exceed its capacity, and
3. Each vehicle starts and ends its route at the depot.

# Our Challenge

For our challenge, we use a version of the Capacitated Vehicle Routing problem with configurable difficulty, where the following two parameters can be adjusted in order to vary the diffculty of the challenge:

- Parameter 1:  $num\textunderscore{}nodes$
- Parameter 2: $percent\textunderscore{}better\textunderscore{}than\textunderscore{}baseline$

$num\textunderscore{}nodes$ is the number of customers - 1 (includes depot) which are uniformly at random placed on a grid of 500 by 500 with the depot at the center (250, 250). 

The demand of each customer is uniformly at random selected from the range [15, 30]. The maximimum capacity of each vehicle is set to 100.

We use a naive greedy algorithm to generate the baseline routes by iteratively selecting the closest unvisited node (returning to depot when necessary) until all drop-offs are made.

For a particular $percent\textunderscore{}better\textunderscore{}than\textunderscore{}baseline$, the objective is to find a set of routes such that the total distance travelled is $percent\textunderscore{}better\textunderscore{}than\textunderscore{}baseline$ shorter than the total distance of the baseline routes.