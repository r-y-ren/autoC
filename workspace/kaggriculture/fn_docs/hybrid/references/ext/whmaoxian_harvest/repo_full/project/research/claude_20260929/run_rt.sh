cd /c/Users/ASUS/Documents/ChatGPT/kaggriculture/research/claude_20260929
EPS=$(cat r42have.txt)
run() {
  B=$((B+1))
  FIXSHOPS=1 ../../.venv/Scripts/python.exe surrogate.py MauoXX 31 "$@" -- $EPS > "results/surfix_rt_b$B.txt" 2>&1
  echo "batch done $(date +%H:%M) $*" >> results/rt_progress.log
}
: > results/rt_progress.log
B=0
run cand/rt/rt105.py cand/rt/rt107.py cand/rt/rt103.py cand/rt/rt121.py cand/rt/rt101.py cand/rt/rt108.py cand/rt/rt123.py cand/rt/rt113.py cand/rt/rt118.py cand/rt/rt117.py
run cand/rt/rt104.py cand/rt/rt126.py cand/rt/rt109.py cand/rt/rt119.py cand/rt/rt125.py cand/rt/rt106.py cand/rt/rt110.py cand/rt/rt111.py cand/rt/rt112.py cand/rt/rt114.py
run cand/rt/rt115.py cand/rt/rt116.py cand/rt/rt120.py cand/rt/rt122.py cand/rt/rt124.py cand/rt/rt127.py cand/rt/rt128.py cand/rt/rt100.py cand/rt/rt9.py cand/rt/rt0.py
run cand/rt/rt1.py cand/rt/rt2.py cand/rt/rt3.py cand/rt/rt4.py cand/rt/rt5.py cand/rt/rt6.py cand/rt/rt7.py cand/rt/rt8.py cand/rt/rt10.py cand/rt/rt11.py cand/rt/rt12.py
echo ALLDONE >> results/rt_progress.log
