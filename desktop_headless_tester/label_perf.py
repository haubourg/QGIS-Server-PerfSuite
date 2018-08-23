# this scripts needs to be run with the following environment variable set correctly with the prefix location
# Ex:
#   export LD_LIBRARY_PATH=/home/regis/APPS/QGIS3/qgis3_release/lib
#   export LD_LIBRARY_PATH=/home/regis/APPS/QGIS3/qgis3_release/lib

import time
import sys
import future

try:
    from qgis.core import Qgis
except ImportError:
    from qgis.core import QGis as Qgis

version = Qgis.QGIS_VERSION_INT


if version < 3 :
#QGIS2 specific imports
    from qgis.core import (QgsDataSourceURI,
                           QgsVectorLayer,
                           QgsMapLayerRegistry,
                           QgsApplication,
                           QgsMapSettings,
                           QgsRectangle,
                           QgsMapRendererCustomPainterJob,
                           QgsPalLayerSettings
                           )

    from PyQt4.QtCore import QSize, Qt
    from PyQt4.QtGui import QApplication, QImage, QPainter, QColor

if version >= 3 :
    #QGIS3 specific imports
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

    from PyQt5.QtCore import QSize, Qt
    from PyQt5.QtGui import QImage, QPainter, QColor

    from PyQt5.QtWidgets import QApplication

else :
    print('unsupported version. Exiting perf testing')
    exit()

prefix = "/usr"
# prefix = "/home/regis/APPS/QGIS3/qgis3_release/"
app = QApplication([])
QgsApplication.setPrefixPath(prefix, True)
QgsApplication.initQgis()


# init vector layer
vl = QgsVectorLayer('/data/REFS/opendata/roads_osm.gpkg|roads_osm', 'roads_osm2', 'ogr')
# vl = QgsVectorLayer('/home/regis/APPS/QGIS3/cpp/QGIS/tests/testdata/curved_polys.gpkg|layername=polys', 'curved_poly', 'ogr')

if vl == False :
    print('Error adding vector layer')

print( str(vl.name() ) )
# n_feat = vl.featureCount()
# print( str( n_feat ) )
# Ex:
#   export LD_LIBRARY_PATH=/home/regis/APPS/QGIS3/qgis3_release/lib
#   export
project = QgsProject.instance()
project.addMapLayers([vl])

print('Project Layers:')
for l in project.mapLayers() :
    print(l)

extent = vl.extent()

# map settings
size = QSize(1629, 800)
ms = QgsMapSettings()

crs = QgsCoordinateReferenceSystem("EPSG:2154")
# ms.setExtent( QgsRectangle(-4.7785446167610397,48.2772163121766340,-4.5545540303610084,48.4047377555436498) )

ms.setExtent( extent )
ms.setOutputSize( size )

# QGIS 2 specific

if version < 3 :

    QgsMapLayerRegistry.instance().addMapLayer(vl, False)


# QGIS 3 specific

if version >= 3 :

 # init a canvas object
    canvas = QgsMapCanvas()
    canvas.setDestinationCrs(crs)
    canvas.setLayers([vl])
    # print(canvas.layers())
    # canvas.show()
    #canvas.refresh()



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
ms.setLayers([vl])

# ms.setLayers([vl])
i0 = QImage(size, QImage.Format_RGB32)
i0.fill( Qt.white )
p0 = QPainter(i0)
j0 = QgsMapRendererCustomPainterJob(ms, p0)


start = time.time()
j0.renderSynchronously()# Ex:
#   export LD_LIBRARY_PATH=/home/regis/APPS/QGIS3/qgis3_release/lib
#   export
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
# app.exit()
