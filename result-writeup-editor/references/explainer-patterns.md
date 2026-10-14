# Plain-language explainers

Use when a mechanism is stated only in jargon. Four parts: what is real vs assumed, a human analogy, the exact mechanism, an untested-explanation flag.

## Example (swarm communication modes)

First say what the mechanism is not: real flies do not pass messages; the modes are assumptions used to measure how much shared information is worth.

| Mode | Plain analogy | What actually happens | Real or assumed |
|---|---|---|---|
| Independent | 20 strangers each finding food alone | Each fly learns only from what it eats | Closest to real |
| Gather | Following the crowd without exchanging information | Steering is pulled toward neighbours; learning unchanged | Assumed |
| Observe | "I saw my neighbour eat, I learn a little too" | Flies within 20 units update at half strength when a neighbour eats | Assumed |
| Broadcast | Everyone writing in one shared notebook | Every fly updates at half strength when any fly eats | Not biological; an upper bound |

Then the result, then the reason (marked as untested if it is): "Sharing speeds re-learning after a reversal (untested explanation)."

## Template
1. One sentence: what the reader might wrongly assume.
2. Table: name | analogy | exact mechanism with parameters | real or assumed.
3. Result sentence(s).
4. Reason, labelled tested or untested.

## Rules
- Parameters stay exact (20 units, half strength).
- The analogy explains the idea; it never replaces the mechanism.
- Do not use an analogy that implies a mechanism the system lacks (for example "talking" for broadcast).
