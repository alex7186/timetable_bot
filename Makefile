start:
	pip3 install -r requirements.txt
	python3 crontab_manager.py start

stop:
	python3 crontab_manager.py stop