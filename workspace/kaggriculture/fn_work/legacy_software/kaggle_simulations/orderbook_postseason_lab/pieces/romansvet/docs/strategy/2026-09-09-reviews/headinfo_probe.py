import os, sys
os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, "/mnt/e/_work/kaggriculture3/.claude/worktrees/arms-next/src")
import numpy as np
from kagg3 import spec
from kagg3.core import brain
from kagg3.core import policy as PO

TH = "/mnt/e/_work/kaggriculture3/artifacts/kagg2_games/thetas/"

def obs(day, own, opp, money=18000, opp_money=17000, shed=None, nquad=2):
    def board(tiles):
        kind = np.full(spec.N_TILES, spec.KIND_EMPTY, np.int32)
        occ  = np.full(spec.N_TILES, -1, np.int32)
        td   = np.zeros(spec.N_TILES, np.int32); ty = np.zeros(spec.N_TILES, np.int32)
        for i,(k,o,d,y) in enumerate(tiles): kind[i],occ[i],td[i],ty[i]=k,o,d,y
        return kind,occ,td,ty
    k,o,td,ty = board(own); ok,oo,otd,oty = board(opp)
    sh = np.zeros(spec.N_ITEMS, np.int32) if shed is None else shed
    return brain.PolicyObs(day=np.int32(day), money=np.int32(money), opp_money=np.int32(opp_money),
        kind=k, occ=o, opp_kind=ok, opp_occ=oo, t_day=td, t_yield=ty,
        opp_t_day=otd, opp_t_yield=oty, shed=sh, seeds=np.array([3,2,1,1,2],np.int32)[:spec.N_CROPS],
        nquad=np.int32(nquad), opp_nquad=np.int32(nquad),
        mkt_inv=np.array([spec.MARKET_I0+7,spec.MARKET_I0-4,spec.MARKET_I0,spec.MARKET_I0+2,
                          spec.MARKET_I0-6,spec.MARKET_I0+1,spec.MARKET_I0,spec.MARKET_I0-2,
                          spec.MARKET_I0+3],np.int32)[:spec.N_PRODUCTS],
        price=np.array([spec.DEFAULT_MARKET_PARAMS[n]["base"] for n in spec.PRODUCTS],np.int32),
        shops=np.array([1,0,2,1,0,3,1,0],np.int32))

def pl(c,d,y=0): return (spec.KIND_PLANT,c,d,y)
def an(a,d,y=0): return (int(spec.ANIMAL_STRUCT[a]),a,d,y)

DAY=12
SHED=np.zeros(spec.N_ITEMS,np.int32); SHED[0]=6; SHED[1]=3
# common background: wheat, carrot, 2 chickens, 1 cow, plus opponent board
BG = [pl(spec.I_WHEAT,7)]*6 + [pl(spec.I_CARROT,9)]*4 + [an(0,3,1)]*2 + [an(1,5,0)]
OPP = [pl(spec.I_WHEAT,6)]*8 + [pl(spec.I_TOMATO,2,1)]*4 + [an(0,4,1)]*2

def outs(theta, ob):
    p = PO.unpack(np, np.asarray(theta,np.float32))
    pf, gf, df = brain.features(np, ob)
    fc = brain.production_forecast(np, ob)
    fv = brain.forward_value(np, ob)
    o = PO.forward(np, p, pf, gf, df, fc, fv)
    return (np.asarray(pf),np.asarray(gf),np.asarray(df),np.asarray(fc),np.asarray(fv)), o

def headvec(o):
    return np.concatenate([np.atleast_1d(np.asarray(x,np.float64)).ravel() for x in
        (o.head,o.prio,o.lots,o.aux,o.dev,o.sat,o.crew,o.hire,o.ramp,o.fwd)])

def report(name, obA, obB, thetas):
    print("="*72); print(name)
    for tn, th in thetas.items():
        (pfA,gfA,dfA,fcA,fvA),oA = outs(th,obA)
        (pfB,gfB,dfB,fcB,fvB),oB = outs(th,obB)
        def d(a,b): 
            m=~np.isclose(a,b,rtol=0,atol=0); return int(m.sum()), float(np.abs(a-b).max())
        n_pf,m_pf = d(pfA,pfB); n_gf,m_gf = d(gfA,gfB); n_df,m_df=d(dfA,dfB)
        n_fc,m_fc = d(fcA,fcB); n_fv,m_fv = d(fvA,fvB)
        hA,hB = headvec(oA),headvec(oB); n_h,m_h = d(hA,hB)
        sA,sB = np.asarray(oA.scores),np.asarray(oB.scores); n_s,m_s = d(sA,sB)
        print(f"  theta={tn}")
        print(f"    OLD feats: prod_feat {n_pf} cols max {m_pf:.6g} | glob_feat {n_gf} max {m_gf:.6g} | drain {n_df} max {m_df:.6g}")
        if n_pf: print(f"      prod_feat changed (prod,col): {[tuple(map(int,x)) for x in np.argwhere(pfA!=pfB)][:12]}")
        if n_gf: print(f"      glob_feat changed idx: {list(np.argwhere(gfA!=gfB).ravel())}")
        print(f"    NEW feats: fcast {n_fc}/{fcA.size} max {m_fc:.6g} | fwdval {n_fv}/{fvA.size} max {m_fv:.6g}")
        print(f"    enc scores changed {n_s} max {m_s:.6g}")
        print(f"    GLOBAL-HEAD outputs changed {n_h}/{hA.size} max {m_h:.6g}")
        for fld in ("head","prio","lots","aux","dev","sat","crew","hire","ramp","fwd"):
            a=np.atleast_1d(np.asarray(getattr(oA,fld),np.float64)).ravel()
            b=np.atleast_1d(np.asarray(getattr(oB,fld),np.float64)).ravel()
            if not np.array_equal(a,b): print(f"      {fld}: max|d| {np.abs(a-b).max():.6g}")
        # block contributions
        pA = PO.unpack(np, np.asarray(th,np.float32))
        print(f"    |gp| {np.abs(pA.gp).max():.4g} |fv| {np.abs(pA.fv).max():.4g} |fh| {np.abs(pA.fh).max():.4g} |fs| {np.abs(pA.fs).max():.4g} |g11| {np.abs(pA.g11).max():.4g}")

thetas = {}
for nm,fn in (("flow135_g350_gpfwdfv","flow135_g350_gpfwdfv.npy"),("flow155_g50","flow155_g50.npy")):
    t = np.load(TH+fn); print(nm,"len",t.shape); thetas[nm]=t
print("N_PARAMS",PO.N_PARAMS)

# ---- probe 1: strawberry maturity + standing yield, counts equal
A1 = obs(DAY, [pl(spec.I_STRAWBERRY,1,3)]*10 + BG, OPP, shed=SHED)
B1 = obs(DAY, [pl(spec.I_STRAWBERRY,11,0)]*10 + BG, OPP, shed=SHED)
report("PROBE 1: 10 strawberry planted d1 y=3  ->  planted d11 y=0 (same count, day 12)", A1,B1,thetas)

# ---- probe 2: ten immature strawberry -> ten immature melon, same days
A2 = obs(DAY, [pl(spec.I_STRAWBERRY,11,0)]*10 + BG, OPP, shed=SHED)
B2 = obs(DAY, [pl(spec.I_MELON,11,0)]*10 + BG, OPP, shed=SHED)
report("PROBE 2: 10 immature strawberry (d11) -> 10 immature melon (d11), day 12", A2,B2,thetas)
print("first-yield: straw",spec.CROP_FIRST_YIELD_DAY[spec.I_STRAWBERRY],"melon",spec.CROP_FIRST_YIELD_DAY[spec.I_MELON])
