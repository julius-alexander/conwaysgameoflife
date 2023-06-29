import json


def save_game_state(cells_state):

    json_object = json.dumps(cells_state.tolist(), indent=4)

    with open('game_state.json', 'w') as file:
        file.write(json_object)


def load_game_state(i_file):
    if i_file:
        with open(i_file, 'r') as file:
            game_state = json.load(file)

        return game_state
