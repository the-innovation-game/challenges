from datetime import datetime
import itertools
import os
import json
import argparse

challenges = [
    'c001_satisfiability', 
    'c002_vehicle_routing',
    'c003_knapsack'
]
algorithms = {
    c: [
        f[:-3] for f in os.listdir(f"{c}/algorithms")
        if f.endswith(".py") and f != "__init__.py"
    ]
    for c in challenges
}
param1 = {
    'c001_satisfiability': {
        'name': 'num_variables',
        'default_values': [50, 75, 100, 125, 150, 175, 200]
    }, 
    'c002_vehicle_routing': {
        'name': 'num_nodes',
        'default_values': [40, 60, 80, 100, 120, 140, 160]
    },
    'c003_knapsack': {
        'name': 'num_items',
        'default_values': [200, 225, 250, 275, 300, 325, 350, 375, 400]
    }
}
param2 = {
    'c001_satisfiability': {
        'name': 'clauses_to_variables_percent',
        'default_values': [300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400]
    }, 
    'c002_vehicle_routing': {
        'name': 'percent_better_than_baseline',
        'default_values': [25, 30, 35, 40, 45, 50]
    },
    'c003_knapsack': {
        'name': 'percent_better_than_expected_value',
        'default_values': [20, 30, 40, 50, 60, 70]
    }
}

def dumpObj(o, d=0):
    if isinstance(o, dict):
        return (
            "{\n" + 
            "\n".join(
                "  " * (d+1) + k + ": " + dumpObj(v, d + 1)
                for k, v in o.items()
            ) + 
            "\n" + "  " * d + "}"
        )
    if isinstance(o, list):
        return "[" + ", ".join(str(v) for v in o) + "]"
    else:
        return str(o)

parser = argparse.ArgumentParser("Algorithm Tester", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('challenge', help=f"Pick a challenge:\n{dumpObj(challenges)}")
parser.add_argument('algorithm', help=f"Pick an algorithm for your specific challenge:\n{dumpObj(algorithms)}")
parser.add_argument('-x', nargs='+', type=int, help=f"Pick values for 1st difficulty parameter:\n{dumpObj(param1)}")
parser.add_argument('-y', nargs='+', type=int, help=f"Pick values for 2nd difficulty parameter:\n{dumpObj(param2)}")
parser.add_argument('-d', '--duration', type=float, help="Pick duration to test algorithm for each difficulty parameter combination", default=5)
args = parser.parse_args()

if args.challenge not in challenges:
    parser.error(f"challenge must be one of:\n{dumpObj(challenges)}")
if args.algorithm not in algorithms[args.challenge]:
    parser.error(f"algorithm for challenge '{args.challenge}' must be one of:\n{dumpObj(algorithms[args.challenge])}")
xs = args.x or param1[args.challenge]['default_values']
ys = args.y or param2[args.challenge]['default_values']

Challenge = __import__(f"{args.challenge}.challenge").challenge.Challenge
Difficulty = __import__(f"{args.challenge}.challenge").challenge.Difficulty
solveChallenge = getattr(
    __import__(f"{args.challenge}.algorithms.{args.algorithm}").algorithms,
    args.algorithm
).solveChallenge

print(f"{param1[args.challenge]['name']},{param2[args.challenge]['name']},duration,num_attempts,num_solutions")
for x, y in itertools.product(xs, ys):
    start = datetime.now()
    num_attempts = 0
    num_solutions = 0
    while (elapsed := (datetime.now() - start).total_seconds()) < args.duration:
        try:
            difficulty = Difficulty(x, y)
            challenge = Challenge.generateInstance(num_attempts, difficulty)
            solution = solveChallenge(challenge)
            try:
                solution_dump = json.dumps(solution)
            except:
                raise Exception("Failed to JSON serialize solution")
            solution2 = solveChallenge(challenge)
            try:
                solution_dump2 = json.dumps(solution2)
            except:
                raise Exception("Failed to JSON serialize solution")
            if solution_dump != solution_dump2:
                raise Exception("Mismatched output from re-running algorithm on the same challenge instance. Did you seed your random number generator with 'challenge.seed'?")
            if challenge.verifySolution(solution):
                num_solutions += 1
        except Exception as e:
            raise Exception(f"Error encountered using algorithm '{args.algorithm}' to solve instance of challenge '{args.challenge}' with seed '{num_attempts}' and difficulty '{difficulty}'") from e
        num_attempts += 1
    print(f"{x},{y},{elapsed},{num_attempts},{num_solutions}")