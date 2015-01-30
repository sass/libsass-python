#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <Python.h>
#include "sass_context.h"

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

#ifdef __cplusplus
extern "C" {
#endif

struct PySass_Pair {
    char *label;
    int value;
};

static struct PySass_Pair PySass_output_style_enum[] = {
    {(char *) "nested", SASS_STYLE_NESTED},
    {(char *) "expanded", SASS_STYLE_EXPANDED},
    {(char *) "compact", SASS_STYLE_COMPACT},
    {(char *) "compressed", SASS_STYLE_COMPRESSED},
    {NULL}
};

static PyObject *
PySass_compile_string(PyObject *self, PyObject *args) {
    struct Sass_Context *ctx;
    struct Sass_Data_Context *context;
    struct Sass_Options *options;
    char *string, *include_paths, *image_path;
    const char *error_message, *output_string;
    Sass_Output_Style output_style;
    int source_comments, error_status, precision;
    PyObject *result;

    if (!PyArg_ParseTuple(args,
                          PySass_IF_PY3("yiiyyi", "siissi"),
                          &string, &output_style, &source_comments,
                          &include_paths, &image_path, &precision)) {
        return NULL;
    }

    context = sass_make_data_context(string);
    options = sass_data_context_get_options(context);
    sass_option_set_output_style(options, output_style);
    sass_option_set_source_comments(options, source_comments);
    sass_option_set_include_path(options, include_paths);
    sass_option_set_image_path(options, image_path);
    sass_option_set_precision(options, precision);

    sass_compile_data_context(context);

    ctx = sass_data_context_get_context(context);
    error_status = sass_context_get_error_status(ctx);
    error_message = sass_context_get_error_message(ctx);
    output_string = sass_context_get_output_string(ctx);
    result = Py_BuildValue(
        PySass_IF_PY3("hy", "hs"),
        (short int) !error_status,
        error_status ? error_message : output_string
    );
    sass_delete_data_context(context);
    return result;
}

static PyObject *
PySass_compile_filename(PyObject *self, PyObject *args) {
    struct Sass_Context *ctx;
    struct Sass_File_Context *context;
    struct Sass_Options *options;
    char *filename, *include_paths, *image_path;
    const char *error_message, *output_string, *source_map_string;
    Sass_Output_Style output_style;
    int source_comments, error_status, precision;
    PyObject *source_map_filename, *result;

    if (!PyArg_ParseTuple(args,
                          PySass_IF_PY3("yiiyyiO", "siissiO"),
                          &filename, &output_style, &source_comments,
                          &include_paths, &image_path, &precision, &source_map_filename)) {
        return NULL;
    }

    context = sass_make_file_context(filename);
    options = sass_file_context_get_options(context);

    if (source_comments && PySass_Bytes_Check(source_map_filename)) {
        size_t source_map_file_len = PySass_Bytes_GET_SIZE(source_map_filename);
        if (source_map_file_len) {
            char *source_map_file = (char *) malloc(source_map_file_len + 1);
            strncpy(
                source_map_file,
                PySass_Bytes_AS_STRING(source_map_filename),
                source_map_file_len + 1
            );
            sass_option_set_source_map_file(options, source_map_file);
        }
    }
    sass_option_set_output_style(options, output_style);
    sass_option_set_source_comments(options, source_comments);
    sass_option_set_include_path(options, include_paths);
    sass_option_set_image_path(options, image_path);
    sass_option_set_precision(options, precision);

    sass_compile_file_context(context);

    ctx = sass_file_context_get_context(context);
    error_status = sass_context_get_error_status(ctx);
    error_message = sass_context_get_error_message(ctx);
    output_string = sass_context_get_output_string(ctx);
    source_map_string = sass_context_get_source_map_string(ctx);
    result = Py_BuildValue(
        PySass_IF_PY3("hyy", "hss"),
        (short int) !error_status,
        error_status ? error_message : output_string,
        error_status || source_map_string == NULL ? "" : source_map_string
    );
    sass_delete_file_context(context);
    return result;
}

static PyMethodDef PySass_methods[] = {
    {"compile_string", PySass_compile_string, METH_VARARGS,
     "Compile a SASS string."},
    {"compile_filename", PySass_compile_filename, METH_VARARGS,
     "Compile a SASS file."},
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
    PyObject *output_styles;
    output_styles = PyDict_New();
    PySass_make_enum_dict(output_styles, PySass_output_style_enum);
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

#ifdef __cplusplus
}
#endif
