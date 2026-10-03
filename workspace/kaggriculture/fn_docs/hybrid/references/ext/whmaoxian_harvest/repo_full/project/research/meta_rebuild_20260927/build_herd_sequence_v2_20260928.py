"""Permit the next herd purchase once the prior placement is visibly confirmed."""
from pathlib import Path
import runpy
D=Path(__file__).resolve().parent
old=(D/'herd_sequence_20260928.txt').read_text()
needle="        if state and not state.get('broken') and not state.get('pending'):"
replacement="""        pending_ok=True
        if state:
            farm=observation['farms'][seat]
            for x,y,day in state.get('pending',[]):
                tile=farm['tiles'][y][x]
                pending_ok=pending_ok and isinstance(tile,dict) and tile.get('animal')=='SHEEP' and tile.get('placed_day')==day
        if state and not state.get('broken') and pending_ok:"""
assert old.count(needle)==1
new=old.replace(needle,replacement)
target=D/'herd_sequence_v2_20260928.txt'
if target.exists():assert target.read_text()==new
else:target.write_text(new)
build=(D/'build_herd_sequence_20260928.py').read_text()
build=build.replace('herd_sequence_20260928.txt','herd_sequence_v2_20260928.txt')
build=build.replace("('sequence_'+name+'.py')","('sequence_v2_'+name+'.py')")
build=build.replace('herd_sequence_design.json','herd_sequence_v2_design.json').replace('herd_sequence_jobs.json','herd_sequence_v2_jobs.json')
p=D/'_generated_sequence_v2_builder.py'
if p.exists():assert p.read_text()==build
else:p.write_text(build)
runpy.run_path(str(p),run_name='__main__')
