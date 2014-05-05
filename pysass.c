#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <Python.h>
#include "sass_interface.h"

#if PY_MAJOR_VERSION >= 3
#define PySass_IF_PY3(three, two) (three)
#define PySass_Int_FromLong(v) PyLong_FromLong(v)
#define PySass_Bytes_Check(o) PyBytes_Check(o)
#define PySass_Bytes_GET_SIZE(o) PyBytes_GET_SIZE(o)
#define PySass_Bytes_AS_STRING(o) PyBytes_AS_STRING(o)
#else
#define PySass_IF_PY3(three, two) (two)
#define PySass_Int_FromLong(v) PyInt_FromLong(v)
#define PySass_Bytes_Check(o) PyString_Check(o)
#define PySass_Bytes_GET_SIZE(o) PyString_GET_SIZE(o)
#define PySass_Bytes_AS_STRING(o) PyString_AS_STRING(o)
#endif

struct PySass_Pair {
    char *label;
    int value;
};

static struct PySass_Pair PySass_output_style_enum[] = {
    {"nested", SASS_STYLE_NESTED},
    {"expanded", SASS_STYLE_EXPANDED},
    {"compact", SASS_STYLE_COMPACT},
    {"compressed", SASS_STYLE_COMPRESSED},
    {NULL}
};

static struct PySass_Pair PySass_source_comments_enum[] = {
    {"none", SASS_SOURCE_COMMENTS_NONE},
    {"line_numbers", SASS_SOURCE_COMMENTS_DEFAULT},  /* alias of "default" */
    {"default", SASS_SOURCE_COMMENTS_DEFAULT},
    {"map", SASS_SOURCE_COMMENTS_MAP},
    {NULL}
};

static PyObject *
PySass_compile_string(PyObject *self, PyObject *args) {
    struct sass_context *context;
    char *string, *include_paths, *image_path;
    int output_style, source_comments;
    PyObject *result;

    if (!PyArg_ParseTuple(args,
                          PySass_IF_PY3("yiiyy", "siiss"),
                          &string, &output_style, &source_comments,
                          &include_paths, &image_path)) {
        return NULL;
    }

    context = sass_new_context();
    context->source_string = string;
    context->options.output_style = output_style;
    context->options.source_comments = source_comments;
    context->options.include_paths = include_paths;
    context->options.image_path = image_path;

    sass_compile(context);

    result = Py_BuildValue(
        PySass_IF_PY3("hy", "hs"),
        (short int) !context->error_status,
        context->error_status ? context->error_message : context->output_string
    );
    sass_free_context(context);
    return result;
}

static PyObject *
PySass_compile_filename(PyObject *self, PyObject *args) {
    struct sass_file_context *context;
    char *filename, *include_paths, *image_path;
    int output_style, source_comments, error_status;
    PyObject *source_map_filename, *result;

    if (!PyArg_ParseTuple(args,
                          PySass_IF_PY3("yiiyyO", "siissO"),
                          &filename, &output_style, &source_comments,
                          &include_paths, &image_path, &source_map_filename)) {
        return NULL;
    }

    context = sass_new_file_context();
    context->input_path = filename;
    if (source_comments == SASS_SOURCE_COMMENTS_MAP &&
        PySass_Bytes_Check(source_map_filename)) {
        size_t source_map_file_len = PySass_Bytes_GET_SIZE(source_map_filename);
        if (source_map_file_len) {
            char *source_map_file = malloc(source_map_file_len + 1);
            strncpy(
                source_map_file, 
                PySass_Bytes_AS_STRING(source_map_filename),
                source_map_file_len + 1
            );
            context->source_map_file = source_map_file;
        }
    }
    context->options.output_style = output_style;
    context->options.source_comments = source_comments;
    context->options.include_paths = include_paths;
    context->options.image_path = image_path;

    sass_compile_file(context);

    error_status = context->error_status;
    result = Py_BuildValue(
        PySass_IF_PY3("hyy", "hss"),
        (short int) !context->error_status,
        error_status ? context->error_message : context->output_string,
        error_status || context->source_map_string == NULL
            ? ""
            : context->source_map_string
    );
    sass_free_file_context(context);
    return result;
}

static PyObject *
PySass_compile_dirname(PyObject *self, PyObject *args) {
    struct sass_folder_context *context;
    char *search_path, *output_path, *include_paths, *image_path;
    int output_style, source_comments;
    PyObject *result;

    if (!PyArg_ParseTuple(args,
                          PySass_IF_PY3("yyiyy", "ssiss"),
                          &search_path, &output_path,
                          &output_style, &source_comments,
                          &include_paths, &image_path)) {
        return NULL;
    }

    context = sass_new_folder_context();
    context->search_path = search_path;
    context->output_path = output_path;
    context->options.output_style = output_style;
    context->options.source_comments = source_comments;
    context->options.include_paths = include_paths;
    context->options.image_path = image_path;

    sass_compile_folder(context);

    result = Py_BuildValue(
        PySass_IF_PY3("hy", "hs"),
        (short int) !context->error_status,
        context->error_status ? context->error_message : NULL
    );
    sass_free_folder_context(context);
    return result;
}

static PyMethodDef PySass_methods[] = {
    {"compile_string", PySass_compile_string, METH_VARARGS,
     "Compile a SASS string."},
    {"compile_filename", PySass_compile_filename, METH_VARARGS,
     "Compile a SASS file."},
    {"compile_dirname", PySass_compile_dirname, METH_VARARGS,
     "Compile several SASS files."},
    {NULL, NULL, 0, NULL}
};

static char PySass_doc[] = "The thin binding of libsass for Python.";

void PySass_make_enum_dict(PyObject *enum_dict, struct PySass_Pair *pairs) {
    size_t i;
    for (i = 0; pairs[i].label; ++i) {
        PyDict_SetItemString(
            enum_dict,
            pairs[i].label,
            PySass_Int_FromLong((long) pairs[i].value)
        );
    }
}

void PySass_init_module(PyObject *module) {
    PyObject *output_styles, *source_comments;
    output_styles = PyDict_New();
    PySass_make_enum_dict(output_styles, PySass_output_style_enum);
    PyModule_AddObject(module, "OUTPUT_STYLES", output_styles);
    source_comments = PyDict_New();
    PySass_make_enum_dict(source_comments, PySass_source_comments_enum);
    PyModule_AddObject(module, "SOURCE_COMMENTS", source_comments);
}

#if PY_MAJOR_VERSION >= 3

static struct PyModuleDef sassmodule = {
    PyModuleDef_HEAD_INIT,
    "_sass",
    PySass_doc,
    -1,
    PySass_methods
};

PyMODINIT_FUNC
PyInit__sass()
{
    PyObject *module = PyModule_Create(&sassmodule);
    if (module != NULL) {
        PySass_init_module(module);
    }
    return module;
}

#else

PyMODINIT_FUNC
init_sass()
{
    PyObject *module;
    module = Py_InitModule3("_sass", PySass_methods, PySass_doc);
    if (module != NULL) {
        PySass_init_module(module);
    }
}

#endif
