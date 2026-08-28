import os
import sys

SOFTWARE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SOFTWARE_ROOT not in sys.path:
    sys.path.insert(0, SOFTWARE_ROOT)
