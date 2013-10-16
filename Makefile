SETTINGS=geo.tests.settings
BUILDDIR=~build


mkbuilddir:
	mkdir -p ${BUILDDIR}

test:
	./django-admin.py test geo --settings=${SETTINGS}

clean:
	rm -f .coverage .pytest MEDIA_ROOT MANIFEST *.egg *.pid
	rm -fr ${BUILDDIR} dist *.egg-info .cache build STATIC
	rm -fr docs/apidocs celerybeat-schedule supervisord.log
	find . -name __pycache__ -prune | xargs rm -rf
	find . -name "*.py?" -prune | xargs rm -rf
	find . -name "*.orig" -prune | xargs rm -rf
	rm -f coverage.xml flake.out pep8.out pytest.xml
