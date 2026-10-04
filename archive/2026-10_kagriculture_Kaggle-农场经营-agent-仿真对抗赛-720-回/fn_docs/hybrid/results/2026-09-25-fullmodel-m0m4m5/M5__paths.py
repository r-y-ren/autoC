import glob, sys, os
SOFTWARE = [p for p in glob.glob('/mnt/data/Code/autoC/workspace/*/software') if os.path.isdir(os.path.join(p, 'kaggle_simulations'))][0]
V48H = os.path.join(SOFTWARE, 'kaggle_simulations', 'v48_hybrid')
FNW_ROB = glob.glob('/mnt/data/Code/autoC/workspace/*/fn_work/src/run_official_bench')[0]
def setup():
    for p in (SOFTWARE, FNW_ROB):
        if p not in sys.path:
            sys.path.insert(0, p)
