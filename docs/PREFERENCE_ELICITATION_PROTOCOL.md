# Preference elicitation and survey analysis protocol

Version: pilot-1.0, 2026-11-05. This protocol supplements [Member C's sensitivity analysis](SENSITIVITY_AND_REVIEW.md); it does not change the frozen data, eligibility, illustrative weights or requirements. The research question remains how decision framing, preference timing and sensitivity affect a model shortlist, and how genuine review can revise that frame.

## What the earlier short questionnaire can support

The eight-question plain-English form is an exploratory discussion aid. A top priority, qualitative deal-breaker or hypothetical A/B choice does not identify four cardinal weights, benchmark cutoffs or acceptable value functions. Do not convert those responses directly into an additive recommendation. More questions alone do not solve this identification problem.

The research pilot adds a link between requested evidence and the planned analysis:

| Evidence collected | Intended use | Required qualification |
| --- | --- | --- |
| Participant code, relationship to the project, selected workflow and prior exposure | Match later review and separate decision participants from outside perspectives | One workflow per response; unknown group membership is a separate stratum |
| Unprompted objectives before the supplied metric list | Identify omissions in the decision frame | Qualitative coding with original responses retained privately |
| Metric definitions and comprehension responses | Check that participants distinguish benchmark proxies from deployment quantities | Clarify misunderstandings; never silently reinterpret a budget or waiting-time answer |
| Four numeric hard cutoffs, NONE or DISCUSS | Screen candidates before compensatory ranking | Numeric bounds are inclusive; missing and unresolved answers are not “no limit” |
| One reference improvement and four relative ratings over stated ranges | Derive provisional swing weights | Ratings require discussion and participant confirmation before an individual model run |
| Linear-scale and compensation responses, rationale, readiness | Identify objections to the proposed additive model | A disagreement is a result to discuss, not an error to remove |
| Later confirmed input version and revisions after viewing consequences | Describe retained and changed framing/preferences | A form submission alone is not a frozen comparison or completed constructive review |

## Methodological basis

Questions should be specific, neutral and answerable, with distinct alternatives and clear units; one response should not ambiguously evaluate different constructs. Keep wording stable when comparing phases. These choices follow [Pew Research Center's question-design guidance](https://www.pewresearch.org/writing-survey-questions/). The open objectives question precedes the metric prompts to reduce prompting effects.

[AAPOR's best-practice guidance](https://aapor.org/standards-and-ethics/best-practices/) supports planning from the research objective, allowing unresolved responses, separating missing answers from substantive alternatives, and pretesting before fieldwork. Our operational choice is a versioned pilot plus a short human think-aloud check; a successful browser check is not evidence of human comprehension. [US Census questionnaire-testing guidance](https://www.census.gov/about/policies/quality/standards/appendixa2.html) distinguishes expert review from respondent-based testing.

The [Government Analysis Function's 2024 MCDA guide](https://analysisfunction.civilservice.gov.uk/policy-store/an-introductory-guide-to-mcda/) supports comparing whole changes over explicit ranges rather than generic “importance”, normalizing relative ratings, and examining value-function and compensation assumptions. Its public-appraisal approach treats monetary costs separately from weighted benefits; this study does **not** claim to reproduce that policy framework. The older [2009 MCDA manual](https://assets.publishing.service.gov.uk/media/5a790545e5274a2acd18b975/1132618.pdf), section 7.3.4.1, illustrates an inverse-linear cost criterion. Here benchmark cost is an explicitly provisional resource proxy in a course-study desirability model, not a monetary benefit-cost appraisal.

## Instrument and administration

The new English instrument has 23 questions in five sections: perspective; metric definitions and comprehension; hard cutoffs; range-specific improvements; assumptions/readiness. Completion time of 10–15 minutes is an estimate to check in the pilot. Numeric questions permit a blank or an explicit request for discussion. No default weights or illustrative cutoff answers are supplied. Compensation acceptance and dependence on other measurements are asked separately.

The same instrument may be offered to the three design-team members and optional outside participants. Record which group each respondent belongs to and use a reusable code rather than full names, contact details or student identifiers. Reserve A/B/C for the team and use separate record identifiers to detect code collisions rather than assuming codes uniquely identify people. Outside participants can contact their inviter and quote their code to arrange clarification and confirmation; without this follow-up their answers remain exploratory. Collect only voluntary responses. Keep source answers, timestamps, codes, form links and filled logs outside public Git. A reusable code does not guarantee anonymity, especially within a three-person team.

Recruitment outside the team is a convenience sample unless a different sampling design is actually implemented and documented. Extra respondents can reveal omitted objectives or explore a wider range of preferences; they do not automatically become the decision owners. Do not pool their answers into team weights or call the sample representative of users, enterprises or all students. Report counts and recruitment methods, not unsupported population claims. More outside responses cannot replace the actual team review required by [WORK_PLAN.md](../WORK_PLAN.md).

The pilot must remain labelled as such. Ask a comparable student to explain, in their own words: what benchmark cost means; what P95 does and does not mean; what a cutoff does; and what a 50-point improvement rating means relative to 100. Record confusing wording and actual completion time. Correct and version the instrument before wider collection. Do not combine pilot and production responses silently or claim that agent review validated the questionnaire.

## Proposed scales and swing ratings

Keep these baseline anchors fixed across elicitation, screening and ranking:

| Criterion | Bad end | Good end | Provisional value function |
| --- | ---: | ---: | --- |
| Selected workflow score | 0 | 100 | score / 100 |
| Irrelevant-call avoidance score | 0 | 100 | score / 100 |
| Whole-benchmark cost, USD | 355.17 | 0.46 | (355.17 − cost) / 354.71 |
| Recorded benchmark P95, seconds | 568.59 | 0.96 | (568.59 − latency) / 567.63 |

These ranges and linear values are modelling proposals, not measured preferences. The imaginary all-bad starting profile and its one-at-a-time improvements need not be actual or feasible candidates. Explain the distinction between valuing improvements and accepting a candidate that violates a hard cutoff. If this comparison is not meaningful to a participant, record the objection and discuss an alternative instead of supplying ratings on their behalf.

The participant chooses a most-valued full improvement, rates it 100, and rates the other full improvements relative to it. Ties at 100 and explicit zero ratings are allowed; four ratings need not sum to 100. Derive provisional weights only when every included rating is resolved:

```text
w_j = r_j / sum(r)
V_i = sum_j w_j * v_j(consequence_ij)
```

Check four finite ratings in [0,100], positive total, maximum 100 and consistency of the selected reference with its rating. Missing, DISCUSS, skipped and genuine zero remain separate. Show the participant the resulting weights in the criterion order above and confirm them together with the workflow, cutoff rules, scales, anchors and candidate-rule version. An unresolved metric objection, failed comprehension check or rejected model assumption triggers clarification, not automatic deletion or fabricated replacement values.

A reference rating of 100 and another of 50 imply that the latter full improvement is roughly half as valuable under this model. Discuss a cross-check against half the value gain on the reference criterion; disagreement may require revised ratings or value functions. This is a diagnostic conversation, not proof of cardinal measurement or additive independence.

Do not recompute resource anchors after an individual's hard screen. Changing ranges or replacing linear scales with log scales changes the interpretation of weights; reassess or explicitly justify any transfer. The illustrative same-weight log experiment in Member C's work is a sensitivity experiment, not evidence that a participant endorsed both scale systems.

## Analysis and input freeze

1. Preserve raw responses and instrument version. Check duplicate participant/workflow responses without deleting history; distinguish a replacement from a separate workflow response. Keep team, outside and undisclosed groups separate.
2. Code hard cutoffs as `numeric`, `none`, `discuss` or `missing`. Validate score cutoffs in [0,100] and resource cutoffs as finite nonnegative values. Inclusive minima use ≥ and inclusive maxima use ≤. Do not clip out-of-range values or interpret an app budget as a benchmark-cost limit.
3. Resolve meaning, model assumptions and ratings through actual participant discussion. Keep both original and corrected records with reasons. Do not derive weights from the short form's priority choices or infer one from a missing response.
4. Show a complete input card and obtain explicit participant confirmation. Save its version, date and `confirmed_at` before computing the designated comparison. Exploratory source results already exist; do not claim fully blind initial elicitation.
5. For each confirmed participant/workflow, report raw consequences, all nondominated candidates, all unscreened additive optima, feasible count, all best feasible optima and ties using absolute score tolerance 1e-12. An empty feasible set remains empty unless a participant explicitly revises a rule.
6. Compare participant-derived cases with the labelled illustrative baseline and examine sensitivity. Allow zero weights: dominated candidates can tie when an improved dimension receives zero weight, so do not discard those additive ties silently. Keep Pareto filtering and all-candidate utility maxima conceptually separate.
7. Retain individual recommendations and disagreements. A proposed mean-weight group scenario requires an agreed aggregation rule and is not consensus by default. Do not let a larger outside sample determine the three team members' weights.

For three members, report paired individual cases and statements such as “two of the three members retained this requirement”. Do not add inferential tests, factor analysis, internal-consistency coefficients or a margin of sampling error merely to make the study look statistical. The form is a decision-elicitation instrument, not a validated psychometric scale. If outside collection grows, keep its descriptive results and sample limitations distinct.

## After-result review

Use a short follow-up tied to the actual confirmed input card and comparison version. First show consequences and trade-offs, not just a winning name. For each matched participant/workflow, record:

1. participant code and confirmed input version;
2. which comparison materials were actually seen;
3. whether the recommendation represents their preferences, with a reason or “not sure”;
4. what surprised them;
5. retained/revised objectives, metric relevance, candidate rules, scales, weights and requirements, distinguished separately;
6. exact replacement values/rules where a revision is proposed;
7. whether a revision depends on other criterion levels;
8. confirmation status and unresolved disagreement.

Where before/after values are compared, retain the same measurement wording, workflow, ranges and model version or explicitly label the change. Confirm each revised input card before recomputation. Report a change after review as a documented revision; without a controlled design, do not attribute it causally to seeing results. Numerical sensitivity alone is not completed participant co-construction.

## Status and next step

Research and instrument preparation are completed; actual participant elicitation, input confirmation and after-result review remain pending. The public protocol contains methods only. Live-form links and exact private instrument files remain in ignored `deliverables/member_c/`. Next: conduct a human cognitive pilot, freeze the production wording, obtain actual responses, confirm individual input cards and run only the resulting reviewable comparisons.
