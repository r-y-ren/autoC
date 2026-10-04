"""mkv.py out.py 'extra-dict' [switch]  -> hybrid with BEST overrides + extra"""
import sys,subprocess
from best_cfg import BEST,SWITCH
ov=dict(BEST); ov.update(eval(sys.argv[2]) if len(sys.argv)>2 else {})
sw=int(sys.argv[3]) if len(sys.argv)>3 else SWITCH
subprocess.run([sys.executable,'mk_hybrid.py',sys.argv[1],str(sw),repr(ov)],check=True)
