#!/usr/bin/env bash
export $(grep -v '^#' .env | xargs)

FILE="docker-compose-qgis.yml"

docker compose -f ${FILE} up -d --force-recreate --remove-orphans
echo "Wait 10 seconds"
sleep 10
echo "Installation of the plugin ${PLUGIN_NAME}"
docker exec -t qgis sh -c "qgis_setup.sh ${PLUGIN_NAME}"
echo "Containers are running"
