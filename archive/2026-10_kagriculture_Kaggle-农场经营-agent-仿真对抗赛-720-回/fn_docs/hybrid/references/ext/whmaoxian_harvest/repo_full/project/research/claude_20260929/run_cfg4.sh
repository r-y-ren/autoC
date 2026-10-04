cd /c/Users/ASUS/Documents/ChatGPT/kaggriculture/research/claude_20260929
A="hours=tuple(range(0,24))"
python mk_cfg.py cand/k17.py cand/combo2.py "_NGTX_CFG.update($A,margin=10)"
python mk_cfg.py cand/k18.py cand/combo2.py "_NGTX_CFG.update($A,margin=20)"
python mk_cfg.py cand/k19.py cand/combo2.py "_NGTX_CFG.update($A,margin=35)"
python mk_cfg.py cand/k20.py cand/combo2.py "_NGTX_CFG.update($A,margin=10,order=('FERTILIZER',))"
python mk_cfg.py cand/k21.py cand/combo2.py "_NGTX_CFG.update($A,margin=10,order=('FERTILIZER','WHEAT'))"
python mk_cfg.py cand/k22.py cand/combo2.py "_NGTX_CFG.update($A,margin=10,order=('WHEAT','FERTILIZER'))"
../../.venv/Scripts/python.exe surrogate.py MauoXX 30 cand/k17.py cand/k18.py cand/k19.py cand/k20.py cand/k21.py cand/k22.py -- $(awk '{print $1}' pool.txt) > results/sur_cfg4.txt 2>&1
tail -7 results/sur_cfg4.txt
