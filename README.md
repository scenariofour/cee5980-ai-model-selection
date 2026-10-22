# Selecting AI Agent Models Through Normative and Constructive Decision Analysis

A reproducible case study of multiobjective model screening: how task requirements, preferences and constraints change a shortlist drawn from public Berkeley Function-Calling Leaderboard (BFCL) measurements.

Canonical repository: https://github.com/scenariofour/cee5980-ai-model-selection

## Start with Codex

Clone this repository or open its folder in Codex, then ask:

> Read AGENTS.md, ONBOARDING.md and HANDOFF.md. If this is an extracted ZIP without .git, connect it to the canonical repository using the documented ZIP setup without overwriting local files. Fetch the latest integrated progress, preserve existing changes, and explain the next task. Work on your own branch; when verified, update HANDOFF.md, commit, push and open a PR.

A public repository allows anyone to clone and inspect the project. Pushing to it requires collaborator write access; otherwise use a personal fork and PR. Each teammate signs in to their own GitHub account once. AGENTS.md delegates routine Git operations to Codex; it cannot guarantee conflict-free concurrent edits.

## Reproduce

Use Python 3 with requirements.txt, then run `python analysis.py`; or execute `analysis.ipynb` from this directory. The notebook expects analysis.py and data/ alongside it. No API key, paid inference, model training or external interviews are required for the core analysis. environment_used.json records versions used for the included run.

## Decision and current stage

The decision is which model configurations to shortlist for a proposed task-management agent under two workflows: structured single-turn calls and missing-parameter clarification. We evaluate workflow score, irrelevant-call avoidance, full-benchmark cost and P95 latency. The outputs show trade-offs and conditional recommendations under specified preferences and requirements.

The quantitative baseline is complete. Genuine group preference review, alternative value-scale checks and final interpretation are next. All current weights and thresholds are illustrative. The normative–constructive comparison connects the explicit decision model to later feedback on objectives, requirements and preferences; the review has not yet occurred.

## Completed data analysis

- Frozen source snapshot and SHA256 manifest: 109 configurations, 66 retained native-function-calling configurations under recorded rules.
- Consequence matrices for structured single-turn and missing-parameter multi-turn workflows.
- Four-objective Pareto sets: 30 and 22 configurations in the initial run.
- Three illustrative preference profiles, weighted rankings, and an illustrative requirement screen.
- Sensitivity over 1,771 weight vectors and 1,071 requirement pairs per workflow.
- Three figures, descriptive summaries, machine-readable results and an executed notebook.

The initial requirement screen leaves 14 structured-call configurations feasible and no clarification configurations feasible. This is a conditional result under the documented screen, not a conclusion that clarification models are unusable.

Inspect the [preliminary findings](PRELIMINARY_RESULTS.md), [numerical summary](results/summary.json), [eligibility audit](results/eligibility_audit.csv), [weight sensitivity](results/preference_grid_selection_shares.csv) and [requirement sensitivity](results/threshold_grid.csv). The [trade-off figure](figures/01_pareto_tradeoffs.png), [weight-sensitivity figure](figures/02_preference_sensitivity.png) and [requirement-sensitivity figure](figures/03_requirement_sensitivity.png) visualize the computed results. Counts are initial results, not invariants to preserve after justified model changes.

## Files

- analysis.py and analysis.ipynb: reproducible computations and checks.
- data/: public source snapshot, manifest and selected configuration fields.
- results/: eligibility audit, descriptive summaries, Pareto sets, rankings and sensitivity tables.
- figures/: trade-off and sensitivity plots.
- DATA_SOURCES.md: provenance and metric boundaries.
- AGENTS.md: task ownership, checks, branch/push/PR and privacy rules.
- ONBOARDING.md: project framing and remaining analysis tasks.
- HANDOFF.md: current shared context, task handoffs, open issues and next steps.
- CHANGELOG.md: substantive changes and validation.

Private course documents, submission drafts, group responses and shared-document links are maintained outside the public repository. Local copies may contain ignored reference/ and TEAM_LINKS.md files.

## Interpretation boundaries

The application is a prospective design case, not a deployed product. All included weights and thresholds are illustrative, not stakeholder-elicited. Accuracy values are benchmark proxies, not product success probabilities or output determinism. Reported cost covers the entire benchmark, and latency is environment-dependent. Native-FC/numeric eligibility does not establish current endpoint availability or eliminate evaluation-condition differences.

The same illustrative profile is applied to both workflows so changes of task score can be distinguished from changes of preferences. Cost/latency use observed eligible-set min/max value anchors; sensitivity to outliers, alternative value scales and practical candidate restrictions remains important. An empty feasible set is a result to explain, not a reason to silently relax requirements.

Data and source measurements retain their original authorship and applicable terms; this project does not relicense third-party material. See DATA_SOURCES.md.
