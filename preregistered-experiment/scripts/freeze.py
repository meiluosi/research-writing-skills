#!/usr/bin/env python3
"""freeze.py write <registration.md> <file> [<file> ...]   -> prints a sha256 list (redirect to PREREG_x.sha256)
   freeze.py check <PREREG_x.sha256>                       -> verifies hashes, lists files modified after the registration.
The first line of the written file records the UTC time of the freeze and the registration file name."""
import sys, os, hashlib, time, datetime
def sha(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()
def write(reg,files):
    print(f"# frozen {datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')} registration={reg}")
    for p in [reg]+[f for f in files if f!=reg]:
        if not os.path.exists(p): sys.exit(f"missing file: {p}")
        print(f"{sha(p)}  {p}")
def check(listing):
    base=os.path.dirname(os.path.abspath(listing)); ts=None; bad=0; late=[]
    lines=[l.rstrip("\n") for l in open(listing) if l.strip()]
    if lines and lines[0].startswith("# frozen"): ts=datetime.datetime.fromisoformat(lines[0].split()[2]).timestamp(); lines=lines[1:]
    for l in lines:
        h,p=l.split(None,1); p=p.strip(); fp=p if os.path.isabs(p) else os.path.join(base,p)
        if not os.path.exists(fp): print(f"MISSING   {p}"); bad+=1; continue
        ok=sha(fp)==h; print(("OK        " if ok else "CHANGED   ")+p); bad+=not ok
        if ts and os.path.getmtime(fp)>ts+1: late.append(p)
    if late: print("\nmodified after the freeze time:\n  "+"\n  ".join(late)+"\n(log each in the deviations file, with the reason and whether results had been seen)")
    print(f"\n{bad} problem(s)" if bad else "\nall hashes match"); sys.exit(1 if bad else 0)
if __name__=="__main__":
    if len(sys.argv)>=3 and sys.argv[1]=="write": write(sys.argv[2],sys.argv[3:])
    elif len(sys.argv)==3 and sys.argv[1]=="check": check(sys.argv[2])
    else: sys.exit(__doc__)
