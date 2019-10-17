# Makefile for QuickOSM

# Add ISO code for any locales you want to support here (space separated)
LOCALES = "fr de en es fi id it nl pl pt pt_BR ru zh_TW"
# Name of the plugin, for the ZIP file
PLUGINNAME = QuickOSM

help:
	$(MAKE) -C qgis_plugin_tools help

docker_test:
	$(MAKE) -C qgis_plugin_tools docker_test PLUGINNAME=$(PLUGINNAME)

i18n_%:
	$(MAKE) -C qgis_plugin_tools i18n_$* LOCALES=$(LOCALES)

release_%:
	$(MAKE) -C qgis_plugin_tools release_$* PLUGINNAME=$(PLUGINNAME)
