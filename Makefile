NT=nosetests

MAINPACKAGE=homesensorhub
MOCKED_TEST_FOLDER=tests/sensors
REAL_TEST_FOLDER=tests/test_integration

NOSEOPTIONS= --with-coverage --cover-html --with-xunit --cover-package=$(MAINPACKAGE)
NOSEOPTIONS+= --cover-inclusive -s

PREPARE_TEST=
ifneq ($(JENKINS_VERSION),)
 PREPARE_TEST+=prepare-test
endif

prepare:
	pip3 install --user -r requirements.txt
prepare-test: prepare
	pip3 install --user -r tests/requirements.txt

mock-nosetest: $(PREPARE_TEST)
	PYTHONPATH=$(MAINPACKAGE) $(NT) $(NOSEOPTIONS) $(MOCKED_TEST_FOLDER)

real-nosetest: $(PREPARE_TEST)
	PYTHONPATH=$(MAINPACKAGE) $(NT) $(NOSEOPTIONS) $(REAL_TEST_FOLDER)
