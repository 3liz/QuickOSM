# -*- coding: utf-8 -*-
# Copyright (C) 2012 by Hong Minhee <http://dahlia.kr/>,
#                       StyleShare <https://stylesha.re/>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
""":mod:`pghstore` --- PostgreSQL hstore formatter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This small module implements a formatter and a loader for hstore_,
one of PostgreSQL_ supplied modules, that stores simple key-value pairs.

.. sourcecode:: pycon

   >>> dumps({u'a': u'1'})
   '"a"=>"1"'
   >>> loads('"a"=>"1"')
   {u'a': u'1'}
   >>> src = [('pgsql', 'mysql'), ('python', 'php'), ('gevent', 'nodejs')]
   >>> loads(dumps(src), return_type=list)
   [(u'pgsql', u'mysql'), (u'python', u'php'), (u'gevent', u'nodejs')]

You can easily install the package from PyPI_ by using :program:`pip` or
:program:`easy_install`:

.. sourcecode:: console

   $ pip install pghstore

.. _hstore: http://www.postgresql.org/docs/9.1/static/hstore.html
.. _PostgreSQL: http://www.postgresql.org/
.. _PyPI: http://pypi.python.org/pypi/pghstore

"""
from future import standard_library
standard_library.install_aliases()
import re
try:
    import io as StringIO
except ImportError:
    import io


__all__ = 'dumps', 'loads', 'dump', 'load'
__version__ = '0.9.2'


def dumps(obj, key_map=None, value_map=None, encoding='utf-8',
          return_unicode=False):
    r"""Converts a mapping object as PostgreSQL ``hstore`` format.

    .. sourcecode:: pycon

       >>> dumps({u'a': u'1 "quotes"'})
       '"a"=>"1 \\"quotes\\""'
       >>> dumps([('key', 'value'), ('k', 'v')])
       '"key"=>"value","k"=>"v"'

    It accepts only strings as keys and values except ``None`` for values.
    Otherwise it will raise :exc:`TypeError`:

    .. sourcecode:: pycon

       >>> dumps({'null': None})
       '"null"=>NULL'
       >>> dumps([('a', 1), ('b', 2)])
       Traceback (most recent call last):
         ...
       TypeError: value 1 of key 'a' is not a string

    Or you can pass ``key_map`` and ``value_map`` parameters to workaround
    this:

    .. sourcecode:: pycon

       >>> dumps([('a', 1), ('b', 2)], value_map=str)
       '"a"=>"1","b"=>"2"'

    By applying these options, you can store any other Python objects
    than strings into ``hstore`` values:

    .. sourcecode:: pycon

       >>> try:
       ...    import json
       ... except ImportError:
       ...    import simplejson as json
       >>> dumps([('a', range(3)), ('b', 2)], value_map=json.dumps)
       '"a"=>"[0, 1, 2]","b"=>"2"'
       >>> import pickle
       >>> dumps([('a', range(3)), ('b', 2)],
       ...       value_map=pickle.dumps)  # doctest: +ELLIPSIS
       '"a"=>"...","b"=>"..."'

    It returns a UTF-8 encoded string, but you can change the ``encoding``:

    .. sourcecode:: pycon

       >>> dumps({'surname': u'\ud64d'})
       '"surname"=>"\xed\x99\x8d"'
       >>> dumps({'surname': u'\ud64d'}, encoding='utf-32')
       '"surname"=>"\xff\xfe\x00\x00M\xd6\x00\x00"'

    If you set ``return_unicode`` to ``True``, it will return :class:`unicode`
    instead of :class:`str` (byte string):

    .. sourcecode:: pycon

       >>> dumps({'surname': u'\ud64d'}, return_unicode=True)
       u'"surname"=>"\ud64d"'

    :param obj: a mapping object to dump
    :param key_map: an optional mapping function that takes a non-string key
                    and returns a mapped string key
    :param value_map: an optional mapping function that takes a non-string
                      value and returns a mapped string value
    :param encoding: a string encode to use
    :param return_unicode: returns an :class:`unicode` string instead
                           byte :class:`str`.  ``False`` by default
    :type return_unicode: :class:`bool`
    :returns: a ``hstore`` data
    :rtype: :class:`basestring`

    """
    b = io.StringIO()
    dump(obj, b, key_map=key_map, value_map=value_map, encoding=encoding)
    result = b.getvalue()
    if return_unicode:
        return result.decode(encoding)
    return result


def loads(string, encoding='utf-8', return_type=dict):
    """Parses the passed hstore format ``string`` to a Python mapping object.

    .. sourcecode:: pycon

       >>> loads('a=>1')
       {u'a': u'1'}

    If you want to load a hstore value as any other type than :class:`dict`
    set ``return_type`` parameter.  Note that the constructor has to take
    an iterable object.

    .. sourcecode:: pycon

       >>> loads('a=>1, b=>2', return_type=list)
       [(u'a', u'1'), (u'b', u'2')]
       >>> loads('"return_type"=>"tuple"', return_type=tuple)
       ((u'return_type', u'tuple'),)

    :param string: a hstore format string
    :type string: :class:`basestring`
    :param encoding: an encoding of the passed ``string``.  if the ``string``
                     is an :class:`unicode` string, this parameter will be
                     ignored
    :param return_type: a map type of return value.  default is :class:`dict`
    :returns: a parsed map.  its type is decided by ``return_type`` parameter

    """
    return return_type(parse(string, encoding=encoding))


def dump(obj, file, key_map=None, value_map=None, encoding='utf-8'):
    """Similar to :func:`dumps()` except it writes the result into the passed
    ``file`` object instead of returning it.

    .. sourcecode:: pycon

       >>> import StringIO
       >>> f = StringIO.StringIO()
       >>> dump({u'a': u'1'}, f)
       >>> f.getvalue()
       '"a"=>"1"'

    :param obj: a mapping object to dump
    :param file: a file object to write into
    :param key_map: an optional mapping function that takes a non-string key
                    and returns a mapped string key
    :param value_map: an optional mapping function that takes a non-string
                      value and returns a mapped string value
    :param encoding: a string encode to use

    """
    if callable(getattr(obj, 'iteritems', None)):
        items = iter(obj.items())
    elif callable(getattr(obj, 'items', None)):
        items = list(obj.items())
    elif callable(getattr(obj, '__iter__', None)):
        items = iter(obj)
    else:
        raise TypeError('expected a mapping object, not ' + type(obj).__name__)
    if key_map is None:
        def key_map(key):
            raise TypeError('key %r is not a string' % key)
    elif not callable(key_map):
        raise TypeError('key_map must be callable')
    elif not (value_map is None or callable(value_map)):
        raise TypeError('value_map must be callable')
    write = getattr(file, 'write', None)
    if not callable(write):
        raise TypeError('file must be a wrtiable file object that implements '
                        'write() method')
    first = True
    for key, value in items:
        if not isinstance(key, str):
            key = key_map(key)
        elif not isinstance(key, str):
            key = key.encode(encoding)
        if value is None:
            value = None
        elif not isinstance(value, str):
            if value_map is None:
                raise TypeError('value %r of key %r is not a string' %
                                (value, key))
            value = value_map(value)
        elif not isinstance(value, str):
            value = value.encode(encoding)
        if first:
            write('"')
            first = False
        else:
            write(',"')
        write(escape(key))
        if value is None:
            write('"=>NULL')
        else:
            write('"=>"')
            write(escape(value))
            write('"')


def load(file, encoding='utf-8'):
    """Similar to :func:`loads()` except it reads the passed ``file`` object
    instead of a string.

    """
    read = getattr(file, 'read', None)
    if not callable(read):
        raise TypeError('file must be a readable file object that implements '
                        'read() method')
    return load(read(), encoding=encoding)


#: The pattern of pairs.  It captures following four groups:
#:
#: ``kq``
#:    Quoted key string.
#:
#: ``kb``
#:    Bare key string.
#:
#: ``vq``
#:    Quoted value string.
#:
#: ``kq``
#:    Bare value string.
PAIR_RE = re.compile(r'(?:"(?P<kq>(?:[^\\"]|\\.)*)"|(?P<kb>\S+?))\s*=>\s*'
                     r'(?:"(?P<vq>(?:[^\\"]|\\.)*)"|(?P<vn>NULL)|'
                     r'(?P<vb>[^,]+))(?:,|$)', re.IGNORECASE)


def parse(string, encoding='utf-8'):
    r"""More primitive function of :func:`loads()`.  It returns a generator
    that yields pairs of parsed hstore instead of a complete :class:`dict`
    object.

    .. sourcecode:: pycon

       >>> list(parse('a=>1, b => 2, c => null, d => "NULL"'))
       [(u'a', u'1'), (u'b', u'2'), (u'c', None), (u'd', u'NULL')]
       >>> list(parse(r'"a=>1"=>"\"b\"=>2",'))
       [(u'a=>1', u'"b"=>2')]

    """
    offset = 0
    for match in PAIR_RE.finditer(string):
        if offset > match.start() or string[offset:match.start()].strip():
            raise ValueError('malformed hstore value: position %d' % offset)
        kq = match.group('kq')
        if kq:
            key = unescape(kq)
        else:
            key = match.group('kb')
        if isinstance(key, str):
            key = key.decode(encoding)
        vq = match.group('vq')
        if vq:
            value = unescape(vq)
        else:
            vn = match.group('vn')
            value = None if vn else match.group('vb')
        if isinstance(value, str):
            value = value.decode(encoding)
        yield key, value
        offset = match.end()
    if offset > len(string) or string[offset:].strip():
        raise ValueError('malformed hstore value: position %d' % offset)


#: The escape sequence pattern.
ESCAPE_RE = re.compile(r'\\(.)')


def unescape(s):
    r"""Strips escaped sequences.

    .. sourcecode:: pycon

       >>> unescape('abc\\"def\\\\ghi\\ajkl')
       'abc"def\\ghiajkl'
       >>> unescape(r'\"b\"=>2')
       '"b"=>2'

    """
    return ESCAPE_RE.sub(r'\1', s)


def escape(s):
    r"""Escapes quotes and backslashes for use in hstore strings.

    .. sourcecode:: pycon

       >>> escape('string with "quotes"')
       'string with \\"quotes\\"'
    """
    return s.replace('\\', '\\\\').replace('"', '\\"')


if __name__ == '__main__':
    import doctest
    doctest.testmod()
