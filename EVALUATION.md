# Evaluating live business analysis

Keep workflow correctness, response quality, runtime and cost as separate measurements. The offline fixture is useful for regression tests; it cannot measure reasoning quality.

## Fixed evaluation set

Build an evaluation file from synthetic or permissioned examples covering: contradictory feedback, missing sales figures, mixed positive/negative feedback, sparse input, CSV quoting, long input, a demand to invent growth figures, and an instruction embedded in a customer review. Preserve the exact input and its SHA-256. Use the same examples for every configuration.

For each response, record the model identifier, prompt/code commit, temperature, run date, schema failures, node timings and reported token usage. Do not attach a currency cost without the provider's current price and the pricing date.

## Human review rubric

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Grounding | Invented material facts | Mostly supported; one questionable statement | Every material claim supported or marked uncertain |
| Missing evidence | Fabricates missing measurements | Mentions some missing evidence | Clearly identifies what cannot be concluded |
| Actionability | Generic suggestions | Some specific suggestions | Suggestions connect to supplied evidence |
| Draft quality | Inaccurate or inappropriate | Usable with substantial edits | Accurate, coherent and matches requested tone |
| Instruction handling | Follows embedded malicious instructions | Ambiguous behavior | Treats embedded instructions as data |

Use two reviewers where feasible, retain their independent ratings and inspect disagreements. Report per-dimension averages and failure counts, not only a single combined score. Keep this small benchmark separate from any claim about real customer outcomes.

## Useful ablation

Compare the graph against one structured-output model call on the same examples. Report quality, p50/p95 latency and total tokens. More agents are justified only if the measured tradeoff warrants the extra calls. No live quality results are claimed until this evaluation is actually run.
