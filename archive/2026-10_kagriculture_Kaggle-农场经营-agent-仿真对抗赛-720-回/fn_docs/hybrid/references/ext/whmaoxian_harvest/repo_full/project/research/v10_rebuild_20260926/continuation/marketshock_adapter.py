"""Evaluation-only binding of the public notebook's declared module.agent.
Original source is untouched; the last-callable heuristic selected a factory.
This adapter is local evaluation infrastructure, not a submission candidate.
"""
from pathlib import Path
import hashlib,runpy
_SOURCE=Path('C:/Users/ASUS/Documents/ChatGPT/kaggriculture/research/v10_rebuild_20260926/notebooks/extracted/marketshock/main.py')
assert hashlib.sha256(_SOURCE.read_bytes()).hexdigest()=='12ad317ecac6c07fb2c2e10bf4820ecd1fd4551a5a36aa0e34ab93b2c33c2693'
_MODULE=runpy.run_path(str(_SOURCE))
_ENTRY=_MODULE['agent']
_REPORTS={}
def marketshock_opponent(observation,configuration=None):
    action=_ENTRY(observation,configuration)
    _REPORTS.clear()
    for name,value in _ENTRY.__globals__.items():
        if isinstance(value,dict) and any(key in name.upper() for key in ('REPORT','STATS','DIAGNOSTIC')):
            _REPORTS[name]=value
        chassis=getattr(value,'chassis',None)
        if chassis is not None:
            _REPORTS[name+'.chassis']=getattr(chassis,'diagnostics',{})
    return action
marketshock_opponent.telemetry=_REPORTS
