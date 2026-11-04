# Three-person completion plan

This plan divides the remaining model-selection study into three analytical roles. Each person owns technical work, writes the corresponding interpretation and reviews another person's work. Codex can handle research, calculations, document preparation and Git operations in each teammate's checkout.

Roles A, B and C are proposed assignments, not records of accepted ownership or completed contributions. Each teammate should claim one role with their GitHub handle in their task-branch handoff entry. Agree on role changes before editing shared files; record actual contributions separately from this plan.

## Goal and current baseline

Explain how workflow, preferences and minimum requirements change a shortlist of AI model configurations, using the original normative/constructive decision-analysis framing. Readers should understand the BFCL data and see what different selections mean in practical task examples.

The existing [preliminary results](PRELIMINARY_RESULTS.md) and [summary](results/summary.json) record 109 audited configurations, 66 eligible configurations, Pareto sets of 30 and 22, and illustrative screens with 14 and 0 feasible configurations. Consequence matrices, rankings, sensitivity grids, figures and an executed notebook already exist. This plan does not claim these computations have been rerun or that participant preference review has occurred.

The remaining work is to verify and explain the data, develop worked selection examples, complete bounded robustness checks and document genuine preference review. Public deliverables are reproducibility and methodological material. Submission drafts, course instructions, participant responses and personal forms remain private under [AGENTS.md](AGENTS.md).

## Division of work

| Role | Main responsibility | Writing responsibility | Cross-review responsibility |
| --- | --- | --- | --- |
| Member A | BFCL provenance, metric definitions, eligibility and candidate comparability | Case context, data explanation, metric limitations and source references | Review Member C's sensitivity assumptions and interpretation |
| Member B | Baseline decision-model verification and practical selection examples | Pareto/additive/satisficing methods, baseline results and worked examples | Review Member A's source definitions and eligibility claims |
| Member C | Scale/extreme-observation sensitivity, switching boundaries and preference-review facilitation | Robustness findings, documented preference-review interpretation and theoretical discussion | Review Member B's calculations, criteria and examples |

All three supply their own preferences, write their sections, check the final interpretation and report actual contributions. Member C coordinates review inputs; this does not make Member C responsible for everyone else's writing or for inventing a consensus.

## Member A — Explain the evidence and its limits

**Own:** `DATA_SOURCES.md` and a new `docs/BFCL_GUIDE.md`. Read the raw snapshot, manifest, eligibility audit and relevant analysis code. Keep any report section draft in ignored `deliverables/`.

- [ ] Verify the frozen snapshot SHA256 and inspect inclusion/exclusion reasons without modifying raw data.
- [ ] Check official BFCL sources for the definitions relevant to the frozen columns: native function calling, Non-Live Simple AST, Multi Turn Miss Param, Irrelevance Detection, total benchmark cost and P95 latency. Cite primary sources and record any mismatch between historical data and current descriptions.
- [ ] Explain function calling, test inputs/expected outputs and category-specific evaluation for a reader unfamiliar with BFCL. Explain AST in plain language rather than assuming prior knowledge.
- [ ] Create a metric dictionary containing original column, meaning, units, preferred direction, analytical use and limitation. Explain why Overall Acc is a comparison baseline rather than another additive criterion.
- [ ] Walk through one real configuration row. Distinguish whole-benchmark cost from deployment spend, environment-dependent P95 latency from a service guarantee, and benchmark accuracy from deployment success or determinism.
- [ ] Audit candidate comparability and explain the native-FC/numeric filter. Recommend a narrower practical subset only with explicit criteria and evidence; otherwise describe the unresolved availability/comparability limits.
- [ ] Draft the context/data/limitations sections and verify Member C's sensitivity conclusions against the documented assumptions.

**Acceptance:** a new reader can interpret every selected field and one consequence row; definitions and exclusions are traceable to evidence; unresolved source questions are explicit.

**Handoff to B/C:** verified dictionary, metric caveats, proposed corrections and any defensible candidate-restriction rule. A correction to code or analytical eligibility is reviewed and implemented by the active analysis editor rather than edited concurrently by Member A.

## Member B — Verify the decision model and make choices concrete

**Own:** a new `docs/DECISION_METHODS_AND_EXAMPLES.md`; baseline verification notes. Member B is the initial active editor of `analysis.py` and `analysis.ipynb` if corrections are necessary. Update existing generated outputs only for justified analysis changes, not for prose edits.

- [ ] Reproduce the baseline in an environment satisfying `requirements.txt`; compare the saved results and explain differences.
- [ ] Check eligibility counts, score directions/ranges, Pareto dominance and duplicates, weighted scores, all tied optima and sensitivity-grid integrity. Independently verify at least one dominance comparison and additive-score calculation.
- [ ] Explain the distinction between Pareto filtering, compensatory additive ranking and minimum-requirement screening followed by ranking. Document value anchors, weight order and illustrative thresholds.
- [ ] Prepare at least three worked selection cases using actual result rows. Each includes workflow, exact criteria, selected configuration, raw consequences, trade-off and a practical interpretation.
- [ ] Cover a preference change, a requirement-induced change and the empty clarification shortlist. Baseline examples include balanced versus resource-focused structured selection, the screened structured choice, and balanced versus quality-focused clarification selection. Recheck configuration IDs and numbers before publishing.
- [ ] Define a small hypothetical `create_task` schema with explicit required fields. Show a complete request, a request needing clarification and a request requiring no tool call. Label conversations and calls as hypothetical illustrations, not observed model responses; do not assert that a selected model has been tested on them.
- [ ] Draft the methods/results/examples sections and cross-check Member A's source definitions and eligibility explanation.

**Acceptance:** each example follows criteria → reproducible choice → practical trade-off. All numbers match the current saved outputs, no tie is hidden and illustrative weights/requirements remain labeled.

**Handoff to C:** baseline verification record, integrated code corrections if any, result-table locations and example comparisons. Member B's analysis PR must be reviewed and merged by an authorized maintainer before Member C begins editing shared analysis code. If no correction is needed, record that the code-editing handoff can proceed from the existing baseline.

## Member C — Test robustness and interpret preference review

**Own:** a new `docs/SENSITIVITY_AND_REVIEW.md`; proposed `results/robustness_comparisons.csv` and an additional figure only if needed. Become the active editor of `analysis.py` and `analysis.ipynb` after Member B's explicit handoff. Keep actual responses and filled decision logs private.

- [ ] State comparisons before running them. Compare baseline linear resource-value scales with log-scaled values, holding eligible configurations, workflow/avoidance scales and weights fixed. Specify anchors and formulas; explain that weights over changed scales imply changed trade-offs.
- [ ] Check dependence on extreme observations by separately omitting maximum-cost configurations, maximum-latency configurations and their union, including tied maxima. Hold baseline anchors fixed first; recompute anchors only as a separately labeled experiment. Preserve the baseline and raw data.
- [ ] Use any narrower candidate-set experiment only after Member A supplies a defensible rule. Do not choose restrictions to obtain a preferred winner.
- [ ] Show which winners or shortlists change and which remain stable. Explain at least one preference-switching interval with a specified path for all four weights summing to one; preserve tied optima.
- [ ] Explain why the clarification screen has no feasible candidate using requirement failure counts and trade-offs. Treat grid boundaries as intervals; verify exact values from consequences before reporting precise switching thresholds. Keep the original illustrative requirements visible.
- [ ] Prepare the same private questions for all three participants: workflow, objectives, essential/negotiable requirements and valued improvements over stated consequence ranges. Obtain actual answers, dates and prior result exposure; never simulate participant evidence.
- [ ] Freeze confirmed inputs before a designated comparison, then collect review reactions to the trade-offs/examples. Log retained assumptions, revisions and disagreement. Distinguish changes to objectives, metric relevance, scales, candidates, weights and requirements. Existing exploratory results prevent a claim of fully blind initial elicitation.
- [ ] Publish only methodological interpretation that respects the private-response boundary. Explain how explicit calculations and actual revisions relate to normative and constructive decision aiding. If responses remain unavailable, disclose that the group-review stage is incomplete and keep the analysis illustrative.
- [ ] Draft the robustness/review/theory sections and verify Member B's calculations and practical claims.

**Acceptance:** changes in selection are reproducible and attributable to specified assumptions. Every claimed participant judgment has genuine private provenance; sensitivity analysis alone is not presented as completed participant co-construction.

## Schedule and dependencies

Dates are proposed internal project targets for 2026 and should be revised together if needed. Official course/submission requirements remain in private materials.

| Target | Member A | Member B | Member C | Gate |
| --- | --- | --- | --- | --- |
| Nov 3–6 | Audit definitions and exclusions | Reproduce and verify the baseline | Prepare private preference questions and begin collecting actual responses | Source questions and initial inputs recorded |
| Nov 7–10 | Finish guide; review examples for metric misuse | Finish methods/examples and any baseline corrections | Specify sensitivity comparisons without editing B's active code | B hands off shared analysis editing after review/integration |
| Nov 11–20 | Review sensitivity assumptions | Check comparison outputs and clarify examples | Run robustness checks and facilitate genuine preference review | Reproducible switches and accurate review status |
| Nov 21–25 | Draft context/data/limitations | Draft methods/results/examples | Draft robustness/review/theory | Each person supplies a complete section and citations |
| Nov 26–Dec 4 | Review C's sections | Review A's sections | Review B's sections | Group resolves substantive comments and agrees on the analysis freeze |
| Dec 5–10 | Audit source claims and references | Independently check calculations and example values | Check final figures, sensitivity claims and review provenance | One authorized maintainer regenerates consolidated artifacts; all review final report |

No role should wait for every other task: A's source audit, B's baseline reproduction and C's question preparation can begin independently. C's code changes wait for B's handoff; the final interpretation waits for verified outputs and an honest account of available feedback.

## Codex workflow for each teammate

1. Open your own designated checkout. Read [AGENTS.md](AGENTS.md), [ONBOARDING.md](ONBOARDING.md), [HANDOFF.md](HANDOFF.md) and this plan. Fetch canonical main and preserve existing work.
2. Claim a role in your branch's handoff entry with your GitHub handle and exact task/files. Use `work/<github-login>/<topic>` branches. The handoff records intent; coordination and PR review remain necessary.
3. Ask Codex to complete one bounded deliverable, verify it, update the handoff/changelog, commit only relevant public files, push and open a PR against canonical main. Private drafts stay ignored. No teammate needs to run Git commands manually.
4. Review your assigned teammate's deliverable against its acceptance conditions. Record substantive issues and checks actually performed. The maintainer merges reviewed PRs only when explicitly asked; teammates then fetch the integrated changes.
5. Keep one active editor of shared analysis code. Reconcile concurrent handoff/changelog additions rather than replacing another contributor's entry. At final integration, one maintainer regenerates consolidated artifacts and others cross-check them.

For analysis changes, run `python analysis.py` in the configured environment and all required checks in AGENTS.md, execute all cells of an edited notebook and inspect changed plots. For documentation-only work, verify affected claims and links without rerunning unrelated experiments. Counts are baseline observations, not targets to preserve after justified corrections.

### Member A starter prompt

> Read AGENTS.md, ONBOARDING.md, HANDOFF.md and WORK_PLAN.md. I am taking Member A. Fetch canonical main, preserve existing work and create my task branch. Audit BFCL definitions, provenance, eligibility and candidate comparability; write DATA_SOURCES.md and docs/BFCL_GUIDE.md with primary-source support and a worked row. Keep raw data immutable and private report drafts ignored. Verify claims/links, update handoff/changelog, push and open a PR. Do not edit shared analysis code concurrently with its active owner.

### Member B starter prompt

> Read AGENTS.md, ONBOARDING.md, HANDOFF.md and WORK_PLAN.md. I am taking Member B. Fetch canonical main, preserve existing work and create my task branch. Reproduce and independently verify the baseline, then write docs/DECISION_METHODS_AND_EXAMPLES.md with actual values, exact selection criteria and labeled hypothetical task examples. Coordinate any corrections to analysis.py and its notebook as the initial active editor. Verify the deliverable, update handoff/changelog, push and open a PR; record the code-editing handoff for Member C after review/integration.

### Member C starter prompt

> Read AGENTS.md, ONBOARDING.md, HANDOFF.md and WORK_PLAN.md. I am taking Member C. Fetch canonical main and preserve existing work. Prepare genuine private preference questions and specify bounded scale/extreme-observation comparisons. Begin shared analysis edits only after Member B's recorded handoff and integration of any corrections. Produce reproducible sensitivity outputs and docs/SENSITIVITY_AND_REVIEW.md; retain responses privately and disclose incomplete feedback. Run required checks, update handoff/changelog, push and open a PR. Do not invent preferences or group consensus.

## Final completion checklist

- [ ] A reader unfamiliar with BFCL can understand the data before reading rankings.
- [ ] At least three worked examples connect different criteria to selections and practical trade-offs.
- [ ] Baseline and robustness outputs reproduce, with assumptions and ties documented.
- [ ] Preference-review status and theoretical interpretation reflect what actually occurred.
- [ ] Every person supplies analytical writing and completes their assigned cross-review.
- [ ] Report numbers, examples, figures and citations agree with the final integrated artifacts.
- [ ] Private participant records, course materials, personal forms and submission drafts remain outside Git.
- [ ] All participants review the final private report against the applicable template/instructions; optional presentation work is shared if needed.

Codex assistance does not replace participants' own judgments or evidence of actual contributions. This plan describes intended work; completed contributions belong in verified handoff entries and private reporting records.
