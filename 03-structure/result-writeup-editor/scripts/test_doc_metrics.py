import sys, os, tempfile; sys.path.insert(0,os.path.dirname(__file__)); import doc_metrics as D
def tmp(text):
    f=tempfile.NamedTemporaryFile("w",suffix=".md",delete=False,encoding="utf-8"); f.write(text); f.close(); return f.name
a=tmp("## 先说一个场景\n\n我查了日志，我把参数改成了 0.5，我写了一份报告。结果是 1.2%。\n\n## 3. 结果：四个发现\n\n平均净奖励 +44.0。\n\n下一篇：第 2 篇。\n")
r=D.analyse(a)
assert r["narration_per_1000"]>0, "narration not detected"
assert len(r["headings_off_spine"])==1 and r["headings_off_spine"][0][1]=="先说一个场景", r["headings_off_spine"]
assert r["boilerplate"], "teaser not detected"
b=tmp("## 1. 场景：开头\n\n日志排查：参数 0.5。结果是 1.2%。\n"); assert D.analyse(b)["narration_per_1000"]==0
lost,new=D.compare(a,b); assert "44" in lost, lost
c=tmp("该结论的证据是一组很长的句子，用来测试跨文件重复检测是否工作良好，好的。"); d=tmp("该结论的证据是一组很长的句子，用来测试跨文件重复检测是否工作良好，好的。"); assert D.duplicates([c,d]), "duplicates"
print("doc_metrics.py: all checks passed")
