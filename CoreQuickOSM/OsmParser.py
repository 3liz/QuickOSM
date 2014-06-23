# -*- coding: utf-8 -*-
from qgis.core import QgsVectorLayer, QgsFeature, QgsField, QgsFields, QgsVectorFileWriter
from PyQt4.QtCore import QVariant

from osgeo import gdal
from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException
import pghstore
import tempfile
import os

class OsmParser:
    '''
    Parse an OSM file with OGR
    '''
    
    #Layers available in the OGR driver for OSM
    OSM_LAYERS = ['points','lines','multilinestrings','multipolygons','other_relations']
    
    #Dict to build the full ID of an object
    OSM_TYPE = {'node':'n', 'way':'w', 'relation':'r'}
    
    #Whitle list for the attribute table, if set to None all the keys will be keep
    WHITE_LIST = {'multilinestrings': None, 'points': None, 'lines': None, 'multipolygons': None}
    
    def __init__(self,osmFile, layers = OSM_LAYERS, whiteListColumn = WHITE_LIST, deleteEmptyLayers = False):
        self.__osmFile = osmFile
        self.__layers = layers
        self.__whiteListColumn = whiteListColumn
        self.__deleteEmptyLayers = deleteEmptyLayers
        
    def parse(self):
        '''
        Start parsing the osm file
        '''
        
        #Configuration for OGR
        current_dir = os.path.dirname(os.path.realpath(__file__))
        osmconf = current_dir + '/osmconf.ini'
        gdal.SetConfigOption('OSM_CONFIG_FILE', osmconf)
        gdal.SetConfigOption('OSM_USE_CUSTOM_INDEXING', 'NO')
        
        if not os.path.isfile(self.__osmFile):
            raise GeoAlgorithmExecutionException, "File doesn't exist"
        
        uri = self.__osmFile + "|layername="
        layers = {}
        osm_type = {'node':'n', 'way':'w', 'relation':'r'}
        
        #Foreach layers
        for layer in self.__layers:
            layers[layer] = {}
            
            #Reading it with a QgsVectorLayer
            layers[layer]['vectorLayer'] = QgsVectorLayer(uri + layer, "test_" + layer,"ogr")
            
            if layers[layer]['vectorLayer'].isValid() == False:
                raise GeoAlgorithmExecutionException, "Error on the layer", layers[layer]['vectorLayer'].lastError()
            
            #Set some default tags
            layers[layer]['tags'] = ['id_full','osm_id','osm_type']
            
            #Save the geometry type of the layer
            layers[layer]['geomType'] = layers[layer]['vectorLayer'].wkbType()
            
            #Set a featureCount
            layers[layer]['featureCount'] = 0
            
            for feature in layers[layer]['vectorLayer'].getFeatures():
                layers[layer]['featureCount'] += 1
                
                #Get the "others_tags" field
                attrs = None
                if layer in ['points','lines','multilinestrings','other_relations']:
                    attrs = feature.attributes()[1:]
                else:
                    #In the multipolygons layer, there is one more column before "other_tags"
                    attrs = feature.attributes()[2:]
                
                if attrs[0]:
                    hstore = pghstore.loads(attrs[0])
                    for key in hstore:
                        if key not in layers[layer]['tags']: #If the key in OSM is not already in the table
                            if self.__whiteListColumn[layer]: #
                                if key in self.__whiteListColumn[layer]:
                                    layers[layer]['tags'].append(key)
                            else:
                                layers[layer]['tags'].append(key)
        
        #Delete empty layers if this option is set to True
        if self.__deleteEmptyLayers:
            deleteLayers = []
            for keys,values in layers.iteritems() :
                if values['featureCount'] < 1:
                    deleteLayers.append(keys)
            for layer in deleteLayers:
                del layers[layer]

        #Creating GeoJSON files for each layers
        for layer in self.__layers:
            tf = tempfile.NamedTemporaryFile(delete=False,suffix="_"+layer+".geojson")
            layers[layer]['geojsonFile'] = tf.name
            tf.flush()
            tf.close()
            
            #Adding the attribute table
            fields = QgsFields()
            for key in layers[layer]['tags']:
                fields.append(QgsField(key, QVariant.String))
            fileWriter = QgsVectorFileWriter(layers[layer]['geojsonFile'],'UTF-8',fields,layers[layer]['geomType'],layers[layer]['vectorLayer'].crs(),'GeoJSON')
            
            #Foreach feature in the layer
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