#!/usr/bin/env bash
export $(grep -v '^#' .env | xargs)

#xhost +

docker run -d \
  --name qgis-testing-environment \
  -v  $(pwd)/../:/plugin \
  -e DISPLAY=:99 \
  qgis/qgis:release-3_16

sleep 10

echo "Setting up"
docker exec -t qgis-testing-environment sh -c "cd /plugin && cp CHANGELOG.md docs/"
docker exec -t qgis-testing-environment sh -c "cd /plugin && cp CONTRIBUTING.md docs/"
docker exec -t qgis-testing-environment sh -c "python3 -m pip install -r /plugin/requirements/doc.txt"
docker exec -t qgis-testing-environment sh -c "cd /plugin && mkdocs gh-deploy --clean --force --verbose"

docker kill qgis-testing-environment
docker rm qgis-testing-environment
