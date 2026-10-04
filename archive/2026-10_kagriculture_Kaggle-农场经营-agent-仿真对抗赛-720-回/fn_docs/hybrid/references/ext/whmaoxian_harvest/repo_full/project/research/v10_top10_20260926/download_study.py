"""Download only validated public replay JSON, never executable code."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import gzip, hashlib, json, requests
ROOT=Path(__file__).resolve().parent

def download(episode):
    target=ROOT/'study_replays'/f'{episode}.json.gz'
    if target.exists():
        raw=gzip.decompress(target.read_bytes())
    else:
        url=f'https://www.kaggle.com/competitions/episodes/{episode}/replay.json'
        data=bytearray()
        with requests.get(url,stream=True,timeout=60) as response:
            response.raise_for_status()
            for chunk in response.iter_content(131072):
                data.extend(chunk)
                if len(data)>60000000:raise ValueError('Replay exceeds size limit')
        raw=bytes(data)
    game=json.loads(raw)
    assert game['info']['EpisodeId']==episode and len(game['steps'])==720
    target.parent.mkdir(exist_ok=True)
    if not target.exists():target.write_bytes(gzip.compress(raw,compresslevel=5))
    return dict(episode=episode,sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw))

if __name__=='__main__':
    split=json.loads((ROOT/'replay_split.json').read_text(encoding='utf-8'))
    with ThreadPoolExecutor(max_workers=3) as pool:receipts=list(pool.map(download,sorted({r['episode'] for r in split['study']})))
    (ROOT/'study_download_receipt.json').write_text(json.dumps(receipts,indent=2),encoding='utf-8')
    print(json.dumps(dict(downloaded=len(receipts))),flush=True)
