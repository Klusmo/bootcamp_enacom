"""Knapsack problem"""
from typing import List

from science_optimization.builder import (
    BuilderOptimizationProblem,
    Variable,
    Constraint,
    Objective,
)

from science_optimization.function import (
    FunctionsComposite,
    LinearFunction,
)

import numpy as np
from valuable_item import ValuableItem


class Knapsack(BuilderOptimizationProblem):
    """Knapsack problem builder"""

    def __init__(self, capacity: float, available_items: List[ValuableItem]):
        self.__capacity = capacity
        self.__items = available_items

    @property
    def __num_vars(self) -> int:
        return len(self.__items)

    @property
    def __weights(self) -> np.array:
        return np.array([item.cost for item in self.__items]).reshape(-1, 1)

    @property
    def __values(self) -> np.array:
        return np.array([item.profit for item in self.__items]).reshape(-1, 1)

    def build_variables(self):
        x_min = np.zeros((self.__num_vars, 1))
        x_max = np.ones((self.__num_vars, 1))
        x_type = ["d"] * self.__num_vars  # Discrete variable

        return Variable(x_min, x_max, x_type)

    def build_constraints(self) -> Constraint:
        """Problem constraints"""
        ineq_cons = FunctionsComposite()
        eq_cons = FunctionsComposite()

        # c * x - d <= 0
        constraint = LinearFunction(c=self.__weights, d=-self.__capacity)
        ineq_cons.add(constraint)

        # 1 and 5 are the indices + 1 of the variables that will be used in the constraint
        # x1 + x5 <= 1
        coeficients = np.array([[1, 0, 0, 0, 1, 0, 0, 0]]).transpose()
        constants = -1
        constraint2 = LinearFunction(c=coeficients, d=constants)
        ineq_cons.add(constraint2)

        # 2 and 4 are the indices + 1 of the variables that will be used in the constraint
        # x2 and x4 must be selected together
        # x2 = x4 ->> x2 - x4 = 0
        coeficients = np.array([[0, 1, 0, -1, 0, 0, 0, 0]]).transpose()
        constants = 0
        constraint3 = LinearFunction(c=coeficients, d=constants)
        eq_cons.add(constraint3)

        return Constraint(ineq_cons=ineq_cons, eq_cons=eq_cons)

    def build_objectives(self) -> Objective:
        # minimize -v*x
        objective_function = LinearFunction(c=-self.__values)

        function_builder = FunctionsComposite()
        function_builder.add(objective_function)

        return Objective(objective=function_builder)
