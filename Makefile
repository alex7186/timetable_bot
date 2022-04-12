today =`date '+%Y-%m-%d  %H:%M:%S'`

pull:
	cd ~/scripts/timetable_bot

	git add .
	git commit -m "autocommit $(today)"
	git push origin master

setup:
	pip3 install -r requirements.txt
	python3 /home/pi/scripts/timetable_bot/crontab_manager.py start

start:
	python3 /home/pi/scripts/timetable_bot/app.py /home/pi/scripts/timetable_bot

stop:
	python3 /home/pi/scripts/timetable_bot/crontab_manager.py stop