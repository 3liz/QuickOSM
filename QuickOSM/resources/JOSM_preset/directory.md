# Update presets

Website : https://josm.openstreetmap.de/wiki/Presets
Presets : https://github.com/simonpoole/beautified-JOSM-preset/releases

```bash
cd QuickOSM/resources/JOSM_preset
wget https://josm.openstreetmap.de/export/HEAD/josm/trunk/resources/data/defaultpresets.xml -O defaultpresets.xml
wget https://github.com/simonpoole/beautified-JOSM-preset/releases/latest/download/josm_preset.xml -O josm_preset.xml
wget https://github.com/simonpoole/beautified-JOSM-preset/releases/latest/download/josm_preset_orig_icons.xml -O josm_preset_orig_icons.xml

# i18n with *.po files
wget https://github.com/simonpoole/beautified-JOSM-preset/releases/download/4.8.0/vespucci_zip.zip -O /tmp/vespucci_zip.zip
rm -rf /tmp/vespucci
mkdir /tmp/vespucci
unzip /tmp/vespucci_zip.zip -d /tmp/vespucci
mv /tmp/vespucci/*.po ../i18n
echo "4.8.0" > ../i18n/version.txt*
echo "4.8.0" > version.txt
cd .. && zip i18n.zip -r i18n
```
