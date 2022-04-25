import json

# operating with config.json file
def get_config(SCRIPT_PATH):
    with open(f"{SCRIPT_PATH}/misc/config.json", "r") as f:
        return json.load(f)


def set_config(SCRIPT_PATH, current_config: dict):
    with open(f"{SCRIPT_PATH}/misc/config.json", "w") as f:
        f.write(json.dump(current_config))
