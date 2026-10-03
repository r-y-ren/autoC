import requests, time, json
URL = 'https://www.kaggle.com/api/i/competitions.EpisodeService/ListEpisodes'


def q(sid):
    while True:
        r = requests.post(URL, json={'submissionId': sid}, timeout=60)
        if r.status_code == 429:
            time.sleep(180)
            continue
        return r.json()


for sid in range(56674896, 56674600, -1):
    d = q(sid)
    for s in d.get('submissions', []):
        if s['id'] == sid and s['teamId'] == 16899200:
            json.dump(d, open(f'eplists/{sid}.json', 'w'))
            print('FOUND', sid, s, len(d.get('episodes', [])), flush=True)
            raise SystemExit
    print('no', sid, flush=True)
    time.sleep(4)
