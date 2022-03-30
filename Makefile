pull:
	cd ~/shared/scripts/timetable_bot

	today=`date '+%Y_%m_%d__%H_%M_%S'`;

	git add .;
	git commit -m $today;
	git push origin master
	# git pull https://github.com/alex7186/timetable_bot master	


setup:
	pip3 install -r requirements.txt
	python3 crontab_manager.py start

start:
	python3 app.py /home/pi/shared/scripts/timetable_bot

stop:
	python3 crontab_manager.py stop