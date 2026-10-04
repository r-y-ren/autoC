"""Inspect the bounded endgame planner in the frozen R2 source."""
from pathlib import Path
import ast,json
D=Path(__file__).resolve().parent;R=D.parents[1]
text=(R/'submissions/release_v10_r2/main.py').read_text(encoding='utf-8')
results=[]
for scope,source in [('outer',text)]+[('literal_'+str(n.lineno),n.value) for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Constant) and isinstance(n.value,str) and 'plan_terminal' in n.value]:
    lines=source.splitlines()
    for i,line in enumerate(lines):
        if len(line)>1500:continue
        if any(word in line for word in ('plan_terminal(', 'max_simulations', 'proposals_per_actor')):
            results.append(dict(scope=scope,line=i+1,context='\n'.join(lines[max(0,i-3):min(len(lines),i+6)])))
for result in results:print(json.dumps(result),flush=True)
(D/'terminal_settings_inspection.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
