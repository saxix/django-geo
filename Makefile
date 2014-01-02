BUILDDIR=./~build
DJANGO_14=django==1.4.10
DJANGO_15=django==1.5.5
DJANGO_16=django==1.6.1
DJANGO_DEV=git+git://github.com/django/django.git
DBNAME=geo

mkbuilddir:
	mkdir -p ${BUILDDIR}/cache

test:
	py.test -vvv

clean:
	rm -fr ${BUILDDIR} dist *.egg-info .coverage
	find . -name __pycache__ -o -name "*.py?" -o -name "*.orig" -prune | xargs rm -rf
	find geo/locale -name django.mo | xargs rm -f


coverage: mkbuilddir
	py.test --cov=geo --cov-report=html --cov-report=term --cov-config=tests/.coveragerc -vvv


init-db:
	@sh -c "if [ '${DBENGINE}' = 'mysql' ]; then mysql -e 'DROP DATABASE IF EXISTS ${DBNAME};'; fi"
	@sh -c "if [ '${DBENGINE}' = 'mysql' ]; then pip install  MySQL-python; fi"
	@sh -c "if [ '${DBENGINE}' = 'mysql' ]; then mysql -e 'CREATE DATABASE IF NOT EXISTS ${DBNAME};'; fi"

	@sh -c "if [ '${DBENGINE}' = 'pg' ]; then psql -c 'DROP DATABASE IF EXISTS ${DBNAME};' -U postgres; fi"
	@sh -c "if [ '${DBENGINE}' = 'pg' ]; then psql -c 'CREATE DATABASE ${DBNAME};' -U postgres; fi"
	@sh -c "if [ '${DBENGINE}' = 'pg' ]; then pip install -q psycopg2; fi"

ci:
	@sh -c "if [ '${DJANGO}' = '1.4.x' ]; then pip install ${DJANGO_14}; fi"
	@sh -c "if [ '${DJANGO}' = '1.5.x' ]; then pip install ${DJANGO_15}; fi"
	@sh -c "if [ '${DJANGO}' = '1.6.x' ]; then pip install ${DJANGO_16}; fi"
	@sh -c "if [ '${DJANGO}' = 'dev' ]; then pip install ${DJANGO_DEV}; fi"
	@pip install coverage
	@python -c "from __future__ import print_function;import django;print('Django version:', django.get_version())"
	@echo "Database:" ${DBENGINE}

	pip install -r geo/requirements/install.pip -r geo/requirements/testing.pip
	$(MAKE) coverage
