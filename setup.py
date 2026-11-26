from os import environ, path

from Cython.Build import cythonize
from setuptools import Extension, setup
from distutils.ccompiler import get_default_compiler

LIBCUE_SRC = ("cd.c", "cdtext.c", "rem.c", "time.c", "cue_parser.c", "cue_scanner.c")
LIBCUE_PATH = environ.get("LIBCUE_PATH", path.join("vendor", "libcue"))
LIMITED_API = bool(environ.get("PYLIBCUE_LIMITED_API"))

ext_options = {
    "sources": [path.join("pylibcue", "_cue.pyx"), *(path.join(LIBCUE_PATH, i) for i in LIBCUE_SRC)],
    "include_dirs": [LIBCUE_PATH],
    "define_macros": [("LIBCUE_QUIET_MODE", None)],
    "language": "c",
}

if get_default_compiler() != "msvc":
    ext_options["extra_compile_args"] = ["-fvisibility=hidden", "-g0"]

if LIMITED_API:
    ext_options["py_limited_api"] = True
    ext_options["define_macros"].append(("Py_LIMITED_API", 0x030B0000))

extensions = [Extension("pylibcue._cue", **ext_options)]

if LIMITED_API:
    setup(
        ext_modules=cythonize(extensions),
        options={"bdist_wheel": {"py_limited_api": "cp311"}, "build": {"build_base": "build/abi3"}},
    )
else:
    setup(ext_modules=cythonize(extensions), options={"build": {"build_base": "build/cpython"}})
