def get_token(SCRIPT_PATH):
    with open(f"{SCRIPT_PATH}/token.txt", "r") as f:
        return f.read()
