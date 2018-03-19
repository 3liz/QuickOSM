""":mod:`pghstore` --- PostgreSQL hstore formatter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This small module implements a formatter and a loader for hstore_,
one of PostgreSQL_ supplied modules, that stores simple key-value pairs.

.. sourcecode:: pycon

   >>> dumps({'a': '1'})
   '"a"=>"1"'
   >>> loads('"a"=>"1"')
   {'a': '1'}
   >>> src = [('pgsql', 'mysql'), ('python', 'php'), ('gevent', 'nodejs')]
   >>> loads(dumps(src), return_type=list)
   [('pgsql', 'mysql'), ('python', 'php'), ('gevent', 'nodejs')]

You can easily install the package from PyPI_ by using :program:`pip` or
:program:`easy_install`:

.. sourcecode:: console

   $ pip install pghstore

.. _hstore: http://www.postgresql.org/docs/9.1/static/hstore.html
.. _PostgreSQL: http://www.postgresql.org/
.. _PyPI: http://pypi.python.org/pypi/pghstore

"""


from .version import VERSION
try:
    from ._speedups import dumps, loads
except ImportError:
    from ._native import dump, dumps, load, loads
else:
    def dump(obj, file):
        file.write(dumps(obj, file))

    def load(file):
        return loads(file.read())

__all__ = '__version__', 'dump', 'dumps', 'load', 'loads'


#: (:class:`basestring`) The version string e.g. ``'0.9.2'``.
#:
#: .. deprecated:: 1.0.0
#:    Use :mod:`pghstore.version` module instead.
__version__ = VERSION

