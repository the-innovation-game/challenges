from c001_satisfiability.challenge import Challenge
from typing import Tuple
import numpy as np

def solveChallenge(challenge: Challenge) -> Tuple[list, int]:
    # Schöning’s algorithm
    abs_clauses = np.abs(challenge.clauses)
    # random initial assignment
    np.random.seed(challenge.seed)
    variables = np.random.rand(challenge.difficulty.num_variables) < 0.5
    signature = challenge.seed
    for _ in range(challenge.difficulty.num_variables):
        # evaluate clauses and find any that are unsatisfied
        substituted = variables[abs_clauses - 1]
        np.logical_not(substituted, where=challenge.clauses < 0, out=substituted)
        unsatisfied_clauses = np.where(~np.any(substituted, axis=1))[0]
        num_unsatisfied_clauses = len(unsatisfied_clauses)
        if num_unsatisfied_clauses == 0:
            break
        # flip the value of a random variable from a random unsatisfied clause
        rand_unsatisfied_clause = unsatisfied_clauses[signature % num_unsatisfied_clauses]
        rand_variable = abs_clauses[rand_unsatisfied_clause, signature % 3]
        variables[rand_variable - 1] = ~variables[rand_variable - 1]
        # update signature in such a way that its near impossible to replicate except by 
        # running this algorithm on this particular challenge instance
        signature += (
            (-1) ** (signature % 2) * # random sign flip
            rand_variable * rand_unsatisfied_clause
        )
    return variables.tolist(), signature
