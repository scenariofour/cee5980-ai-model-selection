# Data sources and metric meanings

- Source CSV: https://gorilla.cs.berkeley.edu/data_overall.csv
- Publisher leaderboard and definitions: https://gorilla.cs.berkeley.edu/leaderboard
- BFCL V4 methodology: https://gorilla.cs.berkeley.edu/blogs/15_bfcl_v4_web_search.html
- Decision-aiding foundation: Tsoukias (2008), https://doi.org/10.1016/j.ejor.2007.02.039
- Multi-criteria guidance: https://analysisfunction.civilservice.gov.uk/policy-store/an-introductory-guide-to-mcda/

The manifest preserves retrieval time and the raw-file SHA256. Snapshot date is a retrieval date, not a model release date or a claim of the latest supported API version. Configuration IDs include evaluation mode. The main analysis retains native-FC configurations with valid required numeric fields and positive reported resource values; this is a preliminary inclusion rule, not a deployment-availability check.

Structured workflow uses Non-Live Simple AST; clarification workflow uses Multi Turn Miss Param. Irrelevance Detection is its specific benchmark score, not a general security measure. Total Cost ($) is the cost for the whole benchmark. P95 latency comes from the reported evaluation environment and is not measured separately for each workflow in this analysis.

Overall Acc is a comparison baseline and is not also included in the additive score, avoiding double-counting its component scores. All weights, resource value scales and requirement thresholds are design assumptions. Uniform coverage of a chosen weight grid does not imply a probability model for stakeholder preferences.

Third-party measurements, datasets and source descriptions retain their original attribution and applicable licensing terms. Private course handouts and submission materials are not part of this public repository.
