BUILDDIR=./~build
DJANGO_14:='django>=1.4,<1.5'
DJANGO_15:='django>=1.5,<1.6'
DJANGO_16:='django>=1.6,<1.7'
DJANGO_17=https://www.djangoproject.com/download/1.7c1/tarball/
DJANGO_DEV=git+git://github.com/django/django.git
DBNAME=geo

mkbuilddir:
	mkdir -p ${BUILDDIR}/cache


install-deps:
	@pip install -q \
	        -r geo/requirements/install.pip \
	        -r geo/requirements/testing.pip \
	        python-coveralls==2.4.2


test: mkbuilddir
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

ci: init-db install-deps
	@sh -c "if [ '${DJANGO}' = '1.4.x' ]; then pip install ${DJANGO_14}; fi"
	@sh -c "if [ '${DJANGO}' = '1.5.x' ]; then pip install ${DJANGO_15}; fi"
	@sh -c "if [ '${DJANGO}' = '1.6.x' ]; then pip install ${DJANGO_16}; fi"
	@sh -c "if [ '${DJANGO}' = '1.7.x' ]; then pip install ${DJANGO_17}; fi"
	@sh -c "if [ '${DJANGO}' = 'dev' ]; then pip install ${DJANGO_DEV}; fi"
	@pip install coverage
	@python -c "from __future__ import print_function;import django;print('Django version:', django.get_version())"
	@echo "Database:" ${DBENGINE}


	$(MAKE) coverage
