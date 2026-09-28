#!/usr/bin/env bash
set -u
K=/home/renyxin/.local/bin/kaggle
cd /tmp/r33audit
python3 - << 'EOF' > /tmp/kagr_root/replay_ids.txt
import json
meta=json.load(open("/tmp/kagr_root/meta_summary.json"))
ids=[]
for tag in ("r32","r33"):
    lst=json.load(open(f"/tmp/kagr_root/episodes-{tag}-{meta[tag]['ref']}.json"))
    ids += [str(e["id"]) for e in lst if "PUBLIC" in e.get("type","")]
print(" ".join(ids))
EOF
n=$(wc -w < /tmp/kagr_root/replay_ids.txt)
echo "start $(date -u +%FT%TZ) n_ids=$n"
fail=""
for id in $(cat /tmp/kagr_root/replay_ids.txt); do
  f="episode-$id-replay.json"
  if [ -s "$f" ]; then echo "skip $id"; continue; fi
  if $K competitions replay "$id" >/dev/null 2>&1 && [ -s "$f" ]; then
    echo "ok $id $(stat -c%s "$f")"
  else
    echo "RETRY $id"; sleep 5
    if $K competitions replay "$id" >/dev/null 2>&1 && [ -s "$f" ]; then echo "ok2 $id"
    else fail="$fail $id"; echo "FAIL $id"; fi
  fi
  sleep 1
done
echo "failures:$fail"
echo "end $(date -u +%FT%TZ)"
