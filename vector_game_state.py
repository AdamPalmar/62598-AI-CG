import numpy as np


def init_board_state_vector():
    board_state_vector = np.zeros(shape=(1, 9), dtype='int32')
    return board_state_vector


def init_training_game_matrix(size):
    training_game_matrix = np.zeros(shape=(size, 9), dtype='int32')
    return training_game_matrix


def init_end_game_status_vector(size):
    return np.zeros(shape=(size, 5), dtype='int32')


def set_result_of_game(index_game, game_status_matrix, result_of_game, start_index, end_index, first_player):
    # 1, 0, -1
    # Indicates what player to look at
    game_status_matrix[index_game, 0] = result_of_game
    game_status_matrix[index_game, 1] = start_index
    game_status_matrix[index_game, 2] = end_index
    game_status_matrix[index_game, 4] = end_index - start_index

    # print(end_index - start_index ,"Len game")
    if first_player == "player":
        game_status_matrix[index_game, 3] = 1
    else:
        game_status_matrix[index_game, 3] = -1


def set_board_state_vector(player_bool, move_made, state_vector):
    '''
    This method returns the statevector of the game
    :param player_bool:
    :param move_made:
    :param state_vector:

    '''
    move_made = move_made - 1  # There is a indexing convertion

    if player_bool:
        state_vector[0, move_made] = 1
    else:
        state_vector[0, move_made] = -1
    return state_vector


def add_move_to_game_matrix(index, game_matrix, board_vector):
    game_matrix[index] = board_vector


def test():
    board = init_board_state_vector()
    training = init_training_game_matrix(9)

    board = set_board_state_vector(True, 1, board)
    add_move_to_game_matrix(0, training, board)

    board = set_board_state_vector(False, 2, board)
    add_move_to_game_matrix(1, training, board)

    board = set_board_state_vector(True, 3, board)
    add_move_to_game_matrix(2, training, board)

    board = set_board_state_vector(False, 4, board)
    add_move_to_game_matrix(3, training, board)

    board = set_board_state_vector(True, 5, board)
    add_move_to_game_matrix(4, training, board)

    board = set_board_state_vector(False, 6, board)
    add_move_to_game_matrix(5, training, board)

    board = set_board_state_vector(True, 7, board)
    add_move_to_game_matrix(6, training, board)

    board = set_board_state_vector(False, 8, board)
    add_move_to_game_matrix(7, training, board)

    board = set_board_state_vector(True, 9, board)
    add_move_to_game_matrix(8, training, board)

    print(training)
    print("-"*5)
    print(board)
    print(-board)

# test()
