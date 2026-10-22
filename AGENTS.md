# Collaboration instructions

## Canonical project and scope

Repository: https://github.com/scenariofour/cee5980-ai-model-selection
Canonical integration branch: main.
Bootstrap exception: the initial reviewed public import may create and publish main. Subsequent work follows the task-branch and PR workflow below.
Read README.md, ONBOARDING.md and PRELIMINARY_RESULTS.md before changing the analysis. This is a course project on multiobjective decision framing, model screening, Pareto trade-offs, preference timing and sensitivity. Keep the original normative/constructive question as the interpretive foundation. Do not turn it into building a new AI product or a broad benchmark leaderboard.

You are not alone in this codebase. Preserve others' changes and work only on the current task. Do not silently alter source data, assumptions, thresholds or metric meanings to obtain a desired winner. Existing weighting profiles and thresholds are illustrative; actual group feedback must be supplied by participants.

## Session start and ownership

1. Inspect git status, current branch, remotes and recent commits. Never reset, clean, stash or overwrite pre-existing work to obtain a clean checkout.
2. Fetch the canonical repository before beginning. Update a clean local main only by fast-forward. Work on a task branch named work/<github-login>/<short-topic>, not on main. Reuse an existing branch only for the same unfinished task.
3. State the files owned by this task. Keep one active editor for analysis.py. Data preparation, decision models and sensitivity interpretation can be separate tasks, but changes to shared code must be coordinated through PRs. Prefer task-specific modules or analysis notes only when the task warrants them; do not preemptively refactor.
4. Do not edit a shared Google Doc by replacing its entire contents. Read the relevant section and current revision; make scoped edits so collaborators' changes remain intact. The private TEAM_LINKS.md, when present, contains the shared document URL.

## Complete each coding task and synchronize automatically

When the requested task is complete, run the relevant checks, inspect the diff and commit only files belonging to this task. Do not use git add . or git add -A indiscriminately. Update CHANGELOG.md with the substantive change, assumptions and validation. Do not include another person's uncommitted work.

Before pushing, fetch canonical main again. If it has advanced, integrate it into your task branch using a normal merge, preserving published history. Resolve only conflicts that can be understood and verified. If resolution is ambiguous, stop that merge and report the conflicting files; continue independent work where possible. Never claim that fetching or pushing guarantees the absence of semantic conflicts.

Push your task branch automatically and open or update a PR against canonical main using the available GitHub tool or gh CLI. The PR must describe the final change, validation and any modified assumptions. Check its conflict/mergeability status after the remote update and report the branch, commit and PR URL. Do not force-push, delete someone else's branch, push directly to main or auto-merge. A maintainer can ask Codex to integrate reviewed PRs; no teammate needs to operate Git commands manually.

If the authenticated user cannot push to the canonical repo, use that user's existing fork, or create a fork under that user's account, push the task branch there and open a PR to canonical main. Keep the canonical remote available; do not overwrite another user's authentication or share access tokens. If GitHub authentication is unavailable, keep the verified work locally and report the single setup step required; do not invent a successful push.

## Checks and generated files

For analysis changes run python analysis.py in an environment satisfying requirements.txt. Verify the frozen input SHA256, eligibility count, score directions/ranges, Pareto dominance and ties, and sensitivity-output integrity. Review changed plots. A changed valid result is acceptable if its cause is explained; do not tune results merely to preserve the original 30/22 counts.

For notebook edits execute all code cells and check for errors. For documentation-only tasks, verify the affected claims/links rather than rerunning unrelated experiments. Generated figures, CSVs and notebooks are shared artifacts: regenerate and commit them only when the current task requires it, and explain numerical changes. At final integration, one maintainer regenerates the consolidated artifacts.

Keep raw snapshot data immutable. Separate benchmark results from optional local API experiments. Whole-benchmark cost is not deployment spend; accuracy is not output determinism; preference-grid share is not a deployment-success probability. A priori/a posteriori refers to preference timing here, not Bayesian updating. Group feedback is not evidence of enterprise-wide preferences.

## Public repository boundaries

Keep private course documents, submission drafts, NetIDs, actual contribution forms, the filled group decision log and shared-document access links outside Git. They are excluded by .gitignore. Do not override these exclusions or publish secrets/credentials. Public code, source-attributed benchmark measurements and computed results belong in the repo. No paid API calls are needed for the core study.

## Finish report

Give a short summary of changes, checks, results affected, branch/commit and PR link. Identify remaining decisions or access requirements accurately. Do not say main has been updated until the merge is verified. Changes in a local ZIP do not update the canonical repository; use branches and PRs.
