# Tic Tac Toe

# The TicTacToe base game is provided here.
# http://inventwithpython.com/tictactoe.py


import random
import vector_game_state as vgs
import numpy as np

import network_training as network


def drawBoard(board):
    # This function prints out the board that it was passed.

    # "board" is a list of 10 strings representing the board (ignore index 0)
    print('   |   |')
    print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
    print('   |   |')


def inputPlayerLetter(is_training_game=False):
    # Lets the player type which letter they want to be.
    # Returns a list with the player's letter as the first item, and the computer's letter as the second.
    if is_training_game:
        if random.randint(0, 1) == 1:
            return ['X', 'O']
        else:
            return ['O', 'X']
    letter = ''
    while not (letter == 'X' or letter == 'O'):
        print('Do you want to be X or O?')
        letter = input().upper()

    # the first element in the tuple is the player's letter, the second is the computer's letter.
    if letter == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']


def whoGoesFirst():
    # Randomly choose the player who goes first.
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'


def playAgain():
    # This function returns True if the player wants to play again, otherwise it returns False.
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')


def makeMove(board, letter, move):
    board[move] = letter


def isWinner(bo, le):
    # Given a board and a player's letter, this function returns True if that player has won.
    # We use bo instead of board and le instead of letter so we don't have to type as much.
    return ((bo[7] == le and bo[8] == le and bo[9] == le) or  # across the top
            (bo[4] == le and bo[5] == le and bo[6] == le) or  # across the middle
            (bo[1] == le and bo[2] == le and bo[3] == le) or  # across the bottom
            (bo[7] == le and bo[4] == le and bo[1] == le) or  # down the left side
            (bo[8] == le and bo[5] == le and bo[2] == le) or  # down the middle
            (bo[9] == le and bo[6] == le and bo[3] == le) or  # down the right side
            (bo[7] == le and bo[5] == le and bo[3] == le) or  # diagonal
            (bo[9] == le and bo[5] == le and bo[1] == le))  # diagonal


def getBoardCopy(board):
    # Make a duplicate of the board list and return it the duplicate.
    dupeBoard = []

    for i in board:
        dupeBoard.append(i)

    return dupeBoard


def isSpaceFree(board, move):
    # Return true if the passed move is free on the passed board.
    return board[move] == ' '


def getPlayerMove(board):
    # Let the player type in his move.
    move = ' '
    while move not in '1 2 3 4 5 6 7 8 9'.split() or not isSpaceFree(board, int(move)):
        print('What is your next move? (1-9)')
        move = input()
    return int(move)


def chooseRandomMoveFromList(board, movesList):
    # Returns a valid move from the passed list on the passed board.
    # Returns None if there is no valid move.
    possibleMoves = []
    for i in movesList:
        if isSpaceFree(board, i):
            possibleMoves.append(i)

    if len(possibleMoves) != 0:
        return random.choice(possibleMoves)
    else:
        return None


def getComputerMove(board, computerLetter):
    # Given a board and the computer's letter, determine where to move and return that move.
    if computerLetter == 'X':
        playerLetter = 'O'
    else:
        playerLetter = 'X'

    # Here is our algorithm for our Tic Tac Toe AI:
    # First, check if we can win in the next move
    for i in range(1, 10):
        copy = getBoardCopy(board)
        if isSpaceFree(copy, i):
            makeMove(copy, computerLetter, i)
            if isWinner(copy, computerLetter):
                return i

    # Check if the player could win on his next move, and block them.
    for i in range(1, 10):
        copy = getBoardCopy(board)
        if isSpaceFree(copy, i):
            makeMove(copy, playerLetter, i)
            if isWinner(copy, playerLetter):
                return i

    # THIS LINE WAS ADDED
    return chooseRandomMoveFromList(board, [1, 2, 3, 4, 5, 6, 7, 8, 9])

    # # Try to take one of the corners, if they are free.
    # move = chooseRandomMoveFromList(board, [1, 3, 7, 9])
    # if move != None:
    #     return move
    #
    # # Try to take the center, if it is free.
    # if isSpaceFree(board, 5):
    #     return 5
    #
    # # Move on one of the sides.
    # return chooseRandomMoveFromList(board, [2, 4, 6, 8])
    #


def isBoardFull(board):
    # Return True if every space on the board has been taken. Otherwise return False.
    for i in range(1, 10):
        if isSpaceFree(board, i):
            return False
    return True


def print_status(show_print_output, move, board_vector):
    if show_print_output:
        print("The move was ", move)
        print("The board state is ", board_vector)


def init_game(is_training_game, num_plays):
    board_vector = vgs.init_board_state_vector()
    the_board = [' '] * 10
    player_letter, computer_letter = inputPlayerLetter(is_training_game)
    turn = whoGoesFirst()
    game_is_playing = True

    return board_vector, the_board, turn, player_letter, computer_letter, game_is_playing


def run_game_loop(show_print_output, is_training_game, num_games, train_matrix_size):
    print('Welcome to Tic Tac Toe!')
    index_train = 0
    tie_game_index = 0

    train_games_matrix = vgs.init_training_game_matrix(train_matrix_size)
    result_game_vector = vgs.init_end_game_status_vector(num_games)
    while tie_game_index < num_games:
        # Reset the board

        start_index = index_train

        (board_vector, the_board, turn,
         player_letter, computer_letter,
         game_is_playing) = init_game(is_training_game, train_matrix_size)

        first_player = turn

        if show_print_output:
            print('The ' + turn + ' will go first.')

        while game_is_playing:
            if turn == 'player':
                # Player's turn.
                if show_print_output:
                    drawBoard(the_board)

                move = getComputerMove(the_board, player_letter)
                board_vector = vgs.set_board_state_vector(True, move, board_vector)
                vgs.add_move_to_game_matrix(index_train, train_games_matrix, board_vector)
                index_train += 1
                print_status(show_print_output, move, board_vector)

                makeMove(the_board, player_letter, move)

                if isWinner(the_board, player_letter):
                    if show_print_output:
                        drawBoard(the_board)
                        print('Hooray! You have won the game!')

                    # vgs.set_result_of_game(num_game, result_game_vector, 1, start_index, index_train)
                    game_is_playing = False
                else:
                    if isBoardFull(the_board):
                        if show_print_output:
                            drawBoard(the_board)
                            print('The game is a tie!')
                        vgs.set_result_of_game(tie_game_index, result_game_vector, 0,
                                               start_index, index_train,
                                               first_player)
                        tie_game_index += 1
                        break
                    else:
                        turn = 'computer'

            else:
                # Computer's turn.
                move = getComputerMove(the_board, computer_letter)
                board_vector = vgs.set_board_state_vector(False, move, board_vector)
                vgs.add_move_to_game_matrix(index_train, train_games_matrix, board_vector)
                index_train += 1

                if show_print_output:
                    drawBoard(the_board)
                    print_status(show_print_output, move, board_vector)

                makeMove(the_board, computer_letter, move)

                if isWinner(the_board, computer_letter):
                    if show_print_output:
                        drawBoard(the_board)
                        print('The computer has beaten you! You lose.')
                    # vgs.set_result_of_game(num_game, result_game_vector, -1, start_index, index_train)
                    game_is_playing = False
                else:
                    if isBoardFull(the_board):
                        if show_print_output:
                            drawBoard(the_board)
                            print('The game is a tie!')
                        vgs.set_result_of_game(tie_game_index, result_game_vector, 0,
                                               start_index, index_train,
                                               first_player)
                        tie_game_index += 1
                        break
                    else:
                        turn = 'player'

        if not is_training_game:
            if not playAgain():
                break

    return index_train, train_games_matrix, result_game_vector, tie_game_index


def train_network():
    max_index, train_games_matrix, result_game_matrix, num_tie_games = run_game_loop(show_print_output=False,
                                                                                     is_training_game=True,
                                                                                     num_games=10,
                                                                                     train_matrix_size=10000000)
    model = network.network_model()

    # print(np.bitwise_xor(train_games_matrix[0:1, :][0], train_games_matrix[1:2, :][0]))

    for i in range(num_tie_games):
        game_one = get_game(i, result_game_matrix, train_games_matrix)
        # print(game_one)
        first = who_was_first(i, result_game_matrix)
        # print(first)
        train, test = get_game_train_test(game_one, first)
        # print("TRAIN")
        # print(train)
        # print("TEST")
        # print(test)
        model.fit(train, test,
                  nb_epoch=1,
                  batch_size=1,)




def get_game(num_game, results_games, train_plays):
    start = results_games[num_game:num_game + 1, 1][0]
    end = results_games[num_game:num_game + 1, 2][0]
    return train_plays[start:end, :]


def get_game_train_test(game, is_first):
    if is_first == 1:
        train = np.zeros(shape=(5, 9), dtype='int32')
        test = np.zeros(shape=(5, 9), dtype='int32')

        test[0:1, :] = game[0:1, :]

        for index, turn in enumerate([1, 3, 5, 7]):
            index += 1
            train[index: index + 1, :] = game[turn: turn + 1, :]
            test[index: index + 1, :] = np.bitwise_xor(game[turn - 1:turn, :],
                                                       game[turn: turn + 1, :])
        return train, test

    if is_first == -1:
        train = np.zeros(shape=(4, 9), dtype='int32')
        test = np.zeros(shape=(4, 9), dtype='int32')

        for index, turn in enumerate([0, 2, 4, 6]):
            train[index: index + 1, :] = game[turn: turn + 1, :]
            test[index: index + 1, :] = np.bitwise_xor(game[turn: turn + 1, :],
                                                       game[turn + 1: turn + 2, :])
        return train, test


def who_was_first(num_game, results_games):
    return results_games[num_game:num_game + 1, 3][0]


train_network()
