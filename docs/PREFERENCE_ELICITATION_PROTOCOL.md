# Preference elicitation and survey analysis protocol

Version: public-pilot-2.0, 2026-11-05. This protocol supplements [Member C's sensitivity analysis](SENSITIVITY_AND_REVIEW.md); it does not change the frozen data, eligibility, illustrative weights or requirements. The research question remains how decision framing, preference timing and sensitivity affect a model shortlist, and how genuine review can revise that frame.

## Two parts with different purposes

The current general-audience English survey requires no project knowledge. It collects descriptive preferences and choices between hypothetical models. A separate facilitated team session elicits and confirms the quantitative inputs needed for a model recommendation. A top priority, generic importance rating or hypothetical A/B choice does not identify four cardinal weights, benchmark cutoffs or acceptable value functions. Do not convert public-survey responses directly into an additive recommendation. More questions alone do not solve this identification problem.

The public survey has this question-to-analysis map:

| Evidence collected | Intended use | Required qualification |
| --- | --- | --- |
| Q1: team membership; Q2: AI-assistant use in the past 30 days | Describe respondents; keep team, outside and undisclosed membership separate | No personal identifier is requested; this survey cannot match individuals across phases |
| Q3–6: importance of matching requests, acting only when asked, time and price | Report ordered response distributions for each feature | Ordinal categories, not cardinal weights; “Not sure” is distinct from low importance and skipped answers |
| Q7: accuracy versus time; Q8: accuracy versus price | Describe choices at the stated trade-offs | Both other features are held equal; invented examples, not observations of real models |
| Q9: unrequested task creation versus time; Q10: unrequested task creation versus price | Describe tolerance for this action in two distinct comparisons | Denominator is 100 requests that did not ask for task creation; do not mix with task-request accuracy |
| Q11: what to do when a deadline is omitted | Identify workflow-framing preferences and disagreements | The hypothetical app permits tasks without deadlines; this is not a correctness test or an automatic benchmark-rule revision |
| Q12: longest generally acceptable wait | Report waiting-time categories and context dependence | Interval data; do not impute midpoints or map personal waiting time to benchmark P95 |
| Q13: response when no assistant meets all preferences | Describe willingness to defer choice or investigate trade-offs | These are stated intentions, not observed decisions or accepted threshold relaxations |
| Q14: optional comment on other considerations or unclear wording | Code omitted objectives and comprehension concerns | Prompt follows supplied features, so it is not an unprompted objectives measure |

Four paired choices are not a full factorial or conjoint design and do not identify a four-criterion cardinal utility model. Keep Model A, Model B, no preference, neither and insufficient information as separate categories for every comparison. The quality/action-avoidance advantage appears under A twice and B twice; labels are fixed, not randomly assigned. Do not claim experimental counterbalancing or infer stable preference parameters from these four choices alone.

## Methodological basis

Questions should be specific, neutral and answerable, with distinct alternatives and clear units; one response should not ambiguously evaluate different constructs. Keep wording stable when comparing phases. These choices follow [Pew Research Center's question-design guidance](https://www.pewresearch.org/writing-survey-questions/). The public survey uses one concrete to-do-list situation, a fully labelled importance scale, definitions before model comparisons, and explicit uncertain/no-choice alternatives. The facilitated team session asks about objectives before supplying the metric list to reduce prompting effects.

[AAPOR's best-practice guidance](https://aapor.org/standards-and-ethics/best-practices/) supports planning from the research objective, allowing unresolved responses, separating missing answers from substantive alternatives, and pretesting before fieldwork. Our operational choice is a versioned pilot plus a short human think-aloud check; a successful browser check is not evidence of human comprehension. [US Census questionnaire-testing guidance](https://www.census.gov/about/policies/quality/standards/appendixa2.html) distinguishes expert review from respondent-based testing.

The [Government Analysis Function's 2024 MCDA guide](https://analysisfunction.civilservice.gov.uk/policy-store/an-introductory-guide-to-mcda/) supports comparing whole changes over explicit ranges rather than generic “importance”, normalizing relative ratings, and examining value-function and compensation assumptions. Its public-appraisal approach treats monetary costs separately from weighted benefits; this study does **not** claim to reproduce that policy framework. The older [2009 MCDA manual](https://assets.publishing.service.gov.uk/media/5a790545e5274a2acd18b975/1132618.pdf), section 7.3.4.1, illustrates an inverse-linear cost criterion. Here benchmark cost is an explicitly provisional resource proxy in a course-study desirability model, not a monetary benefit-cost appraisal.

## Instrument and administration

The current public English instrument, “Choosing an AI Task Assistant: Your Preferences”, has 14 questions in three sections: preferences; definitions and model comparisons; further comparisons and situations. Thirteen questions are multiple choice and the last is an optional paragraph. All questions may be skipped. It defines artificial intelligence (AI), AI model, correct result, unrequested task creation, example time and example price. It does not ask about project results, technical workflow labels, benchmark metrics, participant codes or numerical weights. The 5–7 minute completion estimate awaits human measurement. Examples are explicitly imaginary; price is USD per 100 requests, not a subscription or actual benchmark cost.

The same public survey may be offered to team members and optional outside participants. Membership is self-reported, with a “Prefer not to say” option. Do not infer who filled it out or retrospectively link anonymous answers. No email collection or sign-in requirement through a one-response limit is enabled, and public response summaries are off. This improves accessibility but does not ensure one response per person. Ask for one response per person, document recruitment and possible duplicates, and do not invent a way to identify unique people. Keep raw answers, timestamps, live links and filled logs outside public Git.

The original 23-question technical pilot is archived privately and superseded for general-audience collection; zero submitted responses were observed before revision. Its quantitative content is reserved as a draft for the separate facilitated team module below. There, record the participant, selected workflow, prior exposure to project results and a dated input version privately. Codes may support agreed matched review, but do not guarantee anonymity within a three-person team. Define benchmark cost, P95, cutoffs, value scales and swing ratings before asking anyone to use them; explain these with examples and a teach-back check. No default participant weights or cutoff answers may be supplied.

Recruitment outside the team is a convenience sample unless a different sampling design is actually implemented and documented. Extra respondents can reveal omitted objectives or explore a wider range of preferences; they do not automatically become the decision owners. Do not pool their answers into team weights or call the sample representative of users, enterprises or all students. Report counts and recruitment methods, not unsupported population claims. More outside responses cannot replace the actual team review required by [WORK_PLAN.md](../WORK_PLAN.md).

The instrument remains a pilot in the study records. Ask a student unfamiliar with the project to explain the scenario, “correct result”, unrequested task creation, the price denominator and one A/B trade-off in their own words. Ask what was unclear and measure completion time. Correct and version the wording before wider collection. Do not combine instrument versions or pilot and production responses silently. Browser navigation and agent review are not human comprehension validation. In the facilitated module, separately check benchmark cost, P95, hard cutoffs and the meaning of a 50-point swing rating relative to 100.

## Public-survey analysis

Preserve the exact instrument version, recruitment channel, collection phase and raw answers privately. Use a generated record ID for a response row, not a claim about a unique person. For each question report the number answering, category counts and percentages with that denominator; report skipped answers separately. Retain uncertain and undisclosed responses as explicit categories. Analyse the four importance items separately, without summing, averaging into an index or normalizing them into model weights. All four may be rated highly; that is a result, not a reason to force rankings.

Describe each paired choice at its exact values. With sufficient counts, cross-tabulate by reported team membership or AI-use frequency and show cell counts; avoid unstable subgroup claims from tiny cells. The three team members' anonymous public answers cannot be matched to later individual decisions. Qualitative comments can identify omitted criteria, but do not silently add a criterion or change frozen thresholds. Q11 deliberately allows deadline omission, unlike the required-deadline schema in the separate task example; treat this as evidence about framing, not a failed comprehension answer. The survey supports descriptive analysis, not population estimates, causal effects, measured willingness to pay or benchmark-derived recommendations.

## Facilitated team module: proposed scales and swing ratings

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

## Facilitated team analysis and input freeze

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

Research and the general-audience form revision are completed; the human pilot, actual participant elicitation, quantitative input confirmation and after-result review remain pending. The public protocol contains methods only. Live-form links, the exact 14-question instrument, archived technical pilot and headers-only response templates remain in ignored `deliverables/member_c/`. Next: conduct a human cognitive pilot, freeze public production wording, collect descriptive responses, then separately facilitate and confirm the team's quantitative input cards before the designated model comparisons.
