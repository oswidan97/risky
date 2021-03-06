from game.agents.base_agent import BaseAgent
from game.action_handlers.actions import reinforce_territory
from random import seed
from random import randint
import operator

class PassiveAgent(BaseAgent):

    def __init__(self, player_name):
        super().__init__(player_name)

    def place_initial_armies(self, initial_state):
        """ Place Initial Armies on board. Executed once at begining of game.

            Arguments:\\
                * current_state: The current Map State of the game.\\
            Returns:\\
                * result_state: The resulting Map State of the game.
        """
        ARMIES_NUMBER = 1
        # Get all owned territories
        owned_territories = initial_state.get_owned_territories(self.player_name)

        # Add one army to a random territory
        random_int = randint(0, len(owned_territories) - 1)
        print("passive random element to place init armies",random_int)
        owned_territories[random_int].number_of_armies += ARMIES_NUMBER

    def take_turn(self, current_state):
        """ Take Turn in game. Executed each turn on agents.

            Arguments:\\
                * current_state: The current Map State of the game.\\
            Returns:\\
                * result_state: The resulting Map State of the game.
        """
        return self.passive_strategy(current_state)

    def passive_strategy(self, current_state):
        """ Employs Passive Strategy: that places all of its bonus armies to the territory with
            the fewest armies, and doesn’t make any attacks.

            Arguments:\\
                * current_state: The current Map State of the game.\\
            Returns:\\
                * result_state: The resulting Map State of the game.
        """
        # Retrieve the player owned territories
        player_owned_territories = current_state.get_owned_territories(self.player_name)

        # Sort the owned territories based on the number of armies
        player_owned_territories.sort(key=operator.attrgetter('number_of_armies'))

        # Get the territory with the fewest number of armies
        territory_with_fewest_armies = player_owned_territories[0]

        # Reinforce the territory with the fewest number of armies with the additional armies
        reinforce_territory(current_state, territory_with_fewest_armies,current_state.get_additional_armies(self.player_name))

        return current_state
