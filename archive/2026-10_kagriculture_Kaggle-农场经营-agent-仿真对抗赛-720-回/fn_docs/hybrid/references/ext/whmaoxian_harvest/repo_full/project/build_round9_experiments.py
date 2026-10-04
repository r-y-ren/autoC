"""Reconstruct Round9 experimental sources without changing any frozen bytes."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
base_path=ROOT/'submissions/release_v8/main.py'
assert hashlib.sha256(base_path.read_bytes()).hexdigest()=='9fa83701138e80e3e5f9a6479cc2fa1c7e8a8965c4bd85d4e45d05ec5d4ffd4e'
base=base_path.read_text(encoding='utf-8')
def suffix(name):return (ROOT/f'experiments/round9_{name}_suffix.txt').read_text(encoding='utf-8')
market=base+suffix('final_market')
combined=market+'\n_CXD_FROM=720\n_ADV_LOOK=4\n_ADV_TO=718\n'
herd=suffix('herd');market_herd=combined+herd.replace('_R9H_PARENT=round8_production_fusion_agent','_R9H_PARENT=round9_final_market_agent')
variants={'final_market':market,'final_market4':market+'\n_ADV_LOOK=4\n','nocxd':base+'\n_CXD_FROM=720\n',
'market_combined':combined,'herd':base+herd,'market_herd':market_herd,'herd_margin':market_herd+suffix('herd_margin'),
'market_slack':combined+suffix('slack'),'herd_contract':market_herd+suffix('herd_margin')+suffix('herd_contract')}
manifest={}
for name,text in variants.items():
 path=ROOT/f'experiments/round9_{name}.py'
 if path.exists():assert path.read_text(encoding='utf-8')==text,f'Frozen source differs: {path}'
 else:path.write_text(text,encoding='utf-8')
 manifest[name]={'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size}
(ROOT/'research/round9/build_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(manifest,indent=2))
