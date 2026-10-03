#!/bin/sh
# usage: build.sh out.py [python-dict-overrides]
out=$1; shift
cat engine/farm.py engine/p2_plan.py engine/p3_tasks.py engine/p4_units.py engine/p5_market.py engine/p6_blueprint.py > "$out"
if [ -n "$1" ]; then printf '\nOVERRIDES.update(%s)\n' "$1" >> "$out"; fi
