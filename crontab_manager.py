from crontab import CronTab
import sys

args = list(sys.argv)[1:]

if 'start' in args:
    cron = CronTab(user=True)
    

    for existing_job in cron:
        if existing_job.comment == 'timetable_bot':
            cron.remove(existing_job)

    job = cron.new(
        command=f"python3 /home/pi/shared/timetable_bot/sending_timetable.py",
        comment="timetable_bot"
        )
    job.setall(45, 0, None, None, None)

    cron.write()

elif 'stop' in args:
    cron = CronTab(user=True)

    for existing_job in cron:
        if existing_job.comment == 'timetable_bot':
            cron.remove(existing_job)
            
    cron.write()
