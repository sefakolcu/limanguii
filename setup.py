from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(
        ["mar_gui.py"],
        language_level="3"  # Set language level explicitly
    ),
)