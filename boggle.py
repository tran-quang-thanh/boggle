import random
import secrets
import string
import time

from flask import Flask, request, abort
import itertools

app = Flask(__name__)
game_data_key_id = dict()
game_data_key_token = dict()


with open("test_board.txt", "r") as test_board_file:
    test_board = test_board_file.read()


with open("dictionary.txt", "r") as dictionary_file:
    dictionary = dictionary_file.read()


@app.route('/games', methods=['POST'])
def create_game():
    if request.method == 'POST':
        duration = request.json.get('duration')
        rand = request.json.get('random')
        if duration is None or rand is None or type(duration) != int or rand not in [True, False]:
            return {'message': "Invalid input"}, 400
        game = start_game(duration, rand)
        return game, 201


def random_generate():
    letters = random.choices(string.ascii_uppercase, k=16)
    no_of_stars = random.randint(0, 4)
    for _ in range(no_of_stars):
        letters[random.randint(0, 15)] = '*'
    return ', '.join(letters)


def start_game(duration, rand):
    if rand is True:
        board = random_generate()
    else:
        board = request.json.get('board')
        if board is None:
            board = test_board
    game = {
        'id': next(itertools.count()),
        'token': secrets.token_hex(16),
        'duration': duration,
        'board': board,
        'time_left': duration,
        'points': 0,
        'timestamp': int(time.time())
    }
    game_data_key_id[game['id']] = game
    game_data_key_token[game['token']] = game
    return game


@app.route('/games/<game_id>', methods=['PUT', 'GET'])
def interact_with_game(game_id):
    game_id = int(game_id)
    if request.method == 'PUT':
        token = request.json.get('token')
        if token not in game_data_key_token:
            abort(400)
        game = game_data_key_token[token]
        if game['id'] != game_id:
            abort(400)
        word = request.json.get('word')
        updated_game = receive_word(game, word)
        if 'message' in updated_game:
            return updated_game, 400
        else:
            game_data_key_token[token] = updated_game
            game_data_key_id[game_id] = updated_game
            return updated_game, 200

    if request.method == 'GET':
        if game_id not in game_data_key_id:
            return {'message': "This game id doesn't exist"}, 404
        else:
            return game_data_key_id[game_id], 200


def receive_word(game, word):
    if word in dictionary:
        game['time_left'] -= (int(time.time()) - game['timestamp'])
        if game['time_left'] >= 0:
            game['points'] += 3
        else:
            return {'message': "You have run out of time"}
    else:
        return {'message': "This word doesn't exist"}
    return game
