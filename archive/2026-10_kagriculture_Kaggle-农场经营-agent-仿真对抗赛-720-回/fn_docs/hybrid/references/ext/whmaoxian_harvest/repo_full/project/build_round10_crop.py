"""Create an isolated V10 candidate: reclaim idle labor for mature crop harvests.

Only changes the V9 slack layer. The released V9 bytes are never modified.
"""
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
source = ROOT / 'submissions/release_v9/main.py'
target = ROOT / 'experiments/round10_crop_slack.py'
assert hashlib.sha256(source.read_bytes()).hexdigest() == '6b13532fbc2b55b59c6cae8ed8d5cd29fe82d18a7d7e044ed130217e3d1c09d3'
text = source.read_text(encoding='utf-8')
needle = '''        if best is None:continue
        _,site,op,quantity=best;targets.add(site)'''
addition = '''        # A spare hand can save a mature crop or empty a full ongoing plant.
        # Native future harvest requests and workers' scheduled jobs are reserved.
        for y,row in enumerate(farm['tiles']):
            for x,tile in enumerate(row):
                if not isinstance(tile,dict) or tile.get('kind')!='PLANT':continue
                crop=tile.get('crop');units=int(tile.get('yield_units',0))
                if crop not in ('WHEAT','CARROT','TOMATO','STRAWBERRY','MELON') or units<=0:continue
                age=day-int(tile.get('planted_day',day))
                maxday={'WHEAT':4,'CARROT':3,'MELON':12}.get(crop)
                if maxday is not None:
                    ready=age>=maxday
                else:
                    ready=units>=4 or (0<=int(tile.get('max_lifespan_step',-1))<=step+24)
                # Recover a dying crop before the midnight unwatered refresh.
                if not ready and age>=({'WHEAT':2,'CARROT':2,'TOMATO':8,'STRAWBERRY':10,'MELON':10}[crop]):
                    ready=int(tile.get('consecutive_unwatered',0))>=1 and not tile.get('watered_today')
                if not ready or stock_total+units>85:continue
                site=(x,y)
                if (site,'HARVEST') in reserved or site in targets:continue
                distance=abs(pos[0]-x)+abs(pos[1]-y)
                if distance+1>23-step%24:continue
                price=int(obs['market']['prices'].get(crop,0))
                if price<2 and crop!='WHEAT':continue
                score=units*max(1,price)/(distance+1)
                if best is None or score>best[0]:best=(score,site,'HARVEST',units)
        if best is None:continue
        _,site,op,quantity=best;targets.add(site)'''
assert text.count(needle)==1
text=text.replace(needle,addition)
needle2="for item in ('MILK','WOOL','EGG','FERTILIZER'):"
assert text.count(needle2)==1
text=text.replace(needle2,"for item in ('MILK','WOOL','EGG','FERTILIZER','WHEAT','CARROT','TOMATO','STRAWBERRY','MELON'):")
needle3="for item in ('MILK','WOOL','EGG'):"
assert text.count(needle3)==1
text=text.replace(needle3,"for item in ('MILK','WOOL','EGG','CARROT','TOMATO','STRAWBERRY','MELON'):")
if target.exists():assert target.read_text(encoding='utf-8')==text
else:target.write_text(text,encoding='utf-8')
print(target.relative_to(ROOT),hashlib.sha256(target.read_bytes()).hexdigest())
