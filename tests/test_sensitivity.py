"""Small counterexamples for the sensitivity calculations' numerical risks."""
import unittest
import numpy as np
import pandas as pd
import sensitivity as s


class SensitivityTests(unittest.TestCase):
    def test_log_scale_endpoints_and_proportional_midpoint(self):
        actual = s.resource_value(np.array([1., 10., 100.]), (1., 100.), 'log')
        np.testing.assert_allclose(actual, [1., .5, 0.], atol=1e-14)

    def test_extreme_omission_keeps_all_tied_maxima_out(self):
        df = pd.DataFrame({'model': ['a', 'b', 'c', 'd'],
                           'benchmark_cost': [100., 100., 10., 1.],
                           'p95_latency': [1., 2., 20., 3.]})
        scenarios = {name: (subset, anchors, scale) for name, subset, anchors, scale in s.scenarios(df)}
        self.assertEqual(scenarios['omit_cost_fixed'][0].model.tolist(), ['c', 'd'])
        self.assertEqual(scenarios['omit_union_fixed'][0].model.tolist(), ['d'])
        self.assertEqual(scenarios['omit_cost_fixed'][1]['benchmark_cost'], [1., 100.])
        self.assertEqual(scenarios['omit_cost_reanchored'][1]['benchmark_cost'], [1., 10.])

    def test_switch_preserves_crossing_ties_and_identical_alternatives(self):
        # A and duplicate A win before t=.5; B wins after; all tie at .5.
        values = np.array([[1., 0.], [1., 0.], [0., 1.]])
        rows = s.switching_path(values, ['a', 'a2', 'b'], [1., 0.], [0., 1.])
        intervals = [r for r in rows if r['kind'] == 'interval']
        self.assertEqual([(r['t_start'], r['t_end'], r['winners']) for r in intervals],
                         [(0., .5, ['a', 'a2']), (.5, 1., ['b'])])
        middle = [r for r in rows if r['kind'] == 'point' and r['t_start'] == .5]
        self.assertEqual(middle[0]['winners'], ['a', 'a2', 'b'])

    def test_unswitched_path_includes_endpoint_only_tie(self):
        rows = s.switching_path(np.array([[1., 1.], [0., 1.]]), ['a', 'b'], [1., 0.], [0., 1.])
        self.assertEqual([r['winners'] for r in rows if r['kind'] == 'interval'], [['a']])
        self.assertEqual(rows[-1]['winners'], ['a', 'b'])

    def test_tolerance_does_not_hide_close_but_distinct_winner(self):
        self.assertEqual(s.optima(np.array([.9, .9+1e-8])), [1])
        self.assertEqual(s.optima(np.array([.9, .9+1e-13])), [0, 1])

    def test_path_finds_winner_that_is_neither_endpoint_winner(self):
        rows = s.switching_path(np.array([[1., 0.], [.75, .75], [0., 1.]]),
                                ['a', 'middle', 'b'], [1., 0.], [0., 1.])
        intervals = [r for r in rows if r['kind'] == 'interval']
        self.assertEqual([(r['t_start'], r['t_end'], r['winners']) for r in intervals],
                         [(0., .25, ['a']), (.25, .75, ['middle']), (.75, 1., ['b'])])

    def test_requirement_boundary_includes_ties_and_impossible_single_relaxation(self):
        df = pd.DataFrame({'model': ['a', 'b', 'c'], 'clarification': [60., 60., 58.],
                           'avoidance': [80., 80., 80.], 'benchmark_cost': [1., 2., 1.],
                           'p95_latency': [17., 17., 15.]})
        failures, boundaries = s.requirement_diagnostics(df, 'clarification')
        by_field = {r['requirement']: r for r in boundaries}
        self.assertEqual(by_field['p95_latency']['first_feasible_boundary'], 17.)
        self.assertEqual(by_field['p95_latency']['boundary_models'], '["a", "b"]')
        self.assertEqual(by_field['clarification']['first_feasible_boundary'], 58.)
        self.assertIsNone(by_field['avoidance']['first_feasible_boundary'])
        self.assertEqual(sum(r['count'] for r in failures if r['kind'] == 'disjoint_pattern'), 3)


if __name__ == '__main__':
    unittest.main()
