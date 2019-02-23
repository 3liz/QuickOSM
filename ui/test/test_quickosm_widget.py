# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QuickOSM
 A QGIS plugin
 OSM Overpass API frontend
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

import unittest

# This import is to enable SIP API V2
# noinspection PyUnresolvedReferences
import qgis  # pylint: disable=unused-import
from test.utilities import get_qgis_app

QGIS_APP, CANVAS, IFACE, PARENT = get_qgis_app()

from QuickOSM.ui.QuickOSMWidget import QuickOSMWidget


class TestQuickOSMWidget(unittest.TestCase):

    def setUp(self):
        self.widget = QuickOSMWidget()

    def tearDown(self):
        self.widget = None

    def test_sort_nominatim_places(self):
        """Test if reorder last nominatim places works."""
        existing_places = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        new_list = self.widget.sort_nominatim_places(existing_places, '3')
        expected = ['3', '1', '2', '4', '5', '6', '7', '8', '9', '10']
        self.assertListEqual(expected, new_list)

        existing_places = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        new_list = self.widget.sort_nominatim_places(existing_places, '11')
        expected = ['11', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.assertListEqual(expected, new_list)

        existing_places = ['1', '2', '3', '4', '5']
        new_list = self.widget.sort_nominatim_places(existing_places, '3')
        expected = ['3', '1', '2', '4', '5']
        self.assertListEqual(expected, new_list)

        existing_places = ['1', '2', '3', '4', '5']
        new_list = self.widget.sort_nominatim_places(existing_places, '6')
        expected = ['6', '1', '2', '3', '4', '5']
        self.assertListEqual(expected, new_list)

        existing_places = ['1', '2', '3', '4', '5']
        new_list = self.widget.sort_nominatim_places(existing_places, '1')
        expected = ['1', '2', '3', '4', '5']
        self.assertListEqual(expected, new_list)

        existing_places = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        new_list = self.widget.sort_nominatim_places(existing_places, '1')
        expected = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        self.assertListEqual(expected, new_list)


if __name__ == '__main__':
    suite = unittest.makeSuite(TestQuickOSMWidget)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
