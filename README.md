# Skills

Two families that work together: **research process** (get a result you can trust) and **writing** (say it clearly and keep it true). `writing-router` connects them.

```
            results you can trust                         a document readers can use
  preregistered-experiment -> independent-review  ->  tech-article-draft -> result-writeup-editor -> concise-edit -> ai-pattern-edit
                                   ^                                                 |                 |               |
                                   |_____________ ESCALATE (claim may be wrong) ____|_________________|_______________|
                                                                                     v
                                                                              preservation-check  (required after any edit)
```

| Skill | Level | One line |
|---|---|---|
| [`preregistered-experiment`](preregistered-experiment/SKILL.md) | process | Register hypotheses and decision rules before running; freeze with hashes; verdict rules; deviation log |
| [`independent-review`](independent-review/SKILL.md) | process | Context-free sub-agent review for leakage, no-op baselines, broken controls, overclaiming |
| [`tech-article-draft`](tech-article-draft/SKILL.md) | writing | Draft from an evidence inventory, with slots for the author's experience |
| [`result-writeup-editor`](result-writeup-editor/SKILL.md) | writing, **document level** | Heading spine, narration to statements, subtraction, plain-language explainers, "why" tables, number check |
| [`concise-edit`](concise-edit/SKILL.md) | writing, sentence level | Omit needless words, active voice, concrete; English and Chinese rules |
| [`ai-pattern-edit`](ai-pattern-edit/SKILL.md) | writing, style | Remove machine-sounding patterns; Chinese list; domain-term guard |
| [`preservation-check`](preservation-check/SKILL.md) | verification | Numbers, literals, verdict words, claim strength, hedges, negations before vs after |
| [`writing-router`](writing-router/SKILL.md) | routing | Which skill, in what order, with one handoff envelope and guards |

## What is different here
Existing writing skills mostly edit sentences or generate articles from a topic. This set adds:
- an editor for the **document level** of result-heavy writing (headings, narration, repetition, hard mechanisms), with measurable metrics (`result-writeup-editor/scripts/doc_metrics.py`);
- a verification step wired into every editing skill (`preservation-check/scripts/preserve.py`, with tests);
- **Chinese-first** pattern lists and rules;
- explicit conflict rules between skills (author voice vs cutting narration, hedges vs concision), written in `writing-router/references/conflict-rules.md`.

## External skills used when installed
| Skill | Source | Used for |
|---|---|---|
| `human-in-the-loop-writing` | github.com/meiluosi/human-in-the-loop-writing | Author presence, five-question audit |
| `rewrite-fidelity` | github.com/meiluosi/rewrite-fidelity-skill | Strict meaning check |
| `zh-disambiguate` | github.com/meiluosi/zh-disambiguate-skill | Chinese text meant for agents |
| `humanizer`, `stop-slop`, `avoid-ai-writing` | see `NOTICE.md` | Longer English pattern lists |

## Install
Copy the folders you want into `~/.claude/skills/` (or a project's `.claude/skills/`). Scripts need Python 3 and the standard library.

## Status
Version 0.2. The writing family was developed while editing one seven-post Chinese series, then tested blind on one further document and reviewed by an independent agent; fixes from both are included. It has not been used on other kinds of text. Reviews are in `verification/`; scope and credits are in `NOTICE.md`.
