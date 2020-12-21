"""Search Algos: MiniMax, AlphaBeta
"""
from utils import ALPHA_VALUE_INIT, BETA_VALUE_INIT
#TODO: you can import more modules, if needed


class SearchAlgos:
    def __init__(self, utility, succ, perform_move, goal=None):
        """The constructor for all the search algos.
        You can code these functions as you like to, 
        and use them in MiniMax and AlphaBeta algos as learned in class
        :param utility: The utility function.
        :param succ: The succesor function.
        :param perform_move: The perform move function.
        :param goal: function that check if you are in a goal state.
        """
        self.utility = utility
        self.succ = succ
        self.perform_move = perform_move
        self.goal= goal
    def search(self, state, depth, maximizing_player):
        pass


class MiniMax(SearchAlgos):

    def search(self, state, depth, maximizing_player):
        """Start the MiniMax algorithm.
        :param state: The state to start from.
        :param depth: The maximum allowed depth for the algorithm.
        :param maximizing_player: Whether this is a max node (True) or a min node (False).
        :return: A tuple: (The min max algorithm value, The direction in case of max node or None in min mode)
        """
        if depth== 0:
            return self.utility(state)
        if not self.goal ==None and self.goal(state):
            return state.Score, (0, 0)
        next_move: tuple = (0, 0)
        promised_score: float = float('-inf') if maximizing_player else float('inf')
        for dir, succ in self.succ(state):
            score, move = self.search(succ, depth-1, not maximizing_player)
            if maximizing_player and score > promised_score:
                promised_score = score
                next_move = dir
            elif not maximizing_player and score < promised_score:
                promised_score = score
                next_move = None

        if maximizing_player:
            return promised_score, next_move
        return promised_score, None


class AlphaBeta(SearchAlgos):

    def search(self, state, depth, maximizing_player, alpha=ALPHA_VALUE_INIT, beta=BETA_VALUE_INIT):
        """Start the AlphaBeta algorithm.
        :param state: The state to start from.
        :param depth: The maximum allowed depth for the algorithm.
        :param maximizing_player: Whether this is a max node (True) or a min node (False).
        :param alpha: alpha value
        :param: beta: beta value
        :return: A tuple: (The min max algorithm value, The direction in case of max node or None in min mode)
        """
        #TODO: erase the following line and implement this function.
        raise NotImplementedError
