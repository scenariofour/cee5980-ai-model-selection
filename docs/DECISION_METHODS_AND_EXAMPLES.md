# Decision methods and worked selection examples

Member B: XinruiXu729. Verified against the frozen baseline on 2026-11-04.
All weights, value scales and minimum requirements below are **illustrative design assumptions**, not elicited group preferences. The examples screen configurations for a proposed task-management agent; they do not demonstrate deployment readiness or observed model behaviour.

## 1. Decision model and reproducibility

The decision is which configuration to shortlist for one of two workflows: structured single-turn tool calls, or multi-turn interactions with missing parameters. Each alternative is a complete `Model` label including its evaluation mode. The two workflows use different benchmark performance columns; avoidance, reported full-benchmark cost and P95 latency stay the same.

The source is [the frozen CSV](../data/bfcl_snapshot_2026-10-21.csv), with retrieval metadata and SHA256 in [the manifest](../data/bfcl_snapshot_manifest.json). The declared rule retains names ending exactly in `(FC)`, four finite score fields in [0, 100] (`overall`, `structured`, `clarification`, `avoidance`), and positive finite cost/latency. This gives 66 of 109 rows; all 43 exclusions fail the suffix rule only. It is a **suffix-based baseline**, not a verified census of all native-FC models. The manifest's prose says three accuracy fields, whereas `load_data()` checks four; the executable rule is stated here without altering source metadata.

Reproduce with an environment satisfying [requirements.txt](../requirements.txt):

```sh
python analysis.py
python scripts/verify_baseline.py --output results/member_b_verification.json
```

The second command independently reconstructs eligibility, consequences, values, Pareto sets, profile ranks/optima, all 1,771 preference vectors and all 1,071 threshold pairs per workflow using scalar standard-library calculations. It never imports `analysis.py`. See [the numerical verification record](../results/member_b_verification.json) and [the reproduction record](../results/member_b_reproduction.json). Notebook execution is recorded separately; the checked-in notebook is preserved.

## 2. Three methods answer different questions

### Pareto filtering: can another configuration improve every criterion?

The four raw objectives are to maximize workflow score and irrelevance detection, and minimize cost and P95 latency. Configuration A dominates B when A is at least as good on all four and strictly better on at least one. In code-independent comparisons the latter two columns are negated. Exact equal consequence vectors do not dominate one another, so duplicates must remain eligible for selection; configuration IDs are unique. There are no identical four-objective vectors in either current workflow.

The exact Pareto sets contain 30 structured and 22 clarification configurations. This filter removes avoidable trade-offs without choosing weights. Being nondominated alone does not make an alternative useful for the proposed agent.

An independently checked structured comparison uses actual rows:

| Configuration | Structured score (%) | Avoidance (%) | Full-benchmark cost (USD) | P95 (s) |
| --- | ---: | ---: | ---: | ---: |
| xLAM-2-32b-fc-r (FC) | 80.42 | 80.23 | 6.00 | 17.66 |
| Gemini-3-Pro-Preview (FC) | 75.50 | 77.85 | 224.69 | 58.48 |

xLAM is better on both scores, costs less and has lower P95, so it dominates this Gemini configuration for these four measured criteria. In clarification the workflow scores are 67.50 versus 56.50, giving the same dominance relation. This says nothing about omitted capabilities or the models' headline Overall Acc.

### Additive value: which compensatory trade-off fits stated preferences?

For workflow score `p`, avoidance `a`, benchmark cost `c` and latency `l`, the value vector is:

```text
v = [p/100, a/100, (355.17-c)/(355.17-0.46), (568.59-l)/(568.59-0.96)]
V = w_performance*v1 + w_avoidance*v2 + w_cost*v3 + w_latency*v4
```

The score anchors for performance/avoidance are the fixed 0–100 benchmark bounds. The resource anchors are the observed minima/maxima among all 66 retained configurations: USD 0.46–355.17 and 0.96–568.59 seconds. Resource denominators are therefore 354.71 and 567.63. Higher value is always better; a resource at the minimum receives 1 and at the maximum receives 0. These anchors are held fixed across the two workflows. New candidates or new anchors constitute a changed model and must be labelled.

| Illustrative profile | Workflow | Avoidance | Cost value | Latency value |
| --- | ---: | ---: | ---: | ---: |
| balanced | 0.40 | 0.20 | 0.20 | 0.20 |
| quality_focused | 0.60 | 0.25 | 0.075 | 0.075 |
| resource_focused | 0.25 | 0.15 | 0.35 | 0.25 |

These weights value improvements **over the stated ranges**. A weight of 0.20 on cost does not mean 20% of a deployment budget. The additive form assumes compensatory, separable values: gains on one criterion can offset losses on another. It is not a causal model or a guarantee of task success. Overall Acc remains a comparison baseline rather than another criterion, to avoid double-counting component scores.

For xLAM-2-32b-fc-r (FC), structured values are approximately `[0.8042, 0.8023, 0.9843816075, 0.9705794267]`. Keeping full precision in the formula:

```text
V_balanced = 0.40*(80.42/100) + 0.20*(80.23/100)
           + 0.20*((355.17-6.00)/354.71)
           + 0.20*((568.59-17.66)/567.63)
           = 0.873132206849922
```

This independently reproduces the saved score. For clarification only the first component changes to 0.6750, giving 0.821452206849922. Competition ranks use `1 + number of strictly larger scores`, so exact equal scores share a rank. Winning sets include every score within absolute tolerance 1e-12 of the maximum; displayed rounding never defines a tie.

### Minimum requirements, then ranking: what is acceptable first?

The illustrative screen requires **all** of:

- workflow score at least 60%;
- avoidance at least 80%;
- whole-benchmark cost at most USD 100;
- reported P95 at most 15 seconds.

Only feasible alternatives are ranked by balanced value. Hard limits cannot be compensated by high performance. The resulting counts are 14 structured and zero clarification configurations. An empty feasible set is reported explicitly rather than silently relaxing the screen.

## 3. Actual consequences used in the worked cases

Names below are exact configuration IDs; scores and resource measurements come from the frozen snapshot.

| Configuration | Structured (%) | Clarification (%) | Avoidance (%) | Benchmark cost (USD) | P95 (s) |
| --- | ---: | ---: | ---: | ---: | ---: |
| xLAM-2-32b-fc-r (FC) | 80.42 | 67.50 | 80.23 | 6.00 | 17.66 |
| Gemini-2.5-Flash-Lite (FC) | 70.92 | 15.00 | 92.50 | 7.55 | 1.67 |
| Gemini-2.5-Flash (FC) | 74.33 | 32.00 | 93.67 | 26.36 | 5.62 |
| xLAM-2-70b-fc-r (FC) | 78.25 | 74.00 | 79.11 | 25.10 | 91.21 |
| Hammer2.1-3b (FC) | 79.33 | 16.00 | 86.12 | 10.89 | 47.44 |

All listed optima are unique under the 1e-12 rule. These are selections from the complete 66-row set, not comparisons limited to this small explanatory table.

### Case 1: structured calls, changing preferences

**Criteria:** structured workflow; no hard screen; compare balanced weights `[0.40, 0.20, 0.20, 0.20]` with resource-focused weights `[0.25, 0.15, 0.35, 0.25]`, using the same candidates and anchors.

**Choice:** balanced selects xLAM-2-32b-fc-r (FC), score 0.873132206850; resource-focused selects Gemini-2.5-Flash-Lite (FC), score 0.908741440533. In the latter profile xLAM scores 0.908573419313, only **0.000168021219** lower. These are unique optima, not ties rounded to three decimals. Under the quality-focused structured profile the unique optimum is Hammer2.1-3b (FC), score 0.832933352888.

**Trade-off and practical reading:** Flash-Lite gives up 9.50 percentage points of structured performance, gains 12.27 points of avoidance and lowers P95 by 15.99 seconds compared with xLAM; its benchmark cost is USD 1.55 higher. Thus “resource-focused” does not mean selecting the cheapest row. For an illustrative task agent receiving already-complete requests, this expresses a stronger preference for resource/response-time and avoidance trade-offs. It does not establish actual response time or accuracy on the task examples below. The small value gap motivates Member C's scale and preference sensitivity work.

### Case 2: structured calls, requirements change the choice

**Criteria:** balanced structured weights plus all four minimum requirements in section 2.

**Choice:** 14 rows pass; the unique balanced-value optimum among them is Gemini-2.5-Flash (FC), score 0.868414606474. It passes with structured 74.33%, avoidance 93.67%, benchmark cost USD 26.36 and P95 5.62 seconds. Without the screen xLAM wins, but its P95 of 17.66 exceeds 15 and excludes it before ranking. Flash-Lite also passes but scores 0.864432205173 under balanced weights.

**Trade-off and practical reading:** compared with xLAM, the screened choice sacrifices 6.09 structured points and costs USD 20.36 more for the benchmark, while gaining 13.44 avoidance points and lowering P95 by 12.04 seconds. A design team treating the reported 15-second limit as essential makes this a hard acceptability decision. The benchmark latency still needs separate deployment validation; the result is not a service guarantee.

### Case 3: clarification, more weight on quality

**Criteria:** clarification workflow; no hard screen; compare balanced and quality-focused profiles with unchanged anchors.

**Choice:** balanced selects xLAM-2-32b-fc-r (FC), score 0.821452206850. Quality-focused selects xLAM-2-70b-fc-r (FC), score 0.774640529078; xLAM-32b scores 0.752197077569 under that same quality-focused profile. Scores under different profiles must not be treated as a common performance scale.

**Trade-off and practical reading:** 70b gains 6.50 clarification points, loses 1.12 avoidance points, raises benchmark cost by USD 19.10 and raises P95 by 73.55 seconds. A team prioritizing fully correct missing-parameter conversations over these measured resource penalties may shortlist it. This does not show that it asks the right question in the hypothetical conversation below. Both profile winners fail the original 15-second screen; they are attractive only under the stated unscreened comparison.

### Case 4: clarification with an empty acceptable set

**Criteria:** the original clarification screen (60%, 80%, USD 100, 15 s); balanced ranking only after screening.

**Choice:** none. Exactly three retained rows reach 60% clarification:

| Configuration | Clarification (%) | Avoidance (%) | Cost (USD) | P95 (s) | Failed limits |
| --- | ---: | ---: | ---: | ---: | --- |
| xLAM-2-32b-fc-r (FC) | 67.50 | 80.23 | 6.00 | 17.66 | latency |
| xLAM-2-70b-fc-r (FC) | 74.00 | 79.11 | 25.10 | 91.21 | avoidance, latency |
| xLAM-2-8b-fc-r (FC) | 65.00 | 63.28 | 20.92 | 108.81 | avoidance, latency |

The other 63 rows fail performance. Across all 66 rows, 32 fail avoidance, seven fail cost and 29 fail latency; these counts overlap and must not be added. This is a consequence of the current candidate rule and requirements, not proof that clarification models are unusable. The action is to review evidence and requirements explicitly, not substitute an infeasible winner. The excluded GLM row discussed in section 6 demonstrates why candidate definition matters.

## 4. Tie and sensitivity-output policies

The preference grid enumerates every nonnegative four-weight vector in steps of 0.05 summing to one: `C(23,3) = 1,771`. It operates on the **Pareto set first** and splits a vector's contribution equally among all maximizing Pareto configurations. Every saved share was independently recomputed. There are no tied Pareto optima on either current grid, and shares sum to one per workflow.

At zero-weight boundaries, dominated configurations can tie if the Pareto filter is omitted: this occurs at two structured and four clarification vectors. They are intentionally absent from the Pareto-first shares. Therefore these results are not shares of all utility maximizers over all 66 rows. They also are not stakeholder preference probabilities or deployment-success probabilities.

The requirement grid contains 51 performance minima (0–100 by 2) times 21 avoidance minima (0–100 by 5), or 1,071 pairs per workflow, holding resource limits at USD 100 and 15 seconds. `balanced_choice` stores a single representative after descending score and alphabetical ID sorting; it is not an all-ties field. Independent enumeration found **zero threshold rows with tied optima** in this baseline. The verifier records every tied set if one appears in future outputs, rather than interpreting the representative as the complete set. Numerical results live in [weight shares](../results/preference_grid_selection_shares.csv) and [threshold grid](../results/threshold_grid.csv).

## 5. Hypothetical task-management illustrations

These conversations and calls are invented teaching examples. **No shortlisted model was run on them**, and the BFCL scores do not measure success on this schema. Assume this single tool is available; it creates a task and cannot answer general questions.

```json
{
  "name": "create_task",
  "description": "Create one task in an existing list with an explicit deadline.",
  "parameters": {
    "type": "object",
    "properties": {
      "title": {"type": "string", "minLength": 1},
      "list_id": {"type": "string", "minLength": 1},
      "due_at": {"type": "string", "format": "date-time"}
    },
    "required": ["title", "list_id", "due_at"],
    "additionalProperties": false
  }
}
```

The deadline must include date, time and UTC offset. List existence and permissions require application checks beyond JSON-schema shape validation.

**Complete request (structured illustration).** User: “Create a task titled Submit draft in list ID course-project, due November 10, 2026 at 5 pm New York time (UTC−05:00).” An illustrative call is:

```json
{"name":"create_task","arguments":{"title":"Submit draft","list_id":"course-project","due_at":"2026-11-10T17:00:00-05:00"}}
```

**Missing parameter (clarification illustration).** User: “Create a task titled Submit draft in list ID course-project.” Assistant: “What date, time and time zone should I use for the deadline?” No call yet: `due_at` is required. User: “November 10, 2026 at 5 pm New York time, UTC−05:00.” The same illustrative call above can then be formed. Inventing a deadline would violate the stated schema/request interpretation.

**No applicable tool (avoidance illustration).** User: “Explain what a Pareto frontier means.” Assistant explains the concept in text; no `create_task` call is appropriate because the user requested no task creation.

## 6. Cross-review of Member A and decisions still open

Reviewed Member A's unmerged [PR #6](https://github.com/scenariofour/cee5980-ai-model-selection/pull/6), branch `work/zilingyan110-lang/member-a-bfcl-guide` at `b117bd4`, including `docs/BFCL_GUIDE.md` and `DATA_SOURCES.md`. This records a cross-review, not a merge or edits to A's files.

The publisher [leaderboard](https://gorilla.cs.berkeley.edu/leaderboard) still points to commit `f7cf735` and `bfcl-eval==2025.12.17`. The fixed [scoring/cost implementation](https://github.com/ShishirPatil/gorilla/blob/f7cf735/berkeley-function-call-leaderboard/bfcl_eval/eval_checker/eval_runner_helper.py), [model configurations](https://github.com/ShishirPatil/gorilla/blob/f7cf735/berkeley-function-call-leaderboard/bfcl_eval/constants/model_config.py), [irrelevance evaluation](https://github.com/ShishirPatil/gorilla/blob/f7cf735/berkeley-function-call-leaderboard/bfcl_eval/eval_checker/eval_runner.py) and [multi-turn checker](https://github.com/ShishirPatil/gorilla/blob/f7cf735/berkeley-function-call-leaderboard/bfcl_eval/eval_checker/multi_turn_eval/multi_turn_checker.py) were inspected. Frozen rows, not today's live CSV, remain the numerical authority.

- **Confirmed:** Overall Acc is excluded from additive criteria; the source code uses group weights 10/10/10/30/40, while the page calls it unweighted. Recalculation from displayed frozen component scores agrees with all 109 headline values within 0.01 percentage points (maximum absolute difference 0.00675). This is a documentation mismatch, not a reason to add Overall Acc as a fifth criterion.
- **Confirmed:** cost is a whole-suite estimate with token-priced and GPU-time paths; P95 pools recorded suite latencies. Scores are category-specific proxies, not deployment guarantees. The executable rule checks four accuracy fields, which A's guide correctly states.
- **Confirmed with mapping cautions:** seven named suffix/`is_fc_model` disagreements in A's table are present in the fixed source. Several Qwen configuration keys share display names but agree on the relevant FC flag and cost type; Claude Haiku 4.5 has erroneous display labels in the fixed configuration file. Exact display-name joining alone is therefore insufficient. These metadata issues need an explicit reviewed mapping, not silent label replacement.
- **Confirmed consequence:** GLM-4.6 (FC thinking) is excluded by the current suffix rule despite a true FC source flag. Its frozen clarification 63.00%, avoidance 84.96%, cost USD 4.64 and P95 13.50 satisfy all four limits. Adding that row would make the clarification set non-empty. This is a labelled eligibility diagnostic, not an adopted revised baseline or a recommendation for GLM.
- **Confirmed observation; cause unproven:** Ministral-8B-Instruct-2410 (FC) and Llama-3.1-Nemotron-Ultra-253B-v1 (FC) have zero call-producing scores and 100% avoidance in the snapshot. No-call/undecodable output can pass irrelevance scoring. The snapshot alone cannot prove why these runs scored zero. Treat them as diagnostic flags rather than automatically declaring invalid runs. Ministral sets the 568.59-second anchor; Nemotron is in both Pareto sets.
- **Update for A:** the live page read on 2026-11-04 displays “Last Updated: 2026-04-12”, whereas A's earlier guide records 2025-12-16. Keep the historical retrieval attribution and update the present-tense page claim when A revises the guide. This does not change the frozen input or evaluation checkpoint.

No arithmetic correction is indicated by the baseline audit. The eligibility and all-zero-row proposals change modelling assumptions and require a reviewed rule; neither has been silently applied. Member C can perform labelled scale/extreme-row experiments on this reproducible baseline, but recommendations must retain these caveats until candidate/validity decisions are integrated. Actual participant inputs and report drafts remain private.

## 7. Handoff and report-ready interpretation

The methods/results/examples prose above is the public analytical draft for Member B's report sections. A report should state the screen and preference profile before naming a winner; report all tied optima; retain whole-benchmark units; and distinguish calculated choices from hypothetical task behaviour. The original normative/constructive framing concerns explicit assumptions followed by genuine design-team review. A priori versus a posteriori denotes the timing of preference articulation, not Bayesian updating, and numerical sensitivity alone does not establish completed constructive review.

Shared analysis code and checked-in generated artifacts are unchanged. No calculation correction is required before Member C starts from the existing baseline. Following maintainer review of this PR, B releases its active-editing claim; C must fetch the integrated handoff before editing shared code. Candidate-rule changes still need a separate reviewed decision. This PR does not claim completed participant review, a merged Member A guide, or final group consensus.
