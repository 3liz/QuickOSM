#!/usr/bin/env bash

LOCALES=$*

files_to_translate=`find . -regex ".*\(ui\|py\)$" -type f`
files_to_translate='quick_osm.py '${files_to_translate}

for LOCALE in ${LOCALES}
do
    echo "resources/i18n/QuickOSM_"${LOCALE}".ts"
    pylupdate5 -noobsolete ${files_to_translate} -ts resources/i18n/QuickOSM_${LOCALE}.ts
done
