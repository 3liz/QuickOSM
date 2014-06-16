# -*- coding: utf-8 -*-
from qgis.core import QgsVectorLayer, QgsFeature, QgsField, QgsFields, QgsVectorFileWriter
from PyQt4.QtCore import QVariant

from osgeo import gdal
import pghstore
import tempfile
import os

class OsmParser:
    
    OSM_LAYERS = ['points','lines','multilinestrings','multipolygons','other_relations']
    OSM_TYPE = {'node':'n', 'way':'w', 'relation':'r'}
    
    def __init__(self,osmFile, layers = OSM_LAYERS, whiteListColumn = None, deleteEmptyLayers = False):
        self.__osmFile = osmFile
        self.__layers = layers
        self.__whiteListColumn = whiteListColumn
        self.__deleteEmptyLayers = deleteEmptyLayers
        
        
    def parse(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        osmconf = current_dir + '/osmconf.ini'
        gdal.SetConfigOption('OSM_CONFIG_FILE', osmconf)
        gdal.SetConfigOption('OSM_USE_CUSTOM_INDEXING', 'NO')
        uri = self.__osmFile + "|layername="
        layers = {}
        osm_type = {'node':'n', 'way':'w', 'relation':'r'}
        
        for layer in self.__layers:
            layers[layer] = {}
            layers[layer]['vectorLayer'] = QgsVectorLayer(uri + layer, "test_" + layer,"ogr")
            
            if layers[layer]['vectorLayer'].isValid() == False:
                raise Exception, "Error on the file"
            
            layers[layer]['featureCount'] = None
            layers[layer]['tags'] = ['id_full','osm_id','osm_type']
            layers[layer]['geomType'] = layers[layer]['vectorLayer'].wkbType()
            featureCount = 0
            for feature in layers[layer]['vectorLayer'].getFeatures():
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
                            if self.__whiteListColumn != None:
                                if self.__whiteListColumn[layer] != None:
                                    if key in self.__whiteListColumn[layer]:
                                        layers[layer]['tags'].append(key)
                            else:
                                layers[layer]['tags'].append(key)
            layers[layer]['featureCount'] = featureCount
        
        if self.__deleteEmptyLayers == True:
            deleteLayers = []
            for keys,values in layers.iteritems() :
                if values['featureCount'] < 1:
                    deleteLayers.append(keys)
            for layer in deleteLayers:
                del layers[layer]

        for layer in self.__layers:
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
                        OSM_TYPE = "node"
                    elif layer == 'lines':
                        OSM_TYPE = "way"
                    elif layer == 'multilinestrings':
                        OSM_TYPE = 'relation'
                    
                    newAttrs.append(osm_type[OSM_TYPE]+str(attrs[0]))
                    newAttrs.append(attrs[0])
                    newAttrs.append(OSM_TYPE)
                    
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
                        OSM_TYPE = "relation"
                        newAttrs.append(osm_type[OSM_TYPE]+str(attrs[0]))
                        newAttrs.append(osm_type[OSM_TYPE]+str(attrs[0]))
                    else:
                        OSM_TYPE = "way"
                        newAttrs.append(osm_type[OSM_TYPE]+str(attrs[1]))
                        newAttrs.append(attrs[1])
                    newAttrs.append(OSM_TYPE)
                    
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