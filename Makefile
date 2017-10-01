all: clean lint test

flake8:
	flake8 --max-complexity=8 app/*.py app/jobs/*.py support/*.py

jshint:
	jshint app/static/*.js app/static/widgets/*/*.js

lint: flake8 jshint

test:
	python app/tests.py

clean:
	rm -f *.pyc app/*.pyc app/jobs/*.pyc support/*.pyc
	rm -fr app/static/.webassets-cache/
	rm -fr app/static/gen/

widget:
	python support/create_widget.py $(NAME)

dashboard:
	python support/create_dashboard.py $(NAME)

debug:
	python app/run.py --debug

run:
	python app/run.py

run-job:
	python app/run.py --job $(NAME)

google-api-auth:
	python support/google_api_auth.py
