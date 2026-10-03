"""Compare studied openings without simulating or opening held-out data."""
from collections import Counter
import gzip
import json
from pathlib import Path
OUT = Path(__file__).parent/'research/round7/top2'
rows = [r for r in json.loads((OUT/'index.json').read_text()) if r['split']=='study'] + json.loads((OUT/'study_extra_index.json').read_text())
games = [json.loads(gzip.decompress((OUT/f"{r['episode_id']}.json.gz").read_bytes())) for r in rows]

def action(g,r,t, mode='physical'):
    a = g['steps'][t+1][r['seat']]['action']
    ans = {'farmer':a['farmer'],'hands':a.get('hands',[])}
    if mode=='physical':
        ans['market'] = [o for o in a.get('market',[]) if o and o[0]!='SELL']
    return ans

def state(g,r,t):
    o = g['steps'][t][r['seat']]['observation']
    return o['farms'][r['seat']],o['private']

def describe_diff(i,j,t):
    a,b = action(games[i],rows[i],t), action(games[j],rows[j],t)
    fa,pa = state(games[i],rows[i],t)
    fb,pb = state(games[j],rows[j],t)
    diffs=[]
    for n,(aa,bb) in enumerate(zip([a['farmer']]+a['hands'],[b['farmer']]+b['hands'])):
        if aa==bb:
            continue
        posa=([fa['farmer']]+fa['hands'])[n]
        posb=([fb['farmer']]+fb['hands'])[n]
        diffs.append({'unit':n,'reference_action':aa,'candidate_action':bb,'reference_position':posa,'candidate_position':posb,'reference_tile':fa['tiles'][posa[1]][posa[0]],'candidate_tile':fb['tiles'][posb[1]][posb[0]],'reference_inventory':pa['inventories'][n],'candidate_inventory':pb['inventories'][n]})
    return {'turn':t,'reference':a,'candidate':b,'unit_differences':diffs,'reference_money':fa['money'],'candidate_money':fb['money'],'reference_seeds':pa['seeds'],'candidate_seeds':pb['seeds']}

results=[]
for j in range(1,len(rows)):
    first=next((t for t in range(719) if action(games[0],rows[0],t)!=action(games[j],rows[j],t)),719)
    unitfirst=next((t for t in range(719) if action(games[0],rows[0],t,'units')!=action(games[j],rows[j],t,'units')),719)
    mismatch=[t for t in range(72) if action(games[0],rows[0],t)!=action(games[j],rows[j],t)]
    results.append({'reference_episode':rows[0]['episode_id'],'episode_id':rows[j]['episode_id'],'team':rows[j]['team'],'first_difference':first,'first_units_difference':unitfirst,'different_turns_in_first72':mismatch,'first_difference_details':describe_diff(0,j,first) if first<719 else None})

states=[]
for t in [0,11,12,23,24,47,48,71,72,95,96,143,144]:
    physical,positions,tiles,kinds = [],[],[],[]
    for g,r in zip(games,rows):
        f,p=state(g,r,t)
        positions.append(json.dumps([f['farmer'],f['hands']]))
        # Crop identities and location; exclude random empty weeds only.
        cells = [[{k:v for k,v in tile.items() if k in ('kind','crop','animal','planted_day','placed_day')} if isinstance(tile,dict) and tile.get('kind')!='WEED' else None for tile in row] for row in f['tiles']]
        tiles.append(json.dumps(cells,sort_keys=True))
        kinds.append(dict(Counter(tile.get('crop') or tile.get('animal') or tile.get('kind') for row in f['tiles'] for tile in row if isinstance(tile,dict))))
    states.append({'turn':t,'unique_unit_positions':len(set(positions)),'unique_crop_structure_layouts':len(set(tiles)),'layouts_count':dict(Counter(tiles)),'crop_counts':kinds})

out={'study_games':len(rows),'reference':rows[0],'pairwise_to_reference':results,'state_convergence':states}
(OUT/'opening_comparison.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
for x in results:
    print(x['team'],x['episode_id'],'first',x['first_difference'],'units',x['first_units_difference'],'mismatch72',len(x['different_turns_in_first72']),flush=True)
print('convergence',[(x['turn'],x['unique_unit_positions'],x['unique_crop_structure_layouts']) for x in states])
