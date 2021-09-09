# Import the package to document:
import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import kalshi

# Automatically generate documentation pages
from gendocs import Generator
Generator().DocumentPackages(kalshi.Session)
