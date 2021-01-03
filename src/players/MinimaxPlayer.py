"""
MiniMax Player
"""
import utils
from players.AbstractPlayer import AbstractPlayer
import numpy as np
from SearchAlgos import MiniMax
import time
from dataclasses import dataclass
from utils import get_directions
#TODO: you can import more modules, if needed

@dataclass(frozen=True)
class State:
    Board: np.array
    Position: tuple
    Score: float
    Rival_Position: tuple
    Rival_Score: float
    My_Turn: bool


class Player(AbstractPlayer):
    def __init__(self, game_time, penalty_score):
        AbstractPlayer.__init__(self, game_time, penalty_score) # keep the inheritance of the parent's (AbstractPlayer) __init__()
        self.position : tuple = None
        self.rival_position : tuple = None
        self.board : np.array = None
        self.my_score = 0
        self.rival_score = 0
        self.minimax = MiniMax(self.utility_function, self.succ_generator,
                               self.make_move, self.is_goal)
        self.fruit_dict = {}
        #TODO: edit MiniMax init params
        #TODO: initialize more fields, if needed, and the Minimax algorithm from SearchAlgos.py


    def set_game_params(self, board):
        """Set the game parameters needed for this player.
        This function is called before the game starts.
        (See GameWrapper.py for more info where it is called)
        input:
            - board: np.array, a 2D matrix of the board.
        No output is expected.
        """
        self.board = board
        self.position = tuple(np.array(np.where(board == 1)).reshape(-1).tolist())
        self.rival_position = tuple(np.array(np.where(board == 2)).reshape(-1).tolist())
        self.my_score = 0
        self.rival_score = 0
        self.find_fruits()


    def make_move(self, time_limit, players_score):
        """Make move with this Player.
        input:
            - time_limit: float, time limit for a single turn.
        output:
            - direction: tuple, specifing the Player's movement, chosen from self.directions
        """
        #time_limit =10
        start_time = time.time()
        curr_state = State(self.board, self.position,
                           self.my_score, self.rival_position, self.rival_score, True)
        i=1
        score, operator = self.minimax.search(curr_state, i, True)
        end_time = time.time()
        last_search_time= end_time-start_time
        total_minimax_time = end_time-start_time
        max_len= len(self.board[0])+len(self.board)#max (len(self.board[0]), len(self.board))
        while (time_limit - total_minimax_time) > last_search_time**3 and i<max_len:
             i+=1
             start_in_loop = time.time()
             score,operator = self.minimax.search(curr_state, i, True)
             end_time = time.time()
             last_search_time = end_time - start_in_loop
             total_minimax_time = end_time - start_time
        self.board[self.position] = -1
        pos = (self.position[0]+operator[0], self.position[1]+operator[1])
        self.board[pos] = 1
        self.position = pos
        self.update_fruits({})
        return operator



    def set_rival_move(self, pos):
        """Update your info, given the new position of the rival.
        input:
            - pos: tuple, the new position of the rival.
        No output is expected
        """
        self.board[self.rival_position] = -1
        self.rival_position = pos
        self.rival_score += self.board[pos]
        self.update_fruits({})
        self.board[pos] = 2


    def update_fruits(self, fruits_on_board_dict):
        """Update your info on the current fruits on board (if needed).
        input:
            - fruits_on_board_dict: dict of {pos: value}
                                    where 'pos' is a tuple describing the fruit's position on board,
                                    'value' is the value of this fruit.
        No output is expected.
        """
        #TODO: erase the following line and implement this function. In case you choose not to use it, use 'pass' instead of the following line.
        if self.position in self.fruit_dict.keys():
            self.fruit_dict.pop(self.position)
        if self.rival_position in self.fruit_dict.keys():
            self.fruit_dict.pop(self.rival_position)



    ########## helper functions in class ##########
    #TODO: add here helper functions in class, if needed
    def find_fruits(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] >0:
                    self.fruit_dict[(i,j)]=self.board[i][j]




    ########## helper functions for MiniMax algorithm ##########
    # TODO: add here the utility, succ, and perform_move functions used in MiniMax algorithm

    def succ_generator(self, state):
        for direction in get_directions():
            if state.My_Turn:
                pos = (state.Position[0]+direction[0], state.Position[1]+direction[1])
            else:
                pos = (state.Rival_Position[0]+direction[0], state.Rival_Position[1]+direction[1])
            if self.pos_feasible_on_board(state.Board, pos):
                new_board = state.Board.copy()
                if state.My_Turn:
                    new_score = state.Score+new_board[pos]
                    new_board[state.Position] = -1
                    new_board[pos] = 1
                    yield direction, State(new_board, pos, new_score, state.Rival_Position,
                                     state.Rival_Score, False)
                else:
                    new_score = state.Rival_Score + new_board[pos]
                    new_board[state.Position] = -1
                    new_board[pos] = 2
                    yield direction, State(new_board,  state.Position,
                                      state.Score, pos, new_score, True)


    def pos_feasible_on_board(self, board, pos):
        # on board
        on_board = (0 <= pos[0] < len(board) and 0 <= pos[1] < len(self.board[0]))
        if not on_board:
            return False

        # free cell
        value_in_pos = self.board[pos[0]][pos[1]]
        free_cell = (value_in_pos not in [-1, 1, 2])
        return free_cell

    def is_goal(self, state):
        board = state.Board
        pos = state.Position
        can_move = False
        for direction in utils.get_directions():
            next_pos = (pos[0] + direction[0], pos[1] + direction[1])
            can_move = can_move or self.pos_feasible_on_board(board, next_pos)

        return not can_move

    def utility_function(self, state: State):
        if self.is_goal(state):
            return state.Score-self.penalty_score - state.Rival_Score, (0, 0)
        return self.heuristic(state)

    def heuristic(self, state: State):
        closest_fruit_direction= (0,0)
        closest_fruit_distance= float('inf')
        curr_pos = state.Position
        curr_rival_pos= state.Rival_Position
        fruit_value = 0
        count_feasble_directions = 0
        count_feasble_directions_rival = 0
        for direction in utils.get_directions():
            pos = curr_pos[0] + direction[0], curr_pos[1] + direction[1]
            rival_pos= curr_rival_pos[0] + direction[0], curr_rival_pos[1] + direction[1]
            if self.pos_feasible_on_board(state.Board, rival_pos):
                count_feasble_directions_rival+=1
            if self.pos_feasible_on_board(state.Board, pos):
                if closest_fruit_direction == (0, 0):
                    closest_fruit_direction = direction
                count_feasble_directions += 1
                for key in self.fruit_dict:
                    dist = self.calc_dist(pos, key)
                    if dist < closest_fruit_distance:
                        closest_fruit_direction = direction
                        closest_fruit_distance = dist
                        fruit_value= self.fruit_dict[key]

        if count_feasble_directions_rival== 0 and count_feasble_directions==0:
            return state.Score - self.rival_score, closest_fruit_direction
        if count_feasble_directions_rival == 0:
            return state.Score + fruit_value + self.penalty_score - self.rival_score, closest_fruit_direction

        if closest_fruit_distance == float('inf'):
            if count_feasble_directions-count_feasble_directions_rival > 0:
                return state.Score + self.penalty_score/2-self.rival_score, closest_fruit_direction
            else:
                return state.Score - self.rival_score, closest_fruit_direction

        if count_feasble_directions-count_feasble_directions_rival > 0:
            return state.Score + fruit_value + self.penalty_score/2 - self.rival_score, closest_fruit_direction
        else:
            return state.Score + fruit_value - self.rival_score, closest_fruit_direction


    def calc_dist(self, pos1, pos2):
        return abs(pos1[0] - pos2[0] + (pos1[1] - pos2[1]))
