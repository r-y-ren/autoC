import sys,collections,io,contextlib
import kaggle_environments.envs.kaggriculture.kaggriculture as K
LOST=collections.Counter();CALLS=[0]
_od=K._drop_inventories_to_shed
def dropx(private,cap):
    before=collections.Counter(private['shed'])
    for inv in private['inventories']:
        for k,v in inv.items(): before[k]+=v
    _od(private,cap)
    after=collections.Counter(private['shed'])
    for k in before:
        if before[k]>after[k]:
            LOST[(CALLS[0]%2,k)]+=before[k]-after[k]
            if CALLS[0]%2==0: print("day",CALLS[0]//2,k,before[k]-after[k],"shed_before",sum(private["shed"].values()))
    CALLS[0]+=1
K._drop_inventories_to_shed=dropx
from dbg import run
env=run(sys.argv[1],sys.argv[2],int(sys.argv[3]))
print('night overflow (seat0):',{k:v for (i,k),v in LOST.items() if i==0})
print('night overflow (seat1):',{k:v for (i,k),v in LOST.items() if i==1})
