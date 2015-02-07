build:
	python setup.py build

check: tests pep8

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

pep8:
	pep8 --config=.pep8.conf

polltests:
	while true; do inotifywait -e modify,moved_to,close_write,move_self . &>/dev/null ; check; done
