#!/usr/bin/env bash
# pull_renyxin.sh —— 拉我方计分对回放（C_final=56697824, S8=56708866）
# 2026-10-01 fingerprint-scan；kaggle CLI 2.2.4（官方 competitions replay 端点）
set -u
BASE=/mnt/data/Code/autoC/workspace/kaggriculture/fn_docs/hybrid/references/ext/fingerprint-scan
K=kaggle
cd "$BASE/raw/renyxin-replays"
pull () {
  local csv="$1" tag="$2"
  tail -n +2 "$csv" | cut -d, -f1 | while read -r id; do
    f="episode-$id-replay.json"
    if [ -s "$f" ]; then echo "skip $tag $id"; continue; fi
    if $K competitions replay "$id" >/dev/null 2>&1 && [ -s "$f" ]; then
      mv -f "$f" "$tag-$f" 2>/dev/null || true
      echo "ok $tag $id"
    else
      sleep 3
      if $K competitions replay "$id" >/dev/null 2>&1 && [ -s "$f" ]; then
        mv -f "$f" "$tag-$f" 2>/dev/null || true
        echo "ok2 $tag $id"
      else
        echo "FAIL $tag $id"
      fi
    fi
    sleep 1
  done
}
echo "start $(date -u +%FT%TZ)"
pull "$BASE/raw/episodes-Cfinal-56697824.csv" Cfinal
pull "$BASE/raw/episodes-S8-56708866.csv" S8
echo "end $(date -u +%FT%TZ)"
ls | wc -l
