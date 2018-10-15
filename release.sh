#!/bin/bash
echo "Make a zip"

cp -R QuickOSM/ QuickOSM_back/
rm QuickOSM.zip
cd QuickOSM/
git clean -f
git reset --hard HEAD
make clean_pyc
find . -name "*.ui" -type f -delete
find . -name "*.qrc" -type f -delete
find . -name "*.ts" -type f -delete
find . -depth -name 'test' -type d -exec rm -rf '{}' \;
rm -rf .git
rm -rf .github
rm -rf __pycache__  
rm -rf .idea
rm -f .gitignore
rm -rf venv/
rm -f Makefile
rm -f QuickOSM.pro
rm -f README.md
rm -f release.sh
rm -f .travis.yml
rm -f .coverage
rm pylintrc
rm run-env-linux.sh

cd ..
zip -r QuickOSM QuickOSM/
rm -rf QuickOSM/
mv QuickOSM_back/ QuickOSM/