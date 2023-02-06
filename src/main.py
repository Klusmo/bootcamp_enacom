"""Main module"""
from typing import List
import pandas as pd

from valuable_item import ValuableItem
from optimizer import optimization_problem, run_optimization


def items_to_table(options: List[ValuableItem]) -> pd.DataFrame:
    """Returns a table with the options and their values."""
    records = [
        {
            "Opções": i.option,
            "Custo [R$]": i.cost,
            "Lucro [R$]": i.profit,
        }
        for i in options
    ]
    records.append(
        {
            "Opções": "Total",
            "Custo [R$]": sum(i.cost for i in options),
            "Lucro [R$]": sum(i.profit for i in options),
        }
    )
    return pd.DataFrame.from_records(records)


def solve_knapsack_milp(
    capacity: float, items: List[ValuableItem], verbose: bool = False
) -> List[ValuableItem]:
    """Knapsack problem"""

    problem = optimization_problem(capacity, items, verbose)
    decision_variables = run_optimization(problem, verbose)

    selected = []
    for item, item_was_selected in zip(items, decision_variables):
        if item_was_selected:
            selected.append(item)
    return selected


def main():
    """Main function"""

    capacity = 1000
    # normal case
    cost = [470, 400, 170, 270, 340, 230, 50, 440]

    # case with 1 and 5 items must be selected
    # cost = [70, 400, 170, 270, 40, 230, 50, 440]

    # case with 4 is selected and 2 is not selected
    # cost = [470, 800, 170, 270, 340, 230, 50, 440]
    value = [410, 330, 140, 250, 320, 320, 90, 190]

    items = [
        ValuableItem(f"opcao {i+1}", v, w) for i, (v, w) in enumerate(zip(cost, value))
    ]
    selected = solve_knapsack_milp(capacity, items, verbose=True)

    print(f"Investimentos disponíveis: {len(items)}")
    print(f"Capital disponível: {capacity}")
    print(items_to_table(items), end="\n\n")

    print(f"Investimentos escolhidos: {len(selected)}")
    print(items_to_table(selected), end="\n\n")


if __name__ == "__main__":
    main()
