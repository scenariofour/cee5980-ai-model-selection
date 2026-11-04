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

### 2026-11-04 — work/XinruiXu729/member-b-decision-verification

- Owner: XinruiXu729. Role claimed: Member B; initial active analysis editor for this task.
- Files: docs/DECISION_METHODS_AND_EXAMPLES.md, scripts/verify_baseline.py, results/member_b_verification.json, results/member_b_reproduction.json, CHANGELOG.md and this handoff entry.
- Starting state: clean main fast-forwarded to canonical 3acb4a3. Review Member A's unmerged source-audit branch separately; preserve its ownership and changes.
- Completed: reproduced the baseline; added an independent standard-library audit and methods/results prose with four worked selection cases, all-tie policies and three explicitly hypothetical task-call illustrations. Cross-reviewed Member A's PR #6 at b117bd4 against frozen rows and BFCL source checkpoint f7cf735, including seven mode-label disagreements and two all-zero call-score rows; recorded caveats without silently changing eligibility.
- Validation: python analysis.py completed in an isolated requirements-compatible environment; all 16 existing generated artifacts stayed byte-identical. All six notebook code cells executed without errors in an ignored copy. Independent audit verified every eligible consequence, score/rank/Pareto flag, all optima, 1,771 weight vectors and 1,071 requirement pairs per workflow; 30/22 Pareto and 14/0 feasible counts confirmed. Reviewed all three figures, ten documented consequence rows, local links and hypothetical schema/call validity. No analytical code, input, weights, requirements or prior generated outputs changed.
- Review findings: the zero clarification shortlist is conditional on the suffix-based baseline; excluded GLM-4.6 (FC thinking) passes the four frozen requirements. Do not infer failed-run causes solely from zero scores. Member A should refresh its present-tense leaderboard date claim (live page now says 2026-04-12). Pareto-first grid shares omit dominated configurations that would tie at two/four zero-weight boundary vectors; no current Pareto-grid or threshold-grid optimum is tied.
- Handoff to C: no arithmetic correction is needed before working from the existing baseline. After maintainer review of this PR, Member B releases the active shared-code editor role; Member C fetches the integrated handoff before editing shared code. Candidate/validity-rule changes still require an explicit reviewed decision; scale/extreme-row experiments must remain labelled and genuine preference inputs remain private/pending.
- Next: Member C cross-checks these examples, then performs the planned bounded robustness comparisons; Member A reviews the source comments and integrates its own guide via PR. This branch is not merged and does not claim group preference review is complete.

### Entry template

Copy this template for your own branch; preserve existing entries.

- Date / branch / owner (GitHub handle):
- Task and files owned:
- Completed changes:
- Validation run and outcome:
- Open questions / blockers:
- Next concrete step:
- PR link (when available):
