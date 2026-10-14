#!/usr/bin/env python3
"""preserve.py BEFORE AFTER [--json] [--allow-number N ...] [--justified-hedge WORD ...]   (v0.2; Chinese, English, mixed; standard library only)

A heuristic gate for edits. It flags, a human decides. A PASS means "no flagged change", NOT "meaning is equivalent":
comparison reversals ("A better than B" -> "B better than A"), scope narrowing, and re-attached conditions need a manual read.

  numbers      normalised values (sign only after start/space/bracket; ranges and dates split; 1e-3 == 0.001; 5 % == 5%; 1,000 == 1000).
               presence lost/added = ERROR; occurrence count changed = WARN
  operators    comparison symbols (< > <= >= ≥ ≤) count change = ERROR; '=' count change = WARN
  literals     URLs, inline code, versions: lost = ERROR, added = WARN
  strong       claim-strengthening words appearing more often in AFTER = ERROR
  verdicts     result words (等价/不确定/更好/更差/没有证据/equivalent/uncertain/...) count change = WARN
  scope        all/every/所有/全部/任何/none/没有任何 count change = WARN
  hedges       uncertainty words lost = FAIL unless --justified-hedge WORD is given
  negations    ANY change in negation count = WARN, and the sentences carrying negations that disappeared/appeared are printed
Last line: RESULT: FAIL | PASS WITH WARNINGS | PASS   (quote this line in the handoff). Exit code 1 on FAIL.
"""
import sys, re, json, argparse
from collections import Counter
def clean(t): return re.sub(r"```.*?```","",t,flags=re.S)
def norm_numbers(t):
    t=clean(t); t=re.sub(r"https?://[A-Za-z0-9\-._~:/?#@!$&*+,;=%]+","",t); t=re.sub(r"`[^`]*`","",t)
    t=t.replace("−","-").replace("，",",").replace("％","%").replace("＋","+")
    t=re.sub(r"(?<=\d),(?=\d{3}(?!\d))","",t)                                   # thousands separators
    t=re.sub(r"^[#>\s]*\d+(?:\.\d+)*[\.\)、]\s+","",t,flags=re.M)                # heading/list enumerators (marker must be followed by a space)
    t=re.sub(r"(?<=\d)\s+%","%",t)
    out=[]
    for m in re.finditer(r"(?:(?<=^)|(?<=[\s(\[（【:：,，;；=<>]))([+\-])?(\d+(?:\.\d+)?(?:[eE][+\-]?\d+)?)(%?)|(\d+(?:\.\d+)?(?:[eE][+\-]?\d+)?)(%?)",t,flags=re.M):
        sign,num,pct,num2,pct2=m.groups()
        n=num or num2; p=(pct or pct2 or ""); s=(sign or "") if num else ""
        try: v=float(n)
        except ValueError: continue
        out.append(f"{'-' if s=='-' else ''}{v:g}{p}")
    return out
def literals(t):
    t=clean(t); L=set(re.findall(r"https?://[A-Za-z0-9\-._~:/?#@!$&*+,;=%]+",t)); L|=set(re.findall(r"`([^`]+)`",t)); L|=set(re.findall(r"\bv?\d+\.\d+\.\d+\b",t)); return L
OPS=["<=",">=","≤","≥","<",">","="]
VERD=["等价","不确定","更好","更差","没有证据","没测出","equivalent","uncertain","inconclusive","better","worse","no evidence"]
STRONG=[r"证明(?!了?的)",r"证实",r"一定(?!程度|的|范围|数量|条件)",r"完全",r"必然",r"没有用",r"毫无",r"始终",r"总是",r"显然",r"\bproved?\b",r"\bproves\b",r"\bproven\b",r"\bdemonstrates?\b",r"\balways\b",r"\bnever\b",r"\bguarantee",r"\bdefinitely\b",r"\bclearly\b",r"\bno effect\b"]
SCOPE=[r"所有",r"全部",r"任何",r"没有任何",r"\ball\b",r"\bevery\b",r"\bnone\b",r"\bno one\b"]
HEDGE=[r"可能",r"(?<![制节契简公大])约(?![束定会])",r"大约",r"似乎",r"也许",r"或许",r"大致",r"尚未",r"未证实",r"没有单独检验",r"\bprobably\b",r"\babout\b",r"\bapproximately\b",r"\bmay\b",r"\bmight\b",r"\blikely\b",r"\broughly\b",r"\buntested\b",r"\bunverified\b"]
NEG=[r"没有",r"(?<![不])不(?![仅过错少])",r"无",r"未",r"非",r"\bnot\b",r"\bno\b",r"\bnever\b",r"\bcannot\b",r"n't\b"]
def cnt(t,pats): 
    t=t.lower(); return {p:len(re.findall(p,t)) for p in pats if re.search(p,t)}
def show(p): return re.sub(r"\\b|\(\?.*?\)","",p)[:20]
def sentences(t): return [s.strip() for s in re.split(r"(?<=[。！？!?；;])|(?<=[.])\s+|\n+",clean(t)) if len(s.strip())>=6]
def has_neg(s): return any(re.search(p,s.lower()) for p in NEG)
def check(a,b,allow=(),hedge_ok=()):
    A,B=clean(a),clean(b); out=[]
    ca,cb=Counter(norm_numbers(a)),Counter(norm_numbers(b))
    for n in sorted(set(ca)|set(cb)):
        if n in allow: continue
        if n not in cb: out.append(("ERROR","number lost",n))
        elif n not in ca: out.append(("ERROR","number added",n))
        elif ca[n]!=cb[n]: out.append(("WARN","number occurrence count changed",f"{n}: {ca[n]} -> {cb[n]}"))
    for o in OPS:
        x,y=A.count(o),B.count(o)
        if x!=y: out.append(("WARN" if o=="=" else "ERROR","comparison operator count changed",f"{o}: {x} -> {y}"))
    la,lb=literals(a),literals(b)
    for x in sorted(la-lb): out.append(("ERROR","literal lost",x[:80]))
    for x in sorted(lb-la): out.append(("WARN","literal added",x[:80]))
    for w in VERD:
        x,y=A.lower().count(w),B.lower().count(w)
        if x!=y: out.append(("WARN","verdict word count",f"{w}: {x} -> {y}"))
    sa,sb=cnt(A,STRONG),cnt(B,STRONG)
    for p in sb:
        if sb[p]>sa.get(p,0): out.append(("ERROR","claim strengthened (new strong word)",f"{show(p)}: {sa.get(p,0)} -> {sb[p]}"))
    ka,kb=cnt(A,SCOPE),cnt(B,SCOPE)
    for p in set(ka)|set(kb):
        if ka.get(p,0)!=kb.get(p,0): out.append(("WARN","scope word count changed",f"{show(p)}: {ka.get(p,0)} -> {kb.get(p,0)}"))
    ha,hb=cnt(A,HEDGE),cnt(B,HEDGE)
    for p in ha:
        if hb.get(p,0)<ha[p] and show(p) not in hedge_ok: out.append(("FAIL","hedge lost (justify with --justified-hedge)",f"{show(p)}: {ha[p]} -> {hb.get(p,0)}"))
    na=sum(sum(cnt(A,NEG).values()) for _ in [0]); nb=sum(cnt(B,NEG).values()); na=sum(cnt(A,NEG).values())
    if na!=nb:
        out.append(("WARN","negation count changed",f"{na} -> {nb}"))
        sA={s for s in sentences(a) if has_neg(s)}; sB={s for s in sentences(b) if has_neg(s)}
        for s in sorted(sA-sB)[:5]: out.append(("INFO","negation sentence only in BEFORE",s[:90]))
        for s in sorted(sB-sA)[:5]: out.append(("INFO","negation sentence only in AFTER",s[:90]))
    return out
def result(flags):
    if any(l in ("ERROR","FAIL") for l,_,_ in flags): return "FAIL"
    return "PASS WITH WARNINGS" if any(l=="WARN" for l,_,_ in flags) else "PASS"
if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("before"); ap.add_argument("after"); ap.add_argument("--json",action="store_true"); ap.add_argument("--allow-number",nargs="*",default=[]); ap.add_argument("--justified-hedge",nargs="*",default=[]); a=ap.parse_args()
    r=check(open(a.before,encoding="utf-8").read(),open(a.after,encoding="utf-8").read(),set(a.allow_number),set(a.justified_hedge)); res=result(r)
    if a.json: print(json.dumps(dict(result=res,flags=[dict(level=l,kind=k,detail=d) for l,k,d in r]),ensure_ascii=False,indent=1))
    else:
        for l,k,d in r: print(f"{l:5s} {k}: {d}")
        print(f"\nRESULT: {res}   (a pass is not proof of equivalent meaning; read comparisons, scope and condition attachment by hand)")
    sys.exit(1 if res=="FAIL" else 0)
