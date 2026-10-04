"""Build isolated candidates, leaving both historical releases unchanged."""
from pathlib import Path
import hashlib, json
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent/'candidates'
OUT.mkdir(exist_ok=True)
base = (ROOT/'submissions/release_v10/main.py').read_bytes()
assert hashlib.sha256(base).hexdigest() == '3a4601081cc909ae7baf97ec5ddb0e1a8a5a1a27c9cd072cdeaaf7d34c803e0b'
manifest=[]
for buy in (5,6,8,10,15,20,30):
    tail = f'''
# V10 revision study: equal net grain, different opening transaction size.
_R2_OPEN_PARENT = v10_ledger_agent
_R2_OPEN_BUY = {buy}
def r2_opening_agent(observation, configuration=None):
    action = _R2_OPEN_PARENT(observation, configuration)
    if int(observation['step']) == 0:
        orders = action.get('market', [])
        if orders[:2] == [['BUY_PRODUCT','WHEAT',20],['SELL','WHEAT',15]]:
            opening = [['BUY_PRODUCT','WHEAT',_R2_OPEN_BUY]]
            if _R2_OPEN_BUY > 5: opening.append(['SELL','WHEAT',_R2_OPEN_BUY-5])
            action = dict(action, market=opening+orders[2:])
    return action
agent = r2_opening_agent
kaggle_submission_agent = r2_opening_agent
'''
    data=base+tail.encode(); compile(data, 'opening.py', 'exec')
    dest=OUT/f'open_{buy}.py'; dest.write_bytes(data)
    manifest.append(dict(path=dest.relative_to(ROOT).as_posix(),buy=buy,sha256=hashlib.sha256(data).hexdigest()))
(OUT/'opening_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
