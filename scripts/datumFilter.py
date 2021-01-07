# -*- coding: utf-8 -*-

"""
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingFeedback,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterField,
                       QgsProcessingParameterVectorLayer,
                       QgsProcessingParameterDateTime
                       )
from qgis import (processing,utils)
from qgis.core import (QgsMessageLog,QgsProject)
from qgis.utils import iface

class nachDatumFiltern(QgsProcessingAlgorithm):
    # Funktionsübergreifende Namen für die Variablen
    INPUT = 'INPUT'    
    METHODE = 'METHODE'
    FELD = 'FELD'
    METHODES = ['0','1']
    DATE0 = 'DATE0'
    DATE1 = 'DATE1'   
    iface = iface
    def tr(self, string):        
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return nachDatumFiltern()

    def name(self):        
        return 'nachDatumFiltern'

    def displayName(self):        
        return self.tr('Nach Datum filtern')

    
    def group(self):
        return self.tr(self.groupId())

    def groupId(self):
        return ''

    def shortHelpString(self):        
        return self.tr("Mit diesem Script kann ein Vektor Layer mit einem Anfang und Ende Datum gefiltert werden."+'\n'\
        +"Sie können das Layer auswählen, das Sie filtern wollen. Die Spalte, die das Datum enthält, wird automatisch ausgewählt."+'\n'\
        +"Wählen Sie zum Löschen sämtlicher Filter die Methode \'Filter Löschen\' aus."+'\n'\
        +"1. Methode wählen"+'\n'\
        +"2. Layer wählen"+'\n'\
        +"3. Anfangs- und Enddatum eingeben"+'\n'\
        +"4. Auf LOS klicken")
    
    def shortDescription(self):
        return self.tr("Mit diesem Script können mehrere Layer gefiltert werden")
    
    def initAlgorithm(self, config=None):
        self.iface = iface
        self.methoden = ['Filtern','Filter Löschen']       
        
        # Methode: Filtern oder Filter löschen
        self.addParameter(
            QgsProcessingParameterEnum(
            name = self.METHODE,
            description  = self.tr('Methode'),
            options = self.methoden,
            defaultValue = 0
            )
        )        
        # Inputlayer
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                name = self.INPUT,
                description  = self.tr('Input Layer')
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                name = self.FELD,
                description  = self.tr('Datum'),
                allowMultiple = True,
                defaultToAllFields = True,
                parentLayerParameterName = self.INPUT,
                type = QgsProcessingParameterField.DateTime  
            )
        )
        
        self.addParameter(
            QgsProcessingParameterDateTime(
            name = self.DATE0,
            description  = self.tr('Von'),
            type = QgsProcessingParameterDateTime.Date
            )
        )
        self.addParameter(
            QgsProcessingParameterDateTime(
            name = self.DATE1,
            description  = self.tr('Bis'),
            defaultValue = "0",
            type = QgsProcessingParameterDateTime.Date
            )
        )
        
        
    def processAlgorithm(self, parameters, context, feedback):         
        layer = self.parameterAsVectorLayer(parameters,self.INPUT,context)
        methode = self.parameterAsEnum(parameters, self.METHODE, context)
        feld = self.parameterAsMatrix(parameters, self.FELD, context)
        
        
        
                
        if len(feld) == 1:
            feld = ''.join(feld)
        
            anfang = self.parameterAsString (parameters, self.DATE0, context)
            ende = self.parameterAsString (parameters, self.DATE1, context)
            if methode == 0:        
                filter = '"{spalte}" > \'{an}\' AND "{spalte}" < \'{en}\''.format(spalte = str(feld),an = str(anfang),en =str(ende))
                
                layer.setSubsetString(filter)
                text = "\nEs werden noch noch Features aus dem Layer "'"{}"'" zwischen "'"{}"'" und "'"{}"'" dargestellt\n".format(layer.name(),str(anfang),str(ende))
                feedback.pushInfo(text)
                return {self.INPUT: filter}
            
            if methode == 1:
                layer.setSubsetString('') 
                return {self.METHODE: methode}