"""Report isolated macro interventions separately from joint genomes."""
from pathlib import Path
import json
from report import summarize
from build_population import default
D=Path(__file__).resolve().parent
report=summarize('g1_results.jsonl')
assert report['rows']==1296
variants={v['path']:v for v in json.loads((D/'population_g1.json').read_text())}
output=[]
for group in report['groups']:
    if group['candidate'] not in variants:continue
    genome=variants[group['candidate']]['genome']
    changed={k:v for k,v in genome.items() if v!=default[k]}
    if len(changed)>1:continue
    item=dict(intervention=changed or {'control':'unchanged'},candidate=group['candidate'],
        invalid=group['invalid'],external_gain=group['external_gain'],
        direct=group['families']['r2'],economic_cases_changed=group['changed_economic_cases'],
        wage_delta_total=group['wage_delta_sum'],harvest_delta_total=group['harvest_delta_sum'],
        own_cash_delta_total=group['cash_delta_sum'])
    output.append(item)
(D/'g1_ablations.json').write_text(json.dumps(output,indent=2))
print(json.dumps(output),flush=True)
