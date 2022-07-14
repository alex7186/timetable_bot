_today =`date '+%Y-%m-%d  %H:%M:%S'`
_commit_name = "autocommit $(_today)"
app_name = timetable_bot
_path = $(CURDIR)


push:
	@$(MAKE) --no-print-directory _black
	@$(MAKE) --no-print-directory _git_commit
	@echo "\n⚙️  pushing as $(_commit_name)\n"
	@git push origin master
	@echo "\n✅  done!"

push-force:
	@$(MAKE) --no-print-directory _black
	@$(MAKE) --no-print-directory _git_commit
	@echo "\n⚙️  🚩FORCE🚩  pushing as $(_commit_name)\n"
	@git push --force origin master
	@echo "\n✅  done!"

_black:
	@cd $(_path)
	@echo "\n🧹 cleaning the code...\n"
	@python -m black .

_git_commit:
	@cd $(_path)
	@echo "\n⚙️  pushing to git...\n"
	@git add .
	-@git commit -m $(_commit_name)


setup:
	@cd $(_path)
	@pip3 install -r ./misc/requirements.txt
	@python3 back/crontab_manager.py start

start:
	@cd $(_path)
	@python3 app.py

stop:
	@cd $(_path)
	@python3 back/crontab_manager.py stop