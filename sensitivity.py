"""Member C's additive sensitivity extension; never writes baseline artifacts."""
import hashlib
import json
import math
from itertools import combinations
import numpy as np
import pandas as pd
from analysis import BASE, PROFILES, SCREEN, WORKFLOWS, load_data, nondominated, value_matrix
import matplotlib.pyplot as plt


def optima(scores):
    return np.flatnonzero(np.isclose(scores, np.max(scores), rtol=0, atol=1e-12)).tolist()


def resource_value(x, anchors, scale):
    a, b = anchors
    assert 0 < a < b
    return np.log(b / x) / np.log(b / a) if scale == 'log' else (b - x) / (b - a)


def scenarios(df):
    anchors = {c: [float(df[c].min()), float(df[c].max())]
               for c in ['benchmark_cost', 'p95_latency']}
    yield 'baseline', df, anchors, 'linear'
    yield 'log_resources', df, anchors, 'log'
    cost = df.benchmark_cost.eq(anchors['benchmark_cost'][1])
    latency = df.p95_latency.eq(anchors['p95_latency'][1])
    for label, mask in [('cost', cost), ('latency', latency), ('union', cost | latency)]:
        sub = df.loc[~mask].reset_index(drop=True)
        yield f'omit_{label}_fixed', sub, anchors, 'linear'
        revised = {c: [float(sub[c].min()), float(sub[c].max())] for c in anchors}
        yield f'omit_{label}_reanchored', sub, revised, 'linear'


def switching_path(values, names, start, end):
    """Maximizing envelope of affine scores; open intervals plus boundary ties."""
    intercept = values @ np.asarray(start)
    slope = values @ (np.asarray(end) - np.asarray(start))
    crossings = [0., 1.]
    for i, j in combinations(range(len(values)), 2):
        if slope[i] != slope[j]:
            t = (intercept[j] - intercept[i]) / (slope[i] - slope[j])
            if 0 < t < 1:
                crossings.append(float(t))
    points = sorted(set(crossings))
    intervals = []
    for left, right in zip(points[:-1], points[1:]):
        winners = [names[i] for i in optima(intercept + slope * ((left + right) / 2))]
        if intervals and intervals[-1]['winners'] == winners:
            intervals[-1]['t_end'] = right
        else:
            intervals.append({'kind': 'interval', 't_start': left, 't_end': right, 'winners': winners})
    rows = []
    for segment in intervals:
        t = segment['t_start']
        rows.append({'kind': 'point', 't_start': t, 't_end': t,
                     'winners': [names[i] for i in optima(intercept + slope * t)]})
        rows.append(segment)
    rows.append({'kind': 'point', 't_start': 1., 't_end': 1.,
                 'winners': [names[i] for i in optima(intercept + slope)]})
    return rows


def requirement_diagnostics(df, workflow):
    fields = [workflow, 'avoidance', 'benchmark_cost', 'p95_latency']
    limits = [SCREEN['performance_min'], SCREEN['avoidance_min'],
              SCREEN['benchmark_cost_max'], SCREEN['p95_latency_max']]
    passes = np.column_stack([df[fields[i]] >= limits[i] if i < 2 else df[fields[i]] <= limits[i]
                              for i in range(4)])
    failures = []
    for i, field in enumerate(fields):
        failures.append({'workflow': workflow, 'kind': 'marginal', 'requirement': field,
                         'count': int((~passes[:, i]).sum())})
    patterns = {}
    for row in passes:
        label = '|'.join(fields[i] for i in range(4) if not row[i]) or 'NONE'
        patterns[label] = patterns.get(label, 0) + 1
    failures += [{'workflow': workflow, 'kind': 'disjoint_pattern', 'requirement': k, 'count': v}
                 for k, v in sorted(patterns.items())]
    boundaries = []
    for i, field in enumerate(fields):
        other = passes[:, [j for j in range(4) if j != i]].all(axis=1)
        boundary = None
        candidates = []
        if other.any():
            boundary = float(df.loc[other, field].max() if i < 2 else df.loc[other, field].min())
            candidates = df.loc[other & df[field].eq(boundary), 'model'].tolist()
            accepted = other & (df[field].ge(boundary) if i < 2 else df[field].le(boundary))
            assert accepted.any()
            # Immediately beyond the first-feasible boundary, the other three rules leave no row.
            stricter = other & (df[field].gt(boundary) if i < 2 else df[field].lt(boundary))
            assert not stricter.any()
        boundaries.append({'workflow': workflow, 'requirement': field, 'original_limit': limits[i],
                           'other_three_pass_count': int(other.sum()), 'first_feasible_boundary': boundary,
                           'boundary_models': json.dumps(candidates),
                           'original_screen_feasible_count': int(passes.all(axis=1).sum())})
    return failures, boundaries


def run():
    raw, df, _, manifest = load_data()
    summary = json.loads((BASE / 'results/summary.json').read_text())
    assert len(raw) == summary['raw_configurations'] and len(df) == summary['eligible_configurations']
    comparisons, paths, failures, boundaries = [], [], [], []
    scenario_list = list(scenarios(df))
    independent_pareto = {}
    scalar_checks = 0
    for name, sub, anchors, scale in scenario_list:
        removed = sorted(set(df.model) - set(sub.model))
        for wf in WORKFLOWS:
            values = np.column_stack([sub[wf] / 100, sub.avoidance / 100,
                                      resource_value(sub.benchmark_cost, anchors['benchmark_cost'], scale),
                                      resource_value(sub.p95_latency, anchors['p95_latency'], scale)])
            assert np.isfinite(values).all() and (values >= -1e-12).all() and (values <= 1+1e-12).all()
            raw_objectives = np.column_stack([sub[wf], sub.avoidance, -sub.benchmark_cost, -sub.p95_latency])
            pareto = nondominated(raw_objectives)
            # Strictly increasing resource-value transforms preserve raw Pareto membership.
            assert np.array_equal(pareto, nondominated(values))
            if name == 'baseline':
                independent = [not any(all(y >= x for x, y in zip(row, other)) and
                                      any(y > x for x, y in zip(row, other))
                                      for other in raw_objectives) for row in raw_objectives]
                assert independent == pareto.tolist()
                independent_pareto[wf] = int(pareto.sum())
                np.testing.assert_allclose(values, value_matrix(df, wf, anchors), rtol=0, atol=1e-14)
                saved = pd.read_csv(BASE / f'results/{wf}_consequence_and_rankings.csv').set_index('model').loc[df.model]
            for profile, weights in PROFILES.items():
                scores = values @ weights
                # Scalar calculation independently checks every scenario's score, including log values.
                for position, (_, row) in enumerate(sub.iterrows()):
                    components = [float(row[wf]) / 100, float(row.avoidance) / 100]
                    for field in ['benchmark_cost', 'p95_latency']:
                        a, b = anchors[field]
                        x = float(row[field])
                        components.append(math.log(b / x) / math.log(b / a) if scale == 'log' else (b-x)/(b-a))
                    assert abs(sum(w*x for w, x in zip(weights, components)) - scores[position]) < 1e-12
                    scalar_checks += 1
                indices = optima(scores)
                winners = sub.iloc[indices].model.tolist()
                assert pareto[indices].all()
                if name == 'baseline':
                    assert winners == summary['workflows'][wf]['profile_winners'][profile]
                    np.testing.assert_allclose(scores, saved['value_' + profile], rtol=0, atol=1e-12)
                baseline_winners = summary['workflows'][wf]['profile_winners'][profile]
                ordered = np.sort(scores)[::-1]
                comparisons.append({'scenario': name, 'workflow': wf, 'profile': profile,
                                    'resource_scale': scale, 'candidate_count': len(sub),
                                    'removed_models': json.dumps(removed), 'anchors': json.dumps(anchors),
                                    'winners': json.dumps(winners), 'best_value': float(scores.max()),
                                    'top_two_gap': float(ordered[0] - ordered[1]),
                                    'same_winner_set_as_baseline': set(winners) == set(baseline_winners)})
    for wf in WORKFLOWS:
        values = value_matrix(df, wf, summary['resource_value_anchors'])
        front = nondominated(np.column_stack([df[wf], df.avoidance, -df.benchmark_cost, -df.p95_latency]))
        shares = np.zeros(int(front.sum()))
        grid_count = 0
        for a in range(21):
            for b in range(21-a):
                for c in range(21-a-b):
                    weights = np.array([a, b, c, 20-a-b-c]) / 20
                    tied = optima(values[front] @ weights)
                    shares[tied] += 1 / len(tied)
                    grid_count += 1
        assert grid_count == summary['preference_grid_size_per_workflow']
        saved_shares = pd.read_csv(BASE / 'results/preference_grid_selection_shares.csv')
        saved_shares = saved_shares.loc[saved_shares.workflow == wf].set_index('model').loc[df.loc[front, 'model']]
        np.testing.assert_allclose(shares / grid_count, saved_shares.selection_share, rtol=0, atol=1e-12)
        assert np.isclose((shares / grid_count).sum(), 1)
        threshold_grid = pd.read_csv(BASE / 'results/threshold_grid.csv')
        threshold_grid = threshold_grid.loc[threshold_grid.workflow == wf]
        assert len(threshold_grid) == summary['threshold_grid_size_per_workflow']
        assert set(zip(threshold_grid.performance_min, threshold_grid.avoidance_min)) == {
            (p, a) for p in range(0, 101, 2) for a in range(0, 101, 5)}
        for row in threshold_grid.itertuples():
            feasible = ((df[wf] >= row.performance_min) & (df.avoidance >= row.avoidance_min) &
                        (df.benchmark_cost <= SCREEN['benchmark_cost_max']) &
                        (df.p95_latency <= SCREEN['p95_latency_max']))
            assert int(feasible.sum()) == row.feasible_count
            choices = sorted(df.loc[feasible].iloc[optima(values[feasible] @ PROFILES['balanced'])].model) if feasible.any() else ['NONE']
            assert row.balanced_choice == choices[0]
        for target in ['quality_focused', 'resource_focused']:
            rows = switching_path(values, df.model.tolist(), PROFILES['balanced'], PROFILES[target])
            for row in rows:
                t = (row['t_start'] + row['t_end']) / 2
                weights = (1-t) * np.array(PROFILES['balanced']) + t * np.array(PROFILES[target])
                assert np.isclose(weights.sum(), 1) and (weights > 0).all()
                assert row['winners'] == df.iloc[optima(values @ weights)].model.tolist()
                paths.append({'workflow': wf, 'target': target, **row,
                              'weights_at_start': json.dumps(((1-row['t_start'])*np.array(PROFILES['balanced']) +
                                                             row['t_start']*np.array(PROFILES[target])).tolist()),
                              'weights_at_end': json.dumps(((1-row['t_end'])*np.array(PROFILES['balanced']) +
                                                           row['t_end']*np.array(PROFILES[target])).tolist())})
            # Dense independent evaluation validates the envelope between analytic boundaries.
            intervals = [r for r in rows if r['kind'] == 'interval']
            for t in np.linspace(0, 1, 1001)[1:-1]:
                segment = next(r for r in intervals if r['t_start'] < t < r['t_end'])
                weights = (1-t)*np.array(PROFILES['balanced']) + t*np.array(PROFILES[target])
                assert segment['winners'] == df.iloc[optima(values @ weights)].model.tolist()
        f, b = requirement_diagnostics(df, wf)
        failures.extend(f)
        boundaries.extend(b)
        assert sum(r['count'] for r in f if r['kind'] == 'disjoint_pattern') == len(df)
        assert b[0]['original_screen_feasible_count'] == summary['workflows'][wf]['illustrative_screen_feasible_count']
    pd.DataFrame(comparisons).to_csv(BASE / 'results/robustness_comparisons.csv', index=False)
    path_df = pd.DataFrame(paths)
    path_df['winners'] = path_df.winners.map(json.dumps)
    path_df.to_csv(BASE / 'results/sensitivity_switching_paths.csv', index=False)
    pd.DataFrame(failures).to_csv(BASE / 'results/sensitivity_requirement_failures.csv', index=False)
    pd.DataFrame(boundaries).to_csv(BASE / 'results/sensitivity_requirement_boundaries.csv', index=False)
    make_figure(df, summary['resource_value_anchors'], paths)
    output_names = ['results/robustness_comparisons.csv', 'results/sensitivity_switching_paths.csv',
                    'results/sensitivity_requirement_failures.csv', 'results/sensitivity_requirement_boundaries.csv',
                    'figures/04_preference_paths.png']
    verification = {'source_sha256': manifest['sha256'], 'raw_count': len(raw), 'eligible_count': len(df),
                    'scenario_count': len(scenario_list), 'comparison_count': len(comparisons),
                    'scalar_scores_checked': scalar_checks, 'independent_baseline_pareto_counts': independent_pareto,
                    'baseline_weight_vectors_checked_per_workflow': grid_count,
                    'baseline_requirement_pairs_checked_per_workflow': len(threshold_grid),
                    'checks': ['input_hash', 'baseline_scores_and_all_profile_winners', 'scale_ranges_and_directions',
                               'pareto_preservation_and_positive_weight_optima', 'all_scenario_scalar_scores',
                               'baseline_pareto_first_grid_shares_and_requirement_grid',
                               'analytic_switches_and_3996_interior_path_checks', 'requirement_boundaries_and_failure_patterns'],
                    'outputs_sha256': {p: hashlib.sha256((BASE / p).read_bytes()).hexdigest() for p in output_names},
                    'participant_review': 'incomplete; no participant responses supplied',
                    'shared_code_handoff': 'pending integration of Member B PR #7; shared code unchanged'}
    (BASE / 'results/member_c_verification.json').write_text(json.dumps(verification, indent=2) + '\n')
    print(json.dumps(verification, indent=2))


def make_figure(df, anchors, paths):
    fig, axes = plt.subplots(2, 2, figsize=(12, 7), layout='constrained')
    for row, wf in enumerate(WORKFLOWS):
        values = value_matrix(df, wf, anchors)
        for col, target in enumerate(['quality_focused', 'resource_focused']):
            ax = axes[row, col]
            relevant = [r for r in paths if r['workflow'] == wf and r['target'] == target]
            names = list(dict.fromkeys(model for r in relevant for model in r['winners']))
            t = np.linspace(0, 1, 200)
            weights = np.array(PROFILES['balanced'])[:, None]*(1-t) + np.array(PROFILES[target])[:, None]*t
            for model in names:
                position = df.index[df.model == model][0]
                ax.plot(t, values[position] @ weights, label=model.replace(' (FC)', ''))
            for r in relevant:
                if r['kind'] == 'point' and 0 < r['t_start'] < 1:
                    ax.axvline(r['t_start'], color='gray', linestyle=':', linewidth=1)
                    ax.text(r['t_start'], .98, f"t={r['t_start']:.4f}", transform=ax.get_xaxis_transform(),
                            ha='right', va='top', fontsize=8)
            ax.set(title=f'{WORKFLOWS[wf]} → {target.replace("_", " ")}',
                   xlabel='t: balanced (0) to target profile (1)', ylabel='Additive value at w(t)')
            ax.legend(fontsize=8, loc='best')
            ax.grid(alpha=.15)
    fig.suptitle('Illustrative preference paths: frozen linear scales; vertical lines mark tied optima')
    fig.savefig(BASE / 'figures/04_preference_paths.png', dpi=180)
    plt.close(fig)


if __name__ == '__main__':
    run()
