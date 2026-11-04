# Change log

## BFCL source audit and data guide (Member A)

Added docs/BFCL_GUIDE.md: version provenance, plain-language explanation of function calling, FC/Prompt and AST, the three test categories with real test entries, a metric dictionary, how Overall Acc, cost and P95 latency are computed, a worked row and an eligibility/comparability audit. Updated DATA_SOURCES.md with the evaluation-code source and corrected metric descriptions. Findings for the active analysis editor: the `(FC)` suffix rule disagrees with the source FC flag for 7 configurations, including GLM-4.6 (FC thinking), which would pass the illustrative clarification screen that currently has 0 feasible rows; two included configurations score 0% on every call-producing category and 100% on Irrelevance Detection, one of them in both Pareto sets and the other setting the P95 anchor; cost mixes API token pricing (27 rows) with a GPU-time estimate (39 rows). Validation: rechecked raw SHA256, reproduced Overall Acc for all 109 rows from the release weights, recomputed the worked balanced score, recounted exclusions, licence groups and resource ranges, and read definitions in the `bfcl-eval==2025.12.17` code and data. No code, raw data, thresholds or results changed; proposed corrections are left to the active analysis editor.

## Plan three-person project completion

Added WORK_PLAN.md with proposed roles for BFCL evidence, decision-model verification/practical examples, and robustness/preference review. Each role owns analytical writing and cross-review; shared analysis code has a sequential handoff. Linked the plan from README, onboarding and handoff. Checked saved-result claims, documentation links, dependencies and public/private boundaries. Assignments and feedback are not assumed confirmed. No analytical assumptions, code or numerical outputs changed.

## Clarify completed analysis and reporting

Updated README with the decision case, completed quantitative work, direct result links and remaining preference review. Independently checked the recorded numerical results. Reviewed the private progress update against its assignment prompt and verified one-page local and native layouts. No analysis code, data or numerical outputs changed.

## Single local workspace

Documented one designated working checkout per computer. Added exclusions for local notes, report exports and archived drafting materials. Consolidation retained source history and verified identical files before removing a redundant project copy. Analysis and numerical results are unchanged.

## Shared handoff and ZIP onboarding

Added HANDOFF.md and required agents to read and maintain it. Documented attaching canonical Git history to an extracted ZIP without overwriting local files, and clarified branch/PR synchronization. Checked referenced paths, ZIP contents and the Git-history attachment procedure. No analysis or numerical outputs changed.

## Initial public baseline

Published a frozen public-data screening analysis: data eligibility audit, two workflow consequence matrices, exact Pareto sets, illustrative weighted/threshold comparisons, sensitivity grids, figures and an executed notebook. Input integrity, dominance, scoring and notebook checks passed. Actual stakeholder preferences remain to be collected privately.
