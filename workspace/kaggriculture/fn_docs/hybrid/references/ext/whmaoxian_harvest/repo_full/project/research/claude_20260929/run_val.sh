cd /c/Users/ASUS/Documents/ChatGPT/kaggriculture/research/claude_20260929
: > results/val_progress.log
FIXSHOPS=1 ../../.venv/Scripts/python.exe surrogate.py MauoXX 31 cand/h9.py cand/rmA.py cand/rmB.py cand/rmC.py cand/fin_none.py cand/fin_26.py -- $(cat all244.txt) > results/surfix_val244.txt 2>&1
echo "old244 done $(date +%H:%M)" >> results/val_progress.log
../../.venv/Scripts/python.exe surrogate2.py upper.txt 31 val_upper cand/h9.py cand/rmA.py cand/rmB.py cand/rmC.py cand/fin_none.py cand/fin_26.py > results/sur2_val_upper.txt 2>&1
echo "upper done $(date +%H:%M)" >> results/val_progress.log
FIXSHOPS=1 ../../.venv/Scripts/python.exe surrogate.py MauoXX 31 cand/rmA.py cand/rmB.py cand/rmC.py cand/fin_none.py cand/fin_26.py -- $(cat r42have.txt) > results/surfix_val186.txt 2>&1
echo "ALLDONE $(date +%H:%M)" >> results/val_progress.log
