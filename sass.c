#include <Python.h>
#include "sass_interface.h"

typedef struct {
    PyObject_HEAD
    struct sass_options options;
} sass_OptionsObject;

static int
sass_Options_init(sass_OptionsObject *self, PyObject *args, PyObject *kwds)
{
    static char *sig[] = {"include_paths", "image_path", NULL};
    PyObject *include_paths, *image_path, *item;
    char *include_paths_cstr, *item_buffer, *image_path_cstr;
    size_t include_paths_len, include_paths_size, i, offset, item_size,
           image_path_size;
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "OS", sig,
                                     &include_paths, &image_path)) {
        return -1;
    }

    self->options.output_style = SASS_STYLE_NESTED;

    if (include_paths == Py_None) {
        PyErr_SetString(PyExc_TypeError, "include_paths must not be None");
        return -1;
    }
    if (PyString_Check(include_paths)) {
        if (PyString_AsStringAndSize(include_paths,
                                     &include_paths_cstr, &include_paths_size)
            != 0) {
            return -1;
        }
        self->options.include_paths = malloc(sizeof(char) *
                                             (include_paths_size + 1));
        strncpy(self->options.include_paths,
                include_paths_cstr,
                include_paths_size + 1);
        self->options.include_paths[include_paths_size] = '\0';
    }
    else if (PySequence_Check(include_paths)) {
        include_paths_len = PySequence_Size(include_paths);
        if (include_paths_len < 0) {
            return -1;
        }
        include_paths_size = 0;
        for (i = 0; i < include_paths_len; ++i) {
            item = PySequence_GetItem(include_paths, i);
            if (item == NULL) {
                return -1;
            }
            if (!PyString_Check(item)) {
                PyErr_Format(PyExc_TypeError,
                             "include_paths must consists of only strings, "
                             "but #%d is not a string", i);
                return -1;
            }
            include_paths_size += PyString_Size(item);
        }
        // add glue chars
        if (include_paths_len > 1) {
            include_paths_size += include_paths_len - 1;
        }
        self->options.include_paths = malloc(sizeof(char) *
                                             (include_paths_size + 1));
        // join
        offset = 0;
        for (i = 0; i < include_paths_len; ++i) {
            if (i) {
                self->options.include_paths[offset] = ':';
                ++offset;
            }
            item = PySequence_GetItem(include_paths, i);
            PyString_AsStringAndSize(item, &item_buffer, &item_size);
            strncpy(self->options.include_paths + offset,
                    item_buffer, item_size);
            offset += item_size;
        }
        self->options.include_paths[include_paths_size] = '\0';
    }
    else {
        PyErr_SetString(PyExc_TypeError,
                        "include_paths must be a string or a sequence of "
                        "strings");
        return -1;
    }

    if (PyString_AsStringAndSize(image_path,
                                 &image_path_cstr, &image_path_size) != 0) {
        return -1;
    }
    self->options.image_path = malloc(sizeof(char) * (image_path_size + 1));
    strncpy(self->options.image_path, image_path_cstr, image_path_size + 1);
    self->options.image_path[image_path_size] = '\0';

    return 0;
}

static void
sass_Options_dealloc(sass_OptionsObject *self)
{
    free(self->options.include_paths);
    free(self->options.image_path);
    self->ob_type->tp_free((PyObject *) self);
}

static PyObject *
sass_Options_get_include_paths(sass_OptionsObject *self, void *closure)
{
    size_t i, j;
    char *paths;
    PyObject *list;
    int tmp;

    paths = self->options.include_paths;
    list = PyList_New(0);
    if (list == NULL) {
        return NULL;
    }
    Py_INCREF(list);

    i = j = 0;
    do {
        if (i > j && (paths[i] == ':' || paths[i] == '\0')) {
            tmp = PyList_Append(list,
                                PyString_FromStringAndSize(paths + j, i - j));
            if (tmp != 0) {
                return NULL;
            }
            j = i + 1;
        }
    }
    while (paths[i++]);

    return list;
}

static PyObject *
sass_Options_get_image_path(sass_OptionsObject *self, void *closure)
{
    PyObject *string;
    string = PyString_FromString(self->options.image_path);
    Py_INCREF(string);
    return string;
}

static PyGetSetDef sass_Options_getset[] = {
    {"include_paths", (getter) sass_Options_get_include_paths, NULL,
     "The list of paths to include."},
    {"image_path", (getter) sass_Options_get_image_path, NULL,
     "The path to find images."},
    {NULL}
};

static PyTypeObject sass_OptionsType = {
    PyObject_HEAD_INIT(NULL)
    .ob_size = 0,
    .tp_name = "sass.Options",
    .tp_basicsize = sizeof(sass_OptionsObject),
    .tp_itemsize = 0,
    .tp_dealloc = (destructor) sass_Options_dealloc,
    .tp_print = 0,
    .tp_getattr = 0,
    .tp_setattr = 0,
    .tp_compare = 0,
    .tp_repr = 0,
    .tp_as_number = 0,
    .tp_as_sequence = 0,
    .tp_as_mapping = 0,
    .tp_hash = 0,
    .tp_call = 0,
    .tp_str = 0,
    .tp_getattro = 0,
    .tp_setattro = 0,
    .tp_as_buffer = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_doc = "The object which contains compilation options.",
    .tp_traverse = 0,
    .tp_clear = 0,
    .tp_richcompare = 0,
    .tp_weaklistoffset = 0,
    .tp_iter = 0,
    .tp_iternext = 0,
    .tp_methods = 0,
    .tp_members = 0,
    .tp_getset = sass_Options_getset,
    .tp_base = 0,
    .tp_dict = 0,
    .tp_descr_get = 0,
    .tp_descr_set = 0,
    .tp_dictoffset = 0,
    .tp_init = (initproc) sass_Options_init,
    .tp_alloc = 0,
    .tp_new = 0
};

static PyMethodDef sass_methods[] = {
    {NULL}
};

PyMODINIT_FUNC
initsass()
{
    PyObject *module;

    sass_OptionsType.tp_new = PyType_GenericNew;
    if (PyType_Ready(&sass_OptionsType) < 0) {
        return;
    }

    module = Py_InitModule3("sass", sass_methods,
                            "The thin binding of libsass for Python.");
    if (module == NULL) {
        return;
    }
    Py_INCREF(&sass_OptionsType);
    PyModule_AddObject(module, "Options", (PyObject *) &sass_OptionsType);
}
