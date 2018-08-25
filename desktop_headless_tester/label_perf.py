# this scripts needs to be run with the following environment variable set correctly with the prefix location
# Ex. for QGIS native install:
#   export PYTHON_PATH=
#   export LD_LIBRARY_PATH=/home/regis/APPS/QGIS3/qgis3_release/lib
#   export QGIS_PREFIX=/home/regis/APPS/QGIS/ltr/
#
# Ex.  for QGIS locally compiled
#   export PYTHON_PATH=export PYTHONPATH=/home/regis/APPS/QGIS3/qgis3_release/share/qgis/python
#   export LD_LIBRARY_PATH=/home/regis/APPS/QGIS3/qgis3_release/lib
#   export QGIS_PREFIX=/home/regis/APPS/QGIS3/qgis3_release
#


import time
import sys
import future
import os

# conditional imports (ugly):

try:
    from qgis.core import Qgis
except ImportError:
    from qgis.core import QGis as Qgis

try:
    from PyQt4.QtGui import QApplication, QImage, QPainter, QColor
    from PyQt4.QtCore import QSize, Qt
    from PyQt4.QtGui import QApplication, QImage, QPainter, QColor

except ImportError:
    from PyQt5.QtCore import QSize, Qt
    from PyQt5.QtGui import QImage, QPainter, QColor
    from PyQt5.QtWidgets import QApplication


try:    #QGIS2 specific imports
    print("Imports for QGIS 2")
    from qgis.core import (QgsDataSourceURI,
    QgsVectorLayer,
    QgsProject,
    QgsMapLayerRegistry,
    QgsApplication,
    QgsMapSettings,
    QgsRectangle,
    QgsMapRendererCustomPainterJob,
    QgsPalLayerSettings,
    QgsCoordinateReferenceSystem)

    from qgis.gui import QgsMapCanvas

except ImportError:
    print("Imports for QGIS 3")
    from qgis.core import (QgsDataSourceUri,
    QgsVectorLayer,
    QgsProject,
    QgsApplication,
    QgsMapSettings,
    QgsRectangle,
    QgsMapRendererCustomPainterJob,
    QgsPalLayerSettings,
    QgsCoordinateReferenceSystem)

    from qgis.gui import QgsMapCanvas

app = QApplication([])

# prefix_qgis2 = "/home/regis/APPS/QGIS/ltr"
# prefix_qgis3 = "/usr"
prefix = os.environ['QGIS_PREFIX']
print("Setting prefix to : " + prefix )
QgsApplication.setPrefixPath(prefix, True)
QgsApplication.initQgis()

version = int(Qgis.QGIS_VERSION_INT)

try :
    pythonpath = os.environ['PYTHONPATH']
    print('Python PATH : ' + pythonpath)
except :
    print('Python PATH not set')

print('LD Library PATH: ' + os.environ['LD_LIBRARY_PATH'])
print('QGIS version tested : ' + str(version))


# init vector layer
vl = QgsVectorLayer('/data/REFS/opendata/roads_osm_2154.gpkg|roads_osm', 'roads_osm2', 'ogr')

vl.extent()

if vl == False :
    print('Error adding vector layer')

print( str(vl.name() ) )

# map settings
project = QgsProject.instance()

# crs = QgsCoordinateReferenceSystem("EPSG:2154")
crs = vl.crs()
print('layer crs is :' + crs.toWkt())
ms = QgsMapSettings()
ms.setDestinationCrs(crs)
print('Map CrRS is : ' + ms.destinationCrs().toWkt())

extent = vl.extent()
print('Extent : ' + extent.asWktCoordinates())
ms.setExtent( extent )
size = QSize(1629, 800)
ms.setOutputSize( size )

# QGIS 2 specific
if version < 30000 :

    QgsMapLayerRegistry.instance().addMapLayer(vl)
    ms.setLayers([vl.id()])


# QGIS 3 specific
if version >= 30000 :

    project.addMapLayers([vl])
    ms.setLayers([vl])

# activate labeling

# vl.setCustomProperty("labeling", "pal")
# vl.setCustomProperty("labeling/enabled", "true")
# vl.setCustomProperty("labeling/drawLabels", "true")
# vl.setCustomProperty("labeling/fontFamily", "Arial")
# vl.setCustomProperty("labeling/fontSize", "10")
# vl.setCustomProperty("labeling/fieldName", "'name'")
# vl.setCustomProperty("labeling/isExpression", "true")


# parallel
# place = QgsPalLayerSettings.Line
# vl.setCustomProperty("labeling/placement", str(place))
# vl.setCustomProperty("labeling/placementFlags", "14")

i0 = QImage(size, QImage.Format_RGB32)
i0.fill( Qt.white )
p0 = QPainter(i0)
j0 = QgsMapRendererCustomPainterJob(ms, p0)


start = time.time()
j0.renderSynchronously()
t0 = time.time() - start

p0.end()
i0.save('/tmp/para.png')

# horizontal
# place = QgsPalLayerSettings.Horizontal
# vl.setCustomProperty("labeling/placement", str(place))
# vl.setCustomProperty("labeling/placementFlags", "14")

i1 = QImage(size, QImage.Format_RGB32)
i1.fill(Qt.white)
p1 = QPainter(i1)
j1 = QgsMapRendererCustomPainterJob(ms, p1)
start = time.time()


j1.renderSynchronously()
t1 = time.time() - start

p1.end()
i1.save('/tmp/hori.png')

print(str('PERF_PARA: ') + str(t0))
print(str('PERF_HORI: ') + str(t1))
print(str('PERF_RATIO: ') + str(t0/t1))

QgsApplication.exitQgis()
app.exit()

print('------Script end-------')
