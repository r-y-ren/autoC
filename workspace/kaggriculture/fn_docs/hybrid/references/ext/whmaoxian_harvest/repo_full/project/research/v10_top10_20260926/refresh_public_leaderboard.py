"""Read public leaderboard metadata only; no credentials or submissions."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,requests
D=Path(__file__).resolve().parent
stamp=datetime.now(timezone.utc);tag=stamp.strftime('%Y%m%dT%H%M%SZ')
url='https://www.kaggle.com/api/i/competitions.LeaderboardService/GetLeaderboard'
response=requests.post(url,json={'competitionId':147734},timeout=40)
response.raise_for_status();raw=response.content
assert len(raw)<25000000,'Unexpectedly large metadata response'
data=json.loads(raw);teams={int(t['teamId']):t for t in data['teams']}
rows=[]
for row in data['publicLeaderboard'][:10]:
    team=teams[int(row['teamId'])]
    rows.append(dict(rank=row['rank'],team=team['teamName'],submission=row['submissionId'],display_score=row['displayScore']))
self_rows=[row for row in data['publicLeaderboard'] if int(row['teamId'])==16899200]
record=dict(captured_utc=stamp.isoformat(),source=url,response_sha256=hashlib.sha256(raw).hexdigest(),top10=rows,own_team_board_entries=self_rows,scope='Public displayed board entries, not identification of every uploaded version.')
(D/('public_board_'+tag+'.json')).write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
(D/'latest_public_board.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(record,ensure_ascii=False),flush=True)
