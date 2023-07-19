# The Innovation Game Challenges

This repo contains code for the challenges and algorithms featured in [The Innovation Game](http://the-innovation-game.com/)

# Table of Contents
1. [Overview](#1-overview)
2. [Earning TIG Tokens](#2-earning-tig-tokens)
3. [Repo Structure](#3-repo-structure) 
4. [Our Challenges](#4-our-challenges)
5. [Developing & Testing Your Algorithm](#5-developing--testing-your-algorithm)
6. [Submitting Your Algorithm](#submitting-your-algorithm)

# 1. Overview

Algorithms Power Modern Science.

The Innovation Game rewards TIG Tokens for open development of algorithms commensurate with performance improvement.

By providing monetary incentives, The Innovation Game aims to extend the reach of Open Source to algorithms in computational science. In these areas, R&D progress is largely dictated by access to cutting-edge algorithms as performance improvements can reduce computation times by multiple orders of magnitude.

[Read our whitepaper to learn why Open Source currently doens't work well in these areas.](https://files.the-innovation-game.com/the-innovation-game-whitepaper-v1.pdf)

# 2. Earning TIG Tokens

Innovators are players who use their brain power to develop faster algorithms, contributing them under an Open Source license to the The Innovation Game.

Contributed algorithms are pushed to a private version of this repository until the start of a new round (every Monday 00:00 UTC), whereupon the algorithms are merged with this public repository.

Public algorithms can then be benchmarked by players in The Innovation Game. Top performing benchmarks submitted by Benchmarkers earn them TIG Tokens. Innovators earn a royalty when Benchmarkers earn TIG Tokens using their algorithms.

In this way Benchmarkers are incentivised to find the best performing algorithms, and Innovators are incentivised to contribute the best performing algorithms.

# 3. Repo Structure

This repository stores challenges and algorithms in the following structure:

```
├── <challenge_id> # challenge folder with prefix cXXX_ (e.g. c001_satisfiability)
│   ├── __init__.py
│   ├── challenge.py
│   ├── README.md # challenge specific descriptions
│   ├── algorithms
│   │   ├── default.py # every challenge has a naive algorithm called default
│   │   ├── <algorithm_id>.py # user submitted algorithm
│   │   ├── ...
│   │   ├── <algorithm_id>.py # user submitted algorithm
│
├── <challenge_id> # another challenge
├── ...
└── <challenge_id> # another challenge
```

## 3.1 `challenge.py`

Every `challenge.py` implements a `Difficulty` and `Challenge` dataclass:

```
@dataclass
class Difficulty:
    <parameter1>: int
    <parameter2>: int

@dataclass
class Challenge:
    seed: int # The seed used to randomly generate this `Challenge` instance
    difficulty: Difficulty # An instance of `Difficulty` used to generate this `Challenge` instance.
    
    <other challenge specific fields>

    def verifySolution(solution) -> bool:
      # function that outputs true if solution solves the challenge instance. false otherwise

    @classmethod
    def generateInstance(seed: int, difficulty: Difficulty) -> "Challenge":
      # function that generates an instance of the challenge
```

These classes can be imported as follows:
```
from <challenge_id>.challenge import Challenge, Difficulty
```

## 3.2 `algorithms`

Every algorithm is a single python file that must define a `solveChallenge(challenge, logIntermediateValue=int)` function, where:

* `challenge` is an instance of the `Challenge`
* `logIntermediateValue` is a function that takes a single integer as input. Your algorithm should call this function every so often to build up a "signature" for your algorithm. This signature is used to detect when Benchmarkers claim they are using algorithm 'X' but in fact are using algorithm 'Y'

### **IMPORTANT**

* Not every challenge instance has a solution! Your algorithm should take this into account and try to exit early

* Your algorithm will be ran in a sandbox with no internet access and limited to built-in python 3.9 libraries, numpy 1.25.0, and the relevant `challenge.py`

* AWS lambdas are used to re-run randomly sampled benchmarks. If your algorithm takes more than 1024MB of memory or takes longer than 15s to finish, the benchmark is rejected.  

# 4. Our Challenges

If you want to propose a challenge to be featured in The Innovation Game, please reach out to us on [Discord](https://discord.gg/cAuS733x4d).

The Innovation Game currently features the following challenges:

1. [Boolean Satisfiability (3-SAT)](c001_satisfiability/README.md)

2. [Capacitated Vehicle Routing](c002_vehicle_routing/README.md)

3. [Knapsack Problem](c003_knapsack/README.md)

# 5. Developing & Testing Your Algorithm

1. Read section 3 above before getting started

2. Develop your algorithm locally. It is recommended that you start by copying, renaming and modifying an existing algorithm

3. Test your algorithm locally. Example:

```python
from <YOUR CHALLENGE>.algorithms.<YOUR ALGORITHM ID> import solveChallenge
from <YOUR CHALLENGE>.challenge import Challenge, Difficulty
from datetime import datetime

difficulty = Difficulty(<Param1>, <Param2>)
results = {'solved': 0, 'no solution found': 0, 'errored': 0}
start = datetime.now()
for seed in range(100):
    challenge = Challenge.generateInstance(seed, difficulty)
    try:
        solution = solveChallenge(challenge)
        if challenge.verifySolution(solution):
            results['solved'] += 1
        else:
            results['no solution found'] += 1
    except:
        results['errored'] += 1

seconds_elapsed = (datetime.now() - start).total_seconds()
print(f"Seconds elapsed: {seconds_elapsed}")
print(f"Results: {results}")
```

3. Test your algorithm will be accepted by submitting it with `dry_run` enabled:

    a. You can get an API Key through our [Simple Benchmarker on Google Colabs](https://colab.research.google.com/github/the-innovation-game/simple_benchmarker/blob/master/notebook.ipynb)

```python
import requests

API_URL = "https://api.the-innovation-game.com/prod"
API_KEY = "<YOUR API KEY>"
CHALLENGE_ID = "<YOUR ALGORITHM'S CHALLENGE>" # e.g. c001_satisfiability

result = requests.post(
    f"{API_URL}/player/submitAlgorithm/{CHALLENGE_ID}",
    headers={
        'X-Api-Key': API_KEY,
    },
    params={
        'dry_run': True # IMPORTANT
    },
    files={
        # REQUIRED FIELDS
        'algorithm.py': open("<YOUR PYTHON CODE FILE>", "r").read(), # Python code of your algorithm
        'algorithm_id': "<YOUR ALGORITHM ID>", # Name of your algorithm. 20 characters max
        
        # OPTIONAL FIELDS (can remove)
        'algorithm.md': open("<YOUR MARKDOWN FILE>", "r").read(), # Markdown description of your algorithm
        'git_user': "<YOUR GIT USER>", # User of the commit adding your algorithm. 39 characters max
        'git_email': "<YOUR GIT EMAIL>" # Email of the commit adding your algorithm. 50 characters max
    }
).text
print(result)
```

# Submitting Your Algorithm

1. Check the TIG token cost of submitting an algorithm this round (updated every round).

```python
import requests

API_URL = "https://api.the-innovation-game.com/prod"

round_config = requests.get(f"{API_URL}/tig/getLatestBlock").json()

print(f"Current Round: {round_config['round']}")
print(f"Can Submit Algorithm: {not round_config['algorithm_submissions_killswitch'] and round_config['round_started']}")
print(f"Cost to Submit Algorithm: {round_config['algorithm_submission_cost']} TIG Tokens")
print(f"Minimum %Adoption of Algorithm by Benchmarkers to Start Earning Royalties: {round_config['algorithm_adoption_threshold'] * 100}%")
```

2. Check your available TIG tokens:

    a. You can always earn TIG tokens through our [Simple Benchmarker on Google Colabs](https://colab.research.google.com/github/the-innovation-game/simple_benchmarker/blob/master/notebook.ipynb)

```python
import requests

API_URL = "https://api.the-innovation-game.com/prod"
API_KEY = "<YOUR API KEY>"

summary = requests.get(
    f"{API_URL}/player/getSummary",
    headers={
        'X-Api-Key': API_KEY
    }
).json()

total_earnt = summary['benchmarker_earnings']['total'] + summary['innovator_earnings']['total']
total_spent = summary['total_spent']
print(f"Total TIG Earnt: {total_earnt}")
print(f"Total TIG Spent: {total_spent}")
print(f"Total TIG Available: {total_earnt - total_spent}")
```

3. Submit your algorithm. You need to enable `accept_terms`:

    a. If your algorithm is derived from Open Source code,  make sure to adhere to any license terms. All other algorithms will be subject to the Open Source license in their particular challenge's folder.

```python
import requests

API_URL = "https://api.the-innovation-game.com/prod"
API_KEY = "<YOUR API KEY>"
CHALLENGE_ID = "<YOUR ALGORITHM'S CHALLENGE>" # e.g. c001_satisfiability

result = requests.post(
    f"{API_URL}/player/submitAlgorithm/{CHALLENGE_ID}",
    headers={
        'X-Api-Key': API_KEY,
    },
    params={
        'accept_terms': True # IMPORTANT
    },
    files={
        # REQUIRED FIELDS
        'algorithm.py': open("<YOUR PYTHON CODE FILE>", "r").read(), # Python code of your algorithm
        'algorithm_id': "<YOUR ALGORITHM ID>", # Name of your algorithm. 20 characters max
        
        # OPTIONAL FIELDS (can remove)
        'algorithm.md': open("<YOUR MARKDOWN FILE>", "r").read(), # Markdown description of your algorithm
        'git_user': "<YOUR GIT USER>", # User of the commit adding your algorithm. 39 characters max
        'git_email': "<YOUR GIT EMAIL>" # Email of the commit adding your algorithm. 50 characters max
    }
).text
print(result)
```