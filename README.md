

## this app created by Yasser Janah (contact@yasser-janah.com).

to run the app, please follow the steps below:

	# open 3 tabs in your termianl:
		# in first tab run  : 
			$ virtualenv -p $(which python3) env && redis-server
		# in second tab run : 
			$ source env/bin/activate && cd mainapp && pip3 install -r requirements.txt && python manage.py runserver
		# in third one run  : 
			$ source env/bin/activate && cd mainapp && celery -A mainapp worker -l info


thanks @CyberDefenders
