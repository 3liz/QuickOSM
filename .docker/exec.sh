#!/usr/bin/env bash

docker exec -it qgis sh -c "cd /tests_directory/QuickOSM && qgis_testrunner.sh qgis_plugin_tools.infrastructure.test_runner.test_package"
