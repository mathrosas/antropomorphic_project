## DO NOT MANUALLY INVOKE THIS setup.py — use catkin instead.
from catkin_pkg.python_setup import generate_distutils_setup
from setuptools import setup

# fetch values from package.xml
setup_args = generate_distutils_setup(
    packages=['antropomorphic_project'],   # <-- your Python package name
    package_dir={'': 'src'},               # modules live under src/
)

setup(**setup_args)