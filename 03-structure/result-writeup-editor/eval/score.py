#!/usr/bin/env python3
"""score.py  -> precision/recall of the narration flag in doc_metrics.py against independent labels (labels.json).
The sample is stratified: every flagged sentence plus a random sample of the unflagged ones, so recall is weighted by the sampling ratio."""
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts")); import doc_metrics as D
here = os.path.dirname(os.path.abspath(__file__))
which = sys.argv[1] if len(sys.argv) > 1 else "dev"        # dev = sentences.json/labels.json (used to tune the regex); heldout = untouched set
sf, lf = ("sentences.json", "labels.json") if which == "dev" else ("sentences_heldout.json", "labels_heldout.json")
S = json.load(open(os.path.join(here, sf))); L = json.load(open(os.path.join(here, lf)))
flag = lambda s: bool(D.ZH_NARR.search(s) or D.EN_NARR.search(s))
fl = [x for x in S if flag(x["text"])]; nf = [x for x in S if not flag(x["text"])]
meta = json.load(open(os.path.join(here, "heldout_meta.json"))) if which != "dev" else None
w = (meta["unflagged_population"] / len(nf)) if meta else 2.98   # sampling weight of the unflagged sentences
from collections import Counter
c_fl = Counter(L[str(x["id"])] for x in fl); c_nf = Counter(L[str(x["id"])] for x in nf)
tp = c_fl["narration"]; fp_stance = c_fl["stance"]; fp_other = c_fl["fact"] + c_fl["other"]
fn = c_nf["narration"] * w
print(f"flagged sentences: {len(fl)}  labels: {dict(c_fl)}")
print(f"unflagged sample: {len(nf)}  labels: {dict(c_nf)}  (weight {w:.2f})")
print(f"precision (flagged that are narration): {tp}/{len(fl)} = {tp/max(len(fl),1):.2f}")
print(f"flagged but stance (should be kept): {fp_stance}/{len(fl)} = {fp_stance/max(len(fl),1):.2f}")
print(f"recall (weighted): {tp}/({tp}+{fn:.1f}) = {tp/max(tp+fn,1e-9):.2f}")
print("false positives:"); [print("  -", x["text"][:80], "[", L[str(x["id"])], "]") for x in fl if L[str(x["id"])] != "narration"]
print("missed narration (unflagged sample):"); [print("  -", x["text"][:80]) for x in nf if L[str(x["id"])] == "narration"]
