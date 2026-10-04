import sys,collections
import glog
seed=int(sys.argv[3]) if len(sys.argv)>3 else 1002
T0=int(sys.argv[4]) if len(sys.argv)>4 else 288
res={}
for a,b in ((sys.argv[1],sys.argv[2]),(sys.argv[2],sys.argv[2])):
    env,fin=glog.run(a,b,seed)
    agg=collections.defaultdict(lambda:[0,0])
    for t,p,op,it,pr in glog.LOG:
        if p==0 and t>=T0: agg[op+':'+it][0]+=1;agg[op+':'+it][1]+=pr
    res[a if a!=b else 'REF']=(fin,agg)
keys=sorted(set().union(*[set(v[1]) for v in res.values()]))
names=list(res)
print(' '*22,'  '.join(f'{n[-12:]:>22s}' for n in names))
for k in keys:
    print(f'{k:22s}','  '.join(f'{res[n][1][k][0]:6d} {res[n][1][k][1]:8d} ({res[n][1][k][1]/max(1,res[n][1][k][0]):5.1f})' for n in names))
print('final',[res[n][0] for n in names])
