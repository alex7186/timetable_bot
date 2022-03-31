today =`date '+%Y_%m_%d__%H_%M_%S'`

pull:
	cd ~/shared/scripts/timetable_bot

	git add .
	git commit -m "autocommit $(today)"
	git push origin master

setup:
	pip3 install -r requirements.txt
	python3 crontab_manager.py start

start:
	python3 app.py /home/pi/shared/scripts/timetable_bot

stop:
	python3 crontab_manager.py stop