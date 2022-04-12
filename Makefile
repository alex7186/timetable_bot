today =`date '+%Y-%m-%d  %H:%M:%S'`

push:
	cd ~/scripts/timetable_bot
	python -m black .
	git add .
	git commit -m "autocommit $(today)"
	git push origin master

setup:
	pip3 install -r ./misc/requirements.txt
	cd ~/scripts/timetable_bot
	python3 /.crontab_manager.py start

start:
	cd ~/scripts/timetable_bot
	python3 ./app.py /home/pi/scripts/timetable_bot

stop:
	cd ~/scripts/timetable_bot	
	python3 ./crontab_manager.py stop