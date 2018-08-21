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

    from PyQt4.QtCore import QSize
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

    from PyQt5.QtCore import QSize
    from PyQt5.QtGui import QImage, QPainter, QColor

    from PyQt5.QtWidgets import QApplication

else :
    print('unsupported version. Exiting perf testing')
    exit()

prefix = "/usr/bin"
app = QApplication([])
QgsApplication.setPrefixPath(prefix, True)
QgsApplication.initQgis()




# init vector layer
vl = QgsVectorLayer("dbname='/data/REFS/opendata/roads_osm.gpkg' table=\"roads_osm\" (geometry) sql=", "roads_osm", "gpkg")



extent = vl.extent()

# map settings
size = QSize(1629, 800)
ms = QgsMapSettings()
crs = QgsCoordinateReferenceSystem("EPSG:2154")
QgsProject.instance().setCrs(crs)
# ms.setExtent( QgsRectangle(-4.7785446167610397,48.2772163121766340,-4.5545540303610084,48.4047377555436498) )

ms.setExtent( extent )


# QGIS 2 specific
# QgsMapLayerRegistry.instance().addMapLayer(vl, False)

# QGIS 3 specific
QgsProject.instance().addMapLayer(vl, False)

# activate labeling
vl.setCustomProperty("labeling", "pal")
vl.setCustomProperty("labeling/enabled", "true")
vl.setCustomProperty("labeling/drawLabels", "true")
vl.setCustomProperty("labeling/fontFamily", "Arial")
vl.setCustomProperty("labeling/fontSize", "10")
vl.setCustomProperty("labeling/fieldName", "'name'")
vl.setCustomProperty("labeling/isExpression", "true")


# parallel
place = QgsPalLayerSettings.Line
vl.setCustomProperty("labeling/placement", str(place))
vl.setCustomProperty("labeling/placementFlags", "14")

ms.setLayers([vl])
i0 = QImage(size, QImage.Format_RGB32)
p0 = QPainter(i0)
j0 = QgsMapRendererCustomPainterJob(ms, p0)

start = time.time()
j0.renderSynchronously()
t0 = time.time() - start

p0.end()
i0.save('/tmp/para.png')

# horizontal
place = QgsPalLayerSettings.Horizontal
vl.setCustomProperty("labeling/placement", str(place))
vl.setCustomProperty("labeling/placementFlags", "14")

ms.setLayers([vl])
i1 = QImage(size, QImage.Format_RGB32)
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

app.exit()
