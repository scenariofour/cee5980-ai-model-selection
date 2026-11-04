# BFCL guide for this project

This guide explains the data behind the model screen: what the Berkeley Function Calling Leaderboard (BFCL) measures, what each column we use means, how one row turns into a consequence row, and where the data stop supporting comparisons. It is written for a reader who has not used BFCL before.

Status: Member A deliverable (source audit). It changes no code, raw data, thresholds or results. Items marked **proposed correction** are for the active editor of `analysis.py` to review; they are not applied here.

## 1. Which version of BFCL this is

| Item | Value | Evidence |
| --- | --- | --- |
| Raw file | `data/bfcl_snapshot_2026-10-21.csv`, 109 rows, 36 columns | file itself |
| Retrieved | 2026-10-22 01:08 UTC (2026-10-21 in US Eastern time) from `https://gorilla.cs.berkeley.edu/data_overall.csv` | `data/bfcl_snapshot_manifest.json` |
| SHA256 | `ede5081a24bc5ac7f9b3b09a52af6bcfcd35aa0f1709239fed979db77a8159a6`, rechecked 2026-11-03, matches the manifest | `sha256sum` |
| Benchmark version | BFCL V4, leaderboard marked "Last Updated: 2025-12-16" | leaderboard page [1] |
| Evaluation code | leaderboard states commit `f7cf735`, equivalently PyPI `bfcl-eval==2025.12.17` | leaderboard page [1] |

All code and test files cited below were read from the `bfcl-eval==2025.12.17` release [2], the version the leaderboard names for reproduction. The current GitHub `main` [3] has the same scoring weights and cost formula. The snapshot date is a retrieval date. It is not a model release date, and the file has not been compared with whatever the live CSV says today.

## 2. Function calling in plain language

A model is given a user request plus a list of tools. Each tool is described as a JSON schema: a name, a description and typed parameters, some of them required. The model should either produce a call such as `calculate_triangle_area(base=10, height=5)` or decide that no tool fits and answer in text. BFCL checks whether that decision and the call are right.

**FC versus Prompt.** The leaderboard defines FC as native tool-calling support and Prompt as a workaround that uses the model's normal text generation [1]. In FC mode the tool list goes through the provider's tool interface and the call comes back as structured data. In Prompt mode the tools are written into the system prompt and the call is parsed from text. The same base model can appear in both modes with different scores, so each row is a model plus a mode. This project calls that a configuration.

**AST.** An abstract syntax tree is the parsed structure of a function call: the function name and each argument with its value. BFCL's "AST" categories do not run the function. They parse the model's call and compare its structure to an answer key. In the release code the simple-call checker rejects a call for a wrong function name, a missing required parameter, an unexpected parameter, a wrong type, or a value outside the accepted list [2, `eval_checker/ast_eval/ast_checker.py`]. The answer key can list several acceptable values. For example, an optional `unit` parameter can be either `"units"` or omitted.

## 3. The three test categories used here

**Non-Live Simple AST (structured workflow).** One user turn, one tool, one expected call. Test entries are written by the BFCL team ("non-live"), not collected from real users. The score is the unweighted mean of three sub-sets: Python (400 entries), Java (100) and JavaScript (50) [2, `eval_runner_helper.py` and `data/`]. Because the mean is unweighted, the 50 JavaScript entries carry as much weight as the 400 Python entries.

> Example `simple_python_0`: "Find the area of a triangle with a base of 10 units and height of 5 units." Tool: `calculate_triangle_area(base: integer, height: integer, unit: string)`, with `base` and `height` required. Accepted answer: `base=10`, `height=5`, `unit` either `"units"` or omitted.

**Multi Turn Miss Param (clarification workflow).** 200 multi-turn conversations over simulated APIs such as a file system [2]. In at least one turn the user leaves out information a call needs. The correct behaviour in that turn is to make no call and ask. The user then supplies the detail in a later turn. A conversation counts as correct only if every turn passes. Calls are executed, the end state of the simulated system must match the reference, the model's executed results must contain the reference results, and turns that expect no call must contain none [2, `multi_turn_eval/multi_turn_checker.py`].

> Example `multi_turn_miss_param_0`, turn 4: "Move one of the file in document directory to temp as well ... juxtapose it with 'previous_report.pdf'". The reference has no call for this turn. Turn 5 then says "The specific file is previous_report.pdf.", and only now are `mv` and `diff` expected.

**Irrelevance Detection (avoidance criterion).** Requests that none of the given tools can answer. A test passes when the output contains no decodable function call [2, `eval_runner.py`, `_evaluate_single_relevance_entry`]. The column is the unweighted mean of two sets: non-live `irrelevance` (240 entries) and user-contributed `live_irrelevance` (884) [2].

> Example `irrelevance_0`: "Calculate the area of a triangle given the base is 10 meters and height is 5 meters." The only tool offered is `determine_body_mass_index`. The right output is no call.

Since output that fails to decode also counts as "no call", a configuration that never produces a usable call scores 100% here. Section 7 shows that this happens in the eligible set.

## 4. Metric dictionary

All accuracy columns are percentages of test entries passed, 0 to 100. "Use here" refers to `analysis.py`.

| Original column | Project name | Meaning | Units | Better | Use here | Main limitation |
| --- | --- | --- | --- | --- | --- | --- |
| `Model` | `model` | display name: model plus mode in brackets | text | n/a | ID; the `(FC)` suffix decides eligibility | label does not always match the code's FC flag (section 7) |
| `Non-Live Simple AST` | `structured` | single-call accuracy, unweighted mean of Python/Java/JS sets | % | higher | workflow criterion, structured | static parsing only; small JS set has equal weight |
| `Multi Turn Miss Param` | `clarification` | share of 200 conversations fully correct when a parameter is missing | % | higher | workflow criterion, clarification | simulated APIs; all-or-nothing per conversation |
| `Irrelevance Detection` | `avoidance` | share of no-tool-fits requests answered without a call, mean of 2 sets | % | higher | avoidance criterion, both workflows | rewards silence and broken output equally; not a security measure |
| `Total Cost ($)` | `benchmark_cost` | estimated USD for running the whole BFCL suite once | USD | lower | resource criterion | two different formulas (section 6); not deployment spend |
| `Latency 95th Percentile (s)` | `p95_latency` | 95th percentile of recorded per-call latencies across the whole suite | s | lower | resource criterion | measured from Berkeley's setup; pooled over all categories, not per workflow |
| `Overall Acc` | `overall` | BFCL's weighted headline score | % | higher | comparison baseline only, never in the additive score | contains the avoidance score and other category scores, so adding it would double-count |

Other columns (`Organization`, `License`, latency mean/SD, other categories) are kept in the raw file but not used by the decision model.

## 5. How Overall Acc is built, and a documentation mismatch

The release code computes Overall Acc as a weighted mean of five groups with weights 10, 10, 10, 30 and 40 [2, `eval_runner_helper.py`]:

`Overall = 0.1 × Non-Live + 0.1 × Live + 0.1 × Irrelevance Detection + 0.3 × Multi Turn + 0.4 × Agentic`

Non-Live here is the mean of the four non-live AST columns, and Agentic is the mean of `Web Search Acc` and `Memory Acc`. Using the snapshot's own columns, this formula reproduces `Overall Acc` for all 109 rows within 0.01 points.

**Mismatch to record:** the leaderboard page says Overall Accuracy is the unweighted average of all sub-categories [1]. The code and the data agree with the 10/10/10/30/40 weights instead. The V4 blog [4] describes the score composition in more detail; only its search-indexed text could be read from this workspace. Either way, the conclusion for this project does not change: Overall Acc includes Irrelevance Detection, which is already a criterion here, and is dominated (70%) by multi-turn and agentic tasks. It stays a comparison baseline.

## 6. How cost and latency are produced

From `get_cost_latency_info` in the release code [2]:

- **API models** (a token price is set in the model config): cost = total input tokens × input price + total output tokens × output price, summed over every scored test entry.
- **Locally hosted open models** (no token price): cost = total recorded latency in hours × $23.92 per hour for an 8×H100 node ÷ 100 concurrent requests. This estimates GPU rental time on Berkeley's hardware. It is not a price anyone charges.
- **Latency** for all models: every non-zero per-call latency recorded across the suite is pooled; the column reports the 95th percentile. API latency includes network and provider queueing at the time of the run.

Of the 66 eligible configurations, 27 have token prices (API cost) and 39 use the GPU-time estimate. This mix is the main reason cost is only a rough comparison across rows. For local models cost and latency are also mechanically linked, since cost is computed from latency.

What these columns are **not**: whole-benchmark cost is not deployment spend, which depends on traffic, prompt length and current prices; P95 latency is not a service-level guarantee; and accuracy is not a deployment success rate or evidence of output determinism.

## 7. Worked row: xLAM-2-32b-fc-r (FC)

This configuration is the balanced-profile winner in both workflows (`results/summary.json`), so it is worth reading closely.

| Column | Raw value | Reading |
| --- | --- | --- |
| Model | xLAM-2-32b-fc-r (FC) | Salesforce open model, native FC mode; source config agrees it is FC |
| License | cc-by-nc-4.0 | non-commercial licence as reported in the snapshot |
| Non-Live Simple AST | 80.42% | about 4 in 5 single calls fully correct; the highest structured score in the eligible set |
| Multi Turn Miss Param | 67.50% | about 2 in 3 missing-parameter conversations fully correct |
| Irrelevance Detection | 80.23% | declined to call in about 4 in 5 no-fit requests |
| Total Cost ($) | 6.00 | GPU-time estimate for the whole suite on Berkeley's hardware, not an API bill |
| Latency 95th Percentile (s) | 17.66 | 95% of recorded calls took up to 17.66 s in that setup |
| Overall Acc | 54.66% | rank 18 on BFCL's headline score, not used in our score |

Turning it into values (balanced weights 0.40/0.20/0.20/0.20, structured workflow; anchors are the eligible-set minimum and maximum: cost 0.46 to 355.17, P95 0.96 to 568.59):

- workflow value = 80.42 / 100 = 0.8042
- avoidance value = 80.23 / 100 = 0.8023
- cost value = (355.17 − 6.00) / (355.17 − 0.46) = 0.9844
- latency value = (568.59 − 17.66) / (568.59 − 0.96) = 0.9706
- balanced score = 0.4 × 0.8042 + 0.2 × 0.8023 + 0.2 × 0.9844 + 0.2 × 0.9706 = **0.8731**, matching `value_balanced` in `results/structured_consequence_and_rankings.csv`.

It still fails the illustrative requirement screen in both workflows, because its P95 latency of 17.66 s is above the 15 s limit. Its high cost and latency values come partly from the very wide anchors (section 8).

## 8. Eligibility and comparability audit

The current rule keeps a row if its name ends in `(FC)`, the four score fields are numeric in 0 to 100, cost and P95 are positive, and all fields are finite. Checked against `results/eligibility_audit.csv` and the release model configs [2]:

**8.1 Every exclusion comes from the name suffix.** All 43 excluded rows fail only the `(FC)` test; none fail the numeric or resource checks. Their labels: 34 `(Prompt)`, 1 `(Prompt + Thinking)`, 1 `(FC thinking)`, 7 with no mode label.

**8.2 The suffix and the source's FC flag disagree for 7 rows.** The release config has an `is_fc_model` flag for each configuration. Comparing it with the suffix rule:

| Configuration | Name ends `(FC)` | Source `is_fc_model` | Currently |
| --- | --- | --- | --- |
| GLM-4.6 (FC thinking) | no | True | excluded |
| BitAgent-Bounty-8B | no | True | excluded |
| Arch-Agent-32B | no | True | excluded |
| Arch-Agent-3B | no | True | excluded |
| Arch-Agent-1.5B | no | True | excluded |
| ToolACE-2-8B (FC) | yes | False | included |
| Ministral-8B-Instruct-2410 (FC) | yes | False | included |

(Claude-Haiku-4-5-20251001 has a mislabelled display name in the 2025.12.17 config; current GitHub `main` lists its FC entry with `is_fc_model=True`, consistent with its inclusion.)

GLM-4.6 (FC thinking) matters for the results. Its raw values are clarification 63.00, avoidance 84.96, cost 4.64 and P95 13.50, which pass every illustrative clarification requirement (≥60, ≥80, ≤100, ≤15). The current clarification screen reports 0 feasible configurations. With this row eligible, it would report at least one. This is an observation about the eligibility rule, not a recommendation for that model.

What `is_fc_model` means for local open models with custom handlers has not been confirmed in the documentation, so the flag is evidence, not proof. **Proposed correction:** decide eligibility from an explicit, documented mode list (for example the source flag, or the suffix plus named exceptions) and record the decision for all 7 rows above.

**8.3 Two included rows look like failed runs.** Ministral-8B-Instruct-2410 (FC) and Llama-3.1-Nemotron-Ultra-253B-v1 (FC) score 0% on every non-live, live and multi-turn column and 100% on Irrelevance Detection. Section 3 explains the mechanism: output with no decodable call passes irrelevance tests. Consequences in the current analysis:

- Nemotron-Ultra (cost 0.72, P95 2.40, avoidance 100) is in **both** Pareto sets, because no other row matches its avoidance score at that cost and latency.
- Ministral-8B sets the P95 anchor maximum of 568.59 s, which compresses everyone else's latency values toward 1.

**Proposed correction:** flag configurations with 0% on all call-producing categories as invalid for the avoidance criterion (or exclude them), state the rule, and rerun. This overlaps with Member C's extreme-observation check.

**8.4 Cost is computed two ways.** 27 eligible rows use API token prices; 39 use the GPU-time estimate (section 6). The two are not the same kind of number. A within-type comparison or a sensitivity check that drops cost for the local rows would show how much this matters.

**8.5 Resource ranges are wide and skewed.** Cost runs from 0.46 to 355.17 (median 16.76) and P95 from 0.96 to 568.59 s (median 12.09). Seven eligible rows exceed $100 and twelve exceed 100 s P95. Linear values over these anchors are dominated by a few rows. Member C's log-scale and outlier comparisons address this.

**8.6 Practical availability is not checked.** Thirteen eligible rows carry non-commercial or research-only licences as reported in the snapshot (`cc-by-nc-4.0` and variants, `qwen-research`, `Mistral AI Research License`), including the balanced winner. Licence text in the snapshot has not been verified against the model pages, and nothing here is legal advice. The snapshot also says nothing about whether an API endpoint still exists.

**8.7 Candidate restriction: not recommended yet.** Possible rules, each with an explicit criterion, are listed for group discussion:

1. Mode rule from 8.2 (affects 7 rows).
2. Validity rule from 8.3 (affects 2 rows).
3. Commercial-use rule: drop rows whose snapshot licence forbids commercial use (13 rows), only if the group's decision context is commercial deployment.
4. Cost-type rule: compare API-priced and locally estimated rows separately.

Rules 1 and 2 correct data problems and could apply to the baseline. Rules 3 and 4 change the decision question and should be separately labelled experiments. None was chosen to produce a particular winner.

## 9. Open questions

- Is the 10/10/10/30/40 weighting or the page's "unweighted average" the intended description? The code and data say weighted.
- What exactly does `is_fc_model=False` mean for `ToolACE-2-8B (FC)` and `Ministral-8B-Instruct-2410 (FC)`, which use local handlers?
- The live leaderboard page and blogs could only be read through search-indexed text from this workspace; a direct read of the full pages would confirm sections 2 and 5.
- The raw file has not been compared with the current live CSV, so later corrections by BFCL are unknown.

## Sources

1. BFCL leaderboard page, https://gorilla.cs.berkeley.edu/leaderboard (FC/Prompt definitions, cost/latency notes, Overall Accuracy description, last-updated date, evaluation commit and PyPI version).
2. `bfcl-eval` 2025.12.17 on PyPI, https://pypi.org/project/bfcl-eval/2025.12.17/ : `bfcl_eval/eval_checker/eval_runner_helper.py` (scores, weights, cost, latency), `eval_runner.py` (irrelevance scoring), `ast_eval/ast_checker.py`, `multi_turn_eval/multi_turn_checker.py`, `constants/model_config.py` (FC flags, prices), `constants/eval_config.py` ($23.92/h, 100 concurrent), `data/BFCL_v4_*.json` (test entries and counts).
3. BFCL source on GitHub, https://github.com/ShishirPatil/gorilla/tree/main/berkeley-function-call-leaderboard (`TEST_CATEGORIES.md`; `main` at commit 6ea5797 checked for the same weights and cost formula).
4. BFCL V4 Part 1 blog, https://gorilla.cs.berkeley.edu/blogs/15_bfcl_v4_web_search.html (V4 score composition).
5. Patil et al., "The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models", ICML 2025.
