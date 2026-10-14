---
name: concise-edit
description: "Use to tighten Chinese (or English) prose at the sentence and paragraph level: drop empty verbs, restore nominalised verbs, split overloaded sentences, replace degree words with quantities. Triggers: 精简句子, 去冗词, 句子太啰嗦, 改成主动, tighten the wording, cut filler. Not for document structure (result-writeup-editor) or AI patterns (ai-pattern-edit)."
version: 0.2.0
---

# Concise Edit

Sentence-level tightening that never changes what is claimed. It ends with `edit-verification`.

## Process
1. Mark only the sentences that fail a rule below; leave the rest alone.
2. Make the smallest change that fixes the rule; keep the author's terms and numbers.
3. Run `edit-verification`. A rule never outranks a hedge or a number.

## Chinese rules (the part no other skill here covers)
1. 删空转的动词：进行/加以/予以 + 动词，直接用动词（"进行了检查"→"检查了"）；"的"字链超过三个就拆。
2. 名词化动词还原："对……的验证"→"验证……"。
3. 一句一事：超过 60 字且含两个以上转折的句子拆开。
4. 能主动就不用"被"：主语是施动者时。
5. 量化代替程度词："很大程度上"给出数字或删；"相当/非常/比较"不承载程度时删。
6. 并列项等长，动词和结构一致。
7. 结论放句首，原因放后面，除非原因是读者最需要的新信息。
8. 去口头铺垫："其实、说白了、也就是说"开头的句子，直接说后半句。

## English
Use the standard principles: omit needless words, active voice where the actor matters, positive form unless the claim is a negation, concrete over vague, related words together, emphasis at the end. For longer lists see `external/humanizer` and the copy-editing process in `docs/ecosystem-analysis.md`.

## Do not
Delete a hedge that carries uncertainty ("可能", "about"); rewrite quotations, titles, code, or names; compress a definition the reader needs at first use; replace the author's voice with a neutral one (a style sample outranks these rules).

## Chain position
Before: `result-writeup-editor`. After: `ai-pattern-edit` (if needed), then `edit-verification`.
