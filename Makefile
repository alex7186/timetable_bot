today =`date '+%Y-%m-%d  %H:%M:%S'`
commit_name = "autocommit $(today)"
app_name = timetable_bot
path = $(CURDIR)


push:
	@cd $(path)
	@echo "\n🧹 cleaning the code...\n"
	@python -m black .
	@echo "\n⚙️  pushing to git...\n"
	@git add .
	-@git commit -m $(commit_name)
	@echo "\n⚙️ pushing as $(commit_name)"
	@git push origin main
	@echo "\n✅ done!"

push-force:
	@cd $(path)
	@echo "\n🧹 cleaning the code...\n"
	@python -m black .
	@echo "\n⚙️  pushing to git...\n"
	@git add .
	-@git commit -m $(commit_name)
	@echo "\n🚩 FORCE 🚩 pushing as $(commit_name)"
	@git push --force origin master
	@echo "\n✅ done!"

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