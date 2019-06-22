# coding=utf-8
"""Common functionality used by regression tests."""

from os.path import dirname, abspath, join


def test_data_path(*args):
    """Return the absolute path to the QuickOSM test data or directory path.

    :param args: List of path e.g. ['control', 'files',
        'test-error-message.txt'] or ['control', 'scenarios'] to get the path
        to scenarios dir.
    :type args: list

    :return: Absolute path to the test data or dir path.
    :rtype: str
    """
    path = dirname(__file__)
    path = abspath(join(path, 'data'))
    for item in args:
        path = abspath(join(path, item))

    return path
