# Tic Tac Toe

# The TicTacToe base game is provided here.
# http://inventwithpython.com/tictactoe.py


import random
import vector_game_state as vgs
import numpy as np
from keras.models import Sequential
import network_training as network
from keras.models import model_from_json


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
            return ['X', 'O', False]
        else:
            return ['O', 'X', False]
    letter = ''
    while not (letter == 'X' or letter == 'O' or letter == 'A'):
        print('Do you want to be X or O? A for autoplay')
        letter = input().upper()

    # the first element in the tuple is the player's letter, the second is the computer's letter.
    if letter == 'X':
        return ['X', 'O', False]
    elif letter == 'O':
        return ['O', 'X', False]
    else:
        return ['X', 'O', True]


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
    # for i in range(1, 10):
    #     copy = getBoardCopy(board)
    #     if isSpaceFree(copy, i):
    #         makeMove(copy, computerLetter, i)
    #         if isWinner(copy, computerLetter):
    #             return i
    #
    # # Check if the player could win on his next move, and block them.
    # for i in range(1, 10):
    #     copy = getBoardCopy(board)
    #     if isSpaceFree(copy, i):
    #         makeMove(copy, playerLetter, i)
    #         if isWinner(copy, playerLetter):
    #             return i

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
    player_letter, computer_letter, ai_vs_ai = inputPlayerLetter(is_training_game)
    turn = whoGoesFirst()
    game_is_playing = True

    return board_vector, the_board, turn, player_letter, computer_letter, game_is_playing, ai_vs_ai


def run_game_loop_train(show_print_output, is_training_game, num_games, train_matrix_size):
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
         game_is_playing, ai_vs_ai) = init_game(is_training_game, train_matrix_size)

        first_player = turn

        vgs.add_move_to_game_matrix(index_train, train_games_matrix, board_vector)
        index_train += 1

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

                    vgs.set_result_of_game(tie_game_index, result_game_vector, 1,
                                           start_index, index_train,
                                           first_player)
                    tie_game_index += 1
                    game_is_playing = False
                else:
                    if isBoardFull(the_board):
                        if show_print_output:
                            drawBoard(the_board)
                            print('The game is a tie!')
                        # vgs.set_result_of_game(tie_game_index, result_game_vector, 0,
                        #                        start_index, index_train,
                        #                        first_player)
                        # tie_game_index += 1
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
                    game_is_playing = False
                else:
                    if isBoardFull(the_board):
                        if show_print_output:
                            drawBoard(the_board)
                            print('The game is a tie!')
                        # vgs.set_result_of_game(tie_game_index, result_game_vector, 0,
                        #                        start_index, index_train,
                        #                        first_player)
                        # tie_game_index += 1
                        break
                    else:
                        turn = 'player'

        if not is_training_game:
            if not playAgain():
                break

    return index_train, train_games_matrix, result_game_vector, tie_game_index


def network_make_move(network, random_chance, board_vector, the_board, letter_x_o):
    if random.randint(0, random_chance) == 0:
        move = getComputerMove(the_board, letter_x_o)
    else:
        network_action = network.predict(board_vector)
        move = network_action.argmax() + 1
        while True:
            if isSpaceFree(the_board, move):
                break
            else:
                network_action[0, move - 1] = 0
                move = network_action.argmax() + 1

    return move


def run_game_loop_net_vs_net(show_print_output, is_training_game, num_games, train_matrix_size, network_model,
                             random_move_chance):
    index_train = 0
    number_of_games = 0

    player_1_loses = 0
    index_player_1_game = 0

    player_2_loses = 0

    train_games_matrix_player_1 = vgs.init_training_game_matrix(train_matrix_size)
    result_game_vector_player_1 = vgs.init_end_game_status_vector(num_games)

    while number_of_games < num_games:
        # Reset the board


        start_index = index_train

        (board_vector, the_board, turn,
         player_letter, computer_letter,
         game_is_playing, ai_vs_ai) = init_game(is_training_game, train_matrix_size)

        turn = 'player'
        first_player = turn

        vgs.add_move_to_game_matrix(index_train, train_games_matrix_player_1, board_vector)

        index_train += 1

        if show_print_output:
            print('The ' + turn + ' will go first.')

        while game_is_playing:
            if turn == 'player':
                # Player's turn.
                if show_print_output:
                    drawBoard(the_board)

                move = network_make_move(network_model, random_move_chance, board_vector, the_board, player_letter)

                board_vector = vgs.set_board_state_vector(True, move, board_vector)

                vgs.add_move_to_game_matrix(index_train, train_games_matrix_player_1, board_vector)
                index_train += 1

                print_status(show_print_output, move, board_vector)

                makeMove(the_board, player_letter, move)

                if isWinner(the_board, player_letter):
                    if show_print_output:
                        drawBoard(the_board)
                        print('Hooray! You have won the game!')

                    player_2_loses += 1
                    vgs.set_result_of_game(index_player_1_game, result_game_vector_player_1, 1,
                                           start_index, index_train,
                                           first_player)

                    index_player_1_game += 1
                    number_of_games += 1
                    game_is_playing = False
                else:
                    if isBoardFull(the_board):
                        if show_print_output:
                            drawBoard(the_board)
                            print('The game is a tie!')
                        vgs.set_result_of_game(index_player_1_game, result_game_vector_player_1, 0,
                                               start_index, index_train,
                                               first_player)
                        number_of_games += 1
                        index_player_1_game += 1
                        break
                    else:
                        turn = 'computer'

            else:
                # Computer's turn.
                move = network_make_move(network_model, random_move_chance, -board_vector, the_board, computer_letter)
                # move = getComputerMove(the_board,computer_letter)

                board_vector = vgs.set_board_state_vector(False, move, board_vector)
                vgs.add_move_to_game_matrix(index_train, train_games_matrix_player_1, board_vector)
                index_train += 1

                if show_print_output:
                    drawBoard(the_board)
                    print_status(show_print_output, move, board_vector)

                makeMove(the_board, computer_letter, move)

                if isWinner(the_board, computer_letter):
                    if show_print_output:
                        drawBoard(the_board)
                        print('The computer has beaten you! You lose.')
                    number_of_games += 1
                    player_1_loses += 1
                    game_is_playing = False

                else:
                    if isBoardFull(the_board):
                        if show_print_output:
                            drawBoard(the_board)
                            print('The game is a tie!')

                        number_of_games += 1
                        break
                    else:
                        turn = 'player'

        if number_of_games == num_games:
            # print(number_of_games, "Number of games")
            # print("Player 1 losses", player_1_loses, "Player 2 losses" , player_2_loses)
            if player_1_loses < player_2_loses or player_1_loses == player_2_loses or (num_games - (player_1_loses + player_2_loses)) > 10:

                print("Loses ", player_1_loses, player_2_loses, " Tied games",
                      num_games - (player_1_loses + player_2_loses))
                return index_train, train_games_matrix_player_1, result_game_vector_player_1[
                                                                 :index_player_1_game], index_player_1_game
            else:
                # print("Player 2 wins most games")
                # Re init game
                index_train = 0
                player_1_loses = 0
                index_player_1_game = 0
                player_2_loses = 0
                number_of_games = 0
                train_games_matrix_player_1 = vgs.init_training_game_matrix(train_matrix_size)
                result_game_vector_player_1 = vgs.init_end_game_status_vector(num_games)


def run_game_vs_network(network):
    print('Welcome to Tic Tac Toe!')

    while True:
        # Reset the board
        the_board = [' '] * 10
        player_letter, computer_letter, ai_vs_ai = inputPlayerLetter()
        turn = whoGoesFirst()
        turn = "computer"

        print('The ' + turn + ' will go first.')
        game_is_playing = True
        board_vector = vgs.init_board_state_vector()

        while game_is_playing:
            if turn == 'player':
                # Player's turn.
                drawBoard(the_board)
                if ai_vs_ai:
                    move = network_make_move(network, 1, -board_vector, the_board, computer_letter)
                else:
                    move = getPlayerMove(the_board)

                print("YOU MADE MOVE", move)
                board_vector = vgs.set_board_state_vector(False, move, board_vector)
                makeMove(the_board, player_letter, move)

                if isWinner(the_board, player_letter):
                    drawBoard(the_board)
                    print('Hooray! You have won the game!')
                    game_is_playing = False
                else:
                    if isBoardFull(the_board):
                        drawBoard(the_board)
                        print('The game is a tie!')
                        break
                    else:
                        turn = 'computer'

            else:
                # Computer's turn.

                move = network_make_move(network, 100, board_vector, the_board, computer_letter)

                print("COMPUTER MAKES MOVE", move)
                board_vector = vgs.set_board_state_vector(True, move, board_vector)

                makeMove(the_board, computer_letter, move)

                if isWinner(the_board, computer_letter):
                    drawBoard(the_board)
                    print('The computer has beaten you! You lose.')
                    game_is_playing = False
                else:
                    if isBoardFull(the_board):
                        drawBoard(the_board)
                        print('The game is a tie!')
                        break
                    else:
                        turn = 'player'

                        # if not playAgain():
                        #     break


def train_loop(model, random_move_chance, num_games):
    for i in range(10):
        max_index, train_games_matrix, result_game_matrix, num_tie_games = run_game_loop_net_vs_net(
            show_print_output=False,
            is_training_game=True,
            num_games=num_games,
            train_matrix_size=100000000,
            network_model=model,
            random_move_chance=random_move_chance)

        # print(result_game_matrix)

        total_train, total_test = init_train_test_matrix(result_game_matrix)

        fill_train_test_matrix(total_train, total_test, result_game_matrix, train_games_matrix, num_tie_games)
        #
        # print("RESULT MATRIX", result_game_matrix)
        # print(total_test)
        model.fit(total_train, total_test,
                  nb_epoch=1,
                  batch_size=1)


def load_model():
    # load json and create model
    loaded_model = network.create_model()
    loaded_model.load_weights("model.h5")
    return loaded_model


def save_model(model):
    # serialize model to JSON

    model.save('model.h5')


def train_network():
    max_index, train_games_matrix, result_game_matrix, num_tie_games = run_game_loop_train(show_print_output=False,
                                                                                           is_training_game=True,
                                                                                           num_games=10000,
                                                                                           train_matrix_size=100000000)
    # init model
    model = network.network_model()

    # First run


    total_train, total_test = init_train_test_matrix(result_game_matrix)
    fill_train_test_matrix(total_train, total_test, result_game_matrix, train_games_matrix, num_tie_games)
    model.fit(total_train, total_test,
              nb_epoch=1,
              batch_size=1)

    for random_chance in range(2, 15):
        print("-" * 30 + "Starting run " + str(random_chance) + "-" * 30)
        train_loop(model, random_move_chance=3, num_games=1000)

    # save_model(model)

    run_game_vs_network(model)


def get_game(num_game, results_games, train_plays):
    start = results_games[num_game:num_game + 1, 1][0]
    end = results_games[num_game:num_game + 1, 2][0]
    return train_plays[start:end, :], end - start


def get_game_train_test(game, is_first, lenth_of_game):
    size_of_array = int(lenth_of_game / 2)

    if is_first == 1:
        train = np.zeros(shape=(size_of_array, 9), dtype='int32')
        test = np.zeros(shape=(size_of_array, 9), dtype='int32')

        # for index, turn in enumerate([0,2,4,6,8]):
        counter = 0
        for index in range(lenth_of_game):
            if index % 2 == 0:
                train[counter: counter + 1, :] = game[index: index + 1, :]
                test[counter: counter + 1, :] = np.bitwise_xor(game[index:index + 1, :],
                                                               game[index + 1: index + 2, :])

                counter += 1

        return train, test

    if is_first == -1:
        train = np.zeros(shape=(size_of_array, 9), dtype='int32')
        test = np.zeros(shape=(size_of_array, 9), dtype='int32')

        counter = 0
        for index in range(lenth_of_game - 1):
            if index % 2 == 1:
                train[counter: counter + 1, :] = game[index: index + 1, :]
                test[counter: counter + 1, :] = np.bitwise_xor(game[index: index + 1, :],
                                                               game[index + 1: index + 2, :])
                counter += 1

        return train, test


def who_was_first(num_game, results_games):
    return results_games[num_game:num_game + 1, 3][0]


def init_train_test_matrix(results_game):
    train_size = 0
    for i in results_game:
        train_size += int(i[4] / 2)
    total_train = np.zeros(shape=(train_size, 9), dtype='int32')
    total_test = np.zeros(shape=(train_size, 9), dtype='int32')

    return total_train, total_test


def fill_train_test_matrix(total_train, total_test, result_game_matrix, train_games_matrix, num_games):
    index = 0
    for i in range(num_games):
        game_one, length_of_game = get_game(i, result_game_matrix, train_games_matrix)
        first = who_was_first(i, result_game_matrix)
        train, test = get_game_train_test(game_one, first, length_of_game)
        total_train[index: index + train.shape[0], :] = train
        total_test[index: index + test.shape[0], :] = test
        index = index + test.shape[0]


def play_loaded_model():
    model = load_model()
    run_game_vs_network(model)


train_network()
# play_loaded_model()
