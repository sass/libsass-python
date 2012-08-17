#include <Python.h>
#include "sass_interface.h"

static struct {
    char *label;
    int value;
} PySass_output_style_enum[] = {
    {"nested", SASS_STYLE_NESTED},
    {"expanded", SASS_STYLE_EXPANDED},
    {"compact", SASS_STYLE_COMPACT},
    {"compressed", SASS_STYLE_COMPRESSED},
    {NULL}
};

static PyObject *PySass_CompileError;

static PyObject *
PySass_compile(PyObject *self, PyObject *args, PyObject *kwds)
{
    PyObject *string, *filename, *dirname, *search_path, *output_path,
             *output_style, *include_paths, *image_path,
             *result, *item;
    int expected_kwds, output_style_v;
    char *include_paths_v, *image_path_v, *item_buffer;
    Py_ssize_t include_paths_num, include_paths_size, i, offset, item_size;
    union {
        struct sass_context *string;
        struct sass_file_context *filename;
        struct sass_folder_context *dirname;
    } context;

    if (PyTuple_Size(args)) {
        PyErr_SetString(PyExc_TypeError, "compile() takes only keywords");
        return NULL;
    }
    if (PyDict_Size(kwds) < 1) {
        PyErr_SetString(PyExc_TypeError,
                        "compile() requires one of string, filename, or "
                        "dirname");
        return NULL;
    }

    expected_kwds = 1;
    string = PyDict_GetItemString(kwds, "string");
    filename = PyDict_GetItemString(kwds, "filename");
    dirname = PyDict_GetItemString(kwds, "dirname");

    if (string == NULL && filename == NULL && dirname == NULL) {
        PyErr_SetString(PyExc_TypeError,
                        "compile() requires one of string, filename, or "
                        "dirname");
        return NULL;
    }
    if (string != NULL && !(filename == NULL && dirname == NULL) ||
        filename != NULL && !(string == NULL && dirname == NULL) ||
        dirname != NULL && !(string == NULL && filename == NULL)) {
        PyErr_SetString(PyExc_TypeError,
                        "string, filename, and dirname arguments are "
                        "exclusive for each other.  use only one at a time");
        return NULL;
    }

    output_style = PyDict_GetItemString(kwds, "output_style");
    include_paths = PyDict_GetItemString(kwds, "include_paths");
    image_path = PyDict_GetItemString(kwds, "image_path");

    if (output_style == NULL || output_style == Py_None) {
        output_style_v = SASS_STYLE_NESTED;
    }
    else if (PyString_Check(output_style)) {
        item_size = PyString_Size(output_style);
        if (item_size) {
            for (i = 0; PySass_output_style_enum[i].label; ++i) {
                if (0 == strncmp(PyString_AsString(output_style),
                                 PySass_output_style_enum[i].label,
                                 item_size)) {
                    output_style_v = PySass_output_style_enum[i].value;
                    break;
                }
            }
        }
        if (PySass_output_style_enum[i].label == NULL) {
            PyErr_SetString(PyExc_ValueError, "invalid output_style option");
            return NULL;
        }
        ++expected_kwds;
    }
    else {
        PyErr_SetString(PyExc_TypeError, "output_style must be a string");
        return NULL;
    }

    if (include_paths == NULL || include_paths == Py_None) {
        include_paths_v = "";
    }
    else if (PyString_Check(include_paths)) {
        include_paths_v = PyString_AsString(include_paths);
        ++expected_kwds;
    }
    else if (PySequence_Check(include_paths)) {
        include_paths_num = PySequence_Size(include_paths);
        include_paths_size = 0;
        for (i = 0; i < include_paths_num; ++i) {
            item = PySequence_GetItem(include_paths, i);
            if (item == NULL) {
                return NULL;
            }
            if (!PyString_Check(item)) {
                PyErr_Format(PyExc_TypeError,
                             "include_paths must consists of only strings, "
                             "but #%zd is not a string", i);
                return NULL;
            }
            include_paths_size += PyString_Size(item);
        }
        // add glue chars
        if (include_paths_num > 1) {
            include_paths_size += include_paths_num - 1;
        }
        include_paths_v = malloc(sizeof(char) * (include_paths_size + 1));
        // join
        offset = 0;
        for (i = 0; i < include_paths_num; ++i) {
            if (i) {
                include_paths_v[offset] = ':';
                ++offset;
            }
            item = PySequence_GetItem(include_paths, i);
            PyString_AsStringAndSize(item, &item_buffer, &item_size);
            strncpy(include_paths_v + offset, item_buffer, item_size);
            offset += item_size;
        }
        include_paths_v[include_paths_size] = '\0';
    }
    else {
        PyErr_SetString(PyExc_TypeError,
                        "include_paths must be a list or a colon-separated "
                        "string");
        return NULL;
    }

    if (image_path == NULL || image_path == Py_None) {
        image_path_v = ".";
    }
    else if (PyString_Check(image_path)) {
        image_path_v = PyString_AsString(image_path);
        ++expected_kwds;
    }
    else {
        PyErr_SetString(PyExc_TypeError, "image_path must be a string");
        return NULL;
    }

    if (string) {
        if (!PyString_Check(string)) {
            PyErr_SetString(PyExc_TypeError, "string must be a string");
            result = NULL;
            goto finalize;
        }

        context.string = sass_new_context();
        context.string->source_string = PyString_AsString(string);
        context.string->options.output_style = output_style_v;
        context.string->options.include_paths = include_paths_v;
        context.string->options.image_path = image_path_v;

        sass_compile(context.string);

        if (context.string->error_status) {
            PyErr_SetString(PySass_CompileError, context.string->error_message);
            result = NULL;
            goto finalize_string;
        }

        result = PyString_FromString(context.string->output_string);

finalize_string:
        sass_free_context(context.string);
        goto finalize;
    }
    else if (filename) {
        if (!PyString_Check(filename)) {
            PyErr_SetString(PyExc_TypeError, "filename must be a string");
            result = NULL;
            goto finalize;
        }
        context.filename = sass_new_file_context();
        context.filename->input_path = PyString_AsString(filename);
        context.filename->options.output_style = output_style_v;
        context.filename->options.include_paths = include_paths_v;
        context.filename->options.image_path = image_path_v;

        sass_compile_file(context.filename);

        if (context.filename->error_status) {
            PyErr_SetString(PySass_CompileError,
                            context.filename->error_message);
            result = NULL;
            goto finalize_filename;
        }

        result = PyString_FromString(context.filename->output_string);

finalize_filename:
        sass_free_file_context(context.filename);
        goto finalize;
    }
    else if (dirname) {
        if (!PySequence_Check(dirname) || PySequence_Size(dirname) != 2) {
            PyErr_SetString(
                PySequence_Check(dirname) ? PyExc_ValueError: PyExc_TypeError,
                "dirname must be a (search_path, output_path) pair"
            );
            result = NULL;
            goto finalize;
        }

        search_path = PySequence_GetItem(dirname, 0);
        output_path = PySequence_GetItem(dirname, 1);

        context.dirname = sass_new_folder_context();
        context.dirname->search_path = PyString_AsString(search_path);
        context.dirname->output_path = PyString_AsString(output_path);
        context.dirname->options.output_style = output_style_v;
        context.dirname->options.include_paths = include_paths_v;
        context.dirname->options.image_path = image_path_v;

        sass_compile_folder(context.dirname);

        if (context.dirname->error_status) {
            PyErr_SetString(PySass_CompileError,
                            context.dirname->error_message);
            result = NULL;
            goto finalize_dirname;
        }

        result = Py_None;

finalize_dirname:
        sass_free_folder_context(context.dirname);
        goto finalize;
    }
    else {
        PyErr_SetString(PyExc_RuntimeError, "something went wrong");
        goto finalize;
    }

finalize:
    if (include_paths != NULL && PySequence_Check(include_paths)) {
        free(include_paths_v);
    }
    return result;
}

static PyMethodDef PySass_methods[] = {
    {"compile", PySass_compile, METH_KEYWORDS, "Compile a SASS source."},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
initsass()
{
    PyObject *module, *version;

    module = Py_InitModule3("sass", PySass_methods,
                            "The thin binding of libsass for Python.");
    if (module == NULL) {
        return;
    }
#ifdef LIBSASS_PYTHON_VERSION
    version = PyString_FromString(LIBSASS_PYTHON_VERSION);
#else
    version = PyString_FromString("unknown");
#endif
    PyModule_AddObject(module, "__version__", version);
    PySass_CompileError = PyErr_NewException("sass.CompileError",
                                             PyExc_ValueError,
                                             NULL);
    Py_INCREF(PySass_CompileError);
    PyModule_AddObject(module, "CompileError", PySass_CompileError);
}
