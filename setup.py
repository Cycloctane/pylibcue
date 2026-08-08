from os import environ, path

from Cython.Build import cythonize
from setuptools import Extension, setup
from distutils.ccompiler import get_default_compiler

LIBCUE_SRC = ("cd.c", "cdtext.c", "rem.c", "time.c", "cue_parser.c", "cue_scanner.c")
LIBCUE_PATH = environ.get("LIBCUE_PATH", path.join("vendor", "libcue"))

extensions = [
    Extension(
        "pylibcue._cue",
        [path.join("pylibcue", "_cue.pyx"), *(path.join(LIBCUE_PATH, i) for i in LIBCUE_SRC)],
        include_dirs=[LIBCUE_PATH],
        define_macros=[("LIBCUE_QUIET_MODE", None), ("Py_LIMITED_API", 0x030A0000)],
        extra_compile_args=(
            ["-fvisibility=hidden", "-g0"] if get_default_compiler() != "msvc" else []
        ),
        py_limited_api=True,
        language="c",
    )
]

setup(ext_modules=cythonize(extensions), options={"bdist_wheel": {"py_limited_api": "cp310"}},)
