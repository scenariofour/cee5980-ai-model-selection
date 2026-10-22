# Project onboarding

## Research question

Which model configurations are attractive for structured single-turn versus missing-parameter multi-turn tool use, and how do preferences and minimum requirements change the recommendation? This bounded design case applies normative and constructive decision-aiding ideas through explicit quantitative evaluation and a documented preference-review process.

## Course contribution

Make multiobjective framing, Pareto trade-offs and a priori versus a posteriori preference timing central. Use values/objectives, decisions, uncertain conditions and consequences; commensuration/additive value; satisficing; sensitivity; robustness and vulnerability. Calculate the finite candidate set directly rather than adding an MOEA solely to name an algorithm. Do not confuse preference timing with Bayesian prior/posterior probabilities or equate one calculation method with an entire normative/constructive approach.

## Current analysis

Read PRELIMINARY_RESULTS.md, results/summary.json and analysis.py. All current weighting profiles and thresholds are illustrative. Separate measured data from judgments and forecasts. Source data are frozen; future changes must be explicit and traceable. The current analysis is model screening, not evidence of deployment readiness or a causal effect of model age.

## Next useful tasks

1. Reproduce and inspect the source definitions and candidate comparability.
2. Check alternate value scales/outlier treatment and a narrower practical candidate set.
3. Obtain short, genuine preference statements from the actual design team through a private log, review trade-offs and document resulting revisions.
4. Explain recommendation-switching boundaries, assumptions and transfer limits.
5. Use verified results in the private course report, with numbered figures and references and accurate technical contributions.

Keep the project manageable and primarily reproducible from public data. Each member owns analytical work and cross-checks another part. Preserve others' changes and use AGENTS.md for Git synchronization. Private submission requirements and shared-document URLs are not published in this repository.

## Starting from the team ZIP

1. Download and extract AI_Model_Selection_Starter.zip into a normal local folder, then open the extracted AI_Model_Selection_Starter folder as a project in Codex. The ZIP is a snapshot; it does not include .git or automatically track later updates.
2. Ask Codex to read AGENTS.md, ONBOARDING.md and HANDOFF.md, connect this folder to the canonical repository, fetch current work and state the next task before editing. See README.md for a ready-to-paste prompt.
3. Agent setup when .git is absent: clone the canonical repository into a new temporary sibling directory, verify its origin URL, then move only that clone's .git directory into this folder if .git is still absent. A normal clone supplies the matching index and history while leaving every extracted file untouched. Inspect git status and the diff before continuing. Preserve local/private files and treat any differences as existing work; do not discard or publish them indiscriminately. Do not use git init followed by an unrelated root commit. Remove only the disposable clone you created after the transfer succeeds.
4. If .git already exists, inspect it and use its history; do not replace it. Follow AGENTS.md for task branches and merging canonical updates while preserving local edits.
5. Sign in to your own GitHub account when publishing changes. Codex can use a fork and PR if you lack canonical write access. GitHub login is not needed just to run the local analysis.
6. At task completion, Codex updates HANDOFF.md, validates changes and pushes a task branch with a PR. Once the PR is reviewed and merged, others fetch it to receive the integrated handoff and work.
