---
name: tech-article-draft
description: "Use to draft a technical or research article, blog post, or project write-up FROM SUPPLIED EVIDENCE: sharpen the claim, inventory the evidence with its source, choose a heading spine, outline with evidence slots, draft only what the evidence supports, leave visible slots for the author's own experience, and hand off to the editing skills. Chinese or English. Triggers: write a post about these results, draft the blog, turn this experiment into an article, outline the write-up, 把实验写成文章, 起草博客, 写第N篇, 出个提纲. Not for editing an existing draft (use result-writeup-editor)."
version: 0.1.0
---

# Tech Article Draft

Most "blog generator" skills fill a fixed template from a topic. For a write-up of real results the topic is not the problem; the evidence is. This skill drafts from an evidence inventory, so every claim in the draft can be traced to a number, a file, or the author's own statement.

## When to use
The author has results (experiments, audits, comparisons, a project history) and needs a first draft or an outline.

## Process

### 1. Capture four things (ask in one message, at most five questions)
1. **Claim:** the one sentence the reader should remember. If the author cannot say it, the piece is not ready; offer two candidates and ask.
2. **Reader and situation:** who, and what they are stuck on or want to decide.
3. **Evidence inventory:** a table of facts you may use. Each row: fact | number or quote | where it comes from (file, run, the author). Facts from memory are marked unverified and not used as results.
4. **Boundaries:** where the claim stops being true, and what the author does not want said.

If the author declines, draft in scaffold mode: fewer claims, more slots.

### 2. Choose a spine
Pick from `result-writeup-editor/references/heading-spines.md` (experiment post, audit, protocol, multi-round, summary). For a series, fix the spine once.

### 3. Outline with evidence slots
Each chapter: function, one-sentence point, the evidence rows it uses, the figure or table it needs, and any author slot. Show the outline before drafting a long piece.

### 4. Draft
- Open with the reader's situation or the one result that changes what they believe; not with what the post covers.
- One claim per section, with its number or interval next to it.
- State hard mechanisms with the plain-language table (`result-writeup-editor/references/explainer-patterns.md`).
- Add a `design | reason` table where the reader will ask why.
- Titles are names or answers, not captions: no "Name: explainer" shape.
- Wherever the piece needs the author's own experience, a scene, or a stance you do not have, leave a slot: `[AUTHOR: the moment you realised this]`. Keep to the five slots that matter, ranked; mark the most valuable one.
- Never invent anecdotes, quotes, numbers, results, or feelings. A claim without an evidence row is cut or becomes a question.

### 5. Hand back
List the slots (ranked), the stances you wrote on the author's behalf, and facts to verify. Tag every such stance in the draft itself as `[CONFIRM: ...]` so it cannot be published unreviewed. Then route: author fills slots -> `result-writeup-editor` -> `concise-edit` -> `ai-pattern-edit` -> `edit-verification`.

## Title rules
A short noun phrase or the question the page answers; specific enough to pick the piece out of many; no appended explainer after a dash or colon. Put the explanation in the subtitle line.

## Pairing
- Slots and author presence: `human-in-the-loop-writing`.
- Evidence reliability before writing: `preregistered-experiment`, `independent-review`.
- Everything after the draft: `writing-router`.
