# Boggle

##Introduction

This is a backend code of game [Boggle](https://en.wikipedia.org/wiki/Boggle).<br/>
There are 3 methods included: [`POST`](#POST), [`PUT`](#PUT), and [`GET`](#GET):<br/>
- [`POST`](#POST): This method is used when system calls to create a new game, a `json`
object represents the game will be returned
- [`PUT`](#PUT): This method is the interaction between player and server.
When user input a word, this method is triggered and it will check whether it is
a valid answer and update the game accordingly.<br/>
- [`GET`](#GET): This method returns a `json` object represents the game to user.

## Functionality
###Global variable

- `game_data_key_id`: hash map to store game with key is id
- `game_data_key_token`: hash map to store game with key is token
- `test_board`: default board that is get from `test_board.txt`
- `dictionary`: set of all allowed words to play, get from `dictionary.txt`

###POST

- Parameters:
  + `duration` (required): the time (in seconds) that specifies the duration of
    the game
  + `random` (required): if `true`, then the game will be generated with random
    board.  Otherwise, it will be generated based on input.
  + `board` (optional): if `random` is not true, this will be used as the board
    for new game. If this is not present, new game will get the default board
    from `test_board.txt`
- `create_game` is generated first. It first gets
and check required parameters. If either those values is invalid, it will return
`400` error, else function `start_game` is generated
- `start_game` receive `duration` and `random` as input. `Board` is set as the
description above. A `game` json object is then created with attributes:
    + `id`: ID of game
    + `token`: token of game
    + `duration`: duration of game in seconds
    + `board`: board of game as described
    + `time_left`: time remaining for game, initially is set to equal `duration`
    + `points`: points that a player gained, initially set to 0
    + `timestamp`: time clock when game is created, it is used to calculate 
    `time_left`
- Game is added to 2 hash maps. Finally, a response status `201` is created. 

###PUT

- Parameters:
  + `id` (required): The ID of the game
  + `token` (required): The token for authenticating the game
  + `word` (required): The word that can be used to play the game
- `interact_with_game` function is generated under method `PUT`.
It first checks `id` and `token`. If either of these violates the data in one
of the hashmaps, a `400` status is returned, else `word` is called then passed
to `receive_word` function
- `receive_word` receives `word` and `game` as inputs:
    + `word` isn't in [`dictionary`](#dictionary): return `400` response
    + `word` is in [`dictionary`](#dictionary): `time_left` is updated:
        - `time_left` < 0: return `400` response
        - `time_left` > 0: increases point by 3 and return updated game with
        `200` response
        
###GET

- Parameters:
  + `id` (required): The ID of the game
- `interact_with_game` function is generated under method `GET`.
If `id` isn't in [`game_data_key_id`](#game_data_key_id): return `404` response,
else return game with `200` response
