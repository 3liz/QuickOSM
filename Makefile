# Makefile for QuickOSM

test: clean_pyc pep8 test_suite

test_suite:
	@echo
	@echo "---------------------"
	@echo "Regression Test Suite"
	@echo "---------------------"
	@-export PYTHONPATH=`pwd`:$(PYTHONPATH);export QGIS_DEBUG=0;export QGIS_LOG_FILE=/dev/null;export QGIS_DEBUG_FILE=/dev/null;nosetests -v --with-id --with-coverage --cover-package=core 3>&1 1>&2 2>&3 3>&- || true

i18n_1_prepare:
	@echo Updating strings locally 1/4
	@./update_strings.sh fr de en fi it nl ru zh-TW

i18n_2_push:
	@echo Push strings to Transifex 2/4
	@tx push -s

i18n_3_pull:
	@echo Pull strings from Transifex 3/4
	@tx pull -a

i18n_4_compile:
	@echo Compile TS files to QM 4/4
	@lrelease i18n/QuickOSM_fr.ts -qm i18n/QuickOSM_fr.qm
	@lrelease i18n/QuickOSM_de.ts -qm i18n/QuickOSM_de.qm
	@lrelease i18n/QuickOSM_fi.ts -qm i18n/QuickOSM_fi.qm
	@lrelease i18n/QuickOSM_it.ts -qm i18n/QuickOSM_it.qm
	@lrelease i18n/QuickOSM_nl.ts -qm i18n/QuickOSM_nl.qm
	@lrelease i18n/QuickOSM_ru.ts -qm i18n/QuickOSM_ru.qm
	@lrelease i18n/QuickOSM_zh-TW.ts -qm i18n/QuickOSM_zh-TW.qm

main_window:
	@echo pyuic5 main_window.ui > ui/main_window.py
	@pyuic5 ui/main_window.ui > ui/main_window.py

quick_query:
	@echo pyuic5 ui/quick_query.ui > ui/quick_query.py
	@pyuic5 ui/quick_query.ui > ui/quick_query.py

osm_file:
	@echo pyuic5 ui/osm_file.ui > ui/osm_file.py
	@pyuic5 ui/osm_file.ui > ui/osm_file.py

query:
	@echo pyuic5 ui/query.ui > ui/query.py
	@pyuic5 ui/query.ui > ui/query.py

save_query:
	@echo pyuic5 ui/save_query.ui > ui/save_query.py
	@pyuic5 ui/save_query.ui > ui/save_query.py

generate_ui: main_window quick_query osm_file query save_query

clean_pyc:
	@echo "Cleaning python files"
	@find . -name "*.pyc" -type f -delete

clean_ui:
	@echo "Cleaning UI files"
	@find . -name "*.ui" -type f -delete

clean_test:
	@echo "Cleaning tests files"
	@find . -name test -exec rm -rf {} \;

# Run pep8 style checking
#http://pypi.python.org/pypi/pep8
pep8:
	@echo
	@echo "-----------"
	@echo "PEP8 issues"
	@echo "-----------"
	@pep8 --version
	@pep8 --repeat --ignore=E203,E121,E122,E123,E124,E125,E126,E127,E128,E402 --exclude test/qgis_interface.py,test/utilities.py,resources_rc.py,./ui/main_window.py,./ui/osm_file.py,./ui/save_query.py,./ui/query.py,./ui/quick_query.py . || true

pylint:
	@echo
	@echo "-----------------"
	@echo "Pylint violations"
	@echo "-----------------"
	@pylint --version
	@pylint --reports=n --rcfile=pylintrc controller ui __init__.py quick_osm.py || true