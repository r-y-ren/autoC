from pathlib import Path
import base64, gzip, hashlib, importlib.metadata, io, json, subprocess, sys, tarfile
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import Code, HTML, display
import html

ENGINE_VERSION = '1.32.7'
try:
    installed = importlib.metadata.version('kaggle-environments')
except importlib.metadata.PackageNotFoundError:
    installed = None
if installed != ENGINE_VERSION:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--quiet', '--progress-bar', 'off',
                           'kaggle-environments==' + ENGINE_VERSION])
assert importlib.metadata.version('kaggle-environments') == ENGINE_VERSION
print('Engine:', ENGINE_VERSION)
