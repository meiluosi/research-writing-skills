import sys, os; sys.path.insert(0,os.path.dirname(__file__)); import preserve as P
def R(a,b,**k): return P.result(P.check(a,b,**k))
def kinds(a,b,**k): return {(l,kk) for l,kk,_ in P.check(a,b,**k)}
a="区间 [−0.59, +0.14]，结论是不确定。约 300 个实例，见 `foo.py` 和 https://x.org/a。可能有偏向。"
assert R(a,a)=="PASS"
assert ("ERROR","number lost") in kinds(a,a.replace("300","若干"))
assert ("ERROR","number added") in kinds(a,a+" 另有 42 个。")
assert ("ERROR","claim strengthened (new strong word)") in kinds(a,a.replace("不确定","完全没有用"))
assert R(a,a.replace("可能有偏向","有偏向"))=="FAIL"
assert R(a,a.replace("可能有偏向","有偏向"),hedge_ok={"可能"})!="FAIL"
assert ("ERROR","literal lost") in kinds(a,a.replace("`foo.py`","脚本"))
assert R(a,a.replace("300","三百"),allow={"300"})!="FAIL"
# reviewer cases
assert ("WARN","negation count changed") in kinds("The effect is not significant.","The effect is significant.")
assert ("WARN","negation count changed") in kinds("没有证据表明有效。","有证据表明有效。")
assert ("ERROR","comparison operator count changed") in kinds("p < 0.05","p > 0.05")
assert R("Always check.","check.")!="FAIL" and ("ERROR","claim strengthened (new strong word)") in kinds("check.","Always check.")
assert R("Probably yes.","Yes.")=="FAIL"
assert not any(l in("ERROR","FAIL") for l,_,_ in P.check("range 5-10 in 2026-10-14","range 5 to 10 in 14 Oct 2026",allow={"2026"}) if _!="number added")  # ranges/dates: only 'added'/'lost' for the changed date format, never a bogus negative number
assert P.norm_numbers("1e-3")==P.norm_numbers("0.001")
assert P.norm_numbers("5 %")==P.norm_numbers("5%") and P.norm_numbers("1,000")==P.norm_numbers("1000")
assert "42.5" in P.norm_numbers("42.5 percent at line start")
assert P.norm_numbers("3 3 3")==["3","3","3"] and ("WARN","number occurrence count changed") in kinds("3 3 3","3")
assert ("ERROR","claim strengthened (new strong word)") not in kinds("在一定程度上有效。","在一定程度上有效。 ") 
assert ("ERROR","claim strengthened (new strong word)") not in kinds("a","受制约的一定范围内")
assert not P.cnt("制约","(?<![制节契简公大])约(?![束定会])".split("|")) 
print("preserve.py v0.2: all checks passed")
