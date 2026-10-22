# Shared project handoff

Canonical repository: https://github.com/scenariofour/cee5980-ai-model-selection
Read this with AGENTS.md and ONBOARDING.md before starting. Fetch canonical main to see integrated updates. Branch entries describe that branch until merged.

## Integrated baseline

The public baseline contains the frozen BFCL snapshot, eligibility audit, consequence matrices for two workflows, exact Pareto sets, illustrative weighted and requirement comparisons, sensitivity grids, three figures and an executed notebook. See PRELIMINARY_RESULTS.md and results/summary.json for numbers and limitations.

Source integrity, independent Pareto calculations, scoring checks, notebook execution and figure review were completed for the baseline; details are in results/verification_report.json. These are prior checks, not a claim that every future revision has been validated.

All current weights and thresholds are illustrative. Actual group preference feedback has not been recorded in the public analysis. The study screens configurations; it does not establish deployment readiness or whether older models are more deterministic. Private course/report materials remain outside Git.

## Next useful work

No individual ownership is assigned here yet. At the start of a task, state the selected task and files in your branch's entry; avoid two simultaneous editors of analysis.py.

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

### Entry template

Copy this template for your own branch; preserve existing entries.

- Date / branch / owner (GitHub handle):
- Task and files owned:
- Completed changes:
- Validation run and outcome:
- Open questions / blockers:
- Next concrete step:
- PR link (when available):
