import json
from crontab import CronTab
import sys
import os

from config_manager import get_config

args = list(sys.argv)[1:]
SCRIPT_PATH = "/".join(os.path.realpath(__file__).split("/")[:-2])
CONFIG = get_config(SCRIPT_PATH)
CRONTAB_SETUP = CONFIG["CRONTAB_SETUP"]


with open(f"{SCRIPT_PATH}/misc/config.json", "r") as f:
    config_data = json.load(f)
APP_NAME = config_data["APP_NAME"]

if "start" in args:
    cron = CronTab(user=True)

    for existing_job in cron:
        if existing_job.comment == APP_NAME:
            cron.remove(existing_job)

    job = cron.new(command=f"python3 {SCRIPT_PATH}/app.py", comment=APP_NAME)
    job.setall(CRONTAB_SETUP)

    cron.write()

elif "stop" in args:
    cron = CronTab(user=True)

    for existing_job in cron:
        if existing_job.comment == APP_NAME:
            cron.remove(existing_job)

    cron.write()
