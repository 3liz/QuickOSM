#!/usr/bin/env bash

echo 'Stopping/killing containers'
docker-compose -f docker-compose-qgis.yml kill
docker-compose -f docker-compose-qgis.yml rm -f
