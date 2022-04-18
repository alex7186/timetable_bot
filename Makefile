today =`date '+%Y-%m-%d  %H:%M:%S'`

push:
	cd ~/scripts/timetable_bot
	python -m black .
	git add .
	git commit -m "autocommit $(today)"
	git push origin master

setup:
	cd ~/scripts/timetable_bot
	pip3 install -r ./misc/requirements.txt
	python3 ./back/crontab_manager.py start

start:
	cd ~/scripts/timetable_bot
	python3 ./app.py

stop:
	cd ~/scripts/timetable_bot	
	python3 ./back/crontab_manager.py stop