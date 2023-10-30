from c001_satisfiability.challenge import Challenge
import numpy as np

def solveChallenge(challenge: Challenge) -> list:
    # Schöning’s algorithm
    abs_clauses = np.abs(challenge.clauses)
    # algorithm must be deterministic given the same challenge
    np.random.seed(challenge.seed)
    variables = np.random.rand(challenge.difficulty.num_variables) < 0.5
    # pre-generate a bunch of random integers
    rand_ints = np.random.randint(0, 2 ** 32, size=(2, challenge.difficulty.num_variables))
    for i in range(challenge.difficulty.num_variables):
        # evaluate clauses and find any that are unsatisfied
        substituted = variables[abs_clauses - 1]
        np.logical_not(substituted, where=challenge.clauses < 0, out=substituted)
        unsatisfied_clauses = np.where(~np.any(substituted, axis=1))[0]
        num_unsatisfied_clauses = len(unsatisfied_clauses)
        if num_unsatisfied_clauses == 0:
            break
        # flip the value of a random variable from a random unsatisfied clause
        rand_unsatisfied_clause = unsatisfied_clauses[rand_ints[0, i] % num_unsatisfied_clauses]
        rand_variable = abs_clauses[rand_unsatisfied_clause, rand_ints[1, i] % 3]
        variables[rand_variable - 1] = ~variables[rand_variable - 1]
    return variables.tolist()