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

### 2026-11-05 — work/scenariofour/member-c-sensitivity

- Owner: scenariofour. Role claimed: Member C, as assigned by the user. Started from clean canonical main at 3acb4a3 after fetching A/B's pending branches.
- Files: sensitivity.py, tests/test_sensitivity.py, docs/SENSITIVITY_AND_REVIEW.md, results/robustness_comparisons.csv, three results/sensitivity_*.csv tables, results/member_c_verification.json, figures/04_preference_paths.png, CHANGELOG.md and this entry. Private blank preference questions remain in ignored deliverables/member_c/.
- Completed: specified eight scenarios before computation; produced 48 scale/extreme-observation profile comparisons, analytic switching intervals with explicit tied boundaries, requirement-failure partitions and first-feasible boundaries. Added public robustness/review/theory prose and cross-reviewed B's examples at 6b5f761. Prepared identical private questions without inventing responses. Shared analysis.py/notebook and baseline artifacts are unchanged; B's shared-code handoff awaits review/integration of PR #7.
- Findings: fixed-anchor extreme omissions preserve all six profile/workflow winners. Log resource scales change four of six; cost/union omission with reanchoring changes the structured resource-focused winner. Clarification first becomes feasible at a performance floor of 58% or P95 ceiling of 17.66 s when varying that requirement alone; original requirements remain in force. All results are conditional on the existing suffix-based candidate rule.
- Validation: python analysis.py passed and all 18 pre-existing data/result/figure/preliminary artifacts stayed byte-identical. Seven synthetic numerical tests passed; independently checked 3,120 scalar scenario scores, baseline Pareto membership (30/22), all 1,771 preference vectors and 1,071 requirement pairs per workflow, 3,996 interior path points, boundary ties and requirement partitions. Reviewed the new figure. pip check, Python compilation, documentation links and diff whitespace checks passed.
- Open: actual participant responses/review, candidate/validity-rule decisions from A/B, and integration of their unmerged PRs. This extension does not release B's shared-code ownership or establish group consensus.
- Next: A/B review the sensitivity assumptions and outputs; collect three real private preference responses, freeze confirmed comparison inputs, then rerun only approved revisions. Maintainer integrates reviewed PRs and consolidates artifacts.
- PR: pending publication.

### Entry template

Copy this template for your own branch; preserve existing entries.

- Date / branch / owner (GitHub handle):
- Task and files owned:
- Completed changes:
- Validation run and outcome:
- Open questions / blockers:
- Next concrete step:
- PR link (when available):
