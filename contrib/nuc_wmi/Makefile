clean:
	rm -rf .coverage build/ deb_dist/ dist/ python/cover python/nuc_wmi.egg-info nuc_wmi-*.tar.gz
	find . -type f -name "*~" -exec rm {} +
	find . -type f -name "*.pyc" -exec rm {} +
	find . -type d -name "__pycache__" -exec rmdir {} +
deb:
	DEB_BUILD_OPTIONS=nocheck python setup.py --command-packages=stdeb.command bdist_deb
nosetests:
	python setup.py nosetests --cover-branches --cover-html --cover-html-dir ./cover --cover-package nuc_wmi -d -s -v --with-coverage --py3where python/
test:
	pylint python/nuc_wmi python/test/
	python setup.py test
