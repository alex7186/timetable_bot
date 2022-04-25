today =`date '+%Y-%m-%d  %H:%M:%S'`
commit_name = "autocommit $(today)"
app_name = timetable_bot
path = ~/scripts/$(app_name)

push:
	@cd $(path)
	@python -m black .
	@git add .
	@git commit -m $(commit_name)
	@git push origin master
	@echo "\n✅ succussfully pulled as $(commit_name)"

setup:
	@cd $(path)
	@pip3 install -r ./misc/requirements.txt
	@python3 back/crontab_manager.py start

start:
	@cd $(path)
	@python3 app.py

stop:
	@cd $(path)
	@python3 back/crontab_manager.py stop