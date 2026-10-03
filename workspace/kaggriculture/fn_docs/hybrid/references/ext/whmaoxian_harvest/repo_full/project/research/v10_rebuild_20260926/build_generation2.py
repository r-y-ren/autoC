"""Explicit behavioral ablations; every candidate and all failures are retained."""
from pathlib import Path
import hashlib,json
OUT=Path(__file__).resolve().parent; ROOT=OUT.parents[1]
DEST=OUT/'generation2'; DEST.mkdir(exist_ok=True)
v9=(ROOT/'submissions/release_v9/main.py').read_bytes()
v10=(ROOT/'submissions/release_v10/main.py').read_bytes()
opening=(OUT/'candidates/open_5.py').read_bytes()[len(v10):].decode()
ledger=v10.decode().split('# Align the inherited public-flow observer with the final executable sell list.')[1]
ledger='# Align the inherited public-flow observer with the final executable sell list.'+ledger
ledger=ledger.replace('_V10_LEDGER_PARENT = v10_pressure_agent','_V10_LEDGER_PARENT = round9_slack_agent')
profiles=[
 ('v9_safe','v9',{}), ('v9_ledger_safe','ledger',{}),
 ('h4','v10',{'_V10_ADV_HORIZON':4}),
 ('h8','v10',{'_V10_ADV_HORIZON':8}),
 ('h24','v10',{'_V10_ADV_HORIZON':24}),
 ('h48','v10',{'_V10_ADV_HORIZON':48}),
 ('h12_stock12','v10',{'_V10_ADV_THRESHOLD':12}),
 ('h24_stock12','v10',{'_V10_ADV_HORIZON':24,'_V10_ADV_THRESHOLD':12}),
 ('h12_book','v10',{'_ADV_BOOK':True,'_ADV_SUBTRACT_DEBTS':True}),
 ('h12_unprotected','v10',{'_ADV_PROTECT':False}),
 ('h12_observed4','v10',{'_OR2_SN_K':4}),
 ('h0','v10',{'_V10_ADV_HORIZON':0}),
]
records=[]
for name,base,settings in profiles:
    raw=v9 if base=='v9' else v9+ledger.encode() if base=='ledger' else v10
    parent='round9_slack_agent' if base=='v9' else 'v10_ledger_agent'
    wrapper=opening.replace('_R2_OPEN_PARENT = v10_ledger_agent',f'_R2_OPEN_PARENT = {parent}')
    changes='\n# Frozen generation-2 ablation parameters.\n'+'\n'.join(f'{k} = {v!r}' for k,v in settings.items())+'\n'
    result=raw+changes.encode()+wrapper.encode()
    compile(result,str(DEST/(name+'.py')),'exec')
    path=DEST/(name+'.py');path.write_bytes(result)
    records.append(dict(name=name,path=path.relative_to(ROOT).as_posix(),settings=settings,base=base,
                        sha256=hashlib.sha256(result).hexdigest()))
(OUT/'generation2_manifest.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
print('Generation 2 prepared',len(records),'frozen ablations',flush=True)
