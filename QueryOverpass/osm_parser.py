# -*- coding: utf-8 -*-
from qgis.core import QgsApplication, QgsVectorLayer, QgsFeature, QgsField, QgsFields, QgsVectorFileWriter
from PyQt4.QtCore import QVariant

from osgeo import gdal
import pghstore
import tempfile
import os

class OsmParser:
    
    def __init__(self,osmFile, deleteLayers = False):
        self.__osmFile = osmFile
        self.__deleteLayers = deleteLayers
        
        
    def parse(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        osmconf = current_dir + '/osmconf.ini'
        print osmconf
        gdal.SetConfigOption('OSM_CONFIG_FILE', osmconf)
        
        uri = self.__osmFile + "|layername="
        layers = {}
        osmLayers = ['points','lines','multilinestrings','multipolygons','other_relations']        
        osm_type = {'node':'n', 'way':'w', 'relation':'r'}
        
        for layer in osmLayers:
            layers[layer] = {}
            layers[layer]['vectorLayer'] = QgsVectorLayer(uri + layer, "test_" + layer,"ogr")
            layers[layer]['featureCount'] = None
            layers[layer]['tags'] = ['id_full','osm_id','osm_type']
            layers[layer]['geomType'] = layers[layer]['vectorLayer'].wkbType()
            featureCount = 0
            iterator = layers[layer]['vectorLayer'].getFeatures()
            for feature in iterator:
                featureCount += 1
                attrs = None
                if layer in ['points','lines','multilinestrings','other_relations']:
                    attrs = feature.attributes()[1:]
                else:
                    attrs = feature.attributes()[2:]
                if attrs[0]:
                    hstore = pghstore.loads(attrs[0])
                    for key in hstore:
                        if key not in layers[layer]['tags']:
                                layers[layer]['tags'].append(key)
            layers[layer]['featureCount'] = featureCount
        
        if self.__deleteLayers == True:
            deleteLayers = []
            for keys,values in layers.iteritems() :
                if values['featureCount'] < 1:
                    deleteLayers.append(keys)
            for layer in deleteLayers:
                del layers[layer]

        for layer in layers:
            tf = tempfile.NamedTemporaryFile(delete=False,suffix="_"+layer+".geojson")
            layers[layer]['geojsonFile'] = tf.name
            tf.flush()
            tf.close()
            
            fields = QgsFields()
            for key in layers[layer]['tags']:
                fields.append(QgsField(key, QVariant.String))
            fileWriter = QgsVectorFileWriter(layers[layer]['geojsonFile'],'UTF-8',fields,layers[layer]['geomType'],layers[layer]['vectorLayer'].crs(),'GeoJSON')
            
            for feature in layers[layer]['vectorLayer'].getFeatures():
                fet = QgsFeature()
                fet.setGeometry(feature.geometry())
                
                newAttrs= []
                attrs = feature.attributes()
                
                if layer in ['points','lines','multilinestrings']:
                    if layer == 'points':
                        osmType = "node"
                    elif layer == 'lines':
                        osmType = "way"
                    elif layer == 'multilinestrings':
                        osmType = 'relation'
                    
                    newAttrs.append(osm_type[osmType]+str(attrs[0]))
                    newAttrs.append(attrs[0])
                    newAttrs.append(osmType)
                    
                    if attrs[1]:
                        hstore = pghstore.loads(attrs[1])
                        for tag in layers[layer]['tags'][3:]:
                            if unicode(tag) in hstore:
                                newAttrs.append(hstore[tag])
                            else:
                                newAttrs.append("")
                        fet.setAttributes(newAttrs)
                        fileWriter.addFeature(fet)
                    
                elif layer == 'multipolygons':
                    if attrs[0]:
                        osmType = "relation"
                        newAttrs.append(osm_type[osmType]+str(attrs[0]))
                        newAttrs.append(osm_type[osmType]+str(attrs[0]))
                    else:
                        osmType = "way"
                        newAttrs.append(osm_type[osmType]+str(attrs[1]))
                        newAttrs.append(attrs[1])
                    newAttrs.append(osmType)
                    
                    hstore = pghstore.loads(attrs[2])
                    for tag in layers[layer]['tags'][3:]:
                        if unicode(tag) in hstore:
                            newAttrs.append(hstore[tag])
                        else:
                            newAttrs.append("")
                    fet.setAttributes(newAttrs)
                    fileWriter.addFeature(fet)
                    
            del fileWriter        
        return layers