import json,requests
from datetime import datetime,timezone
url='https://www.kaggle.com/api/i/competitions.LeaderboardService/GetLeaderboard'
import os
if os.path.exists("board_raw.json") and os.environ.get("CACHE"):
    data=json.load(open("board_raw.json",encoding="utf-8"))
else:
    r=requests.post(url,json={"competitionId":147734},timeout=60);r.raise_for_status();data=r.json()
open('board_raw.json','w',encoding='utf-8').write(json.dumps(data))
teams={int(t['teamId']):t for t in data['teams']}
lb=data['publicLeaderboard']
print('captured',datetime.now(timezone.utc).isoformat(),'entries',len(lb))
for row in lb[:40]:
    print(row['rank'],row['displayScore'],teams[int(row['teamId'])]['teamName'],row['submissionId'])
own=[r for r in lb if int(r['teamId'])==16899200]
print('OWN',own)
import collections
sc=[float(r['displayScore']) for r in lb if r.get('displayScore')]
for t in (3000,2900,2800,2700,2600,2500,2400,2200,2000):
    print('>=',t,sum(s>=t for s in sc))
