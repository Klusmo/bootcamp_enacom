from typing import List
import numpy as np

from science_optimization.builder import OptimizationProblem
from science_optimization.solvers import Optimizer
from science_optimization.algorithms.linear_programming import Glop

from knapsack import Knapsack
from valuable_item import ValuableItem

def optimization_problem(
    capacity: float, available_items: List[ValuableItem], verbose: bool = False
) -> OptimizationProblem:
    """Builds the optimization problem"""
    knapsack = Knapsack(capacity, available_items)
    problem = OptimizationProblem(builder=knapsack)
    if verbose:
        print(problem.info())
    return problem


def run_optimization(problem: OptimizationProblem, verbose: bool = False) -> np.array:
    """Runs the optimization"""
    optimizer = Optimizer(opt_problem=problem, algorithm=Glop())
    results = optimizer.optimize()
    decision_variables = results.x.ravel()
    if verbose:
        print(f"Decision variable:\n{decision_variables}")
    return decision_variables
