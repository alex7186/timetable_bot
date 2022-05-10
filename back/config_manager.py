import json


def get_config(SCRIPT_PATH):
    # parsing <SCRIPT_PATH>/misc/config.json file
    with open(f"{SCRIPT_PATH}/misc/config.json", "r") as f:
        return json.load(f)


def set_config(SCRIPT_PATH, current_config: dict):
    # writing prepared dict to <SCRIPT_PATH>/misc/config.json file
    with open(f"{SCRIPT_PATH}/misc/config.json", "w") as f:
        f.write(json.dump(current_config))
