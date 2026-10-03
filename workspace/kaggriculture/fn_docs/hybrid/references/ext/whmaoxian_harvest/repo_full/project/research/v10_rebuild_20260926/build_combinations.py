"""Combine individually screened mechanisms for another adversarial round."""
from pathlib import Path
import hashlib,json
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
DEST=OUT/'combinations';DEST.mkdir(exist_ok=True)
base=(OUT/'generation2/h12_observed4.py').read_bytes()
template=(OUT/'opening_pressure_template.py.txt').read_text(encoding='utf-8')
profiles=[
 ('observed4_h24',{'_V10_ADV_HORIZON':24},None),
 ('observed1_h24',{'_V10_ADV_HORIZON':24,'_OR2_SN_K':1},None),
 ('observed8_h24',{'_V10_ADV_HORIZON':24,'_OR2_SN_K':8},None),
 ('observed4_h48',{'_V10_ADV_HORIZON':48},None),
 ('observed4_book',{'_ADV_BOOK':True,'_ADV_SUBTRACT_DEBTS':True},None),
 ('observed4_q8',{},(8,True,1)),
 ('observed4_q16',{},(16,True,1)),
 ('observed4_q24',{},(24,True,1)),
 ('observed4_q24last3',{},(24,False,3)),
 ('observed4_h24_q16',{'_V10_ADV_HORIZON':24},(16,True,1)),
]
records=[]
for name,settings,pressure in profiles:
    text='\n# Combination candidate; not an approved release.\n'+'\n'.join(f'{k}={v!r}' for k,v in settings.items())+'\n'
    if pressure:
        q,front,slots=pressure
        text+=template.replace('_R3_QUANTITY = 8',f'_R3_QUANTITY = {q}').replace('_R3_FRONT = True',f'_R3_FRONT = {front}').replace('_R3_SLOTS = 1',f'_R3_SLOTS = {slots}')
    raw=base+text.encode();compile(raw,name,'exec')
    path=DEST/(name+'.py');path.write_bytes(raw)
    records.append(dict(name=name,path=path.relative_to(ROOT).as_posix(),settings=settings,
                        opening_pressure=pressure,sha256=hashlib.sha256(raw).hexdigest()))
(OUT/'combination_manifest.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
print('Frozen combinations prepared',len(records),flush=True)
