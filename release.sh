#!/bin/bash
echo "Make a zip"

cp -R QuickOSM/ QuickOSM_back/
rm QuickOSM.zip
cd QuickOSM/
make clean_pyc
find . -name "*.ui" -type f -delete
find . -name "*.qrc" -type f -delete
find . -name "*.ts" -type f -delete
rm -rf .git
rm -rf .idea
rm .gitignore
rm Makefile
rm QuickOSM.pro
rm README.md
rm release.sh

cd ..
zip -r QuickOSM QuickOSM/
rm -rf QuickOSM/
mv QuickOSM_back/ QuickOSM/