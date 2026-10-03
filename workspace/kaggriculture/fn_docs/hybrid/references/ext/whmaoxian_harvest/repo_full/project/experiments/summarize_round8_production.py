"""Read standard-game replays for confirmed yields, sales, spoilage and labor.

Reconstruct only one turn's unit actions with the official helper; no agent is
rerun and no outcome is generated. Tomatoes cannot be bought as products, so
observed storage plus SELL requests identifies executed sales exactly.
"""
import contextlib
import copy
import io
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
with contextlib.redirect_stdout(io.StringIO()):
    from kaggle_environments.envs.kaggriculture import kaggriculture as engine
rows=[]
for path in sorted((ROOT/'results').glob('round8_production_final_*-seed*-seat*-replay.json')):
    g=json.loads(path.read_text(encoding='utf-8'));seat=int(path.stem.split('-seat')[1].split('-')[0])
    players=[]
    for p in (0,1):
        daily={d:dict(day=d,planted=0,watered=0,fertilized=0,harvested=0,sold=0,unit_drop_loss=0,midnight_loss=0,hires=0,labor_cost=0) for d in range(18,30)}
        for t in range(432,719):
            obs=g['steps'][t][p]['observation'];nextobs=g['steps'][t+1][p]['observation'];day=t//24
            action=g['steps'][t+1][p]['action'];farm=copy.deepcopy(obs['farms'][p]);private=copy.deepcopy(obs['private'])
            positions=[farm['farmer'],*farm['hands']]
            initial=private['shed'].get('TOMATO',0)+sum(inv.get('TOMATO',0) for inv in private['inventories'])
            gained=0
            for actor,cmd in enumerate([action['farmer'],*action['hands']]):
                if actor>=len(positions):continue
                x,y=positions[actor];tile=farm['tiles'][y][x]
                if cmd==['PLANT','TOMATO'] and tile is None and private['seeds'].get('TOMATO',0):daily[day]['planted']+=1
                if isinstance(tile,dict) and tile.get('crop')=='TOMATO':
                    if cmd==['WATER'] and not tile.get('watered_today'):daily[day]['watered']+=1
                    if cmd==['FERTILIZE'] and private['inventories'][actor].get('FERTILIZER',0):daily[day]['fertilized']+=1
                    if cmd==['HARVEST'] and day-tile['planted_day']>=8:
                        gained+=tile['yield_units'];daily[day]['harvested']+=tile['yield_units']
                engine._apply_unit_action(farm,private,actor,cmd,10,day,24,100)
            in_units=sum(inv.get('TOMATO',0) for inv in private['inventories'])
            in_shed=private['shed'].get('TOMATO',0)
            daily[day]['unit_drop_loss']+=initial+gained-in_units-in_shed
            sold=0
            for order in action['market'][:10]:
                if len(order)>=3 and order[:2]==['SELL','TOMATO']:
                    qty=min(in_shed,max(0,int(order[2])));sold+=qty;in_shed-=qty
            daily[day]['sold']+=sold
            nextshed=nextobs['private']['shed'].get('TOMATO',0)
            if t%24==23:
                deposited=nextshed-in_shed
                assert 0<=deposited<=in_units,(path,t,p,deposited,in_units)
                daily[day]['midnight_loss']+=in_units-deposited
            else:assert nextshed==in_shed,(path,t,p,nextshed,in_shed)
            before=obs['farms'][p]['hires_today'];after=nextobs['farms'][p]['hires_today']
            if after>=before:
                daily[day]['hires']+=after-before
                daily[day]['labor_cost']+=sum(engine._fib(n) for n in range(before,after))
        final=g['steps'][-1][p]['observation'];tiles=[x for row in final['farms'][p]['tiles'] for x in row if isinstance(x,dict) and x.get('crop')=='TOMATO']
        summary={k:sum(d[k] for d in daily.values()) for k in ('planted','watered','fertilized','harvested','sold','unit_drop_loss','midnight_loss','hires','labor_cost')}
        summary.update(seat=p,live_tomatoes=len(tiles),unharvested=sum(x['yield_units'] for x in tiles),
                       carried=sum(inv.get('TOMATO',0) for inv in final['private']['inventories']),shed=final['private']['shed'].get('TOMATO',0),daily=list(daily.values()))
        players.append(summary)
    row={'seed':g['info']['seed'],'candidate_seat':seat,'players':players,
         'candidate_additional_actual_labor_cost':players[seat]['labor_cost']-players[1-seat]['labor_cost'],
         'bank_delta':g['steps'][-1][seat]['reward']-g['steps'][-1][1-seat]['reward']}
    rows.append(row)
(ROOT/'research/round8/production_standard_audit.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
for row in rows:
    print(json.dumps({k:v for k,v in row.items() if k!='players'}), [{k:v for k,v in p.items() if k!='daily'} for p in row['players']])
