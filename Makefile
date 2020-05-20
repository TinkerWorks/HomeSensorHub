NT=~/.local/bin/nosetests

prepare:
	pip3 install --user -r requirements.txt
prepare-test: prepare
	pip3 install --user -r tests/requirements.txt

nosetest: prepare-test
	$(NT) --with-coverage --cover-html --with-xunit --cover-package=homesensorhub tests
