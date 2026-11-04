"""Independently audit saved BFCL screening outputs using only the standard library.

Run from any directory: python scripts/verify_baseline.py
Optional: --output results/member_b_verification.json
Does not import analysis.py or overwrite baseline artifacts. Numerical tolerance
for additive optima matches the documented absolute tolerance of 1e-12.
"""
import argparse
import csv
import hashlib
import itertools
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOL = 1e-12
FIELDS = {
    'Overall Acc': 'overall', 'Non-Live Simple AST': 'structured',
    'Multi Turn Miss Param': 'clarification', 'Irrelevance Detection': 'avoidance',
    'Total Cost ($)': 'benchmark_cost', 'Latency 95th Percentile (s)': 'p95_latency',
}


def read_csv(path):
    with (ROOT / path).open(newline='') as f:
        return list(csv.DictReader(f))


def close(a, b):
    return math.isclose(float(a), float(b), rel_tol=0, abs_tol=TOL)


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def dominates(a, b):
    return all(x >= y for x, y in zip(a, b)) and any(x > y for x, y in zip(a, b))


def frontier(points):
    # Scalar pairwise comparisons independent of production NumPy broadcasting.
    return [i for i, b in enumerate(points)
            if not any(dominates(a, b) for j, a in enumerate(points) if i != j)]


def optima(scores, indices):
    indices = list(indices)
    if not indices:
        return []
    best = max(scores[i] for i in indices)
    return [i for i in indices if close(scores[i], best)]


def verify():
    summary = json.loads((ROOT / 'results/summary.json').read_text())
    check(summary['profiles_order'] == ['workflow_performance', 'avoidance', 'cost_value', 'latency_value'],
          'Weight order')
    manifest = json.loads((ROOT / 'data/bfcl_snapshot_manifest.json').read_text())
    raw_path = 'data/bfcl_snapshot_2026-10-21.csv'
    digest = hashlib.sha256((ROOT / raw_path).read_bytes()).hexdigest()
    check(digest == manifest['sha256'] == summary['source_sha256'], 'Frozen input hash')
    raw = read_csv(raw_path)
    candidates, audits = [], []
    for row in raw:
        values = {}
        for original, key in FIELDS.items():
            try:
                values[key] = float(row[original].replace('%', ''))
            except ValueError:
                values[key] = float('nan')
        flags = {
            'native_fc': row['Model'].endswith('(FC)'),
            'valid_score_fields': all(0 <= values[c] <= 100 for c in
                                      ['overall', 'structured', 'clarification', 'avoidance']),
            'positive_resource_fields': all(values[c] > 0 for c in ['benchmark_cost', 'p95_latency']),
            'finite_fields': all(math.isfinite(x) for x in values.values()),
        }
        included = all(flags.values())
        audits.append({'model': row['Model'], **flags, 'included': included})
        if included:
            candidates.append({'model': row['Model'], **values})
    check(len(raw) == manifest['records'] == summary['raw_configurations'], 'Raw count')
    check(len(candidates) == summary['eligible_configurations'], 'Eligibility count')
    check(len({r['model'] for r in candidates}) == len(candidates), 'Unique IDs')
    saved_audit = read_csv('results/eligibility_audit.csv')
    check(len(saved_audit) == len(audits), 'Audit row count')
    for expected, saved in zip(audits, saved_audit):
        check(expected['model'] == saved['model'], 'Audit ID/order')
        for key, value in expected.items():
            if key != 'model':
                check(str(value) == saved[key], f'Audit {key}: {expected["model"]}')
    clean = read_csv('data/eligible_configurations.csv')
    check(len(clean) == len(candidates), 'Saved eligible count')
    for expected, saved in zip(candidates, clean):
        check(expected['model'] == saved['model'], 'Eligible ID/order')
        for key in FIELDS.values():
            check(close(expected[key], saved[key]), f'Eligible field {key}')
    anchors = {key: [min(r[key] for r in candidates), max(r[key] for r in candidates)]
               for key in ['benchmark_cost', 'p95_latency']}
    check(anchors == summary['resource_value_anchors'], 'Anchor values')
    check(frontier([(1, 1), (2, 1), (1, 2), (0, 0), (2, 1)]) == [1, 2, 4],
          'Independent dominance direction, strictness and duplicate check')
    # Cartesian construction differs from the production nested-sum loops.
    grid = [w + (20 - sum(w),) for w in itertools.product(range(21), repeat=3) if sum(w) <= 20]
    check(len(grid) == math.comb(23, 3) == summary['preference_grid_size_per_workflow'], 'Weight grid')
    frequency = read_csv('results/preference_grid_selection_shares.csv')
    thresholds = read_csv('results/threshold_grid.csv')
    screen = summary['illustrative_screen']
    all_ids = list(range(len(candidates)))
    report = {'status': 'passed', 'source_sha256': digest, 'raw_configurations': len(raw),
              'eligible_configurations': len(candidates), 'checks': [
                  'frozen source hash and counts', 'every eligibility flag and eligible consequence',
                  'value anchors, ranges and score directions', 'pairwise Pareto sets and duplicate policy',
                  'every profile score, competition rank and tied optimum',
                  'all Pareto-only preference-grid allocations including zero-weight ties',
                  'every threshold-grid feasible count, representative and all tied optima'],
              'workflows': {}}
    for workflow in ['structured', 'clarification']:
        def vector(row):
            return (row[workflow] / 100, row['avoidance'] / 100,
                    (anchors['benchmark_cost'][1] - row['benchmark_cost']) / (anchors['benchmark_cost'][1] - anchors['benchmark_cost'][0]),
                    (anchors['p95_latency'][1] - row['p95_latency']) / (anchors['p95_latency'][1] - anchors['p95_latency'][0]))
        values = [vector(r) for r in candidates]
        check(all(0 <= x <= 1 for v in values for x in v), 'Value ranges')
        points = [(r[workflow], r['avoidance'], -r['benchmark_cost'], -r['p95_latency']) for r in candidates]
        front = frontier(points)
        ids = lambda indices: sorted(candidates[i]['model'] for i in indices)
        saved = read_csv(f'results/{workflow}_consequence_and_rankings.csv')
        check(len(saved) == len(candidates), 'Consequence count')
        by_id = {r['model']: r for r in saved}
        check(set(by_id) == set(ids(all_ids)), 'Consequence IDs')
        check(ids(front) == sorted(r['model'] for r in read_csv(f'results/{workflow}_pareto_set.csv')), 'Saved Pareto set')
        check(len(front) == summary['workflows'][workflow]['pareto_count'], 'Pareto count')
        profile_winners, scores_by_profile = {}, {}
        for profile, weights in summary['illustrative_profiles'].items():
            check(close(sum(weights), 1) and min(weights) > 0, 'Positive profile weights')
            scores = [math.fsum(w * x for w, x in zip(weights, v)) for v in values]
            scores_by_profile[profile] = scores
            best = optima(scores, all_ids)
            check(set(best) <= set(front), 'Positive-weight winner nondominance')
            profile_winners[profile] = ids(best)
            check(ids(best) == sorted(summary['workflows'][workflow]['profile_winners'][profile]), 'Summary winners/ties')
            for i, row in enumerate(candidates):
                observed = by_id[row['model']]
                check(close(scores[i], observed['value_' + profile]), f'Additive score: {row["model"]}')
                rank = 1 + sum(score > scores[i] for score in scores)
                check(rank == int(observed['rank_' + profile]), 'Competition rank')
        for i, row in enumerate(candidates):
            observed = by_id[row['model']]
            check(observed['pareto'] == str(i in front), 'Pareto flag')
            for key in FIELDS.values():
                check(close(row[key], observed[key]), f'Consequence {key}')
        def feasible(pmin, amin):
            return [i for i, r in enumerate(candidates) if r[workflow] >= pmin and r['avoidance'] >= amin
                    and r['benchmark_cost'] <= screen['benchmark_cost_max'] and r['p95_latency'] <= screen['p95_latency_max']]
        f = feasible(screen['performance_min'], screen['avoidance_min'])
        check(len(f) == summary['workflows'][workflow]['illustrative_screen_feasible_count'], 'Screen count')
        check(ids(optima(scores_by_profile['balanced'], f)) == sorted(summary['workflows'][workflow]['illustrative_screen_winners']), 'Screen optima')
        for i, row in enumerate(candidates):
            check(by_id[row['model']]['illustrative_screen_pass'] == str(i in f), 'Screen flag')
        shares = {i: 0.0 for i in front}
        multiway, dominated_tie_vectors = 0, 0
        for ints in grid:
            scores = [math.fsum(w / 20 * x for w, x in zip(ints, v)) for v in values]
            winners = optima(scores, front)
            multiway += len(winners) > 1
            if set(optima(scores, all_ids)) - set(front):
                dominated_tie_vectors += 1
            for i in winners:
                shares[i] += 1 / (len(winners) * len(grid))
        saved_shares = [r for r in frequency if r['workflow'] == workflow]
        check(len(saved_shares) == len(front) and {r['model'] for r in saved_shares} == set(ids(front)), 'Share rows/IDs')
        check(close(sum(float(r['selection_share']) for r in saved_shares), 1), 'Share total')
        for row in saved_shares:
            i = next(i for i in front if candidates[i]['model'] == row['model'])
            check(close(shares[i], row['selection_share']), 'Every grid share')
            check(int(row['weight_vectors']) == len(grid), 'Grid denominator')
        saved_thresholds = [r for r in thresholds if r['workflow'] == workflow]
        expected_pairs = set(itertools.product(range(0, 101, 2), range(0, 101, 5)))
        check(len(saved_thresholds) == len(expected_pairs) == summary['threshold_grid_size_per_workflow'], 'Threshold count')
        check({(int(r['performance_min']), int(r['avoidance_min'])) for r in saved_thresholds} == expected_pairs, 'Threshold coverage')
        threshold_ties = []
        for row in saved_thresholds:
            feasible_ids = feasible(float(row['performance_min']), float(row['avoidance_min']))
            winners = ids(optima(scores_by_profile['balanced'], feasible_ids))
            check(int(row['feasible_count']) == len(feasible_ids), 'Threshold feasible count')
            check(row['balanced_choice'] == (winners[0] if winners else 'NONE'), 'Threshold representative')
            if len(winners) > 1:
                threshold_ties.append({'performance_min': int(row['performance_min']),
                                       'avoidance_min': int(row['avoidance_min']), 'all_winners': winners})
        a = next(i for i, r in enumerate(candidates) if r['model'] == 'xLAM-2-32b-fc-r (FC)')
        b = next(i for i, r in enumerate(candidates) if r['model'] == 'Gemini-3-Pro-Preview (FC)')
        check(dominates(points[a], points[b]), 'Worked dominance comparison')
        report['workflows'][workflow] = {
            'pareto_count': len(front), 'profile_winners': profile_winners,
            'screen_feasible_count': len(f), 'screen_winners': ids(optima(scores_by_profile['balanced'], f)),
            'consequence_duplicate_groups': [ids(group) for point in set(points)
                                            if len(group := [i for i, p in enumerate(points) if p == point]) > 1],
            'preference_vectors': len(grid), 'pareto_grid_vectors_with_tied_winners': multiway,
            'vectors_where_dominated_candidates_would_also_tie_if_not_filtered': dominated_tie_vectors,
            'threshold_pairs': len(saved_thresholds), 'threshold_ties': threshold_ties,
            'dominance_example': {'dominator': candidates[a]['model'], 'dominated': candidates[b]['model']},
            'worked_balanced_score': scores_by_profile['balanced'][a],
            'screen_failure_counts_nonexclusive': {
                'workflow': sum(r[workflow] < screen['performance_min'] for r in candidates),
                'avoidance': sum(r['avoidance'] < screen['avoidance_min'] for r in candidates),
                'cost': sum(r['benchmark_cost'] > screen['benchmark_cost_max'] for r in candidates),
                'latency': sum(r['p95_latency'] > screen['p95_latency_max'] for r in candidates)}}
    check(len(frequency) == sum(report['workflows'][w]['pareto_count'] for w in report['workflows']), 'No extra share rows')
    check(len(thresholds) == 2 * summary['threshold_grid_size_per_workflow'], 'No extra threshold rows')
    report['interpretation'] = 'Verification of the declared suffix-based baseline, not validation of deployment suitability or participant preferences.'
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = verify()
    serialized = json.dumps(result, indent=2) + '\n'
    if args.output:
        args.output.write_text(serialized)
    print(serialized, end='')
