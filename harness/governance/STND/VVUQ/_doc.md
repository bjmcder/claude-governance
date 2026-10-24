---
id: "STND.VVUQ"
level: "LVL2"
kind: "standard"
title: "Verification, validation, and uncertainty quantification methods"
status: "adopted"
adopted: "2026-10-11"
revision: "1.4"
adopted_by: "The Custodian"
instantiates: ["GOV.18", "GOV.19"]
rank: null
waivable: false
---

## Purpose and scope

This standard holds the default methods by which work produces the evidence that the NUMER profile requires. NUMER states each outcome and its bounds without naming a method; this standard names the methods that current practice supports, with default numbers an agent applies unattended. Its core is three instruments that set how strictly each result is judged. The section Comparison tiers ranks comparisons from bitwise identity, through units in the last place and tolerances set from rounding and numerical error, to statistical criteria and uncertainty statements, and places each tolerance within a bracket between the noise floor of its comparison and the departure it has the purpose of detecting. The section Error budget allocates the required precision among numerical, statistical, input, and model-form components and keeps aleatory and epistemic uncertainty apart. The section Assertion and tracking decides whether each quantity is asserted, tracked, or targeted. The remaining sections give methods and numbers for the evidence those instruments use. STND.VVUQ.83 instantiates GOV.11 and GOV.48 and is binding on agents at every class; every other provision, its numbers included, is a default (GOV.19) and a recommendation, whether its number comes from a source or from a convention: an actor that uses another method or number meeting the same NUMER outcome records the method and its reason as a decision (REPRO.7, PRIN.10), and asks no one. STND.VVUQ.77 and STND.VVUQ.78 rest on LVL0 directly, for claims of comparison and the timing of verification. Methods and numbers change as the field advances; a change here leaves NUMER unchanged.

The provisions were synthesized from a research note of 2026-10-11, kept in the project as claude/research/vvuq-research-notes.md and proposed as a knowledge entry (GOV.32), which surveyed standards bodies, national laboratories, agencies, and the literature, and logged each retrieval. Where a default number rests on a source, the note cites it; where it is a convention that no retrieved source sets, the Notes say so.

## Normative and informative parts

The body of a numbered provision, including a table it contains, is normative. Everything else is informative.

## Terms

This section fixes meaning and imposes no obligation, as the Lexicon does. Terms that NUMER defines, such as numerical method, numerical error, required precision, and stopping criterion, have the meanings NUMER gives them.

| Term | Definition |
| --- | --- |
| Aleatory uncertainty | Uncertainty from variability inherent in a quantity, which more knowledge does not reduce and a probability distribution describes. |
| Apparent order | The observed order computed from three solutions whose successive differences change sign, taken in absolute value. |
| Asserted check | A check whose failure blocks reliance on the result it judges, by failing its test, halting its run, or blocking its change. |
| Batch means | An estimate of the variance of a mean of dependent samples from the variance of the means of consecutive non-overlapping batches. |
| Bulk effective sample size | The effective sample size of the rank-normalized draws. |
| Comparison tier | One of the levels of strictness at which STND.VVUQ.1 ranks comparisons of numerical values. |
| Complex-step check | A check of a first derivative of a real function against the imaginary part of the function evaluated at a complex perturbation of its input, divided by the perturbation. |
| Constraint qualification | A condition on the active constraints at a point, such as linear independence of their gradients, under which a local optimum satisfies the first-order conditions. |
| Contact discontinuity | A discontinuity that is carried by the flow without compression, such as a jump in density at constant pressure and velocity. |
| Controlled component | A component of an error budget that the computation itself sets and is able to reduce: its numerical error, the statistical uncertainty of its own sampling, and the effect of each approximation it makes. |
| Data range parameter | The difference between the largest and smallest values over the refinement levels, divided by one less than their number. |
| Discrepancy principle | The choice of a regularization strength that makes the misfit of the regularized solution equal to a recorded factor times the noise level. |
| Dot-product test | A check that the inner product of a forward derivative product with one vector equals the inner product of the matching adjoint product with another vector. |
| Effective sample size | The number of independent samples that would give the same statistical uncertainty as a set of dependent samples. |
| Effectivity index | The ratio of an error estimator's estimate to the true error on a problem whose solution is known. |
| Epistemic uncertainty | Uncertainty from lack of knowledge, which more data, analysis, or computation is able to reduce. |
| Error budget | The allocation of a result's required precision among the components of its error and uncertainty, recorded in its numerical specification. |
| Extrapolation abscissa | The quantity against which STND.VVUQ.79 and STND.VVUQ.80 fit differences: the logarithm of problem size, or, for an alternative execution path whose hardware contract states an error rate per operation, the count of its operations. |
| Exact value | An integer, logical value, or identifier that no floating-point comparison decides; the result of one correctly rounded operation on bitwise identical operands under the same format, rounding mode, subnormal handling, and contraction setting, without extended intermediate precision; or a value restored by a round trip that preserves every bit. |
| Figure of merit | The inverse of the product of the squared relative error and the computing time of a sampling estimate. |
| Grid convergence index | The error band F_s times the absolute value of e_a, divided by r^p - 1, for the finest of three or more refinement levels, where e_a is the relative difference between the two finest levels, r the refinement ratio, p the observed order, and F_s the safety factor. |
| Guaranteed bound | A bound that holds with certainty under stated assumptions, as one from interval arithmetic or from an a priori error analysis whose assumptions are shown to hold does. |
| Holm step-down procedure | A procedure that controls the probability of rejecting at least one correct hypothesis in a family, by testing ordered p-values against successively less strict thresholds. |
| Jansen estimator | An estimator of a total-effect index from half the mean squared difference between outputs at base points and at points differing in one input, divided by the output variance. |
| Least-squares procedure | An error estimate that fits error models by least squares to four or more refinement levels and sets its safety factor from the quality of the fit. |
| Machine epsilon | The distance from 1 to the next larger number in a floating-point format. |
| Manufactured solution | A chosen function made an exact solution of a model by adding the source terms that its substitution into the model's equations produces. |
| Nested potential scale reduction factor | A potential scale reduction factor computed between groups of chains that each share an initialization, rather than between single chains. |
| Noise floor | The standard uncertainty, or a bound that holds with certainty or rests on documented accuracy under STND.VVUQ.4, of the difference between two correct computations of the compared values, from the rounding, stopping, and statistical uncertainties of both, their difference in discretization, and the uncertainty of the reference. |
| Numerical tolerance | Half of one unit in the last decimal digit to which a value is reported, as JCGM 101 uses it to judge the stability of Monte Carlo results. |
| Observed order | The rate at which error falls between successive refinement levels: ln(e_c/e_f)/ln r from errors against a known solution, or ln(abs(f_3 - f_2)/abs(f_2 - f_1))/ln r from three solutions at constant ratio r, f_1 the finest. |
| Order test | The measurement of a method's observed order over successive refinement levels, against a known solution or, without one, from differences between levels. |
| Pareto shape estimate | The estimated shape parameter of a generalized Pareto distribution fitted to the largest importance weights, which measures how heavy their tail is. |
| Point-detector tally | A next-event estimate of a flux at a point in a Monte Carlo transport calculation. |
| Potential scale reduction factor | A ratio comparing the variance between Markov chains with the variance within them, near 1 when the chains sample one distribution. |
| Probability box | A pair of cumulative distribution functions that bound the distribution of a quantity, expressing aleatory variability within epistemic bounds without merging them. |
| Randomized quasi-Monte Carlo | Sampling by low-discrepancy points randomized so that independent randomizations give an estimate of the statistical uncertainty. |
| Rank plot | Histograms of the ranks of each chain's draws among all chains' draws, uniform when the chains sample one distribution. |
| Refinement level | One set of values of the discretization parameters at which a result is computed for an order test or an error estimate. |
| Refinement ratio | The ratio of a discretization parameter at one refinement level to its value at the next finer level. |
| Relaxation bound gap | The difference between the best feasible objective value found and a proven bound on the optimum, relative to the magnitude of the former. |
| Root seed | The recorded value from which every random number stream of a computation is derived. |
| Safety factor | The factor by which the grid convergence index multiplies its error estimate to give the stated coverage. |
| Saltelli design | A sampling design of two independent base matrices and the k matrices that each take one column from the second, for k inputs. |
| Scaled optimality residual | The dual residual divided by the larger of 100 and the mean absolute multiplier, over 100, as interior-point solvers report it. |
| Shadowing method | A method that computes the derivative of a long-time average of chaotic dynamics from a perturbed trajectory that stays close to the original one. |
| Simulation-based calibration | A test of a posterior computation that draws parameters from the prior, simulates data, and checks that the rank of each drawn parameter among posterior draws is uniform. |
| Standardized error | The difference between an observed value and a surrogate's predicted mean, divided by its predicted standard deviation, at a held-out point. |
| Surrogate | A cheaper model that stands in for a mathematical model or its computation, fitted to evaluations of it. |
| Tail effective sample size | The smaller of the effective sample sizes of the 5 percent and 95 percent quantile estimates. |
| Targeted component | A controlled component that the computation drives to its allocation in the error budget by refinement, more samples, or higher precision, reporting the value it reaches. |
| Taylor remainder test | A check that the remainder of a Taylor expansion built from computed derivatives falls at the predicted rate as a perturbation is halved. |
| Theoretical order | The order of accuracy that analysis of a method predicts as refinement proceeds. |
| Tolerance bracket | The interval of tolerances for a comparison from the multiple of STND.VVUQ.33 times its noise floor, or from the noise floor itself where that is a bound, to the smallest departure that the comparison has the purpose of detecting less the quantile of the detection probability of STND.VVUQ.34 times the noise floor, or less the noise floor itself where that is a bound. |
| Tracked quantity | A quantity recorded with each run or revision it describes and compared with a band set from its recorded baseline. |
| Uncontrolled component | A component of an error budget that the computation does not set: its propagated input uncertainty, that of inputs that are other results included, and its model-form uncertainty. |
| Unit in the last place | The spacing between a floating-point number and the next larger number of the same format. |
| Unit roundoff | Half the machine epsilon: the largest relative error of rounding one real number to a floating-point format. |
| Validation uncertainty | The root sum of squares, at one coverage, of the numerical, input, and measurement uncertainties of a comparison of simulation with measurement. |
| Variance of the variance | The estimated relative variance of the estimated variance of a sample mean, which reveals heavy-tailed contributions. |

## External sources

The methods rest on these frameworks, in the editions current on 2026-10-11 as the research note found them. They are sources of practice, not instruments of this governance.

| Source | Status found |
| --- | --- |
| ASME VVUQ 1-2022, terminology | Current; free of charge |
| ASME V&V 10-2019, computational solid mechanics | Current |
| ASME V&V 20-2009, computational fluid dynamics and heat transfer | Reaffirmed 2021; stabilized maintenance; in effect |
| ASME V&V 40-2018, credibility for medical devices | Stabilized maintenance; in effect |
| ASME VVUQ 20.1-2024, multivariate validation metric | Current |
| NASA-STD-7009B, models and simulations | Approved 2024-03-05 |
| JCGM 100:2008 (GUM) and JCGM 101:2008 (propagation by Monte Carlo) | Current; an amendment of the GUM on non-linearity is in circulation |
| FDA, credibility of computational modeling in medical device submissions | Final guidance, 2023-11-17 |
| National Research Council, Assessing the Reliability of Complex Models (2012) | Reference report |
| JCGM GUM-1:2023, introduction to the expression of uncertainty | Published |
| ASME VVUQ 30.1-2024, scaling for nuclear power system responses | Current |
| MCNP 6.3.2 Theory and User Manual, LA-UR-26-23119 Rev. 1 | Current; not opened by the research |

No standard for verification and validation of machine-learned models had been published by ASME; the learned-surrogate provisions follow the scientific machine-learning literature that the research note cites.

## Notes

Sources of defaults that the research traced to a source:

| Default | Provisions | Source |
| --- | --- | --- |
| Refinement ratio above 1.3; safety factors 1.25 and 3; oscillatory convergence with apparent order | STND.VVUQ.20, STND.VVUQ.22, STND.VVUQ.27 | Celik and others, J. Fluids Eng. 130 (2008) 078001; Roache |
| Order test as acceptance test; manufactured-solution form; factor 100 between rounding or stopping error and discretization error | STND.VVUQ.19, STND.VVUQ.24, STND.VVUQ.29 | Roy, J. Comput. Phys. 205 (2005); margin measured against discretization error (the level-difference form of STND.VVUQ.29 is a convention) |
| Interval of 95 percent coverage for grid estimates | STND.VVUQ.28 | Lisbon 2008 workshop validation procedure implementing ASME V&V 20 |
| Effectivity index | STND.VVUQ.25 | Chamoin and Legoll, arXiv:2110.02160 (2021) |
| Least-squares procedure on four levels; band 0.5 to 2.1; 100 to 1000 margin | STND.VVUQ.26, STND.VVUQ.27 | Eça and Hoekstra, J. Comput. Phys. 262 (2014) 104-130 |
| Rates at shocks and contact discontinuities | STND.VVUQ.23 | Banks, Aslam, and Rider (2008) |
| Probabilistic rounding bound | STND.VVUQ.37 | Higham and Mary, SIAM J. Sci. Comput. (2019) |
| Ten randomizations, Student-t interval | STND.VVUQ.40 | L'Ecuyer, Nakayama, Owen, and Tuffin, GERAD G-2023-67 |
| 59 runs for a one-sided 95/95 limit | STND.VVUQ.44 | Wilks' order-statistic formula |
| Saltelli design; Jansen estimator | STND.VVUQ.45 | Saltelli and others, Comput. Phys. Commun. 181 (2010); Puy and others, IJUQ, arXiv:2009.01147 |
| Conformal coverage limits | STND.VVUQ.46 | Gray and others, arXiv:2501.18426 |
| Standardized errors beyond 3; Mahalanobis check | STND.VVUQ.46 | Bastos and O'Hagan, Technometrics (2009) |
| Model discrepancy | STND.VVUQ.47 | Brynjarsdóttir and O'Hagan, Inverse Problems (2014) |
| Independent forward computation | STND.VVUQ.51 | Colton and Kress, as quoted by Wirgin |
| Simulation-based calibration numbers; data-dependent test quantities | STND.VVUQ.52 | Talts and others (2018); Modrák and others, Bayesian Analysis (2023), doi:10.1214/23-BA1404 |
| No guarantee for heuristic regularization choice | STND.VVUQ.54 | Bakushinskii's veto; Becker, arXiv:1011.3669 |
| Stationarity tolerance 1e-8; scaled residual | STND.VVUQ.55 | Wächter and Biegler, Math. Program. 106 (2006) |
| Feasibility tolerance 1e-6 | STND.VVUQ.55 | Gurobi parameter reference |
| Four chains, 1.01, effective sample sizes above 400, rank plots | STND.VVUQ.58 | Vehtari and others, Bayesian Analysis 16 (2021) |
| Pareto shape threshold | STND.VVUQ.60 | Vehtari and others, JMLR 25(72) (2024) |
| Ten tally-fluctuation checks and their thresholds | STND.VVUQ.61 | MCNP4B manual and a CANTEACH chapter; the current MCNP 6.3.2 manual was not opened |
| Root seed of 128 bits; spawned streams; no arithmetic seeding by worker index | STND.VVUQ.62 | NumPy random-number documentation; L'Ecuyer and others (2017) |
| Fixed-seed and fresh-seed tests | STND.VVUQ.64 | Dutta, Arunachalam, and Misailovic, ICST (2022) |
| Sequential rule of repetition | STND.VVUQ.65 | Gandy, JASA (2009) |
| Implicit derivative error bound | STND.VVUQ.68 | Blondel and others, implicit differentiation (2022) |
| Taylor remainder rates | STND.VVUQ.69 | dolfin-adjoint practice |
| Dot-product tolerance of 100 machine epsilons; 1e-5 as a defect | STND.VVUQ.70 | NEMO tangent and adjoint model practice; Claerbout |
| Complex step of 1e-200 | STND.VVUQ.71 | Martins, Sturdza, and Alonso, ACM TOMS 29(3) (2003); MDO Lab guidance |
| Shadowing for chaotic averages | STND.VVUQ.73 | Wang, Hu, and Blonigan, J. Comput. Phys. (2014) |
| Learned-surrogate verification and fair comparison | STND.VVUQ.76, STND.VVUQ.77 | Jakeman and others, arXiv:2502.15496 (2025); McGreivy and Hakim, arXiv:2407.07218 (2024) |
| Fits on at least six sizes over a factor of sixteen: for deterministic results, the logarithm of the ratio of difference to tolerance, with the one-sided 95 percent prediction interval at the largest size; for stochastic results, the estimated difference weighted by its standard error, with the two-sided 95 percent confidence interval of the fitted value | STND.VVUQ.79, STND.VVUQ.80, STND.VVUQ.81 | Ordinary and weighted least-squares regression; prediction and confidence intervals of a fitted value |
| Grid estimate as a 95 percent interval; division by 1.1, the larger-uncertainty end of the range 1.1 to 1.15 for an error distribution shifted from the finest-level solution | STND.VVUQ.28 | ASME V&V 20, as NIST IR 8298 (2020), section 4.1, summarizes it for the grid convergence index; the standard's text was not opened, and the extension to the least-squares procedure is an inference |
| At least 10^4/(1 - p) fixed trials; stages of at least 10^4 and 100/(1 - p) trials; stability at twice the standard deviation of the stage average within the numerical tolerance | STND.VVUQ.41, STND.VVUQ.42 | JCGM 101:2008 clauses 7.2 and 7.9: clause 7.2 from the JCGM final draft of 2006; clause 7.9 from NPL Report MS 1 (software for GUM Supplement 1), an applied tutorial (AgEcon 207657), and a 2024 application (PubMed Central PMC11525383) |
| Aleatory and epistemic separation; intervals for epistemic inputs; probability boxes; numerical error as epistemic | STND.VVUQ.12, STND.VVUQ.16 | Roy and Oberkampf, Comput. Methods Appl. Mech. Engrg. 200 (2011) |
| Documented accuracy in units in the last place as tested maxima, not proven bounds | STND.VVUQ.4 | GNU C Library manual, section 19.7; HIP math API reference |
| One quarter of a tolerance | STND.VVUQ.10 | Calibration practice of a test uncertainty ratio of 4:1, the 25 percent of tolerance of ANSI/NCSL Z540-1, as a Transcat white paper quotes it |

As the custodian directed on 2026-10-11, every convention and every external standard here is a recommendation; none awaits confirmation. Defaults that are recorded conventions, which no retrieved source sets: the order of the tiers of STND.VVUQ.1, and their admitted differences; the margin of one unit in the last place of STND.VVUQ.4; the tolerance bracket and its two ends (STND.VVUQ.7, STND.VVUQ.8), which reuse the multiple of STND.VVUQ.33 and the power of STND.VVUQ.34; the quarter of the largest uncontrolled component in STND.VVUQ.10, and the quarter and one thirtieth of the omission rule of STND.VVUQ.11; the probability box as the default form of STND.VVUQ.12; the test for asserting of STND.VVUQ.13 and the recorded baseline of STND.VVUQ.14; the 10 percent order tolerance of STND.VVUQ.21; the rate band 0.1 of STND.VVUQ.69; lambda = 2.72 and the square root of 2 ln(40n) divided by 1 - u of STND.VVUQ.37, u being the unit roundoff, chosen so that the source's bounds hold with probability at least 0.95: for a product of n factors the bound fails with probability at most 2 exp(-lambda^2 (1 - u)^2 / 2), and for an inner product of length n with at most n times that probability; the ten Latin hypercube replicates of STND.VVUQ.40, which let the half-sample check of STND.VVUQ.61 be computed; the false-rejection rate 0.001 per suite and power 0.9 of STND.VVUQ.33 and STND.VVUQ.34; the derivative agreements 1e-10 and 1e-6 of STND.VVUQ.71; the factor of ten in STND.VVUQ.75; the 30 degrees of freedom of STND.VVUQ.33; the factor of 100 between complex steps in STND.VVUQ.71; the half-sample agreement of STND.VVUQ.61; the linearity check of STND.VVUQ.43; and the averaging rule of STND.VVUQ.32. Defaults resting on knowledge that the research assumed and did not confirm: failed runs treated as exceeding the limit (STND.VVUQ.44); constraint qualifications, second-order conditions, and the relaxation bound gap (STND.VVUQ.56); condition-number estimators (STND.VVUQ.36); and the Student-t interval across replicated Latin hypercube designs (STND.VVUQ.40).

Two defaults rest on secondary sources, as the custodian authorized on 2026-10-11, because the primary texts could not be opened. STND.VVUQ.28 divides a grid estimate by 1.1, the end of the range 1.1 to 1.15 that NIST IR 8298 attributes to ASME V&V 20 giving the larger standard uncertainty; the factor 2 that the same source gives for an error normal about the finest-level solution is not a default, because three or four refinement levels are unable to show that distribution. A tolerance of the multiple of STND.VVUQ.33 times a grid estimate so converted applies two safety margins; for a correctness check against an exact or manufactured solution, the order test of STND.VVUQ.21 is the tighter check. STND.VVUQ.41 and STND.VVUQ.42 restate the trial-count rule and adaptive procedure of JCGM 101 as its final draft and three independent restatements give them; STND.VVUQ.41 suits inexpensive models, and for a model too costly for 10^4/(1 - p) trials, the order-statistic limits of STND.VVUQ.44, a surrogate checked under STND.VVUQ.46, or a statement of the statistical uncertainty of the interval's endpoints serves instead. JCGM 101 also judges first-order propagation adequate where the endpoints of its coverage interval differ from those of a Monte Carlo propagation by no more than the numerical tolerance; STND.VVUQ.43 judges that comparison against one quarter of the required precision instead, which the error budget sets (STND.VVUQ.10).

How strictly to judge a result. A tolerance tighter than the noise floor of its comparison fails correct work, and repeated false failures invite silent loosening; a tolerance looser than the departure the comparison has the purpose of detecting passes defective work. STND.VVUQ.7 therefore keeps each tolerance within its tolerance bracket, and STND.VVUQ.8 places it by purpose: at the lower end for the correctness of an implementation, which detects the smallest defect the noise floor permits; at the upper end for fitness for use, which leaves a guard band below the required precision. An empty bracket means the comparison is unable to show its claim, and the result stays unverified until its noise floor falls. The tiers of STND.VVUQ.1 are ordered by the sources of difference each admits: bitwise identity admits none, a bound in units in the last place admits one operation's rounding, and each later tier admits a further source. Agreement within 4 units in the last place, the default of a widely used test framework for double-precision equality, is a convention for single operations and short sequences; STND.VVUQ.4 asks for the bound's basis instead. A result judged against a tolerance loosened after the result was seen remains unverified (QA.12). The custodian directs, for every parallel execution model, that strict determinism be an option where it is feasible and not a requirement unless the acceptance criterion of the work or its consequence class demands it. A difference whose every source is declared under HW.12 or recorded with the compared runs, and which lies within the agreement that the acceptance criterion fixed before the comparison, is therefore no defect (STND.VVUQ.82); known jitter between thread counts, process counts, or a processor and an accelerator is settled by that declaration or record and the tier of STND.VVUQ.1. A difference beyond that agreement, or one that remains with the declared sources held fixed, falls outside STND.VVUQ.82, and loosening its tolerance is the decision that STND.VVUQ.8 governs. STND.VVUQ.83 holds agents to the same direction at every class, CSQ4 included, where the other provisions of this standard may be omitted: it forbids only work that an agent starts on its own initiative to remove such a difference, and costs one line of its work report, so that, as the custodian ruled at ratification, it raises no floor (GOV.11, PRIN.10). As the custodian distinguishes, a true race condition is a correctness defect, which DSGN.15 and HW.11 govern and which neither provision excuses, while variation from an order of launch, scheduling, or gathering that is otherwise safe is not of itself a defect. A deterministic mode is permitted as an option, and bitwise identity, where an acceptance criterion asks for it, is reached as STND.VVUQ.2 states. A tracked quantity's band is not a tolerance under NUMER.11 and does not become an acceptance criterion; a tracked quantity is not a tracked defect in the sense of LVL0. Invariants that VV.10 requires are asserted, as LVL0 directs, whatever their tier. A bound that holds only with a stated probability, as that of STND.VVUQ.37 does, is converted to a standard uncertainty (NUMER.13) before it enters a tolerance bracket.

Components of the error budget and their default treatment:

| Component (NUMER.13) | Systematic or random | Aleatory or epistemic | Controlled | Default treatment |
| --- | --- | --- | --- | --- |
| Discretization error | Systematic: trueness | Epistemic | Yes | Targeted to its allocation; its estimate tracked across runs; the method's order asserted in code verification |
| Stopping error | Systematic | Epistemic | Yes | Targeted at one hundredth of the discretization error, or at the rounding error (STND.VVUQ.29) |
| Rounding error | Systematic in one run; a dispersion across platforms | Epistemic | Yes | Asserted at tiers 1 to 3; working precision chosen to meet NUMER.5 |
| Effect of an approximation or a surrogate (NUMER.16, NUMER.17) | Systematic | Epistemic | Yes | Estimated under STND.VVUQ.50; targeted within the required precision |
| Statistical uncertainty of the computation's own sampling | Random: dispersion | Epistemic, reducible by more samples | Yes | Targeted by sample count; stability asserted (STND.VVUQ.42, STND.VVUQ.61) |
| Input uncertainty from variability | Random | Aleatory | No | Characterized by distributions and propagated; tracked |
| Input uncertainty from lack of knowledge | Systematic | Epistemic | No | Intervals or families of distributions; tracked; the largest named for reduction |
| Uncertainty of an input that is another result (NUMER.14) | As that result states | As that result states | No | Carried from that result's own error budget |
| Model-form uncertainty | Systematic | Epistemic | No | Estimated by validation at tier 6, with validation status under STND.VVUQ.48; tracked, not asserted |

Where controlled components are standard uncertainties at one coverage combined by root sum of squares (STND.VVUQ.39), controlled components together at one quarter of the largest uncontrolled component add about 3 percent to the total; where they widen an interval or a probability box (STND.VVUQ.12), they add linearly, about 25 percent. A project instrument is able to tighten the fraction for a more severe consequence class.

Default treatment of common quantities:

| Quantity | Tier of STND.VVUQ.1 | Treatment |
| --- | --- | --- |
| Reruns of the same build, and computations continued from saved state that holds the complete state of the computation | 1 | Asserted |
| Integer and logical outputs that no floating-point comparison decides | 1 | Asserted |
| Elementary functions and short kernels against a reference | 2 | Asserted |
| Conservation, symmetry, and bounds that the model requires (VV.10) | 3 where the discrete scheme preserves the property; 4 where only the model does; 1 for counts | Asserted |
| Results across hardware, decompositions, compilers, or libraries | 3 where no stopping test or branch depends on rounding; 4 otherwise; 5 for chaotic dynamics (STND.VVUQ.32) | Asserted where the bracket is not empty; otherwise the variation is declared under REPRO.3 and the result reported unverified |
| Order of accuracy on exact or manufactured solutions | 4 | Asserted |
| Discretization and stopping error of production results | 4 | Targeted; estimates tracked |
| Statistical uncertainty of Monte Carlo estimates | 5 | Targeted; stability asserted |
| Stochastic results against references | 5 | Asserted under STND.VVUQ.33, STND.VVUQ.34, and STND.VVUQ.35, with a repetition rule (STND.VVUQ.65) |
| Markov chain diagnostics | Preconditions of reliance (NUMER.23) | Asserted at fixed seeds; tracked with fresh seeds |
| Comparison errors against measurements | 6 | Validation status stated (STND.VVUQ.48); the error tracked |
| Epistemic input and model-form uncertainty | 6 | Tracked; the largest named for reduction |
| Earlier outputs of the same code | The tier of the comparison | Asserted as a regression guard (STND.VVUQ.17) |
| Computing time, memory, and operating cost | None | Tracked |

Extending the chains of a run whose diagnostics failed is further sampling, not a repetition of a failed comparison under NUMER.26.

The multiple of STND.VVUQ.33 is 3.29 for one comparison at a rate of 0.001, 3.89 for 10 comparisons, 4.42 for 100, and 4.89 for 1000; a fixed multiple of 3 would reject a correct result in about 0.27 percent of single comparisons, above the default suite rate. For a suite that fails when any comparison fails, the Holm procedure of STND.VVUQ.35 and the multiple of STND.VVUQ.33 fail the suite in the same cases; Holm then identifies which comparisons fail. The effective sample size of 400 makes the diagnostics of STND.VVUQ.58 reliable and gives a Monte Carlo standard error of 0.05 posterior standard deviations; it is not a precision target, which STND.VVUQ.59 sets. Bitwise identity holds only on fixed hardware and software, because parallel reductions and vendor libraries reorder arithmetic. A random number generator that passes a test battery is not thereby proven sound. Batteries differ in power: the TestU01 library holds smaller batteries beside BigCrush, the one that STND.VVUQ.63 named before this revision. A record that names the battery applied, with its revision, lets the test be repeated as it ran. Multistart from several points does not show a global optimum. Under deterministic noise no heuristic choice of a regularization strength is guaranteed to converge, which is why STND.VVUQ.54 prefers the discrepancy principle where the noise level is known. Simulation-based calibration checks the posterior computation against the inversion's own model; the coverage that NUMER.19 requires is shown separately on independently produced data (STND.VVUQ.52). A trajectory of chaotic dynamics beyond its predictability horizon is not converged, whatever its refinement (NUMER.9). NUMER.26 forbids repeating a failed stochastic comparison unless a rule of repetition was recorded before the failure; STND.VVUQ.65 gives the default form of that rule.

STND.VVUQ.77 measures a comparison of a learned and a numerical method under the conditions that HW.22 states for a comparative performance claim, a matter that HW owns. Where HW.22 binds, for a claim between execution paths stated in a reported result or a release, its requirement holds in full; STND.VVUQ.77 extends its conditions as a default to methods compared on one path. STND.VVUQ.79 to STND.VVUQ.81 give the default extrapolation criterion that HW.17 asks to be recorded before a comparison that the reference path cannot complete: one fit for deterministic results, one for stochastic results, and one rule of acceptance for each. For deterministic results the prediction interval of a new observation carries the scatter of the differences; with six sizes it has four degrees of freedom, and it widens with the distance of the extrapolation, so a short trend cannot vouch for a long reach. For stochastic results the sampling noise of each estimate is known from its standard error, so the criterion extrapolates the expected difference, the bias, and judges its confidence interval against the tolerance; more samples at the compared sizes narrow it. In simulation, standard errors of a tenth of the tolerance let a correct path pass at a reach sixteen times beyond the largest compared size, while standard errors of a third of it fail at that reach. The fit against the count of operations, for a path whose contract states an error rate per operation, follows errors that compound with each operation. Choosing compared sizes below and above each size at which the hardware contract states a change of implementation choice, where the reference path reaches them, keeps that switch inside the fit. Where every observed difference is zero, the criterion rests on rounding spacing alone, and the full-size checks of HW.17 are the only guard against failures that appear only at scale. A criterion recorded under STND.VVUQ.80 and STND.VVUQ.81 states its probability of rejecting a correct result, as NUMER.25 asks; that probability depends on the standard errors and on the reach, not on the level of the interval alone, as the simulations above illustrate. The methods for learned surrogates here cover their numerical side; the ML profile owns the record, the error, and the domain of a learned model (ML.2) and leaves these methods to this standard. Methods for validation stay here; MEAS states outcomes for measured data, their acquisition, calibration, and uncertainty among them (MEAS.2), and leaves the choice of validation metric to this standard and to the project.

## References

| Identifier | Title |
| --- | --- |
| DSGN | Design |
| GOV | Governance |
| HW | Execution hardware |
| INTPR | Interpretability |
| MEAS | Measurement and instrumentation |
| ML | Learned models |
| NUMER | Numerical computation |
| PRIME | Prime Directives |
| PRIN | Governing Principles |
| QA | Process |
| REPRO | Reproducibility |
| RSRC | Resources |
| SIMPL | Simplicity |
| VV | Correctness |

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-11 | Adopted. |
| 1.1 | 2026-10-11 | Minor amendment (GOV.41) after the review of its provision pairs and its cold review: STND.VVUQ.37 sets lambda by the probability its analysis supports, 2.72 for a product of n factors and the square root of 2 ln(40n) over one less the unit roundoff for an inner product; STND.VVUQ.40 asks for ten Latin hypercube replicates; STND.VVUQ.50 estimates the effect of a retained performance approximation by runs without it in the regime of each reported result it affects, at that result's discretization, and admits a bound by analysis only for other approximations; STND.VVUQ.61 checks every statistical uncertainty, tallies included, against the fraction recorded under NUMER.23, with estimates scaled by the square root of their sample counts; STND.VVUQ.70 treats a relative discrepancy of 1e-5 as a defect only where its test's tolerance is below 1e-5. |
| 1.2 | 2026-10-18 | Minor amendment (GOV.41), conforming on the adoption of HW: STND.VVUQ.77 measures a comparison of a learned and a numerical method under the conditions of HW.22; new STND.VVUQ.79 to STND.VVUQ.81, in a new section Execution paths, give the default extrapolation criterion for a comparison beyond the reach of the reference path (HW.17); the term Extrapolation abscissa is added. |
| 1.2.1 | 2026-10-19 | Editorial amendment (GOV.41): the informative Notes describe ML and MEAS as adopted; no obligation changes. |
| 1.3 | 2026-10-24 | Minor amendment (GOV.41): new STND.VVUQ.82 treats a difference between compared results that declared run-to-run variation explains, within the agreement of its tier, as no defect; discourages changes made only to remove it unless an acceptance criterion or the consequence class requires bitwise identity; and admits a deterministic mode as an option; new STND.VVUQ.83, binding on agents (GOV.48), forbids an agent to change or extend the work on its own initiative only to remove such a difference, and has it state each difference it leaves. |
| 1.4 | 2026-10-24 | Minor amendment (GOV.41): STND.VVUQ.63 states the outcome that a test battery decides, a published battery of statistical tests of randomness at least as demanding as the use of the generator requires, named with its revision in the record of the work, in place of naming one battery; the Notes say that batteries differ in power, name BigCrush, the battery that the provision named before, beside the smaller ones of its library, and cite ML.2 and MEAS.2 for the matters that ML and MEAS own; References lists ML and MEAS; and, as an editorial change, STND.VVUQ.2 and its row of the table of common quantities speak of a computation that continues from state saved by an earlier run, in place of a checkpoint and its restart. |
