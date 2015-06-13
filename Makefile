# Makefile for QuickOSM

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