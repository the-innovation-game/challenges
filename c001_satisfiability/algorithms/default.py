from c001_satisfiability.challenge import Challenge
import numpy as np

def solveChallenge(challenge: Challenge, logIntermediateInteger=print) -> np.ndarray:
    # Seed the random number generator.
    np.random.seed(challenge.seed)
    # Try up to 1000 attempts to find a solution using a naive algorithm.
    for _ in range(1000):
        # Generate a random assignment of variables.
        v = np.random.rand(challenge.difficulty.num_variables)
        variables = v < 0.5
        # Log an intermediate integer that is near impossible to fake unless this algorithm is ran
        logIntermediateInteger(int(np.max(v) * 10e6))
        # Check if the current assignment satisfies all clauses.
        if challenge.verifySolution(variables):
            break
    return variables
