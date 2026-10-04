"""Close finite Phase-C studies without overwriting the frozen Phase-B selection."""
from pathlib import Path
import datetime,hashlib,json
C=Path(__file__).resolve().parent;D=C.parent;W=D.parent;R=W.parents[1]
selection=json.loads((D/'phase_b/selection.json').read_text())
assert hashlib.sha256((R/selection['candidate']).read_bytes()).hexdigest()==selection['sha256']
counts={}
for name,expected in (('development',1744),('fresh_loss',27),('risk',976)):
    jobs=json.loads((C/f'{name}_jobs.json').read_text())
    ledger=C/f'{name}_results.jsonl'
    rows=[json.loads(line) for line in ledger.read_text(encoding='utf-8').splitlines()]
    assert len(jobs)==len(rows)==expected
    assert {r['id'] for r in rows}=={j['id'] for j in jobs}
    assert all(r.get('valid') for r in rows)
    counts[name]=dict(full_games=len(rows),invalid=0,ledger=ledger.relative_to(R).as_posix(),
                     sha256=hashlib.sha256(ledger.read_bytes()).hexdigest())
result=dict(decision='Retain the unchanged Phase-B candidate; reject all Phase-C additions for release.',
 retained_source=selection['candidate'],retained_sha256=selection['sha256'],
 recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),studies=counts,
 additional_full_games=sum(x['full_games'] for x in counts.values()),
 reasoning=['Readiness variants did not improve public-program win counts; restrictive variants worsened counter-policy results.',
 'Removing the layout gate increased known-loss flips but worsened recent fixed-trace wins from 11 to 9.',
 'Risk controls did not increase wins on public, counter, direct-reference or historical-loss panels; small coin changes are insufficient release evidence.',
 'The three newest fixed-loss probes reproduced old V10 exactly; the retained candidate flips two, but the remaining loss worsens.',
 'Phase-B independent validation remains frozen. These additional studies are development and diagnostics, not new independent validation.'])
(C/'study_decision.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result),flush=True)
