from crontab import CronTab
import sys
import os

from config_manager import get_config

# takes "start" or "stop" as execution argument
args = list(sys.argv)[1:]

SCRIPT_PATH = "/".join(os.path.realpath(__file__).split("/")[:-2])
CONFIG = get_config(SCRIPT_PATH)
CRONTAB_SETUP = CONFIG["CRONTAB_SETUP"]
APP_NAME = CONFIG["APP_NAME"]

# if input arg is "start" then add to cron_table
if "start" in args:
    cron = CronTab(user=True)

    for existing_job in cron:
        if existing_job.comment == APP_NAME:
            cron.remove(existing_job)

    job = cron.new(command=f"python3 {SCRIPT_PATH}/app.py", comment=APP_NAME)
    job.setall(CRONTAB_SETUP)

    cron.write()

# if input arg is "stop" then remove from cron_table
elif "stop" in args:
    cron = CronTab(user=True)

    for existing_job in cron:
        if existing_job.comment == APP_NAME:
            cron.remove(existing_job)

    cron.write()
