from utils.datastructures.priority_queue import PriorityQueue
from game.components import *
from random import seed
from random import random
import heapq
import math


def greedy_best_first_search(initial_state, is_goal, heuristic, visitor):
    """Greedy Best First Search Algorithm

    Keyword arguments:\\
    * initial_state -- starting state of problem.\\
    * heuristic -- a heuristic estimate to goal h(n)

    Return variables:\\
    * None in case of no goal found.\\
    * state -- goal state found.\\
    * nodes_expanded -- final number of expanded nodes to reach goal.\\
    * max_search_depth -- Maximum depth reached where goal resides.
    """
    # Build minimum heap based on heuristic as key.
    frontier = PriorityQueue('min', heuristic)
    frontier.append(initial_state)
    # Build dictionary for O(1) lookups.
    frontier_config = {}
    frontier_config[initial_state] = True
    # Build set of already explored states.
    explored = set()
    # Variables for algorithm evaluation purposes.
    nodes_expanded = 0
    max_search_depth = 0

    while frontier:
        if nodes_expanded >= 10000:
            return (frontier.pop(), nodes_expanded, max_search_depth)
        state = frontier.pop()
        explored.add(state)
        # Goal Test: stop algorithm when goal is reached.
        if is_goal(state):
            return (state, nodes_expanded, max_search_depth)

        nodes_expanded += 1
        for neighbor in visitor.visit(state):
            # Add state to explored states if doesn't already exists.
            if neighbor not in explored and neighbor not in frontier_config:
                frontier.append(neighbor)
                frontier_config[neighbor] = True
                if neighbor.cost > max_search_depth:
                    max_search_depth = neighbor.cost
            # If state is not explored but in frontier, update it's key if less.
            elif neighbor in frontier:
                if heuristic(neighbor) < frontier[neighbor]:
                    frontier.__delitem__(neighbor)
                    frontier.append(neighbor)
    return None

def a_star_search(initial_state, goal_test, heuristic, visitor):
    """A* search Algorithm is greedy best-first graph search with f(n) = g(n)+h(n).

        Args:
        - initial_state -- starting state of problem.
        - goal_test -- Goal test function employed in environment.
        - heuristic -- a heuristic estimate to goal h(n)
        - visitor -- a visitor attached with agent, to ensure layer separation.

        Returns:
        - None in case of no goal found.
        - state -- goal state found.
        - nodes_expanded -- final number of expanded nodes to reach goal.
        - max_search_depth -- Maximum depth reached where goal resides.
    """
    return greedy_best_first_search(initial_state, goal_test, lambda x: x.cost + heuristic(x), visitor)


def real_time_a_star_search(initial_state, goal_test, heuristic, visitor):
    """ An informed search that used to reduce the execution time of A*.

        Args:
        - initial_state : Starting state of problem.
        - heuristic : A heuristic estimate to goal h(n).
        - cost -- A cost function for a state.
        - visitor -- a visitor attached with agent, to ensure layer separation.

        Returns:
        - current_state : A state that eventually will be the goal state.
    """

    visited_states_to_heuristic = {}
    current_state = initial_state
    FIRST_BEST_STATE_INDEX = 2
    SECOND_BEST_TOTAL_COST_INDEX = 0

    while(not goal_test(current_state)):
        total_cost_to_state = []

        # Expand the current state
        for neighbour in visitor.visit(current_state):

            # If the neighbour exists in the visited_states dictionary, then stored heuristic value in the dictionary is used
            # and added to the cost from the current state to the neighbour to get the total cost
            if neighbour in visited_states_to_heuristic.keys():
                neighbour.parent = visited_states_to_heuristic[neighbour].parent
                neighbour.cost = visited_states_to_heuristic[neighbour].cost
                neighbour.depth = visited_states_to_heuristic[neighbour].depth
                neighbour_total_cost = visited_states_to_heuristic[neighbour] + current_state.cost_to(neighbour)

            # Else, then calculate the heuristic value of the neighbour
            # and add it to the cost from the current state to the neighbour to get the total cost
            else:
                neighbour_total_cost = heuristic(neighbour) + current_state.cost_to(neighbour)

            # Store the neighbours & their total cost in a min heap
            # Use random() for tie breaking
            heapq.heappush(total_cost_to_state,
                           (neighbour_total_cost, random(), neighbour))

        temp_state = heapq.heappop(total_cost_to_state)[FIRST_BEST_STATE_INDEX]

        # Store the current state associated with it the second best total cost value
        visited_states_to_heuristic[current_state] = heapq.heappop(
            total_cost_to_state)[SECOND_BEST_TOTAL_COST_INDEX]

        # Choose the state with the minimum total cost to be the new current state
        current_state = temp_state

    return current_state


def minimax_alpha_beta_pruning(initial_state, player_name, opponent_name, utility_function, terminating_test, visitor):
    """ An adverserial search algorithm.

        Args:
        - initial_state -- Starting state of problem.
        - player_name -- The player currently considered as max.
        - opponent_name -- The player currently considered as min.
        - utility_function -- The function that calculates the value of each state to be
            considered by maximize and minimize.
        - terminating_test -- A boolean function that checks wether to consider the state as a
            terminating state and return or not.
        - visitor: The visitor class to be used to take an action in each
            node traversed;it has to contain a visit function that takes no arguments

        Returns:
        - child : A state having the maximum utility that can be reached.
    """
    def minimize(state, alpha, beta):
        if terminating_test(state):
            print("goal reached")
            return None, utility_function(state)

        visitor.player_name = opponent_name
        minChild, minUtility = None, math.inf

        for child in visitor.visit(state):
            dummy_child, utility = maximize(child, alpha, beta)

            if utility < minUtility:
                minChild, minUtility = child, utility
            if minUtility <= alpha:
                break
            if minUtility < beta:
                beta = minUtility

        return minChild, minUtility

    def maximize(state, alpha, beta):
        if terminating_test(state):
            print("goal reached")
            return None, utility_function(state)

        visitor.player_name = player_name
        maxChild, maxUtility = None, -math.inf

        for child in visitor.visit(state):
            dummy_child, utility = minimize(child, alpha, beta)

            if utility > maxUtility:
                maxChild, maxUtility = child, utility
            if maxUtility >= beta:
                break
            if maxUtility > alpha:
                alpha = maxUtility

        return maxChild, maxUtility

    child, utility = maximize(initial_state, -math.inf, math.inf)
    if not child:
        return initial_state
    # print("goal ", len(child.get_owned_territories(visitor.player_name)))
    return child


def real_time_minimax_alpha_beta_pruning(initial_state, player_name, opponent_name, utility_function, cutoff_test, visitor):
    """ An adverserial search algorithm.

        Args:
        - initial_state -- Starting state of problem.
        - player_name -- The player currently considered as max.
        - opponent_name -- The player currently considered as min.
        - utility_function -- The function that calculates the value of each state to be
            considered by maximize and minimize.
        - terminating_test -- A boolean function that checks wether to consider the state as a
            terminating state and return or not.
        - visitor: The visitor class to be used to take an action in each
            node traversed;it has to contain a visit function that takes no arguments

        Returns:
        - child : A state having the maximum utility that can be reached.
    """
    return minimax_alpha_beta_pruning(initial_state, player_name, opponent_name, utility_function, cutoff_test, visitor)
