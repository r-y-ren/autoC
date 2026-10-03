"""Measure discarded inventory in the six declared development replays."""
from pathlib import Path
from collections import Counter
import json
import replay_economics as re
D=Path(__file__).resolve().parent;E=re.fa.engine
unit_original=E._apply_unit_action;day_original=E._end_of_day
stats={};events=[]
def total(private):
    result=Counter(private['shed'])
    for inv in private['inventories']:result.update(inv)
    return result

def unit(farm,private,idx,action,board_size,day,turns_per_day,shed_capacity=100):
    tracked=bool(action and action[0]=='DROP')
    before=total(private) if tracked else None
    result=unit_original(farm,private,idx,action,board_size,day,turns_per_day,shed_capacity)
    if tracked:
        loss=before-total(private)
        if loss:events.append(dict(kind='DROP',day=day,money=farm['money'],loss=dict(loss)))
    return result

def end_day(state,env,day):
    before=[total(s.observation.private) for s in state]
    result=day_original(state,env,day)
    for i,s in enumerate(state):
        loss=before[i]-total(s.observation.private)
        if loss:events.append(dict(kind='DAY_END',day=day,seat=i,loss=dict(loss)))
    return result

def tracked_unit(farm,private,idx,action,board_size,day,turns_per_day,shed_capacity=100):
    seat=farm_ids.setdefault(id(farm),len(farm_ids));assert seat<2
    start=len(events)
    result=unit(farm,private,idx,action,board_size,day,turns_per_day,shed_capacity)
    for event in events[start:]:event['seat']=seat
    return result

if __name__=='__main__':
    reports=[]
    try:
        E._apply_unit_action=tracked_unit;E._end_of_day=end_day
        for row in json.loads((re.SOURCE/'selection.json').read_text()):
            events=[];farm_ids={};result=re.audit(row)
            assert result['valid']
            loss=[Counter(),Counter()]
            for event in events:loss[event['seat']].update(event['loss'])
            reports.append(dict(episode=row['episode'],own_seat=row['seat'],loss=loss,events=events,exact_replay=True))
            print(json.dumps(dict(episode=row['episode'],loss=loss,events=len(events))),flush=True)
        (D/'warehouse_loss_audit.json').write_text(json.dumps(reports,indent=2),encoding='utf-8')
    finally:
        E._apply_unit_action=unit_original;E._end_of_day=day_original
