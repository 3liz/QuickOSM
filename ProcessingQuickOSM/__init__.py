from processing.core.Processing import Processing
from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException

from processing.tools import dataobjects, vector

#Processing <2.5
try:
    from processing.parameters.ParameterString import ParameterString
    from processing.parameters.ParameterExtent import ParameterExtent
    from processing.parameters.ParameterFile import ParameterFile
    from processing.parameters.ParameterVector import ParameterVector
    from processing.parameters.ParameterSelection import ParameterSelection
    from processing.parameters.ParameterNumber import ParameterNumber
    
    from processing.outputs.OutputNumber import OutputNumber
    from processing.outputs.OutputFile import OutputFile
    from processing.outputs.OutputTable import OutputTable
    from processing.outputs.OutputVector import OutputVector
    from processing.outputs.OutputString import OutputString
    
except ImportError:
    pass

#Processing >=2.5
try:
    from processing.core.parameters import *    
    from processing.core.outputs import *
    
except ImportError:
    pass