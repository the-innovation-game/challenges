from typing import Union, Dict
from dataclasses import dataclass
import numpy as np

@dataclass
class Difficulty:
    # Number of variables from which 3 are sampled for each clause in the 3SAT problem
    num_variables: int
    # The ratio of num clauses to num variables in the 3SAT problem in percent (e.g. 3.5 is stored as 350)
    clauses_to_variables_percent: int
    
@dataclass
class Challenge:
    seed: int
    difficulty: Difficulty
    clauses: np.ndarray

    def verifySolution(self, solution: list) -> bool:
        try:
            variables = np.array(solution, dtype=bool)
            if variables.shape != (self.difficulty.num_variables,):
                raise Exception("Invalid variables. Expecting a list of length <num_variables> where entries are either True or False")
            v = variables[np.abs(self.clauses) - 1]
            np.logical_not(v, where=self.clauses < 0, out=v)
            return bool(np.all(np.any(v, axis=1), axis=0))
        except Exception as e:
            raise Exception("Invalid solution") from e

    @classmethod
    def generateInstance(cls, seed: int, difficulty: Union[Difficulty, Dict[str, int]]) -> "Challenge":
        if isinstance(difficulty, dict):
            difficulty = Difficulty(**difficulty)
        np.random.seed(seed)
        num_clauses = int(np.floor(difficulty.num_variables * difficulty.clauses_to_variables_percent / 100))

        # Create clauses by randomly picking 3 distinct variables for each clause.
        clauses = np.argsort(
            np.random.rand(num_clauses, difficulty.num_variables),
            axis=1
        )[:, :3] + 1

        # Randomly negate literals in the clauses.
        clauses = clauses * np.random.choice([-1, 1], size=(num_clauses, 3))

        return cls(
            seed=seed,
            difficulty=difficulty,
            clauses=clauses
        )