#include <Python.h>
#include <stdio.h>
#include <string.h>

#define CHAR_CHECK(s, pos, c)                        \
  if (s[pos] != char) {                              \
    PyErr_Format(PyExc_ValueError,                   \
                 "Encountered %c at %i, was expecting %c.",   \
                 s[pos], pos, c);                             \
    return NULL;                                              \
  }

#define isEven(a) (((a) & 1) == 0)

/*
 * Just like strchr, but find first -unescaped- occurrence of c in s.
 */
char *
strchr_unescaped(char *s, char c) 
{
  char *p = strchr(s, c), *q;
  while (p != NULL) { /* loop through all the c's */
    q = p; /* scan backwards through preceding escapes */
    while (q > s && *(q-1) == '\\')
      q--;
    if (isEven(p-q)) /* even number of esc's => c is good */
        return p;
    p = strchr(p+1, c); /* else odd escapes => c is escaped, keep going */
  }
  return NULL;
}

static PyObject *
_speedups_loads(PyObject *self, PyObject *args)
{
  char *s;
  int i, j, null_value = 0;
  char *p[4];
  PyObject *dict, *key, *value;

  if (!PyArg_ParseTuple(args, "s", &s))
    return NULL;

  dict = PyDict_New();
  
  // Each iteration will find one key/value pair
  while ((p[0] = strchr(s, '"')) != NULL) {
    // move to the next character after the found "
    p[0]++;

    // Find end of key
    p[1] = strchr_unescaped(p[0], '"');

    // Find begining of value or NULL
    for (i=1; 1; i++) {
      switch (*(p[1]+i)) {
      case 'N':
      case 'n':
        // found NULL
        null_value = 1;
        break;
      case '"':
        // found begining of value
        p[2] = p[1]+i+1;
        break;
      case '\0':
        // found end of string
        return dict;
      default:
        // neither NULL nor begining of value, keep looking
        continue;
      }
      break;
    }
     
    key = PyString_FromStringAndSize(p[0], p[1]-p[0]);
    if (null_value == 0) {
      // find and null terminate end of value
      p[3] = strchr_unescaped(p[2], '"');
      value = PyString_FromStringAndSize(p[2], p[3]-p[2]);
    } else {
      Py_INCREF(Py_None);
      value = Py_None;
    }
    PyDict_SetItem(dict, key, value);
    Py_DECREF(key);
    Py_DECREF(value);
    
    // set new search position
    if (null_value == 0) 
      s = p[3]+1;
    else
      s = p[1]+i;

    // reset null value flag
    null_value = 0;
  }
  return dict;
}

#define COMMA ","
#define ARROW "=>"
#define EMPTY ""
#define S_NULL "NULL"
#define CITATION "\""

static PyObject *
_speedups_dumps(PyObject *self, PyObject *args)
{
  int i = 0;
  PyObject *d, *list;
  PyObject *key, *value, *result;
  PyObject *comma, *arrow, *empty, *s_null, *citation;
  Py_ssize_t list_len, pos = 0;
  if (!PyArg_ParseTuple(args, "O", &d))
    return NULL;

  // return empty string if we got an empty dict
  empty = PyString_FromString(EMPTY);
  list_len = PyDict_Size(d)*8-1;
  if (list_len == -1) {
    return empty;
  }
  
  // create string constants
  comma = PyString_FromString(COMMA);
  arrow = PyString_FromString(ARROW);
  s_null = PyString_FromString(S_NULL);
  citation = PyString_FromString(CITATION);
  
  list = PyList_New(list_len);

  while (PyDict_Next(d, &pos, &key, &value)) {
    // add comma (,)
    if (i > 0) {
      Py_INCREF(comma);
      PyList_SetItem(list, i, comma); i++;
    }
    // add key
    Py_INCREF(citation);
    PyList_SetItem(list, i, citation); i++;
    PyList_SetItem(list, i, PyObject_Str(key)); i++;
    Py_INCREF(citation);
    PyList_SetItem(list, i, citation); i++;
    // add arrow (=>)
    Py_INCREF(arrow);
    PyList_SetItem(list, i, arrow); i++;
    // add value or null
    if (value != Py_None) {
      // add value
      Py_INCREF(citation);
      PyList_SetItem(list, i, citation); i++;
      PyList_SetItem(list, i, PyObject_Str(value)); i++;
      Py_INCREF(citation);
      PyList_SetItem(list, i, citation); i++;
    } else {
      // add null
      Py_INCREF(empty);
      PyList_SetItem(list, i, empty); i++;
      Py_INCREF(s_null);
      PyList_SetItem(list, i, s_null); i++;
      Py_INCREF(empty);
      PyList_SetItem(list, i, empty); i++;
    }
  }
  result = PyObject_CallMethod(empty, "join", "O", list);
  Py_DECREF(empty);
  Py_DECREF(comma);
  Py_DECREF(arrow);
  Py_DECREF(s_null);
  Py_DECREF(citation);
  Py_DECREF(list);
  return result;
}


static PyMethodDef CPgHstoreMethods[] = {
    {"loads",  _speedups_loads, METH_VARARGS,
     "Parse (decode) a postgres hstore string into a dict."},
    {"dumps",  _speedups_dumps, METH_VARARGS,
     "Dump (encode) a dict into a postgres hstore string."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC
init_speedups(void)
{
    PyObject *m;

    m = Py_InitModule("pghstore._speedups", CPgHstoreMethods);
    if (m == NULL)
        return;
}

int
main(int argc, char *argv[])
{
    /* Pass argv[0] to the Python interpreter */
    Py_SetProgramName(argv[0]);

    /* Initialize the Python interpreter.  Required. */
    Py_Initialize();

    /* Add a static module */
    init_speedups();

    return 0;
}
