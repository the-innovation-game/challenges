from c003_knapsack.challenge import Challenge
import numpy as np

def solveChallenge(challenge: Challenge) -> list:
    max_weight = challenge.max_weight
    min_value = challenge.min_value
    num_items = challenge.difficulty.num_items
    # each row is a single combo
    # cols 0 to num_items - 1 are flags for which items are in that combo
    # cols -2 is total value of that combo
    # cols -1 is total weight of that combo
    combinations = np.zeros((1, num_items + 2), dtype=int)
    # prioritize high value to weight items
    sorted_items = np.argsort(challenge.values / challenge.weights)[::-1]
    solution = []
    for i in range(challenge.weights.shape[0]):
        item = sorted_items[i]
        # create new combos with current item
        new_combinations = combinations.copy()
        new_combinations[:, -2] -= challenge.values[item]
        new_combinations[:, -1] -= challenge.weights[item]
        new_combinations[:, item] = 1
        # remove combos that exceed weight limit
        new_combinations = new_combinations[np.where(new_combinations[:, -1] >= -max_weight)]
        if new_combinations[0, -2] <= -min_value:
            solution = np.where(new_combinations[0,:num_items])[0].tolist()
            break
        # merge with existing combos
        # if there are multiple combos with the same weight, keep the highest value one
        combinations = np.concatenate((combinations, new_combinations), axis=0)
        combinations = combinations[np.argsort(combinations[:, -2])]
        combinations = combinations[np.unique(combinations[:, -1], return_index=True)[1]]
    return solution