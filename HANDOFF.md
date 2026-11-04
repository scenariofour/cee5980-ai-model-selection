# Shared project handoff

Canonical repository: https://github.com/scenariofour/cee5980-ai-model-selection
Read this with AGENTS.md and ONBOARDING.md before starting. Fetch canonical main to see integrated updates. Branch entries describe that branch until merged.

## Integrated baseline

The public baseline contains the frozen BFCL snapshot, eligibility audit, consequence matrices for two workflows, exact Pareto sets, illustrative weighted and requirement comparisons, sensitivity grids, three figures and an executed notebook. See PRELIMINARY_RESULTS.md and results/summary.json for numbers and limitations.

Source integrity, independent Pareto calculations, scoring checks, notebook execution and figure review were completed for the baseline; details are in results/verification_report.json. These are prior checks, not a claim that every future revision has been validated.

All current weights and thresholds are illustrative. Actual group preference feedback has not been recorded in the public analysis. The study screens configurations; it does not establish deployment readiness or whether older models are more deterministic. Private course/report materials remain outside Git.

## Next useful work

The proposed three-role split is in [WORK_PLAN.md](WORK_PLAN.md); individual role claims remain to be confirmed. At the start of a task, state your GitHub handle, selected role/task and files in your branch's entry; avoid two simultaneous editors of analysis.py. Member B verifies the baseline before handing shared analysis editing to Member C for sensitivity work.

1. Reproduce the baseline and audit source metric definitions and candidate comparability.
2. Test sensitivity to value scales/outliers and a narrower practical candidate set.
3. Collect genuine group preference input privately, then document how the review changes the decision framing or recommendation without publishing private responses.
4. Integrate verified findings into the course report and presentation.

## Task entries

### 2026-10-21 — work/scenariofour/shared-handoff

- Files: HANDOFF.md, AGENTS.md, ONBOARDING.md, README.md, CHANGELOG.md.
- Completed: added a shared handoff, required future agents to maintain it, and documented setup from a ZIP without overwriting local work. Analytical code and numerical results were unchanged.
- Validation: checked documentation references, public-file exclusions and the distributable ZIP; checked that a ZIP copy can attach canonical Git history while preserving its files.
- Next: teammates open the extracted folder in Codex, read the three onboarding files, connect GitHub and select one of the bounded tasks above.
- Open: teammate task ownership and actual preference inputs remain to be decided.

### 2026-10-21 — work/scenariofour/canonical-workspace

- Files: AGENTS.md, .gitignore, HANDOFF.md, CHANGELOG.md; local filesystem organization.
- Completed: consolidated the owner's project into one designated desktop checkout, retaining Git history and private materials. Removed the identical starter-folder copy; retained chat deliverable access through links to the canonical files. Archived earlier drafting intermediates privately and retained the existing dependency environment.
- Validation: compared both starter folders byte-for-byte before removal; verified report identity before linking, repository history/remote continuity and deliverable links.
- Next: open the designated folder for future tasks; fetch integrated changes and select the next analysis task. Teammates continue with their own local copies and PRs.
- Analysis: no code, input data or numerical results changed.

### 2026-10-21 — work/scenariofour/update-readiness

- Files: README.md, HANDOFF.md, CHANGELOG.md; private status-report edits remain outside Git.
- Completed: clarified the decision, completed analyses, result-file links and remaining preference review in README. Revised the private one-page update to address amendments, resources, progress against the original plan and next milestones. Applied localized Humanizer prose editing while preserving analytical claims.
- Validation: independently rechecked source integrity, 109/66 configuration counts, Pareto counts of 30/22, 14/0 feasible configurations and 1,771/1,071 sensitivity-grid sizes. Verified report content against computed results; rendered both local and native document versions as one page. Public links and private exclusions checked. No analytical results changed.
- Next: finish participant preference review and the bounded sensitivity refinements listed above. The owner will complete remaining private submission identity fields; each member uses their own submission copy.

### 2026-11-03 — work/scenariofour/three-person-completion-plan

- Files: WORK_PLAN.md, README.md, ONBOARDING.md, HANDOFF.md, CHANGELOG.md.
- Completed: added a public three-role completion plan with technical deliverables, section writing, cross-review, acceptance checks, internal targets and Codex starter prompts. Roles are proposed and use neutral labels until teammates claim them; shared analysis editing passes from baseline verification to sensitivity work.
- Validation: checked baseline claims against saved results, local documentation links, file ownership/dependencies, privacy exclusions and the scoped diff. No analysis, notebook, source data or numerical outputs changed; experiments were not rerun for this documentation task.
- Open: teammate role claims and genuine preference responses remain pending. Private course requirements, response records and submission drafts remain excluded.
- Next: each teammate claims one role with their GitHub handle and starts its first bounded deliverable. A maintainer reviews this plan before merging; this branch entry is not integrated context until merged.
- PR: [#5](https://github.com/scenariofour/cee5980-ai-model-selection/pull/5).

### 2026-11-03 — work/zilingyan110-lang/member-a-bfcl-guide

- Owner: zilingyan110-lang. Role claimed: Member A.
- Files: docs/BFCL_GUIDE.md (new), DATA_SOURCES.md, CHANGELOG.md, HANDOFF.md. No edits to analysis.py, the notebook, raw data or results.
- Completed: source audit against the evaluation code the leaderboard names (`bfcl-eval==2025.12.17`); guide with plain-language definitions, real test entries, metric dictionary, Overall Acc/cost/latency formulas, worked row (xLAM-2-32b-fc-r) and eligibility/comparability audit with candidate-restriction options.
- Validation: raw SHA256 matches the manifest; Overall Acc reproduced for 109/109 rows with weights 10/10/10/30/40; worked balanced score 0.8731 matches the saved output; exclusion reasons (43, all from the suffix rule), FC-flag mismatches, cost types (27 API, 39 GPU estimate), licence and range counts recounted from the files. Live leaderboard and blog pages were read only through search-indexed text.
- Open for the active analysis editor (Member B now): decide the mode rule for the 7 rows in guide section 8.2 (GLM-4.6 (FC thinking) would make the clarification screen non-empty) and a validity rule for the two 0%/100% rows in section 8.3. Commercial-use and cost-type restrictions are left as labelled options for Member C, not applied.
- Next: Member B reviews sections 3 to 8 as cross-reviewer; Member A drafts the private context/data/limitations section and later reviews Member C's sensitivity assumptions.
- PR: PR_URL

### Entry template

Copy this template for your own branch; preserve existing entries.

- Date / branch / owner (GitHub handle):
- Task and files owned:
- Completed changes:
- Validation run and outcome:
- Open questions / blockers:
- Next concrete step:
- PR link (when available):
