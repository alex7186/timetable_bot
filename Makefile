setup:
	# cd ~/shared/scripts/timetable_bot; git pull https://github.com/alex7186/timetable_bot master
	# pip3 install -r requirements.txt
	python3 crontab_manager.py start

start:
	python3 app.py /home/pi/shared/scripts/timetable_bot

stop:
	python3 crontab_manager.py stop