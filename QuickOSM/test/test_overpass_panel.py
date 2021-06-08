from qgis.core import (
    QgsFeature,
    QgsGeometry,
    QgsPointXY,
    QgsProject,
    QgsVectorLayer,
    edit,
)
from qgis.testing import unittest

from QuickOSM.definitions.gui import Panels
from QuickOSM.ui.dialog import Dialog

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'


class TestQuickOSMWidget(unittest.TestCase):

    def test_sort_nominatim_places(self):
        """Test if reorder last nominatim places works."""
        dialog = Dialog()

        existing_places = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        new_list = dialog.external_panels[Panels.QuickQuery].sort_nominatim_places(existing_places, '3')
        expected = ['3', '1', '2', '4', '5', '6', '7', '8', '9', '10']
        self.assertListEqual(expected, new_list)

        existing_places = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        new_list = dialog.external_panels[Panels.QuickQuery].sort_nominatim_places(existing_places, '11')
        expected = ['11', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.assertListEqual(expected, new_list)

        existing_places = ['1', '2', '3', '4', '5']
        new_list = dialog.external_panels[Panels.QuickQuery].sort_nominatim_places(existing_places, '3')
        expected = ['3', '1', '2', '4', '5']
        self.assertListEqual(expected, new_list)

        existing_places = ['1', '2', '3', '4', '5']
        new_list = dialog.external_panels[Panels.QuickQuery].sort_nominatim_places(existing_places, '6')
        expected = ['6', '1', '2', '3', '4', '5']
        self.assertListEqual(expected, new_list)

        existing_places = ['1', '2', '3', '4', '5']
        new_list = dialog.external_panels[Panels.QuickQuery].sort_nominatim_places(existing_places, '1')
        expected = ['1', '2', '3', '4', '5']
        self.assertListEqual(expected, new_list)

        existing_places = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        new_list = dialog.external_panels[Panels.QuickQuery].sort_nominatim_places(existing_places, '1')
        expected = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        self.assertListEqual(expected, new_list)

    def test_layer(self):
        """ Test when we have a layer in the map canvas. """
        # Maxime, you can edit/remove this test. It's just for demo purpose.
        layer = QgsVectorLayer('Point?crs=epsg:4326&field=id:integer&index=yes', 'test_layer', 'memory')
        with edit(layer):
            f1 = QgsFeature()
            f1.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(10, 10)))
            f1.setAttributes([1])
            f2 = QgsFeature()
            f2.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(5, 15)))
            f2.setAttributes([2])
            layer.addFeatures([f1, f2])
        QgsProject.instance().addMapLayer(layer)

        layer = QgsProject.instance().mapLayersByName('test_layer')[0]
        self.assertIsInstance(layer, QgsVectorLayer)


if __name__ == '__main__':
    suite = unittest.makeSuite(TestQuickOSMWidget)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
