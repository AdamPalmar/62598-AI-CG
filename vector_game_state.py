import numpy as np


def set_board_state_vector(player_bool, move_made, state_vector):
    '''
    This method returns the statevector of the game
    :param player_bool:
    :param move_made:
    :param state_vector:

    '''
    move_made = move_made - 1 #There is a indexing convertion

    if player_bool:
        state_vector[0, move_made] = 1
    else:
        state_vector[0, move_made] = -1
    return state_vector


def init_board_state_vector():
    board_state_vector = np.zeros(shape=(1, 9))
    return board_state_vector


def test():
    board = init_board_state_vector()

    board = set_board_state_vector(True, 0, board)
    board = set_board_state_vector(False, 1, board)

    print(board)
