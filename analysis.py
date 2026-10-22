"""Reproduce preliminary decision analysis from a frozen public BFCL snapshot.
No model API calls, private data, or elicited stakeholder preferences are used.
"""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent
FIELDS = {
    'Model': 'model', 'Overall Acc': 'overall',
    'Non-Live Simple AST': 'structured',
    'Multi Turn Miss Param': 'clarification',
    'Irrelevance Detection': 'avoidance',
    'Total Cost ($)': 'benchmark_cost',
    'Latency 95th Percentile (s)': 'p95_latency',
}
WORKFLOWS = {'structured': 'Structured single-turn', 'clarification': 'Missing-parameter multi-turn'}
PROFILES = {
    'balanced': [.40, .20, .20, .20],
    'quality_focused': [.60, .25, .075, .075],
    'resource_focused': [.25, .15, .35, .25],
}
# Order: workflow score, irrelevant-call avoidance, benchmark-cost value, latency value.
# Profiles and screening thresholds are illustrative assumptions, not elicited group preferences.
SCREEN = {'performance_min': 60., 'avoidance_min': 80., 'benchmark_cost_max': 100., 'p95_latency_max': 15.}


def nondominated(maximize):
    """Exact Pareto filtering: all columns higher-is-better; preserve exact duplicates."""
    x = np.asarray(maximize, dtype=float)
    return np.array([not np.any(np.all(x >= row, axis=1) & np.any(x > row, axis=1)) for row in x])


def preference_grid(step=20):
    # Every four-criterion nonnegative weight vector at increments of 1/step.
    return np.array([(a,b,c,step-a-b-c) for a in range(step+1)
                     for b in range(step-a+1) for c in range(step-a-b+1)], dtype=float) / step


def load_data():
    raw_path = BASE/'data'/'bfcl_snapshot_2026-10-21.csv'
    metadata = json.loads((BASE/'data'/'bfcl_snapshot_manifest.json').read_text())
    assert hashlib.sha256(raw_path.read_bytes()).hexdigest() == metadata['sha256'], 'Frozen input changed'
    raw = pd.read_csv(raw_path)
    df = raw[list(FIELDS)].rename(columns=FIELDS).copy()
    for col in list(FIELDS.values())[1:]:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace('%','',regex=False), errors='coerce')
    native = df['model'].str.endswith('(FC)', na=False)
    score_valid = df[['overall','structured','clarification','avoidance']].apply(lambda s:s.between(0,100)).all(axis=1)
    resource_valid = df[['benchmark_cost','p95_latency']].gt(0).all(axis=1)
    finite = np.isfinite(df.select_dtypes('number')).all(axis=1)
    keep = native & score_valid & resource_valid & finite
    audit = pd.DataFrame({'model':df.model,'native_fc':native,'valid_score_fields':score_valid,
                          'positive_resource_fields':resource_valid,'finite_fields':finite,'included':keep})
    clean = df.loc[keep].reset_index(drop=True)
    assert clean.model.is_unique, 'Duplicate configuration IDs require explicit handling'
    return raw, clean, audit, metadata


def value_matrix(df, workflow, anchors):
    c0,c1 = anchors['benchmark_cost']
    l0,l1 = anchors['p95_latency']
    return np.column_stack([df[workflow]/100, df.avoidance/100,
                            (c1-df.benchmark_cost)/(c1-c0), (l1-df.p95_latency)/(l1-l0)])


def run():
    for folder in ['results','figures']:(BASE/folder).mkdir(exist_ok=True)
    raw, df, audit, source = load_data()
    df.to_csv(BASE/'data'/'eligible_configurations.csv', index=False)
    audit.to_csv(BASE/'results'/'eligibility_audit.csv', index=False)
    df.select_dtypes('number').describe().to_csv(BASE/'results'/'descriptive_statistics.csv')
    df.select_dtypes('number').corr().to_csv(BASE/'results'/'cross_configuration_correlations.csv')
    anchors = {c:[float(df[c].min()),float(df[c].max())] for c in ['benchmark_cost','p95_latency']}
    grid = preference_grid()
    assert grid.shape == (1771,4) and np.allclose(grid.sum(axis=1),1)
    # Direction and duplicate checks independent of the real data.
    assert nondominated([[1,1],[2,1],[1,2],[0,0]]).tolist() == [False,True,True,False]
    assert nondominated([[1,1],[1,1]]).all()
    scenario_results = {}; rankings = []; frequency_rows=[]; threshold_rows=[]
    for wf, label in WORKFLOWS.items():
        performance = df[wf].to_numpy()
        pareto = nondominated(np.column_stack([performance,df.avoidance,-df.benchmark_cost,-df.p95_latency]))
        v = value_matrix(df,wf,anchors)
        assert np.isfinite(v).all() and (v >= -1e-12).all() and (v <= 1+1e-12).all()
        out = df.copy();out['pareto'] = pareto
        winners = {}
        for name, weights in PROFILES.items():
            assert np.isclose(sum(weights),1) and min(weights)>0
            score = v @ np.asarray(weights)
            out['value_'+name] = score
            out['rank_'+name] = pd.Series(score).rank(ascending=False,method='min').astype(int)
            tied = np.isclose(score,score.max(),rtol=0,atol=1e-12)
            assert pareto[tied].all(), 'Positive-weight winner must be nondominated'
            winners[name] = df.loc[tied,'model'].tolist()
        feasible = ((performance >= SCREEN['performance_min']) & (df.avoidance >= SCREEN['avoidance_min']) &
                    (df.benchmark_cost <= SCREEN['benchmark_cost_max']) & (df.p95_latency <= SCREEN['p95_latency_max']))
        out['illustrative_screen_pass'] = feasible
        screen_winners = []
        if feasible.any():
            best = out.loc[feasible,'value_balanced'].max()
            screen_winners = out.loc[feasible & np.isclose(out.value_balanced,best,rtol=0,atol=1e-12),'model'].tolist()
        front = df.loc[pareto].copy()
        scores = v[pareto] @ grid.T
        top = scores.max(axis=0,keepdims=True)
        ties = np.isclose(scores,top,rtol=0,atol=1e-12)
        shares = (ties/ties.sum(axis=0,keepdims=True)).mean(axis=1)
        assert np.isclose(shares.sum(),1)
        for model,share in zip(front.model,shares):
            frequency_rows.append({'workflow':wf,'model':model,'selection_share':float(share),'weight_vectors':len(grid)})
        for pmin in range(0,101,2):
            for rmin in range(0,101,5):
                f = ((performance>=pmin)&(df.avoidance>=rmin)&
                     (df.benchmark_cost<=SCREEN['benchmark_cost_max'])&(df.p95_latency<=SCREEN['p95_latency_max']))
                chosen='NONE'
                if f.any():
                    chosen=out.loc[f].sort_values(['value_balanced','model'],ascending=[False,True]).iloc[0]['model']
                threshold_rows.append({'workflow':wf,'performance_min':pmin,'avoidance_min':rmin,
                                       'feasible_count':int(f.sum()),'balanced_choice':chosen})
        out.sort_values('value_balanced',ascending=False).to_csv(BASE/'results'/f'{wf}_consequence_and_rankings.csv',index=False)
        front.to_csv(BASE/'results'/f'{wf}_pareto_set.csv',index=False)
        scenario_results[wf]={'pareto_count':int(pareto.sum()),'profile_winners':winners,
                              'illustrative_screen_feasible_count':int(feasible.sum()),
                              'illustrative_screen_winners':screen_winners}
        out['workflow']=wf;rankings.append(out)
    combined=pd.concat(rankings,ignore_index=True)
    frequency=pd.DataFrame(frequency_rows);frequency.to_csv(BASE/'results'/'preference_grid_selection_shares.csv',index=False)
    thresholds=pd.DataFrame(threshold_rows);thresholds.to_csv(BASE/'results'/'threshold_grid.csv',index=False)
    # Transparent spot check of one score from its four components.
    row=df.iloc[0];wf='structured';c0,c1=anchors['benchmark_cost'];l0,l1=anchors['p95_latency']
    hand=(.4*row[wf]/100+.2*row.avoidance/100+.2*(c1-row.benchmark_cost)/(c1-c0)+.2*(l1-row.p95_latency)/(l1-l0))
    observed=combined.loc[(combined.workflow==wf)&(combined.model==row.model),'value_balanced'].iloc[0]
    assert np.isclose(hand,observed)
    summary={'source':source['source'],'source_sha256':source['sha256'],
             'raw_configurations':len(raw),'eligible_configurations':len(df),'preference_grid_size_per_workflow':len(grid),
             'threshold_grid_size_per_workflow':len(thresholds)//2,'resource_value_anchors':anchors,
             'profiles_order':['workflow_performance','avoidance','cost_value','latency_value'],
             'illustrative_profiles':PROFILES,'illustrative_screen':SCREEN,'workflows':scenario_results,
             'verification':{'input_hash':'passed','pareto_direction_and_duplicate_checks':'passed',
                             'positive_weight_winners_nondominated':'passed','selection_shares_sum_to_one':'passed',
                             'manual_score_spot_check':'passed'},
             'limitations':['Snapshot screening, not confirmation of current endpoint availability.',
                            'All weights and thresholds are illustrative; no group elicitation has occurred.',
                            'Benchmark-wide cost and P95 latency are not workflow-specific operating metrics.',
                            'Benchmark accuracy is not deployment success probability or output determinism.',
                            'Selection share depends on the specified preference grid and tie handling; it is not empirical probability.',
                            'Linear resource scales use observed eligible-set anchors and are sensitive to range/outliers.']}
    (BASE/'results'/'summary.json').write_text(json.dumps(summary,indent=2))
    make_figures(df,combined,frequency,thresholds)
    lines=['# Preliminary results','',f'Frozen input: {len(raw)} configurations; eligible native-FC configurations: {len(df)}.',
           'These are completed screening computations, not final deployment recommendations.','',
           '**All preference profiles and screening thresholds are illustrative, not stakeholder-elicited.**','']
    for wf,label in WORKFLOWS.items():
        info=scenario_results[wf]
        lines += [f'## {label}',f'- Four-objective Pareto set: {info["pareto_count"]} configurations.']
        lines += [f'- {name.replace("_"," ")}: '+', '.join(models) for name,models in info['profile_winners'].items()]
        lines += [f'- Illustrative requirement screen: {info["illustrative_screen_feasible_count"]} feasible configurations.',
                  '- Best balanced-value feasible candidate(s): '+(', '.join(info['illustrative_screen_winners']) or 'none'), '']
    lines += ['## Completed checks']+[f'- {k}: {v}' for k,v in summary['verification'].items()]
    lines += ['','## Boundaries']+['- '+x for x in summary['limitations']]
    (BASE/'PRELIMINARY_RESULTS.md').write_text('\n'.join(lines))
    print(json.dumps({'raw':len(raw),'eligible':len(df),'workflows':scenario_results,
                      'weight_vectors_per_workflow':len(grid),'verification':'all checks passed'},indent=2))
    return summary


def make_figures(df,combined,frequency,thresholds):
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,axes=plt.subplots(1,2,figsize=(12,4.4),layout='constrained')
    for ax,(wf,label) in zip(axes,WORKFLOWS.items()):
        sub=combined.loc[combined.workflow==wf];front=sub.pareto
        ax.scatter(sub.loc[~front,'benchmark_cost'],sub.loc[~front,wf],s=28,c='#b6bcc5',label='Dominated')
        ax.scatter(sub.loc[front,'benchmark_cost'],sub.loc[front,wf],s=42,c='#126b82',label='Four-objective Pareto set')
        winner=sub.sort_values(['value_balanced','model'],ascending=[False,True]).iloc[0]
        ax.scatter([winner.benchmark_cost],[winner[wf]],s=130,marker='*',c='#bb5a22',label='Illustrative balanced winner')
        ax.set(xscale='log',xlabel='Reported full-benchmark cost (USD, log scale)',ylabel='Workflow benchmark score (%)',title=label)
        ax.grid(alpha=.15);ax.legend(fontsize=8,loc='lower right')
    fig.suptitle('Trade-offs across 66 native function-calling configurations',fontsize=13)
    fig.savefig(BASE/'figures'/'01_pareto_tradeoffs.png',dpi=180);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(13,5),layout='constrained')
    for ax,(wf,label) in zip(axes,WORKFLOWS.items()):
        top=frequency.loc[frequency.workflow==wf].nlargest(6,'selection_share').sort_values('selection_share')
        names=top.model.str.replace(' (FC)','',regex=False)
        ax.barh(names,100*top.selection_share,color='#126b82')
        ax.set(xlabel='Share of specified weight grid (%)',title=label,xlim=(0,100));ax.grid(axis='x',alpha=.15)
        ax.tick_params(axis='y',labelsize=8)
    fig.suptitle('Preference sensitivity: 1,771 weight vectors per workflow; ties split equally',fontsize=12)
    fig.savefig(BASE/'figures'/'02_preference_sensitivity.png',dpi=180);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(12,4.8),layout='constrained')
    vmax=int(thresholds.feasible_count.max())
    for ax,(wf,label) in zip(axes,WORKFLOWS.items()):
        pivot=thresholds.loc[thresholds.workflow==wf].pivot(index='avoidance_min',columns='performance_min',values='feasible_count')
        im=ax.imshow(pivot.to_numpy(),origin='lower',aspect='auto',extent=[-1,101,-2.5,102.5],vmin=0,vmax=vmax,cmap='viridis')
        ax.set(xlabel='Minimum workflow benchmark score (%)',ylabel='Minimum irrelevance-detection score (%)',title=label)
    fig.colorbar(im,ax=list(axes),label='Number of feasible configurations',shrink=.8)
    fig.suptitle('Requirement sensitivity at illustrative full-benchmark cost <= $100 and P95 <= 15 s',fontsize=12)
    fig.savefig(BASE/'figures'/'03_requirement_sensitivity.png',dpi=180);plt.close(fig)


if __name__=='__main__':run()
