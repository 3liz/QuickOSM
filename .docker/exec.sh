#!/usr/bin/env bash
export $(grep -v '^#' .env | xargs)

docker exec -it qgis sh \
  -c "cd /tests_directory/${PLUGIN_NAME} && qgis_testrunner.sh qgis_plugin_tools.infrastructure.test_runner.test_package"
