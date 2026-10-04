"""Inspect bounded, strategy-only constants in the frozen local agent."""
from pathlib import Path
import contextlib,io,json,sys
D=Path(__file__).resolve().parent;R=D.parents[1]
sys.path.insert(0,str(R/'research/v10_rebuild_20260926'))
import fast_arena
entry=fast_arena.load('submissions/release_v10_r2/main.py')
prefixes=('_CS_','_HD2_','_Y_','_V9_HERD','_CA_','_RACE_','_T19_','_VE_','_VT_','_V233_')
values={}
for name,value in entry.__globals__.items():
    if name.startswith(prefixes) and isinstance(value,(str,int,float,bool)) and len(str(value))<180:
        values[name]=value
(D/'runtime_parameters.json').write_text(json.dumps(values,indent=2),encoding='utf-8')
print(json.dumps(values,indent=2),flush=True)
