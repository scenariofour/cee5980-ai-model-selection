# Preliminary results

Frozen input: 109 configurations; eligible native-FC configurations: 66.
These are completed screening computations, not final deployment recommendations.

**All preference profiles and screening thresholds are illustrative, not stakeholder-elicited.**

## Structured single-turn
- Four-objective Pareto set: 30 configurations.
- balanced: xLAM-2-32b-fc-r (FC)
- quality focused: Hammer2.1-3b (FC)
- resource focused: Gemini-2.5-Flash-Lite (FC)
- Illustrative requirement screen: 14 feasible configurations.
- Best balanced-value feasible candidate(s): Gemini-2.5-Flash (FC)

## Missing-parameter multi-turn
- Four-objective Pareto set: 22 configurations.
- balanced: xLAM-2-32b-fc-r (FC)
- quality focused: xLAM-2-70b-fc-r (FC)
- resource focused: xLAM-2-32b-fc-r (FC)
- Illustrative requirement screen: 0 feasible configurations.
- Best balanced-value feasible candidate(s): none

## Completed checks
- input_hash: passed
- pareto_direction_and_duplicate_checks: passed
- positive_weight_winners_nondominated: passed
- selection_shares_sum_to_one: passed
- manual_score_spot_check: passed

## Boundaries
- Snapshot screening, not confirmation of current endpoint availability.
- All weights and thresholds are illustrative; no group elicitation has occurred.
- Benchmark-wide cost and P95 latency are not workflow-specific operating metrics.
- Benchmark accuracy is not deployment success probability or output determinism.
- Selection share depends on the specified preference grid and tie handling; it is not empirical probability.
- Linear resource scales use observed eligible-set anchors and are sensitive to range/outliers.