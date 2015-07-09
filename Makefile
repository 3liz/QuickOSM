# Makefile for QuickOSM

test: clean_pyc pep8 test_suite

test_suite:
	@echo
	@echo "---------------------"
	@echo "Regression Test Suite"
	@echo "---------------------"
	@-export PYTHONPATH=`pwd`:$(PYTHONPATH);export QGIS_DEBUG=0;export QGIS_LOG_FILE=/dev/null;export QGIS_DEBUG_FILE=/dev/null;nosetests -v --with-id --with-coverage --cover-package=core 3>&1 1>&2 2>&3 3>&- || true

i18n_prepare:
	@echo Updating strings
	@pylupdate4 -noobsolete QuickOSM.pro

main_window:
	@echo pyuic4 main_window.ui > ui/main_window.py
	@pyuic4 ui/main_window.ui > ui/main_window_temp.py
	@sed -re 's/import resources_rc/from QuickOSM import resources_rc/g' ui/main_window_temp.py > ui/main_window.py
	@rm ui/main_window_temp.py
	
quick_query:
	@echo pyuic4 ui/quick_query.ui > ui/quick_query.py
	@pyuic4 ui/quick_query.ui > ui/quick_query_temp.py
	@sed -re 's/import resources_rc/from QuickOSM import resources_rc/g' ui/quick_query_temp.py > ui/quick_query.py
	@rm ui/quick_query_temp.py
	
my_queries:
	@echo pyuic4 ui/my_queries.ui > ui/my_queries.py
	@pyuic4 ui/my_queries.ui > ui/my_queries_temp.py
	@sed -re 's/import resources_rc/from QuickOSM import resources_rc/g' ui/my_queries_temp.py > ui/my_queries.py
	@rm ui/my_queries_temp.py
	
osm_file:
	@echo pyuic4 ui/osm_file.ui > ui/osm_file.py
	@pyuic4 ui/osm_file.ui > ui/osm_file_temp.py
	@sed -re 's/import resources_rc/from QuickOSM import resources_rc/g' ui/osm_file_temp.py > ui/osm_file.py
	@rm ui/osm_file_temp.py
	
query:
	@echo pyuic ui/query.ui > ui/query_temp.py
	@pyuic4 ui/query.ui > ui/query_temp.py
	@sed -re 's/import resources_rc/from QuickOSM import resources_rc/g' ui/query_temp.py > ui/query.py
	@rm ui/query_temp.py
	
save_query:
	@echo pyuic4 ui/save_query.ui > ui/save_query.py
	@pyuic4 ui/save_query.ui > ui/save_query_temp.py
	@sed -re 's/import resources_rc/from QuickOSM import resources_rc/g' ui/save_query_temp.py > ui/save_query.py
	@rm ui/save_query_temp.py

clean_pyc:
	@echo "Cleaning python files"
	@find . -name "*.pyc" -type f -delete

# Run pep8 style checking
#http://pypi.python.org/pypi/pep8
pep8:
	@echo
	@echo "-----------"
	@echo "PEP8 issues"
	@echo "-----------"
	@pep8 --version
	@pep8 --repeat --ignore=E203,E121,E122,E123,E124,E125,E126,E127,E128,E402 --exclude test/qgis_interface.py,test/utilities.py,resources_rc.py,./ui/main_window.py,./ui/my_queries.py,./ui/osm_file.py,./ui/save_query.py,./ui/query.py,./ui/quick_query.py . || true

pylint:
	@echo
	@echo "-----------------"
	@echo "Pylint violations"
	@echo "-----------------"
	@pylint --version
	@pylint --reports=n --rcfile=pylintrc controller ui __init__.py quick_osm.py || true