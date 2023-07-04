from c003_knapsack.challenge import Challenge
import numpy as np

def solveChallenge(challenge: Challenge, logIntermediateInteger=print) -> np.ndarray:
    # Seed the random number generator.
    np.random.seed(challenge.seed)
    # Try up to 1000 attempts to find a solution using a naive algorithm.
    for _ in range(1000):
        items = []
        total_weight = 0
        # randomly iterate through items
        for item in np.argsort(np.random.rand(challenge.difficulty.num_items)):
            # add the item if its not too heavy
            if total_weight + challenge.weights[item] <= challenge.max_weight:
                items.append(int(item)) # cast to int because np.int64 is not JSON serialisable
                total_weight += challenge.weights[item]
        # Log an intermediate integer that is near impossible to fake unless this algorithm is ran 
        logIntermediateInteger(int(np.random.rand() * 10e6))       
        # Check if the items is a solution
        if challenge.verifySolution(items):
            break
    return items