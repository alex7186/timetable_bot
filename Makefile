today =`date '+%Y-%m-%d  %H:%M:%S'`
commit_name = "autocommit $(today)"

push:
	@cd ~/scripts/timetable_bot
	@python -m black .
	@git add .
	@git commit -m $(commit_name)
	@git push origin main
	@echo "\n✅ succussfully pulled as $(commit_name)"

setup:
	@cd ~/scripts/timetable_bot
	@pip3 install -r ./misc/requirements.txt
	@python3 back/crontab_manager.py start

start:
	@cd ~/scripts/timetable_bot
	@python3 app.py

stop:
	@cd ~/scripts/timetable_bot	
	@python3 back/crontab_manager.py stop