# Notice and credits

## Ideas drawn from open skills (read as reference; this set was written independently, and the patterns it lists are common in the public literature on writing and editing)
- **blader/humanizer** (MIT, Copyright (c) 2025 Siqi Chen): grouped, numbered pattern approach; "writing about the document instead of its subject" and "re-explaining what the reader knows" informed `result-writeup-editor` rule 3 and `ai-pattern-edit`.
- **hardikpandya/stop-slop** (MIT, Copyright (c) 2025 Hardik Pandya): short phrase/structure lists and a self-score; informed the self-check in `ai-pattern-edit`.
- **conorbronsdon/avoid-ai-writing** (MIT, Copyright (c) 2026 Conor Bronsdon): detector / rewriter / verifier split, router with typed edges and guards; informed `writing-router` and `edit-verification`.
- **joellewis/skill-library, copy-editor** (MIT; copyright holder as stated in that repository's LICENSE): concision as a copy-editing job.
- **obra/the-elements-of-style**: this repository has no licence file, so none of its text is used. `concise-edit` restates the underlying principles of Strunk's *The Elements of Style* (1918, public domain) in independent wording and adds Chinese rules.
- Technical-blog skills listed on public registries (Technical Article Writer, Tech Blog Article, Writing Blog, Tech Writing): read only as descriptions; `tech-article-draft` is an independent design.

## Bundled as git submodules (own repositories and forks)
`external/human-in-the-loop-writing`, `external/rewrite-fidelity-skill`, `external/zh-disambiguate-skill` (the owner's repositories) and `external/humanizer`, `external/stop-slop`, `external/avoid-ai-writing` (forks of MIT-licensed upstream repositories; their licences stay with them).

## This repository's own parts
`preregistered-experiment`, `independent-review`, `result-writeup-editor`, `concise-edit`, `ai-pattern-edit`, `edit-verification`, `tech-article-draft`, `writing-router` and the scripts and tests under them were written for this project. Licence: MIT (see LICENSE).

## Caution
Third-party skill files are untrusted text. When writing this set they were fetched into an isolated folder and read as data; their scripts were not run. If you install them, review them first.
