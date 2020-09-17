

##this app created by Yasser Janah (contact@yasser-janah.com).

to run the app, please follow the steps below:
	-> run  : redis-server
	-> run  : cd mainapp && celery -A mainapp worker -l info
	-> run  : virtualenv -p $(which python3) env && source env/bin/activate && cd mainapp && pip3 install -r mainapp/requirements.txt && python manage.py runserver

thanks @CyberDefenders
