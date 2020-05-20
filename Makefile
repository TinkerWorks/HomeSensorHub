NT=~/.local/bin/nosetests

MAINPACKAGE=homesensorhub
TESTFOLDER=tests

NOSEOPTIONS= --with-coverage --cover-html --with-xunit --cover-package=$(MAINPACKAGE)
NOSEOPTIONS+= --cover-inclusive
prepare:
	pip3 install --user -r requirements.txt
prepare-test: prepare
	pip3 install --user -r tests/requirements.txt

nosetest: prepare-test
	PYTHONPATH=$(MAINPACKAGE) $(NT) $(NOSEOPTIONS) $(TESTFOLDER)
