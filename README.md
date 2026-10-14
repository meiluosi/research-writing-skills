# Research and writing skills

Skills for getting a result you can trust and writing it up so it stays true. Organised as a chain; each folder is one stage, and every stage links to the next.

```
01 Evidence -> 02 Draft -> 03 Structure -> 04 Language -> 05 Verify
                                                              ^
                                    06 Route (decides order, keeps one handoff envelope)
```

| Stage | Folder | Skills here | External (submodules in `external/`) |
|---|---|---|---|
| 01 Evidence | [`01-evidence`](01-evidence/README.md) | `preregistered-experiment`, `independent-review` | |
| 02 Draft | [`02-draft`](02-draft/README.md) | `tech-article-draft` | `human-in-the-loop-writing` (author presence) |
| 03 Structure | [`03-structure`](03-structure/README.md) | `result-writeup-editor` (document level) | |
| 04 Language | [`04-language`](04-language/README.md) | `concise-edit`, `ai-pattern-edit` | `humanizer`, `stop-slop`, `avoid-ai-writing` (reference forks), `zh-disambiguate` (text for agents) |
| 05 Verify | [`05-verify`](05-verify/README.md) | `edit-verification` | `rewrite-fidelity` (the checker) |
| 06 Route | [`06-route`](06-route/README.md) | `writing-router` | |

Full chain, pipelines and when to use which: [`docs/chain.md`](docs/chain.md). What each skill adds and what is redundant: [`docs/ecosystem-analysis.md`](docs/ecosystem-analysis.md). Reviews and tests: [`verification/`](verification/).

## Install
```bash
git clone --recurse-submodules https://github.com/meiluosi/research-writing-skills.git
cd research-writing-skills && scripts/install.sh        # symlinks every skill into ~/.claude/skills
```
`scripts/install.sh --copy` copies instead of linking. Scripts need Python 3 and the standard library only.

## External repositories
| In `external/` | Upstream | Licence |
|---|---|---|
| `human-in-the-loop-writing`, `rewrite-fidelity-skill`, `zh-disambiguate-skill` | github.com/meiluosi (own repositories; edit them there) | as in each repository |
| `humanizer`, `stop-slop`, `avoid-ai-writing` | forks of blader/humanizer, hardikpandya/stop-slop, conorbronsdon/avoid-ai-writing | MIT, see each |

## Status
Version 0.2 (MIT, see `LICENSE`, credits in `NOTICE.md`). Developed while editing one seven-post Chinese series, tested blind on one further document, reviewed by an independent agent. Not yet used on other kinds of text.
