#!/usr/bin/env python3
"""Paired bootstrap CI and the verdict rule.
  python3 verdict.py diffs.txt --margin 0.5 [--level 95] [--better low|high]
diffs.txt: one paired difference (A - B) per line, one line per unit (instance / world / seed-mean).
--better low means a smaller metric is better (e.g. tour length gap); high means larger is better.
Verdict: equivalent if CI inside +-margin; A better/worse if the CI excludes 0 and |mean| >= margin; otherwise uncertain."""
import sys, argparse, numpy as np
def boot_ci(d,level=95,n=4000,seed=0):
    d=np.asarray(d,float); r=np.random.default_rng(seed); m=np.array([d[r.integers(0,len(d),len(d))].mean() for _ in range(n)]); a=(100-level)/2
    return float(d.mean()),float(np.percentile(m,a)),float(np.percentile(m,100-a))
def verdict(m,lo,hi,margin,better="high"):
    s=1 if better=="high" else -1                      # orient so that positive = A better
    m,lo,hi=(m,lo,hi) if s==1 else (-m,-hi,-lo)
    if lo>-margin and hi<margin: note="equivalent"+("" if (lo<=0<=hi) else " (CI excludes 0 but stays under the margin: say 'small, non-zero')")
    elif lo>0 and m>=margin: note="A better"
    elif hi<0 and m<=-margin: note="A worse"
    else: note="uncertain"
    return note
if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("file"); ap.add_argument("--margin",type=float,required=True); ap.add_argument("--level",type=float,default=95); ap.add_argument("--better",choices=["low","high"],default="high")
    a=ap.parse_args(); d=np.loadtxt(a.file); m,lo,hi=boot_ci(d,a.level)
    half=(hi-lo)/2
    print(f"n={len(d)}  mean {m:+.4g}  {a.level:g}% CI [{lo:+.4g}, {hi:+.4g}]  half-width {half:.3g}  margin {a.margin:g}")
    if half>a.margin/2: print("warning: CI half-width exceeds half the margin; this design can barely show equivalence")
    print("verdict:",verdict(m,lo,hi,a.margin,a.better))
