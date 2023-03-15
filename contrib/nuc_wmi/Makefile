clean:
	rm -rf .coverage .eggs/ build/ deb_dist/ dist/ python/cover python/nuc_wmi.egg-info nuc_wmi-*.tar.gz
	find . -type f -name "*~" -exec rm {} +
	find . -type f -name "*.pyc" -exec rm {} +
	find . -type d -name "__pycache__" -exec rmdir {} +

deb_py3:
	DEB_BUILD_OPTIONS=nocheck python3 setup.py --command-packages=stdeb.command bdist_deb

covtests:
	pylint python/nuc_wmi python/test/
	coverage run setup.py test
	coverage report -m
	coverage html

test:
	pylint python/nuc_wmi python/test/
	python setup.py test
