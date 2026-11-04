# Data sources and metric meanings

- Source CSV: https://gorilla.cs.berkeley.edu/data_overall.csv
- Publisher leaderboard and definitions: https://gorilla.cs.berkeley.edu/leaderboard
- Evaluation code named by the leaderboard: `bfcl-eval==2025.12.17` on PyPI (commit `f7cf735`), https://pypi.org/project/bfcl-eval/2025.12.17/
- BFCL source repository: https://github.com/ShishirPatil/gorilla/tree/main/berkeley-function-call-leaderboard
- BFCL V4 methodology: https://gorilla.cs.berkeley.edu/blogs/15_bfcl_v4_web_search.html
- Decision-aiding foundation: Tsoukias (2008), https://doi.org/10.1016/j.ejor.2007.02.039
- Multi-criteria guidance: https://analysisfunction.civilservice.gov.uk/policy-store/an-introductory-guide-to-mcda/

A plain-language explanation of every field used, a worked row and the eligibility/comparability audit are in [docs/BFCL_GUIDE.md](docs/BFCL_GUIDE.md).

The manifest preserves retrieval time and the raw-file SHA256. Snapshot date is a retrieval date, not a model release date or a claim of the latest supported API version. Configuration IDs include evaluation mode. The main analysis retains configurations whose name ends in `(FC)` with valid required numeric fields and positive reported resource values; this is a preliminary inclusion rule, not a deployment-availability check. The suffix disagrees with the source's own FC flag for 7 configurations (guide section 8.2).

Structured workflow uses Non-Live Simple AST, the unweighted mean of Python, Java and JavaScript single-call sets. Clarification workflow uses Multi Turn Miss Param, where a conversation counts only if every turn passes. Irrelevance Detection is the unweighted mean of the non-live and live irrelevance sets; it is a specific benchmark score, not a general security measure, and output with no decodable call also passes it. Total Cost ($) is the estimated cost for the whole benchmark: token prices for API models, an 8×H100 GPU-time estimate for locally hosted models. P95 latency is pooled over the whole benchmark in the reported evaluation environment and is not measured separately for each workflow in this analysis.

Overall Acc is a comparison baseline and is not also included in the additive score, avoiding double-counting its component scores. The release code weights it 10/10/10/30/40 across non-live, live, irrelevance, multi-turn and agentic groups, which reproduces every row; the leaderboard page describes it as an unweighted average. All weights, resource value scales and requirement thresholds are design assumptions. Uniform coverage of a chosen weight grid does not imply a probability model for stakeholder preferences.

Third-party measurements, datasets and source descriptions retain their original attribution and applicable licensing terms. Private course handouts and submission materials are not part of this public repository.
