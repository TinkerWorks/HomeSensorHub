NT=nose2

MAINPACKAGE=homesensorhub
MOCKED_TEST_FOLDER=tests/sensors
REAL_TEST_FOLDER=tests/test_integration

NOSEOPTIONS= --with-coverage --junit-xml

PREPARE_TEST=
ifneq ($(JENKINS_HOME),)
 PREPARE_TEST+=prepare-test
endif

prepare:
	pip3 install --user -r requirements.txt
prepare-test: prepare
	pip3 install --user -r tests/requirements.txt

mock-nosetest: $(PREPARE_TEST)
	PYTHONPATH=$(MAINPACKAGE) $(NT) $(NOSEOPTIONS) -s $(MOCKED_TEST_FOLDER)

real-nosetest: $(PREPARE_TEST)
	PYTHONPATH=$(MAINPACKAGE) $(NT) $(NOSEOPTIONS) -s $(REAL_TEST_FOLDER)
