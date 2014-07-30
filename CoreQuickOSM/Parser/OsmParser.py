# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QuickOSM
                                 A QGIS plugin
 OSM's Overpass API frontend
                             -------------------
        begin                : 2014-06-11
        copyright            : (C) 2014 by 3Liz
        email                : info at 3liz dot com
        contributor          : Etienne Trimaille
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from QuickOSM import *

from osgeo import gdal
from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException
import pghstore
import tempfile
import os

class OsmParser(QObject):
    '''
    Parse an OSM file with OGR
    '''
    
    #Signal percentage
    signalPercentage = pyqtSignal(int, name='signalPercentage')
    #Signal text
    signalText = pyqtSignal(str, name='signalText')
    
    #Layers available in the OGR driver for OSM, other_relations is useless without specific parser
    OSM_LAYERS = ['points','lines','multilinestrings','multipolygons','other_relations']
    OSM_LAYERS = ['points','lines','multilinestrings','multipolygons']
    
    #Dict to build the full ID of an object
    DIC_OSM_TYPE = {'node':'n', 'way':'w', 'relation':'r'}
    
    #Whitle list for the attribute table, if set to None all the keys will be keep
    WHITE_LIST = {'multilinestrings': None, 'points': None, 'lines': None, 'multipolygons': None}
    
    def __init__(self,osmFile, layers = OSM_LAYERS, whiteListColumn = WHITE_LIST, deleteEmptyLayers = False, loadOnly = False, osmConf = None):
        self.__osmFile = osmFile
        self.__layers = layers
        if not whiteListColumn:
            whiteListColumn = {'multilinestrings': None, 'points': None, 'lines': None, 'multipolygons': None}
        self.__whiteListColumn = whiteListColumn
        self.__deleteEmptyLayers = deleteEmptyLayers
        self.__loadOnly = loadOnly
        
        #If an osmconf is provided ?
        if not osmConf:
            current_dir = os.path.dirname(os.path.realpath(__file__))
            self.__osmconf = os.path.join(current_dir,'QuickOSMconf.ini')
        else:
            self.__osmconf = str(osmConf.encode("utf-8"))
        
        QObject.__init__(self)
        
    def parse(self):
        '''
        Start parsing the osm file
        ''' 
        
        #Configuration for OGR
        gdal.SetConfigOption('OSM_CONFIG_FILE', self.__osmconf)
        gdal.SetConfigOption('OSM_USE_CUSTOM_INDEXING', 'NO')
        
        if not os.path.isfile(self.__osmFile):
            raise GeoAlgorithmExecutionException, "File doesn't exist"
        
        import re

        with open(self.__osmFile) as f:
            for line in f:
                s=re.search(r'node',line)
                if s:
                    break
            else:
                raise NoPointsLayerException
        
        
        uri = self.__osmFile + "|layername="
        layers = {}
        
        #If loadOnly, no parsing required:
        #It's used only when we ask to open an osm file
        if self.__loadOnly:
            fileName = os.path.basename(self.__osmFile)
            for layer in self.__layers:
                layers[layer] = QgsVectorLayer(uri + layer, fileName + " " + layer,"ogr")
            
                if not layers[layer].isValid():
                    print "Error on the layer", layers[layer].lastError()
                
            return layers              
        
        #Foreach layers
        for layer in self.__layers:
            self.signalText.emit(QApplication.translate("QuickOSM",u"Parsing layer : " + layer))
            layers[layer] = {}
            
            #Reading it with a QgsVectorLayer
            layers[layer]['vectorLayer'] = QgsVectorLayer(uri + layer, "test_" + layer,"ogr")
            
            if layers[layer]['vectorLayer'].isValid() == False:
                raise GeoAlgorithmExecutionException, "Error on the layer", layers[layer]['vectorLayer'].lastError()
            
            #Set some default tags
            layers[layer]['tags'] = ['full_id','osm_id','osm_type']
            
            #Save the geometry type of the layer
            layers[layer]['geomType'] = layers[layer]['vectorLayer'].wkbType()
            
            #Set a featureCount
            layers[layer]['featureCount'] = 0
            
            for i, feature in enumerate(layers[layer]['vectorLayer'].getFeatures()):
                layers[layer]['featureCount'] += 1
                
                #Improve the parsing if comma in whitelist, we skip the parsing of tags, but featureCount is needed
                if self.__whiteListColumn[layer] == ',':
                    continue
                
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
                            if self.__whiteListColumn[layer]:
                                if key in self.__whiteListColumn[layer]:
                                    layers[layer]['tags'].append(key)
                            else:
                                layers[layer]['tags'].append(key)
                                
                self.signalPercentage.emit(int(100 / len(self.__layers) * (i+1)))
        
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
            self.signalText.emit(QApplication.translate("QuickOSM",u"Creating GeoJSON file : " + layer))
            self.signalPercentage.emit(0)
            
            #Creating the temp file
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
            for i, feature in enumerate(layers[layer]['vectorLayer'].getFeatures()):
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
                    
                    newAttrs.append(self.DIC_OSM_TYPE[osmType]+str(attrs[0]))
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
                        newAttrs.append(self.DIC_OSM_TYPE[osmType]+str(attrs[0]))
                        newAttrs.append(str(attrs[0]))
                    else:
                        osmType = "way"
                        newAttrs.append(self.DIC_OSM_TYPE[osmType]+str(attrs[1]))
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
            
                    self.signalPercentage.emit(int(100 / layers[layer]['featureCount'] * (i+1)))
                  
            del fileWriter
            
        return layers