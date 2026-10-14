# The writing chain

```
01 evidence      preregistered-experiment -> independent-review
02 draft         tech-article-draft       (+ human-in-the-loop-writing: author slots, five-question audit)
03 structure     result-writeup-editor    (headings, narration, repetition, explainers, "why" tables)
04 language      concise-edit -> ai-pattern-edit      (Chinese rules and list; English long tail in external/)
05 verify        edit-verification        (runs rewrite-fidelity; one RESULT line)
06 route         writing-router
branch           zh-disambiguate          (Chinese text meant for agents)
```

## Pipelines
| # | Situation | Order | Links |
|---|---|---|---|
| P1 | New article from results | evidence (if claims are strong) -> draft -> author fills slots -> structure -> language -> verify | [01](../01-evidence/README.md) [02](../02-draft/README.md) [03](../03-structure/README.md) [04](../04-language/README.md) [05](../05-verify/README.md) |
| P2 | Trim and restructure an existing document or series | structure -> language (optional) -> verify | [03](../03-structure/README.md) [04](../04-language/README.md) [05](../05-verify/README.md) |
| P3 | "Sounds like AI" | ai-pattern-edit -> verify | [04](../04-language/README.md) |
| P4 | Author absent | human-in-the-loop-writing -> author -> P2 | [02](../02-draft/README.md) |
| P5 | Results not yet trustworthy | preregistered-experiment -> independent-review -> P1 | [01](../01-evidence/README.md) |
| P6 | Check any edit | edit-verification | [05](../05-verify/README.md) |

## Handoffs between stages
Envelope fields and edge types: [handoff contract](../06-route/writing-router/references/handoff-contract.md). Conflicts between skills: [conflict rules](../06-route/writing-router/references/conflict-rules.md).

## Where to improve next
See [ecosystem analysis](ecosystem-analysis.md), section 5.
