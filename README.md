# The Innovation Game Challenges

This repo contains code for the challenges and algorithms featured in [The Innovation Game](http://the-innovation-game.com/). 

[Refer to this document for terms regarding use of this repository.](https://www.the-innovation-game.com/terms-regarding-repository-and-content)

# Table of Contents
1. [Overview](#1-overview)
2. [Earning TIG Tokens](#2-earning-tig-tokens)
3. [Repo Structure](#3-repo-structure) 
4. [Our Challenges](#4-our-challenges)
5. [Developing & Testing Your Algorithm](#5-developing--testing-your-algorithm)
6. [Submitting Your Algorithm](#6-submitting-your-algorithm)
7. [Licenses](#7-licenses)

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

* An algorithm is a single python file that must define a `solveChallenge(challenge) -> list` function

    * If you are using numpy arrays, remember to convert to a python list! e.g. `arr.tolist()`

* Not every challenge instance has a solution! Your algorithm should take this into account and try to exit early

* Your algorithm will be ran in a sandbox with no internet access and limited to built-in python 3.9 libraries, numpy 1.25.0, and the relevant `challenge.py`

* Solutions submitted by benchmarkers are random sampled and verified by AWS lambdas. If your algorithm takes more than 1024MB of memory or takes longer than 5s to finish, the solution is rejected.

# 4. Our Challenges

If you want to propose a challenge to be featured in The Innovation Game, please reach out to us on [Discord](https://discord.gg/cAuS733x4d).

The Innovation Game currently features the following challenges:

1. [Boolean Satisfiability (3-SAT)](c001_satisfiability/README.md)

2. [Capacitated Vehicle Routing](c002_vehicle_routing/README.md)

3. [Knapsack Problem](c003_knapsack/README.md)

# 5. Developing & Testing Your Algorithm

1. Read section 3 above before getting started

2. Develop your algorithm locally. It is recommended that you start by copying, renaming and modifying an existing algorithm

3. Test your algorithm locally on our small suite of difficulty paramter combinations. 

    * Example: `python algo_tester.py c001_satisfiability default`
    * Options: `python algo_tester.py --help`

# 6. Submitting Your Algorithm

Follow the steps on our [Innovator Dashboard](https://www.the-innovation-game.com/innovator-dashboard)

# 7. Licenses

