build:
	python setup.py build

tests: nosetests2 nosetests3

nosetests2:
	nosetests2

nosetests3:
	nosetests3

install:
	python setup.py install

install-dev:
	python setup.py develop

install-wheel:
	python setup.py bdist_wheel
