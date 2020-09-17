

# this app created by Yasser Janah (contact@yasser-janah.com).

to run the app, please follow the steps below:

	-> run on new tab : redis-server
	-> run on new tab : virtualenv -p $(which python3) env
	-> run on new tab : source env/bin/activate && cd mainapp && pip3 install -r requirements.txt && python manage.py runserver
	-> run on new tab : source env/bin/activate && cd mainapp && celery -A mainapp worker -l info


thanks @CyberDefenders
