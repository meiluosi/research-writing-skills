---
name: concise-edit
description: "Use to tighten prose at the SENTENCE and PARAGRAPH level in English or Chinese: omit needless words, active voice, positive form, concrete language, keep related words together, one topic per paragraph, emphasis at the end. Rules are an independent restatement of the classic public-domain principles (Strunk, 1918) plus Chinese-specific rules. Triggers: tighten the wording, cut filler, wordy sentences, 精简句子, 去冗词, 句子太啰嗦, 改成主动, 说得更直接. Not for document structure (use result-writeup-editor) or AI patterns (use ai-pattern-edit)."
version: 0.1.0
---

# Concise Edit

Sentence-level tightening. It never changes what is claimed, so it always ends with `preservation-check`.

## When to use
Sentences are long, padded, or indirect, and the structure of the document is already fine. For structure, narration, or repetition, run `result-writeup-editor` first.

## Process
1. Read the text once. Mark sentences that fail a rule below. Do not touch sentences that pass.
2. Edit with the smallest change that fixes the rule. Keep the author's terms and numbers.
3. Run `preservation-check`. A rule never outranks a hedge or a number.

## Rules (English)
1. **Omit needless words.** "in order to" -> "to"; "the fact that" -> drop; "it is important to note that" -> drop.
2. **Use the active voice** when the actor matters. Passive stays for unknown or irrelevant actors and for method sections.
3. **Put statements in positive form.** "did not remember" -> "forgot"; keep the negation when the claim is a negation ("no effect found").
4. **Be specific.** Replace "significant", "various", "several" by the quantity.
5. **Keep related words together.** Subject near verb, modifier near its noun.
6. **One topic per paragraph; start with the point.**
7. **Put the emphatic word at the end** of the sentence.
8. **Keep parallel ideas in parallel form.**
9. **Remove intensifiers and softeners** (very, really, basically, quite) unless they carry degree that matters.

## Rules (Chinese)
1. **删虚词和空转的连接。** 进行/加以/予以 + 动词 -> 直接用动词（"进行了检查" -> "检查了"）；"的"字链超过三个就拆。
2. **能用主动就不用"被"。** "被审查指出" 在主语是审查时可改 "审查指出"。
3. **一句一事。** 超过 60 字且含两个以上转折的句子拆开。
4. **名词化动词还原。** "对……的验证" -> "验证……"。
5. **量化代替程度词。** "很大程度上" -> 给出数字或删掉；"相当/非常/比较" 在不承载程度时删。
6. **并列项等长。** 条目的动词和结构一致。
7. **结论放句首，原因放后面**，除非原因是读者最需要的新信息。
8. **去口头铺垫。** "其实、说白了、也就是说"开头的句子，直接说后半句。

## Do not
- Delete a hedge that carries uncertainty ("可能", "about", "untested").
- Rewrite quotations, titles, code, or proper names.
- Compress a definition the reader needs the first time they meet the term.
- Replace the author's voice with a neutral one; if a style sample exists, match its sentence length.

## Pairing
- Structure and narration first: `result-writeup-editor`.
- Machine-sounding patterns: `ai-pattern-edit`.
- Verification: `preservation-check`.
- Principles credit: see `../NOTICE.md`.
