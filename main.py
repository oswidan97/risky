from utils.search_algorithms import greedy_best_first_search
from game.components import *
from game.action_handlers.risk_visitor import RiskVisitor

if __name__ == "__main__":
    territory1 = Territory("ALexandria", "Swidan", 5)
    territory2 = Territory("Cairo", "Swidan", 4)
    territory3 = Territory("Luxor", "Mostafa", 3)

    territory_neighbours_dict = {territory1:[territory2, territory3],
                                 territory2:[territory1],
                                 territory3:[territory1]}

    initial_state = RiskGameState(territory_neighbours_dict, "Swidan")
    greedy_best_first_search(initial_state, lambda x: 1, RiskVisitor())