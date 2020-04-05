"""Python code style check."""

import sys
import unittest
from os.path import abspath, dirname, join
from subprocess import Popen, PIPE

__copyright__ = 'Copyright 2019, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'
__revision__ = '$Format:%H$'


class TestPythonPep(unittest.TestCase):

    """Test Python code."""

    @unittest.skip
    def test_flake8(self):
        """Test if the code is Flake8 compliant."""
        # Root is the root path of the repo
        root = abspath(join(dirname(__file__), '../'))

        if sys.platform.startswith('win'):
            return

        # OSX and linux just delegate to make
        command = ['flake8']
        output = Popen(
            command, stdout=PIPE, cwd=root, encoding='utf8').communicate()[0]
        default_number_lines = 0

        lines = len(output.splitlines()) - default_number_lines
        print(output)
        message = 'Hey mate, go back to your keyboard :)'
        self.assertEqual(lines, 0, message)

    # def test_pep257(self):
    #     """Test if docstrings are PEP257 compliant."""
    #     # Root is the root path of the repo
    #     root = os.path.abspath(
    #         os.path.join(os.path.dirname(__file__), '../../'))
    #     if os.environ.get('ON_TRAVIS', False):
    #         command = ['make', 'pep257']
    #         output = Popen(
    #             command,
    #             stderr=PIPE,
    #             cwd=root,
    #             encoding='utf8').communicate()[1]
    #         default_number_lines = 0
    #     elif sys.platform.startswith('win'):
    #         command = [
    #             'pep257',
    #             '--ignore=D102,D103,D104,D105,D200,D201,D202,D203,'
    #             'D205,D210,D211,D300,D301,D302,D400,D401,'
    #             'safe/']
    #         # Shamelessly hardcoded path for now..TS
    #         path = (
    #             "C:\\PROGRA~1\\QGIS2~1.14\\apps\\Python27\\scripts")
    #         path = os.path.normpath(path)
    #         output = Popen(
    #             command,
    #             stderr=PIPE,
    #             cwd=root,
    #             executable=os.path.join(path, 'pep257.exe'),
    #             encoding='utf8').communicate()[1]
    #         default_number_lines = 0
    #
    #     else:
    #         # OSX and linux just delegate to make
    #         command = ['make', 'pep257']
    #         output = Popen(
    #             command,
    #             stderr=PIPE,
    #             cwd=root,
    #             encoding='utf8').communicate()[1]
    #         default_number_lines = 0
    #
    #     # make pep257 produces some extra lines by default.
    #     print(output)
    #     lines = (len(output.splitlines()) - default_number_lines) / 2
    #
    #     message = (
    #         'Hey mate, go back to your keyboard :) I got %s '
    #         'errors from PEP257.)' % lines)
    #     self.assertEqual(lines, 0, message)


if __name__ == '__main__':
    suite = unittest.makeSuite(TestPythonPep, 'test')
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
