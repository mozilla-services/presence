build:
	virtualenv --no-site-packages .
	bin/python setup.py develop
	bin/pip install circus

