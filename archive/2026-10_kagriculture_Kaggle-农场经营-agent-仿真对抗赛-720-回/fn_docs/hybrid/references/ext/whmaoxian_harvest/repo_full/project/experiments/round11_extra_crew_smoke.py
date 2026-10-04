"""Full official-game physical smoke for the extra fertilizer crew."""
import contextlib
import hashlib
import io
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1193292362
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        from kaggle_environments import make
        from kaggle_environments.agent import get_last_callable
    paths = [ROOT / 'experiments/round11_extra_crew.py',
             ROOT / 'submissions/release_v9/main.py']
    entries = [get_last_callable(p.read_text(encoding='utf-8'), path=str(p)) for p in paths]
    env = make('kaggriculture', configuration={'seed':seed, 'episodeSteps':720}, debug=True)
    env.run(entries)
    hires = []
    fertilized = []
    for step in range(264, 696):
        before = env.steps[step][0].observation
        after = env.steps[step+1][0].observation
        action = env.steps[step][0].action
        native_action = env.steps[step][1].action
        if len(before.farms[0]['hands']) < len(after.farms[0]['hands']) and (
                len(after.farms[0]['hands']) > len(after.farms[1]['hands'])):
            hires.append({'step':step,'own_hands':len(after.farms[0]['hands']),
                          'v9_hands':len(after.farms[1]['hands']),
                          'own_market':action.get('market',[])})
        hands = before.farms[0]['hands']
        if not hands or len(action.get('hands',[])) < len(hands):
            continue
        if action['hands'][len(hands)-1] != ['FERTILIZE']:
            continue
        x,y = hands[-1]
        tile = before.farms[0]['tiles'][y][x]
        next_tile = after.farms[0]['tiles'][y][x]
        if not isinstance(tile,dict) or tile.get('crop') not in ('STRAWBERRY','TOMATO'):
            continue
        day = step//24
        end_pre = env.steps[day*24+23][0].observation.farms[0]['tiles'][y][x]
        dawn = env.steps[(day+1)*24][0].observation.farms[0]['tiles'][y][x]
        rival_pre = env.steps[day*24+23][1].observation.farms[1]['tiles'][y][x]
        rival_dawn = env.steps[(day+1)*24][1].observation.farms[1]['tiles'][y][x]
        fertilized.append({
            'step':step,'day':day,'site':[x,y],'crop':tile['crop'],
            'before_until':tile['fertilized_until_day'],
            'after_until':next_tile.get('fertilized_until_day') if isinstance(next_tile,dict) else None,
            'before_watered':tile['watered_today'],
            'night_own_yield_before':end_pre.get('yield_units') if isinstance(end_pre,dict) else None,
            'dawn_own_yield':dawn.get('yield_units') if isinstance(dawn,dict) else None,
            'night_v9_yield_before':rival_pre.get('yield_units') if isinstance(rival_pre,dict) else None,
            'dawn_v9_yield':rival_dawn.get('yield_units') if isinstance(rival_dawn,dict) else None,
            'v9_same_site_kind':rival_dawn.get('crop') if isinstance(rival_dawn,dict) else None,
            'v9_action_at_step':native_action.get('hands',[])[:2],
        })
    sys.path.insert(0,str(ROOT/'research/round10'))
    from quantify_top_gap import digest_game
    game=env.toJSON()
    game.setdefault('info',{})['EpisodeId']=-seed
    ledgers=[digest_game(game,seat,kind) for seat,kind in ((0,'candidate'),(1,'V9'))]
    cash_products=('STRAWBERRY','TOMATO')
    actual_sales={}
    for ledger in ledgers:
        actual_sales[ledger['identity']]={stage:{p:{'units':ledger['stages'][stage]['sales_units_by_product'].get(p,0),
                                                     'revenue':ledger['stages'][stage]['sales_revenue_by_product'].get(p,0)}
                                              for p in cash_products}
                                          for stage in ('11-15','16-20','21-25','26-29')}
    errors=[str(x.get('stderr'))[:400] for row in env.logs for x in row
            if isinstance(x,dict) and x.get('stderr','').strip()]
    result={'seed':seed,'source_sha256':hashlib.sha256(paths[0].read_bytes()).hexdigest(),
            'entry':entries[0].__name__,'states':len(env.steps),
            'statuses':[x.status for x in env.steps[-1]],'errors':errors[:5],
            'money':[env.steps[-1][i].observation.farms[i]['money'] for i in (0,1)],
            'telemetry':dict(entries[0].telemetry),'extra_hires':hires,
            'fertilized':fertilized,'executed_crop_sales':actual_sales}
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
