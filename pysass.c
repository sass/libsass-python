#include <unistd.h>
#include <Python.h>
#include "sass_interface.h"

#if PY_MAJOR_VERSION >= 3
#define PySass_IF_PY3(three, two) (three)
#define PySass_Int_FromLong(v) PyLong_FromLong(v)
#else
#define PySass_IF_PY3(three, two) (two)
#define PySass_Int_FromLong(v) PyInt_FromLong(v)
#endif

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

static PyObject *
PySass_compile_string(PyObject *self, PyObject *args) {
    struct sass_context *context;
    char *string, *include_paths, *image_path;
    int output_style;
    PyObject *result;

    if (!PyArg_ParseTuple(args,
                          PySass_IF_PY3("yiyy", "siss"),
                          &string, &output_style,
                          &include_paths, &image_path)) {
        return NULL;
    }

    context = sass_new_context();
    context->source_string = string;
    context->options.output_style = output_style;
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
    int output_style;
    PyObject *result;

    if (!PyArg_ParseTuple(args,
                          PySass_IF_PY3("yiyy", "siss"),
                          &filename, &output_style,
                          &include_paths, &image_path)) {
        return NULL;
    }

    context = sass_new_file_context();
    context->input_path = filename;
    context->options.output_style = output_style;
    context->options.include_paths = include_paths;
    context->options.image_path = image_path;

    sass_compile_file(context);

    result = Py_BuildValue(
        PySass_IF_PY3("hy", "hs"),
        (short int) !context->error_status,
        context->error_status ? context->error_message : context->output_string
    );
    sass_free_file_context(context);
    return result;
}

static PyObject *
PySass_compile_dirname(PyObject *self, PyObject *args) {
    struct sass_folder_context *context;
    char *search_path, *output_path, *include_paths, *image_path;
    int output_style;
    PyObject *result;

    if (!PyArg_ParseTuple(args,
                          PySass_IF_PY3("yyiyy", "ssiss"),
                          &search_path, &output_path, &output_style,
                          &include_paths, &image_path)) {
        return NULL;
    }

    context = sass_new_folder_context();
    context->search_path = search_path;
    context->output_path = output_path;
    context->options.output_style = output_style;
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

void PySass_init_module(PyObject *module) {
    PyObject *output_styles;
    size_t i = 0;
    output_styles = PyDict_New();
    for (i = 0; PySass_output_style_enum[i].label; ++i) {
        PyDict_SetItemString(
            output_styles,
            PySass_output_style_enum[i].label,
            PySass_Int_FromLong((long) PySass_output_style_enum[i].value)
        );
    }
    PyModule_AddObject(module, "OUTPUT_STYLES", output_styles);
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
