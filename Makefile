SETTINGS=geo.tests.settings
BUILDDIR=~build
DJANGO_14=django==1.4.9
DJANGO_15=django==1.5.5
DJANGO_16=https://www.djangoproject.com/download/1.6c1/tarball/
DJANGO_DEV=git+git://github.com/django/django.git

mkbuilddir:
	mkdir -p ${BUILDDIR}

init-db:
	@sh -c "if [ '${DBENGINE}' = 'mysql' ]; then mysql -e 'DROP DATABASE IF EXISTS concurrency;'; fi"
	@sh -c "if [ '${DBENGINE}' = 'mysql' ]; then pip install MySQL-python; fi"
	@sh -c "if [ '${DBENGINE}' = 'mysql' ]; then mysql -e 'create database IF NOT EXISTS concurrency;'; fi"

	@sh -c "if [ '${DBENGINE}' = 'pg' ]; then psql -c 'DROP DATABASE IF EXISTS concurrency;' -U postgres; fi"
	@sh -c "if [ '${DBENGINE}' = 'pg' ]; then psql -c 'DROP DATABASE IF EXISTS test_concurrency;' -U postgres; fi"
	@sh -c "if [ '${DBENGINE}' = 'pg' ]; then psql -c 'CREATE DATABASE concurrency;' -U postgres; fi"
	@sh -c "if [ '${DBENGINE}' = 'pg' ]; then pip install -q psycopg2; fi"

test: init-db
	@sh -c "if [ '${DJANGO}' = '1.4.x' ]; then pip install ${DJANGO_14}; fi"
	@sh -c "if [ '${DJANGO}' = '1.5.x' ]; then pip install ${DJANGO_15}; fi"
	@sh -c "if [ '${DJANGO}' = '1.6.x' ]; then pip install ${DJANGO_16}; fi"
	@sh -c "if [ '${DJANGO}' = 'dev' ]; then pip install ${DJANGO_DEV}; fi"
	@python -c "from __future__ import print_function;import django;print('Django version:', django.get_version())"
	@echo "Database:" ${DBENGINE}
	pip install -r geo/requirements/testing.pip python-coveralls coverage

	PYTHONPATH=${PWD} coverage run `which django-admin.py` test geo --settings=${SETTINGS}

clean:
	rm -f .coverage .pytest MEDIA_ROOT MANIFEST *.egg *.pid
	rm -fr ${BUILDDIR} dist *.egg-info .cache build STATIC
	rm -fr docs/apidocs celerybeat-schedule supervisord.log
	find . -name __pycache__ -prune | xargs rm -rf
	find . -name "*.py?" -prune | xargs rm -rf
	find . -name "*.orig" -prune | xargs rm -rf
	rm -f coverage.xml flake.out pep8.out pytest.xml
