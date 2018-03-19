""":mod:`pghstore.version` --- Version data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can find the current version in the command line interface:

.. sourcecode:: console

   $ python -m wand.version
   0.9.2

.. versionadded:: 1.0.0

"""

__all__ = 'VERSION', 'VERSION_INFO'


#: (:class:`tuple`) The version tuple e.g. ``(0, 9, 2)``.
VERSION_INFO = (1, 0, 0)

#: (:class:`basestring`) The version string e.g. ``'0.9.2'``.
VERSION = '%d.%d.%d' % VERSION_INFO

__doc__ = __doc__.replace('0.9.2', VERSION)


if __name__ == '__main__':
    print(VERSION)

