#!/usr/bin/env python3
"""doc_metrics.py - document-level metrics for result-heavy write-ups (Chinese, English, or mixed). Standard library only.

  python3 doc_metrics.py FILE [FILE ...]            per-file report (+ cross-file duplicates when several files are given)
  python3 doc_metrics.py --compare BEFORE AFTER     numbers/percentages that appear in BEFORE but not in AFTER, and the reverse
  python3 doc_metrics.py FILE --json                machine-readable
  --exempt WORDS   comma-separated heading words that are allowed off the spine (default: 术语,glossary,复现,Reproduce,目录)
  A line containing <!--keep--> is treated as reviewed and ignored by the narration check.

What it measures (heuristics, not verdicts):
  narration     sentences where the author narrates their own work ("我做了/我查了/I checked/I ran") per 1000 chars
  first_person  all first-person markers per 1000 chars (stance and story count here too)
  headings      level-2 headings that do not follow "N. function: point" (colon after a function word)
  limits        sections whose heading mentions limits/boundaries/blind spots (consolidate to one place in a series)
  boilerplate   preface/outro/teaser lines ("下一篇", "这一篇讲什么", "谢谢读到这里", "In the next post")
  duplicates    near-identical sentences across files (character 8-gram Jaccard >= 0.6)
"""
import sys, re, json, itertools, argparse
ZH_NARR=re.compile(r"我们?(?:先|又|再|还|也|曾|才|就|都|已经)?(?:做|查|写|把|试|跑|改|加|补|删|重新|检查|验证|选|用|花|找|搭|拿|读|复核|核对|修|调|换|收|停|挑|定|起了|预先登记|登记|更正|重跑)|(?:全部重跑|重新运行|重跑|已更正|后更正|在.{0,6}之后更正|补回|没做|未做|没有包含|被丢弃|已记入|已写进|写进了)")  # v0.3: dropped mental verbs (想/发现/怀疑/担心: stance or finding), added agentless process phrases
EN_NARR=re.compile(r"\b(?:I|We)\s+(?:then\s+|also\s+|first\s+|later\s+|just\s+)?(?:did|ran|checked|wrote|added|tried|found|fixed|changed|decided|looked|tested|built|re-?ran|made|used|picked|switched|removed|rewrote|started)\b")
ZH_FP=re.compile(r"[我](?!们的)"); EN_FP=re.compile(r"\b(?:I|my|me|we|our)\b",re.I)
LIMIT=re.compile(r"局限|边界|盲区|没有证明|没解决|limitation|caveat|boundar|blind spot",re.I)
BOILER=re.compile(r"^(?!>)(?:#+\s*)?(?:\d+\.\s*)?(?:下一篇|这一篇讲什么|谢谢|感谢读到|如果你要做类似|In the next (?:post|part)|Thanks for reading|本文(?:将|会)|接下来我们)")
HEAD2=re.compile(r"^##\s+(.*)$"); SPINE=re.compile(r"^\d+\.\s*[^：:]{1,32}[：:]\s*\S")
NUM=re.compile(r"[+\-−]?\d+(?:\.\d+)?(?:e-?\d+)?\s?%?")
def strip_code(t):
    t=re.sub(r"```.*?```","",t,flags=re.S); return re.sub(r"`[^`]*`","",t)
def sentences(t):
    t=strip_code(t); t=re.sub(r"^>.*$","",t,flags=re.M); t=re.sub(r"\|.*\|","",t); t=re.sub(r"^[>#*\-\s]+","",t,flags=re.M)
    return [s.strip() for s in re.split(r"(?<=[。！？!?；;])|(?<=[.])\s+|\n+",t) if len(s.strip())>=8]
EXEMPT_DEFAULT="术语,glossary,复现,reproduce,目录,contents"
def mask_fences(raw):
    """blank out fenced code blocks and quote lines so line-based metrics (narration, headings) ignore them, keeping line numbers"""
    out=[]; fence=False
    for l in raw.split("\n"):
        if l.lstrip().startswith("```"): fence=not fence; out.append(""); continue
        out.append("" if (fence or l.lstrip().startswith(">")) else l)
    return out
def analyse(path,exempt=None):
    exempt=EXEMPT_DEFAULT if exempt is None else exempt
    raw=open(path,encoding="utf-8").read(); body=strip_code(raw); n=max(len(re.sub(r"\s","",body)),1); lines=mask_fences(raw)
    narr=[(i+1,l.strip()[:90]) for i,l in enumerate(lines) if (ZH_NARR.search(l) or EN_NARR.search(l)) and not l.lstrip().startswith(("|","#","!","<!--")) and "<!--keep-->" not in l]
    heads=[(i+1,HEAD2.match(l).group(1)) for i,l in enumerate(lines) if HEAD2.match(l)]
    ex=[w.strip().lower() for w in exempt.split(",") if w.strip()]
    off=[(i,h) for i,h in heads if not SPINE.match(h) and not re.match(r"^\d+\.\s*(下一篇|Next)",h) and not any(w in h.lower() for w in ex)]
    lim=[(i,h) for i,h in heads if LIMIT.search(h)]
    boil=[(i+1,l.strip()[:60]) for i,l in enumerate(lines) if BOILER.search(l.strip())]
    fp=len(ZH_FP.findall(body))+len(EN_FP.findall(body)); 
    return dict(file=path,chars=n,narration_per_1000=round(1000*len(narr)/n,2),narration_examples=narr[:6],first_person_per_1000=round(1000*fp/n,2),
                headings=len(heads),headings_off_spine=off,limit_sections=lim,boilerplate=boil)
def shingles(s,k=8): s=re.sub(r"\W","",s); return {s[i:i+k] for i in range(max(len(s)-k+1,1))}
def duplicates(paths,thr=0.6):
    items=[(p,s,shingles(s)) for p in paths for s in sentences(open(p,encoding="utf-8").read()) if len(s)>=20]; out=[]
    for (p1,s1,a),(p2,s2,b) in itertools.combinations(items,2):
        if p1==p2: continue
        j=len(a&b)/max(len(a|b),1)
        if j>=thr: out.append((round(j,2),p1,p2,s1[:70]))
    return out
def _norm_numbers(t):
    t=strip_code(t); t=re.sub(r"https?://[A-Za-z0-9\-._~:/?#@!$&*+,;=%]+","",t); t=t.replace("−","-").replace("，",",").replace("％","%")
    t=re.sub(r"(?<=\d),(?=\d{3}(?!\d))","",t); t=re.sub(r"^[#>\s]*\d+(?:\.\d+)*[\.\)、]\s+","",t,flags=re.M); t=re.sub(r"(?<=\d)\s+%","%",t); out=set()
    for m in re.finditer(r"(?:(?<=^)|(?<=[\s(\[（【:：,，;；=<>]))([+\-])?(\d+(?:\.\d+)?(?:[eE][+\-]?\d+)?)(%?)|(\d+(?:\.\d+)?(?:[eE][+\-]?\d+)?)(%?)",t,flags=re.M):
        sign,num,pct,num2,pct2=m.groups(); n=num or num2
        try: v=float(n)
        except ValueError: continue
        out.add(f"{'-' if (num and sign=='-') else ''}{v:g}{pct or pct2 or ''}")
    return out
def numbers(path):
    return _norm_numbers(open(path,encoding="utf-8").read())
def _old_numbers(path):
    t=strip_code(open(path,encoding="utf-8").read()); t=re.sub(r"https?://\S+","",t); t=re.sub(r"^[#>\s]*\d+(?:\.\d+)*[\.\)、]?\s*","",t,flags=re.M)   # drop heading/list enumerators (N. or N.M)
    return {n.strip().replace("−","-").lstrip("+") for n in NUM.findall(t) if re.search(r"\d",n)}
def compare(a,b):
    x,y=numbers(a),numbers(b); return sorted(x-y),sorted(y-x)
if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("files",nargs="+"); ap.add_argument("--compare",action="store_true"); ap.add_argument("--json",action="store_true"); ap.add_argument("--exempt",default=None); a=ap.parse_args()
    if a.compare:
        if len(a.files)!=2: sys.exit("--compare needs BEFORE AFTER")
        lost,new=compare(*a.files); print("numbers in BEFORE but missing in AFTER:",lost or "none"); print("numbers in AFTER but not in BEFORE:",new or "none"); sys.exit(0)
    res=[analyse(p,a.exempt) for p in a.files]; dup=duplicates(a.files) if len(a.files)>1 else []
    if a.json: print(json.dumps(dict(files=res,duplicates=dup),ensure_ascii=False,indent=1)); sys.exit(0)
    print("| file | chars | narration/1000 | first-person/1000 | h2 off-spine | limit sections | boilerplate |\n|---|---|---|---|---|---|---|")
    for r in res: print(f"| {r['file'].split('/')[-1]} | {r['chars']} | {r['narration_per_1000']} | {r['first_person_per_1000']} | {len(r['headings_off_spine'])}/{r['headings']} | {len(r['limit_sections'])} | {len(r['boilerplate'])} |")
    for r in res:
        if r["narration_examples"]: print(f"\n{r['file'].split('/')[-1]} narration examples:"); [print(f"  L{i}: {t}") for i,t in r["narration_examples"]]
        if r["headings_off_spine"]: print(f"{r['file'].split('/')[-1]} headings off the 'N. function: point' spine:",[h for _,h in r["headings_off_spine"]])
    if dup: print("\nnear-duplicate sentences across files:"); [print(f"  {j} {p1.split('/')[-1]} ~ {p2.split('/')[-1]}: {s}") for j,p1,p2,s in dup[:15]]
