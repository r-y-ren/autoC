"""Run exactly one declared development manifest and exit."""
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import json,sys
D=Path(__file__).resolve().parent;R=D.parents[1]
sys.path.insert(0,str(R/'research/macro_population_20260927'))
import arena
if __name__=='__main__':
    manifest=Path(sys.argv[1]);output=Path(sys.argv[2])
    assert manifest.is_file() and manifest.is_relative_to(R/'research')
    assert output.is_relative_to(R/'research')
    jobs=json.loads(manifest.read_text());assert 0<len(jobs)<=20000
    with ProcessPoolExecutor(max_workers=6) as pool:
        arena.batch(pool,dict(manifest=str(manifest),output=str(output)))
    print('FINITE_BATCH_FINISHED',flush=True)
