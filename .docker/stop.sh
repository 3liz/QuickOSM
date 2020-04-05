#!/usr/bin/env bash

echo 'Stopping/killing containers'
docker-compose kill
docker-compose rm -f
