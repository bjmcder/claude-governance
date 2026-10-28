# Verification, validation, and uncertainty quantification methods (STND.VVUQ) 1.5.1

Adopted by The Custodian as revision 1.0 in ledger entry 61 (2026-10-11); revised to 1.1 in entry 63 (2026-10-11), 1.2 in entry 67 (2026-10-18), 1.2.1 in entry 88 (2026-10-19), 1.3 in entry 107 (2026-10-24), 1.4 in entry 122 (2026-10-24), 1.5 in entry 285 (2026-10-28), and 1.5.1 in entry 297 (2026-10-28). This reading copy is composed from the per-provision files in STND/VVUQ/ of the governance harness; the harness files are the system of record.

## Purpose and scope

This standard holds the default methods by which work produces the evidence that the NUMER profile requires. NUMER states each outcome and its bounds without naming a method; this standard names the methods that current practice supports, with default numbers an agent applies unattended. Its core is three instruments that set how strictly each result is judged. The section Comparison tiers ranks comparisons from bitwise identity, through units in the last place and tolerances set from rounding and numerical error, to statistical criteria and uncertainty statements, and places each tolerance within a bracket between the noise floor of its comparison and the departure it has the purpose of detecting. The section Error budget allocates the required precision among numerical, statistical, input, and model-form components and keeps aleatory and epistemic uncertainty apart. The section Assertion and tracking decides whether each quantity is asserted, tracked, or targeted. The remaining sections give methods and numbers for the evidence those instruments use. STND.VVUQ.83 instantiates GOV.11 and GOV.48 and is binding on agents at every class; every other provision, its numbers included, is a default (GOV.19) and a recommendation, whether its number comes from a source or from a convention: an actor that uses another method or number meeting the same NUMER outcome records the method and its reason as a decision (REPRO.7, PRIN.10), and asks no one. STND.VVUQ.77 and STND.VVUQ.78 rest on LVL0 directly, for claims of comparison and the timing of verification. Methods and numbers change as the field advances; a change here leaves NUMER unchanged.

The provisions were synthesized from a research note of 2026-10-11, which surveyed standards bodies, national laboratories, agencies, and the literature, and logged each retrieval; the note is not kept in the project. Where a default number rests on a source, the table of sources in the Notes gives it; where it is a convention that no retrieved source sets, the Notes say so.

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
| MCNP Theory and User Manual | Current release; not opened by the research |

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
| Ten tally-fluctuation checks and their thresholds | STND.VVUQ.61 | an earlier MCNP manual and a CANTEACH chapter; the current MCNP manual was not opened |
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

The multiple of STND.VVUQ.33 is 3.29 for one comparison at a rate of 0.001, 3.89 for 10 comparisons, 4.42 for 100, and 4.89 for 1000; a fixed multiple of 3 would reject a correct result in about 0.27 percent of single comparisons, above the default suite rate. For a suite that fails when any comparison fails, the Holm procedure of STND.VVUQ.35 and the multiple of STND.VVUQ.33 fail the suite in the same cases; Holm then identifies which comparisons fail. The effective sample size of 400 makes the diagnostics of STND.VVUQ.58 reliable and gives a Monte Carlo standard error of 0.05 posterior standard deviations; it is not a precision target, which STND.VVUQ.59 sets. Bitwise identity holds only on fixed hardware and software, because parallel reductions and vendor libraries reorder arithmetic. A random number generator that passes a test battery is not thereby proven sound. Batteries differ in power: the TestU01 library holds smaller batteries beside BigCrush, the largest. A record that names the battery applied, with its revision, lets the test be repeated as it ran. Multistart from several points does not show a global optimum. Under deterministic noise no heuristic choice of a regularization strength is guaranteed to converge, which is why STND.VVUQ.54 prefers the discrepancy principle where the noise level is known. Simulation-based calibration checks the posterior computation against the inversion's own model; the coverage that NUMER.19 requires is shown separately on independently produced data (STND.VVUQ.52). A trajectory of chaotic dynamics beyond its predictability horizon is not converged, whatever its refinement (NUMER.9). NUMER.26 forbids repeating a failed stochastic comparison unless a rule of repetition was recorded before the failure; STND.VVUQ.65 gives the default form of that rule.

STND.VVUQ.77 measures a comparison of a learned and a numerical method under the conditions that HW.22 states for a comparative performance claim, a matter that HW owns. Where HW.22 binds, for a claim between execution paths stated in a reported result or a release, its requirement holds in full; STND.VVUQ.77 extends its conditions as a default to methods compared on one path. STND.VVUQ.79 to STND.VVUQ.81 give the default extrapolation criterion that HW.17 asks to be recorded before a comparison that the reference path cannot complete: one fit for deterministic results, one for stochastic results, and one rule of acceptance for each. For deterministic results the prediction interval of a new observation carries the scatter of the differences; with six sizes it has four degrees of freedom, and it widens with the distance of the extrapolation, so a short trend cannot vouch for a long reach. For stochastic results the sampling noise of each estimate is known from its standard error, so the criterion extrapolates the expected difference, the bias, and judges its confidence interval against the tolerance; more samples at the compared sizes narrow it. In simulation, standard errors of a tenth of the tolerance let a correct path pass at a reach sixteen times beyond the largest compared size, while standard errors of a third of it fail at that reach. The fit against the count of operations, for a path whose contract states an error rate per operation, follows errors that compound with each operation. Choosing compared sizes below and above each size at which the hardware contract states a change of implementation choice, where the reference path reaches them, keeps that switch inside the fit. Where every observed difference is zero, the criterion rests on rounding spacing alone, and the full-size checks of HW.17 are the only guard against failures that appear only at scale. A criterion recorded under STND.VVUQ.80 and STND.VVUQ.81 states its probability of rejecting a correct result, as NUMER.25 asks; that probability depends on the standard errors and on the reach, not on the level of the interval alone, as the simulations above illustrate. The methods for learned surrogates here cover their numerical side; the ML profile owns the record, the error, and the domain of a learned model (ML.2) and leaves these methods to this standard. Methods for validation stay here; MEAS states outcomes for measured data, their acquisition, calibration, and uncertainty among them (MEAS.2), and leaves the choice of validation metric to this standard and to the project.

Under STND.CLASS.10, each default applies from the class that its field `onset` gives, which work of CSQ4 may omit, and STND.VVUQ.83 binds at every class. The core that applies from CSQ3, STND.VVUQ.1, STND.VVUQ.3, STND.VVUQ.5, STND.VVUQ.7, STND.VVUQ.13, STND.VVUQ.17, STND.VVUQ.62, STND.VVUQ.64, and STND.VVUQ.82, with the basis of each tolerance that NUMER.11 asks, chooses the tier of each comparison, handles values that are not finite, states each tolerance with its relative and absolute parts within its bracket, keeps asserted checks and regression guards, and builds and tests random streams, and at CSQ3 STND.VVUQ.64 judges a test with fresh seeds by the criterion that its acceptance criterion states, since STND.VVUQ.33 to STND.VVUQ.35 start at CSQ2; the methods of high-assurance numerics, from error budgets and noise floors to multiplicity control and order tests at several levels, start at CSQ2, so that work of CSQ3 meets NUMER through the core, while the obligations of LVL0 that the other provisions serve apply to it in full. No default raises the floor (GOV.11).

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
| STND.CLASS | Consequence-class criteria |
| VV | Correctness |

## Provisions

### Comparison tiers

#### STND.VVUQ.1 Comparison tier choice

Default, from CSQ3. Instantiates NUMER.11, REPRO.3, VV.1, VV.3.

Each comparison that judges a numerical result SHOULD use the strictest tier of the table of this provision whose admitted differences include every source of difference between the compared values (NUMER.11, REPRO.3, VV.1, VV.3).

| Tier | Admitted differences | Agreement |
| --- | --- | --- |
| 1. Bitwise | None: the values come from the same build, loaded libraries, hardware model, inputs, seeds, process and thread counts, and arithmetic settings, with each reduction and atomic update in a fixed order; or each value is an exact value | Identical bits, with non-finite values judged under STND.VVUQ.3 |
| 2. Units in the last place | Rounding within one elementary function or one fixed sequence of operations, against a correctly rounded or higher-precision reference, with an error bound in units in the last place from documented accuracy or an error analysis | That bound, counted in units in the last place of the reference at the working precision |
| 3. Rounding tolerance | Also rounding through hardware, parallel decomposition, operation order, compiler, or library, on a path whose stopping tests, adaptive choices, pivots, and branches no such rounding alters, with dynamics that are not chaotic | A tolerance set from the rounding error estimated under NUMER.12 |
| 4. Numerical-error tolerance | Also discretization error, stopping error, the effect of an approximation listed under NUMER.16, input or model-form uncertainty that a guaranteed bound limits, and the numerical error of an exact, manufactured, or benchmark solution or of an independent implementation | A tolerance, or an observed order, set from the estimated numerical error, the approximation's estimated effect, each guaranteed bound, and the reference's uncertainty |
| 5. Statistical criterion | Also the statistical uncertainty of an estimate of a stochastic method whose random numbers the other value does not share | A criterion with a stated probability of rejecting a correct result and a stated detection power |
| 6. Uncertainty statement | Also measurement, input, and model-form uncertainty that no guaranteed bound limits | The comparison error with its uncertainty, and, against a measurement, the validation status of STND.VVUQ.48 |

#### STND.VVUQ.2 Bitwise identity

Default, from CSQ2. Instantiates NUMER.11, REPRO.3, VV.1, VV.3.

Where bitwise identity across runs is an acceptance criterion, each reduction on the path of the result SHOULD use a fixed or order-independent summation (NUMER.11, REPRO.3, VV.1, VV.3). Where a computation that continues from state saved by an earlier run is judged by bitwise identity, the saved state SHOULD hold the complete state of the computation, its random number states included (REPRO.3).

#### STND.VVUQ.3 Non-finite values

Default, from CSQ3. Instantiates NUMER.11, REPRO.3, VV.1, VV.3.

A NaN SHOULD agree in a comparison with a NaN only, whatever its payload and sign (NUMER.11, REPRO.3, VV.1, VV.3). An infinity SHOULD agree in a comparison with an infinity of the same sign only (NUMER.11, VV.1, VV.3, REPRO.3). Where the reference of a comparison is finite, a non-finite compared value SHOULD fail the comparison (NUMER.11, VV.1, VV.3, REPRO.3).

#### STND.VVUQ.4 Bounds in last-place units

Default, from CSQ2. Instantiates NUMER.11, VV.1, VV.3, REPRO.3.

Where a documented accuracy in units in the last place is a tested maximum rather than a proven bound, a bound resting on it SHOULD add a recorded margin, by default one unit in the last place (NUMER.11, VV.1, VV.3, REPRO.3). Where the relative rounding error of a value has no bound that holds for each operand in the regime of use, the value SHOULD be judged at tier 3 or a less strict tier of STND.VVUQ.1 (NUMER.11, VV.1, VV.3, REPRO.3). Where a build flushes subnormal values to zero, a value whose magnitude is below the smallest normal number SHOULD be judged at tier 3 or a less strict tier of STND.VVUQ.1 (NUMER.11, VV.1, VV.3, REPRO.3).

#### STND.VVUQ.5 Relative and absolute parts

Default, from CSQ3. Instantiates NUMER.11, VV.1, VV.3, REPRO.3.

Each tolerance of tier 3 or tier 4 of STND.VVUQ.1 SHOULD be the larger of a relative part, taken of the magnitude of the reference, and an absolute part (NUMER.11, VV.1, VV.3, REPRO.3). The absolute part SHOULD be set from the noise floor of values whose reference is zero, and at or below the relative part at the smallest magnitude of the quantity on which its intended use relies (NUMER.11, VV.1, VV.3, REPRO.3).

#### STND.VVUQ.6 Noise floor estimate

Default, from CSQ2. Instantiates NUMER.11, NUMER.13, VV.1, VV.3, REPRO.3, INTPR.9, VV.5.

The record of each tolerance SHOULD state the noise floor of its comparison and the evidence from which the noise floor was estimated (NUMER.11, NUMER.13, VV.1, VV.3, REPRO.3, INTPR.9, VV.5).

#### STND.VVUQ.7 Tolerance bracket

Default, from CSQ3. Instantiates NUMER.11, NUMER.25, VV.5, VV.1, VV.3, REPRO.3.

Each tolerance SHOULD lie within the tolerance bracket of its comparison, by default with the required precision as the departure that the comparison has the purpose of detecting (NUMER.11, NUMER.25, VV.1, VV.3, REPRO.3). Where the tolerance bracket of a comparison is empty, the record SHOULD state that the comparison is unable to show its claim (NUMER.11, VV.1, VV.3, REPRO.3). Where the tolerance bracket of a comparison is empty, the result that it judges SHOULD be reported as unverified while its tolerance bracket stays empty (NUMER.11, VV.5, VV.1, VV.3, REPRO.3).

#### STND.VVUQ.8 Tight and loose tolerances

Default, from CSQ2. Instantiates NUMER.11, VV.3, VV.1, REPRO.3.

A tolerance that checks the correctness of an implementation SHOULD be the lower end of its tolerance bracket (NUMER.11, VV.1, VV.3, REPRO.3). A tolerance that checks the fitness of a result for its intended use SHOULD be the upper end of its tolerance bracket (NUMER.11, VV.1, VV.3, REPRO.3). A tolerance SHOULD be loosened only by a recorded decision that states a noise floor estimated from evidence other than the comparison that prompted the change (NUMER.11, VV.3, VV.1, REPRO.3).

#### STND.VVUQ.82 Declared variation in comparisons

Default, from CSQ3. Instantiates REPRO.3, VV.3, RSRC.4.

Where every source of a difference between compared results is stated in the declaration of run-to-run variation of a compared execution path (HW.12) or in the records of the compared runs, and the difference lies within the agreement that the acceptance criterion of the comparison fixed under STND.VVUQ.1 before the comparison, the difference SHOULD NOT be treated as a defect (REPRO.3, VV.3). Other than where an acceptance criterion of the work, or a provision that applies at its consequence class, requires bitwise identity, a change SHOULD NOT be made only to remove such a difference (REPRO.3, RSRC.4). An execution path MAY offer a mode without run-to-run variation (REPRO.3).

#### STND.VVUQ.83 Agent conduct toward known variation

Binding. Instantiates GOV.11, GOV.48, PRIME.2.

Where every source of a difference between compared results is stated in the record of the work, and the difference lies within the agreement that the work fixed for the comparison, an agent SHALL NOT, on its own initiative, change the work only to remove that difference (GOV.11, GOV.48). Where the work states no acceptance criterion of bitwise identity, an agent SHALL NOT, on its own initiative, extend a unit of work only to make results identical across numbers of threads, numbers of processes, or hardware models (GOV.11, GOV.48). An agent SHALL state in its work report each difference that it leaves under this provision, with its source (PRIME.2, GOV.48).

### Error budget

#### STND.VVUQ.9 Error budget

Default, from CSQ2. Instantiates NUMER.5, NUMER.13, VV.3, VV.5, DSGN.5, REPRO.2, REPRO.7, VV.1, INTPR.9.

Each numerical specification SHOULD allocate the required precision of its quantity of interest among the components of NUMER.13, in an error budget whose allocations, or the rules that set them from estimated components, are recorded before results are seen (NUMER.13, VV.3, INTPR.9, VV.5, VV.1). Where the combined uncertainty of a reported result exceeds its required precision, the report SHOULD state that the result does not meet its required precision (NUMER.5, VV.5, DSGN.5, REPRO.2, REPRO.7, VV.1).

#### STND.VVUQ.10 Controlled component allocation

Default, from CSQ2. Instantiates NUMER.9, NUMER.13, VV.1, INTPR.9, VV.5.

The root sum of squares of the controlled components SHOULD be at or below one quarter of the larger of the required precision and the largest uncontrolled component that is estimated or bounded, each stated at one common probability of containment (NUMER.9, NUMER.13, VV.1, INTPR.9, VV.5).

#### STND.VVUQ.11 Negligible components

Default, from CSQ2. Instantiates NUMER.13, INTPR.9, VV.5, VV.1.

Where components are combined by root sum of squares, the root sum of squares of the components omitted as negligible SHOULD be at or below one quarter of the largest component, each stated at one common probability of containment (NUMER.13, INTPR.9, VV.5, VV.1). Where components are combined by adding intervals or widening a probability box, the sum of the components omitted as negligible SHOULD be at or below one thirtieth of the largest component (NUMER.13, INTPR.9, VV.5, VV.1). Each omitted component SHOULD be listed with its estimate (NUMER.13, INTPR.9, VV.5, VV.1).

#### STND.VVUQ.12 Aleatory and epistemic inputs

Default, from CSQ2. Instantiates NUMER.13, NUMER.15, INTPR.9, VV.5, VV.1, REPRO.6.

Each uncertain input SHOULD be classified in its numerical specification as aleatory or epistemic (NUMER.13, NUMER.15, INTPR.9, VV.5, VV.1, REPRO.6). An epistemic input without a distribution that evidence supports SHOULD be represented by an interval (NUMER.13, INTPR.9, VV.5, VV.1). A result whose inputs include both kinds SHOULD be stated so that its aleatory and epistemic parts stay distinguishable, by default as a probability box (NUMER.13, INTPR.9, VV.5, VV.1).

### Assertion and tracking

#### STND.VVUQ.13 Asserted checks

Default, from CSQ3. Instantiates VV.1, NUMER.11, VV.3, REPRO.3.

Where a property has a reference whose tolerance bracket under STND.VVUQ.7 is not empty, the property SHOULD be judged by an asserted check (VV.1, NUMER.11, VV.3, REPRO.3).

#### STND.VVUQ.14 Tracked quantities

Default, from CSQ2. Instantiates INTPR.7, REPRO.3.

Where a quantity that bears on reliance on a result has no reference, it SHOULD be a tracked quantity (INTPR.7, REPRO.3). The band of a tracked quantity SHOULD be set, by a rule recorded before its first comparison, from a recorded baseline of its history (INTPR.7). A value that departs beyond the band SHOULD NOT enter the baseline without a recorded decision (INTPR.7).

#### STND.VVUQ.15 Targeted components

Default, from CSQ2. Instantiates NUMER.9, NUMER.22, INTPR.9, VV.1.

Each controlled component SHOULD be a targeted component, refined, sampled, or computed at higher precision until it meets its allocation in the error budget (NUMER.9, NUMER.22, VV.1, INTPR.9). Where a targeted component misses its allocation within the budget recorded for the work, the report SHOULD state the value reached, the shortfall, and whether the combined uncertainty meets the required precision (NUMER.9, INTPR.9, VV.1).

#### STND.VVUQ.16 Epistemic components

Default, from CSQ2. Instantiates NUMER.13, VV.5, INTPR.10, INTPR.9, VV.1.

An uncontrolled epistemic component that no guaranteed bound limits SHOULD be tracked rather than judged by an asserted check (NUMER.13, VV.5, INTPR.9, VV.1). Where an epistemic component is the largest in an error budget, the report SHOULD name the data, analysis, or computation that would reduce it (NUMER.13, INTPR.10, INTPR.9, VV.5, VV.1).

#### STND.VVUQ.17 Regression guard failures

Default, from CSQ3. Instantiates VV.1, VV.3.

Where the record of a change does not state, before its regression guards run, that the change alters a guarded result, a failure of one of those guards SHOULD be treated as a defect rather than as a reason to renew its reference (VV.3, VV.1). Where a change whose record states that it alters a guarded result fails that guard, the guard's reference SHOULD be renewed only by a recorded decision that cites the correctness evidence that the changed result passed (VV.3, VV.1).

### Code verification

#### STND.VVUQ.18 Preferred reference oracles

Default, from CSQ2. Instantiates NUMER.6, VV.1, VV.6.

Each numerical method SHOULD be verified against, in order of preference, an exact solution of its mathematical model, a manufactured solution, a benchmark solution confirmed under VV.2, or an independent implementation (NUMER.6, VV.1, VV.6).

#### STND.VVUQ.19 Manufactured solution form

Default, from CSQ2. Instantiates NUMER.6, VV.1, VV.6.

A manufactured solution SHOULD be smooth, keep every derivative and cross-derivative that the model uses nonzero, let no term of the model dominate the others, and be physically realizable (NUMER.6, VV.1, VV.6).

#### STND.VVUQ.20 Order test levels

Default, from CSQ2. Instantiates NUMER.7, VV.1, VV.3, VV.5.

Where a method has an algebraic theoretical order, its order test SHOULD use at least four refinement levels, with a refinement ratio above 1.3 between successive levels, constant where no exact or manufactured solution is available (NUMER.7, VV.1, VV.3, VV.5).

#### STND.VVUQ.21 Order acceptance

Default, from CSQ2. Instantiates NUMER.7, VV.1, VV.3, VV.5.

An order test SHOULD accept the theoretical order where the observed orders of the two finest pairs of levels each lie within 10 percent of it and the observed orders over the levels approach it (NUMER.7, VV.1, VV.3, VV.5).

#### STND.VVUQ.22 Oscillatory convergence

Default, from CSQ2. Instantiates NUMER.7, NUMER.9, VV.1, VV.3, VV.5, INTPR.9.

Where successive differences between refinement levels change sign, the report SHOULD state oscillatory convergence with the apparent order, and claim no order of the method from it (NUMER.7, NUMER.9, VV.1, VV.3, VV.5, INTPR.9).

#### STND.VVUQ.23 Discontinuous solutions

Default, from CSQ2. Instantiates NUMER.7, VV.1, VV.3, VV.5.

Where a reference solution has a discontinuity, the order test SHOULD measure error in a norm recorded before the test, by default the L1 norm, and expect at most first order near a shock and the order p/(p+1) near a contact discontinuity for a scheme of order p (NUMER.7, VV.1, VV.3, VV.5).

#### STND.VVUQ.24 Error separation in order tests

Default, from CSQ2. Instantiates NUMER.7, NUMER.8, VV.1, VV.3, VV.5, INTPR.9.

During an order test, the rounding and stopping errors at each refinement level SHOULD be at least 100 times smaller than its discretization error (NUMER.7, NUMER.8, VV.1, VV.3, VV.5, INTPR.9).

#### STND.VVUQ.25 Adaptive methods

Default, from CSQ2. Instantiates NUMER.6, NUMER.8, VV.1, VV.6, INTPR.9.

Where a method adapts its discretization, its verification SHOULD refine the adaptation tolerance and report the effectivity index of its error estimator on a reference problem (NUMER.6, NUMER.8, VV.1, VV.6, INTPR.9).

### Solution verification

#### STND.VVUQ.26 Error estimators

Default, from CSQ2. Instantiates NUMER.9, VV.1, INTPR.9.

The numerical error of a reported result SHOULD be estimated by Richardson extrapolation with the grid convergence index from at least three refinement levels, by the least-squares procedure from at least four levels where the levels scatter, or by an a posteriori estimator verified under STND.VVUQ.25 (NUMER.9, VV.1, INTPR.9). Each estimate SHOULD report the observed order on which it rests (NUMER.9, VV.1, INTPR.9).

#### STND.VVUQ.27 Safety factor

Default, from CSQ2. Instantiates NUMER.9, VV.1, INTPR.9.

A grid convergence index from three or more refinement levels SHOULD use a safety factor of 1.25 where the observed order lies within the tolerance of STND.VVUQ.21 of the theoretical order, and 3 otherwise (NUMER.9, VV.1, INTPR.9). The least-squares procedure SHOULD use a safety factor of 1.25 where the standard deviation of its fit is below its data range parameter and the observed order p lies in a band recorded before the study, by default 0.5 <= p < 2.1 for a method of theoretical order 2, and otherwise the uncertainty that the procedure gives for that case (NUMER.9, VV.1, INTPR.9).

#### STND.VVUQ.28 Coverage of grid estimates

Default, from CSQ2. Instantiates NUMER.13, INTPR.9, VV.5, VV.1.

An error estimate from the grid convergence index or the least-squares procedure SHOULD be stated as an interval of 95 percent coverage (NUMER.13, INTPR.9, VV.5, VV.1). Where such an estimate is combined with standard uncertainties, it SHOULD be divided by 1.1 (NUMER.13, INTPR.9, VV.5, VV.1).

#### STND.VVUQ.29 Stopping error margin

Default, from CSQ2. Instantiates NUMER.8, NUMER.10, VV.1, INTPR.9.

Each stopping criterion on the path of a reported result SHOULD hold the stopping error at or below the larger of one hundredth of the result's estimated discretization error and its estimated rounding error (NUMER.8, NUMER.10, VV.1, INTPR.9). Within a refinement study, each stopping criterion SHOULD hold the stopping error at or below the larger of one hundredth of the smallest difference between successive refinement levels and the estimated rounding error (NUMER.8, NUMER.10, VV.1, INTPR.9).

#### STND.VVUQ.30 Scaled stopping criteria

Default, from CSQ2. Instantiates NUMER.10, INTPR.9.

Each stopping criterion SHOULD be stated relative to the scale of the quantity it tests (NUMER.10, INTPR.9).

#### STND.VVUQ.31 Pointwise oscillation share

Default, from CSQ2. Instantiates NUMER.9, VV.1, INTPR.9.

Where the error of a reported field is estimated point by point, the report SHOULD give the percentage of points that converge oscillatorily (NUMER.9, VV.1, INTPR.9).

#### STND.VVUQ.32 Chaotic dynamics

Default, from CSQ2. Instantiates NUMER.9, NUMER.22, VV.1, INTPR.9.

Where the dynamics of a model are chaotic, each quantity of interest SHOULD be a statistic over a stated averaging window, with a sampling uncertainty that accounts for autocorrelation (NUMER.9, NUMER.22, VV.1, INTPR.9).

### Statistical criteria

#### STND.VVUQ.33 Acceptance multiple

Default, from CSQ2. Instantiates NUMER.11, NUMER.25, REPRO.3, VV.1, VV.3.

An acceptance criterion against a standard uncertainty SHOULD use the two-sided multiple k = z(1 - a/(2m)) for the false-rejection rate a of its suite and the number m of its comparisons, with a = 0.001 per suite run by default, or the Student-t quantile at the same probability where the standard uncertainty has fewer than 30 degrees of freedom (NUMER.11, NUMER.25, REPRO.3, VV.1, VV.3). An acceptance criterion against an interval or a bound SHOULD use a multiple of 1 only where the interval's coverage is at least 1 - a/m (NUMER.11, NUMER.25, REPRO.3, VV.1, VV.3).

#### STND.VVUQ.34 Detection power

Default, from CSQ2. Instantiates NUMER.25, VV.1, VV.3.

Each acceptance criterion of STND.VVUQ.33 SHOULD hold the standard uncertainty of its compared difference at or below d/(k + 1.28), where d is the required precision, so that a departure equal to the required precision is detected with probability 0.9 (NUMER.25, VV.1, VV.3).

#### STND.VVUQ.35 Multiplicity control

Default, from CSQ2. Instantiates NUMER.25, VV.1, VV.3.

A suite of statistical acceptance criteria SHOULD control its probability of rejecting a correct result by the Holm step-down procedure (NUMER.25, VV.1, VV.3).

### Rounding and precision

#### STND.VVUQ.36 Rounding estimates

Default, from CSQ2. Instantiates NUMER.12, VV.1, INTPR.10.

The rounding error of a reported result SHOULD be estimated by a condition-number estimate with a backward-error bound, by comparison with the same computation at higher precision, or by stochastic arithmetic with a stated confidence (NUMER.12, VV.1, INTPR.10).

#### STND.VVUQ.37 Probabilistic rounding bound

Default, from CSQ2. Instantiates NUMER.12, VV.1, INTPR.10.

Where a rounding estimate uses the probabilistic bound lambda times the square root of n times the unit roundoff, it SHOULD take lambda at or above the value for which its probabilistic error analysis gives a probability of at least 0.95 that the bound holds for that computation, by default 2.72 for a product of n rounding factors and the square root of 2 ln(40n), divided by one less the unit roundoff, for an inner product of length n, state the worst-case bound beside it, and be confined to computations whose rounding errors are independent and of zero mean (NUMER.12, VV.1, INTPR.10).

#### STND.VVUQ.38 Reduced precision

Default, from CSQ2. Instantiates NUMER.5, DSGN.5, REPRO.2, REPRO.7, VV.1.

Each computation in reduced precision on the path of a reported result SHOULD be verified against the same computation at a higher precision (NUMER.5, DSGN.5, REPRO.2, REPRO.7, VV.1).

### Uncertainty

#### STND.VVUQ.39 Root-sum-square combination

Default, from CSQ2. Instantiates NUMER.13, INTPR.9, VV.5, VV.1.

Where components are combined by root sum of squares, each SHOULD be stated at one common coverage and be approximately normally distributed (NUMER.13, INTPR.9, VV.5, VV.1).

#### STND.VVUQ.40 Sampling propagation

Default, from CSQ2. Instantiates NUMER.13, NUMER.22, INTPR.9, VV.5, VV.1.

Uncertainty propagated by sampling SHOULD use simple random sampling, at least ten replicated Latin hypercube designs, or randomized quasi-Monte Carlo with at least ten independent randomizations, with a Student-t interval across replicates for the replicated designs (NUMER.13, NUMER.22, INTPR.9, VV.5, VV.1).

#### STND.VVUQ.41 Monte Carlo trial count

Default, from CSQ2. Instantiates NUMER.13, NUMER.22, INTPR.9, VV.5, VV.1.

Where a fixed number of Monte Carlo trials propagates uncertainty to a coverage interval of probability p, that number SHOULD be at least 10^4/(1 - p) (NUMER.13, NUMER.22, INTPR.9, VV.5, VV.1).

#### STND.VVUQ.42 Adaptive Monte Carlo stopping

Default, from CSQ2. Instantiates NUMER.13, NUMER.22, INTPR.9, VV.5, VV.1.

Where the number of Monte Carlo trials is chosen as the trials run, the trials SHOULD proceed in at least two stages of at least 10^4 and at least 100/(1 - p) trials each, until twice the standard deviation of the mean of the stage values of each of the estimate, its standard uncertainty, and the two endpoints of its coverage interval is at most the numerical tolerance of the standard uncertainty reported to two digits from its first nonzero digit (NUMER.13, NUMER.22, INTPR.9, VV.5, VV.1).

#### STND.VVUQ.43 Propagation methods

Default, from CSQ2. Instantiates NUMER.13, NUMER.15, INTPR.9, VV.5, VV.1, REPRO.6.

Uncertainty from inputs SHOULD be propagated by first-order sensitivities with the input covariances where a sampling check at recorded points gives coverage-interval endpoints within one quarter of the required precision of the first-order ones, by sampling under STND.VVUQ.40 otherwise, by interval propagation where only bounds are known, and by nested sampling, epistemic in the outer loop and aleatory in the inner, where both are present (NUMER.13, NUMER.15, INTPR.9, VV.5, VV.1, REPRO.6).

#### STND.VVUQ.44 Order-statistic limits

Default, from CSQ2. Instantiates NUMER.13, INTPR.9, VV.5, VV.1.

Where a tolerance limit is stated from order statistics, its number of runs SHOULD meet the nonparametric tolerance-limit formula for its coverage and confidence, by default 59 runs for a one-sided 95/95 limit at first order, with every failed or unconverged run counted among the runs and treated as exceeding the limit (NUMER.13, INTPR.9, VV.5, VV.1).

#### STND.VVUQ.45 Sensitivity indices

Default, from CSQ2. Instantiates NUMER.13, INTPR.9, VV.5, VV.1.

Global sensitivity indices SHOULD be estimated on a Saltelli design, with the Jansen estimator for total effects and the statistical uncertainty of each index stated (NUMER.13, INTPR.9, VV.5, VV.1).

#### STND.VVUQ.46 Surrogate checks

Default, from CSQ2. Instantiates NUMER.6, NUMER.13, VV.1, VV.6, INTPR.9, VV.5.

Where a surrogate that states a predictive variance stands in for a model on the path of a reported result, it SHOULD be checked on a validation design held out from its construction, with each standardized error beyond 3 in absolute value investigated, the Mahalanobis distance of the errors compared with its scaled F distribution, and a new held-out design used after each rebuild (NUMER.6, NUMER.13, VV.1, VV.6, INTPR.9, VV.5). A surrogate without a predictive variance SHOULD be checked on a held-out design against the required precision of the results it serves (NUMER.6, VV.1, VV.6). A surrogate's conformal intervals SHOULD be reported as of marginal coverage, holding under exchangeability only (NUMER.13, INTPR.9, VV.5, VV.1).

#### STND.VVUQ.47 Model discrepancy

Default, from CSQ2. Instantiates NUMER.13, NUMER.20, INTPR.9, VV.5, VV.1, INTPR.10.

Where model parameters are calibrated to measurements, the calibration SHOULD include a model-discrepancy term with a recorded prior (NUMER.13, NUMER.20, INTPR.9, VV.5, VV.1, INTPR.10). Where a calibration omits that term, its report SHOULD mark the parameter estimates as possibly biased and overconfident (NUMER.13, NUMER.20, INTPR.9, VV.5, VV.1, INTPR.10).

#### STND.VVUQ.48 Validation statement

Default, from CSQ2. Instantiates NUMER.13, INTPR.10, VV.5, INTPR.9, VV.1.

Model-form uncertainty SHOULD be stated as the comparison error between simulation and measurement with its validation uncertainty, as an estimate of model error at the validation conditions, with each use beyond those conditions stated as extrapolation (NUMER.13, INTPR.10, INTPR.9, VV.5, VV.1). Where the magnitude of the comparison error plus the multiple of STND.VVUQ.33 times its validation uncertainty, stated as a standard uncertainty, is at or below the required precision, the validation status that VV.5 requires SHOULD be stated as met (VV.5). Where that sum exceeds the required precision, the validation status SHOULD be stated as not met at the required precision, with whether the comparison error alone exceeds it (VV.5).

#### STND.VVUQ.49 Input covariances

Default, from CSQ2. Instantiates NUMER.15, REPRO.6, INTPR.9.

Each measured or evaluated input SHOULD carry the covariances that its evaluation or calibration record gives (NUMER.15, REPRO.6, INTPR.9). Propagation by sampling SHOULD draw inputs from those covariances (NUMER.15, REPRO.6, INTPR.9).

### Approximations

#### STND.VVUQ.50 Approximation effects

Default, from CSQ2. Instantiates NUMER.16, NUMER.17, INTPR.10, REPRO.7, RSRC.4, SIMPL.7, VV.1.

The effect of each retained performance approximation SHOULD be estimated by runs without it in the regime of each reported numerical result it affects, at the discretization of that result (NUMER.17, RSRC.4, SIMPL.7, VV.1). The effect of each other approximation listed under NUMER.16 SHOULD be estimated by a run without it at the finest affordable refinement level of each regime it serves, or bounded by analysis (NUMER.16, INTPR.10, REPRO.7).

### Inverse problems

#### STND.VVUQ.51 Independent forward computation

Default, from CSQ2. Instantiates NUMER.19, VV.1, VV.3.

Synthetic data for a recovery test SHOULD come from a forward computation with no connection to the inversion's own, differing from it at least in discretization or solver, with noise drawn from the recorded noise model (NUMER.19, VV.1, VV.3).

#### STND.VVUQ.52 Posterior calibration

Default, from CSQ2. Instantiates NUMER.19, VV.1, VV.3.

Where an inverse method states a posterior distribution, its posterior computation SHOULD be checked by simulation-based calibration on data simulated from the inversion's own model, with at least 1000 simulations, 100 posterior draws each after thinning, bins holding about 20 simulations, a 99 percent band, and test quantities that depend on the data as well as the parameters (NUMER.19, VV.1, VV.3). The coverage that NUMER.19 requires SHOULD then be shown on data from the forward computation of STND.VVUQ.51, by the method of STND.VVUQ.53 (NUMER.19, VV.1, VV.3).

#### STND.VVUQ.53 Interval coverage test

Default, from CSQ2. Instantiates NUMER.19, VV.1, VV.3.

Where an inverse method states a confidence interval, its coverage test SHOULD repeat the recovery over synthetic trials and state the observed coverage with a binomial interval (NUMER.19, VV.1, VV.3).

#### STND.VVUQ.54 Regularization choice

Default, from CSQ2. Instantiates NUMER.20, INTPR.9, INTPR.10.

Where the noise level is known, the regularization strength SHOULD be chosen by the discrepancy principle with a recorded factor above 1 (NUMER.20, INTPR.9, INTPR.10). Where the noise level is unknown, a heuristic choice SHOULD be reported with the statement that it carries no guarantee of convergence under deterministic noise (NUMER.20, INTPR.9, INTPR.10).

### Optimization

#### STND.VVUQ.55 Optimality measures

Default, from CSQ2. Instantiates NUMER.21, INTPR.9, VV.5.

Each optimization result SHOULD report its scaled and unscaled first-order optimality residuals and its largest constraint violation, against a stationarity tolerance of 1e-8 scaled and a feasibility tolerance of 1e-6 by default (NUMER.21, INTPR.9, VV.5).

#### STND.VVUQ.56 Optimum claims

Default, from CSQ2. Instantiates NUMER.21, INTPR.9, VV.5.

A claim of a global optimum SHOULD rest on convexity or on a relaxation bound gap within a recorded tolerance (NUMER.21, INTPR.9, VV.5). A claim of a local optimum SHOULD rest on second-order sufficient conditions under a stated constraint qualification (NUMER.21, INTPR.9, VV.5).

### Stochastic methods

#### STND.VVUQ.57 Dependent samples

Default, from CSQ2. Instantiates NUMER.22, INTPR.9, VV.1.

Where samples are drawn sequentially, their statistical uncertainty SHOULD come from an effective sample size or from batch means (NUMER.22, INTPR.9, VV.1).

#### STND.VVUQ.58 Markov chain diagnostics

Default, from CSQ2. Instantiates NUMER.23, VV.1, INTPR.9.

A Markov chain result SHOULD come from at least four chains from dispersed starts, with a rank-normalized split potential scale reduction factor below 1.01 and bulk and tail effective sample sizes above 400, inspected by rank plots (NUMER.23, VV.1, INTPR.9). Where a sampler runs its chains in groups that each share an initialization, a nested potential scale reduction factor over the groups SHOULD replace the split factor, with its threshold recorded before the run (NUMER.23, VV.1, INTPR.9).

#### STND.VVUQ.59 Markov chain precision

Default, from CSQ2. Instantiates NUMER.22, NUMER.11, INTPR.9, VV.1, VV.3, REPRO.3.

The Monte Carlo standard error of a Markov chain result SHOULD meet the tolerance of its acceptance criterion, independently of the diagnostic thresholds of STND.VVUQ.58 (NUMER.22, NUMER.11, INTPR.9, VV.1, VV.3, REPRO.3).

#### STND.VVUQ.60 Importance weights

Default, from CSQ2. Instantiates NUMER.23, VV.1, INTPR.9.

Where a result uses importance weights from S draws, the Pareto shape estimate of the weights SHOULD be below the smaller of 0.7 and 1 - 1/log10(S) (NUMER.23, VV.1, INTPR.9).

#### STND.VVUQ.61 Tally reliability

Default, from CSQ2. Instantiates NUMER.23, VV.1, INTPR.9.

Each statistical uncertainty of a tally of a history-based Monte Carlo calculation SHOULD pass, over the last half of the histories, the ten tally-fluctuation checks: a mean without monotonic trend; a relative error below 0.10, or below 0.05 for a point-detector tally, decreasing monotonically and as the inverse square root of the number of histories; a variance of the variance below 0.10, decreasing monotonically and as the inverse of the number of histories; a figure of merit constant within its statistical fluctuation and, separately, without monotonic trend; and a fitted tail slope of the history scores above 3 (NUMER.23, VV.1, INTPR.9). Each statistical uncertainty of a reported numerical result, that of a tally included, SHOULD be shown stable by its estimates from the first half and from all of its samples, each replicate of a replicated design counted as one sample and each estimate multiplied by the square root of the number of samples from which it comes, differing by less than the fraction recorded under NUMER.23 of the scaled estimate from all of its samples (NUMER.23, VV.1, INTPR.9).

#### STND.VVUQ.62 Stream construction

Default, from CSQ3. Instantiates NUMER.24, DSGN.17, REPRO.3, VV.1.

Random number streams SHOULD derive from a recorded root seed of at least 128 bits by spawning, by jump-ahead with unique indices, or by counter-based keys never reused (NUMER.24, DSGN.17, REPRO.3, VV.1). A stream SHOULD NOT be seeded with an arithmetic combination of a root seed and a worker index (NUMER.24, DSGN.17, REPRO.3, VV.1).

#### STND.VVUQ.63 Generator testing

Default, from CSQ2. Instantiates NUMER.24, DSGN.17, REPRO.3, VV.1.

Each random number generator SHOULD have passed a published battery of statistical tests of randomness, at least as demanding as the use of the generator requires and named with its revision in the record of the work, applied within single streams and across interleaved streams (NUMER.24, DSGN.17, REPRO.3, VV.1).

#### STND.VVUQ.64 Fixed-seed and fresh-seed tests

Default, from CSQ3. Instantiates NUMER.25, VV.1, VV.3.

Tests of stochastic results SHOULD be of two kinds: fixed-seed tests that detect change, and tests with fresh, logged seeds that judge correctness under the criteria of STND.VVUQ.33, STND.VVUQ.34, and STND.VVUQ.35 (NUMER.25, VV.1, VV.3).

#### STND.VVUQ.65 Repetition rule

Default, from CSQ2. Instantiates NUMER.25, VV.3, VV.1.

Each fresh-seed test of STND.VVUQ.64 SHOULD carry a rule of repetition under NUMER.26, recorded before its first run, that is a sequential test whose combined false-rejection rate and detection power meet STND.VVUQ.33 and STND.VVUQ.34 (NUMER.25, VV.3, VV.1).

### Derivatives

#### STND.VVUQ.66 Computing derivatives

Default, from CSQ2. Instantiates NUMER.27, DSGN.11, DSGN.16.

Derivatives SHOULD be computed by automatic differentiation, forward mode where inputs are fewer than outputs and reverse mode otherwise, by a discrete adjoint, or by implicit differentiation at a converged solution, with Hessian-vector products by forward-over-reverse differentiation (NUMER.27, DSGN.11, DSGN.16).

#### STND.VVUQ.67 Derivatives through iterations

Default, from CSQ2. Instantiates NUMER.28, VV.1, VV.3.

Where derivatives are carried through a repeated computation, its stopping criterion SHOULD also test the convergence of the derivatives (NUMER.28, VV.1, VV.3).

#### STND.VVUQ.68 Implicit derivative error

Default, from CSQ2. Instantiates NUMER.29, INTPR.9, VV.1.

An implicit derivative SHOULD state the forward residual at which it is evaluated, with its error bounded by a constant times that residual, the constant growing as the inverse square of the smallest singular value of the linearized system (NUMER.29, INTPR.9, VV.1).

#### STND.VVUQ.69 Taylor remainder test

Default, from CSQ2. Instantiates NUMER.28, VV.1, VV.3.

Each derivative SHOULD pass a Taylor remainder test over at least four halvings of a perturbation along a random direction, with observed rates within 0.1 of 2 for a first derivative and of 3 where a second derivative is supplied (NUMER.28, VV.1, VV.3).

#### STND.VVUQ.70 Dot-product test

Default, from CSQ2. Instantiates NUMER.28, VV.1, VV.3.

Each discrete adjoint or reverse-mode product SHOULD pass a dot-product test to a relative 100 times the machine epsilon over a short chain of operations, or to the rounding error estimated under NUMER.12 over a long one (NUMER.28, VV.1, VV.3). Each Hessian SHOULD pass the same test for symmetry (NUMER.28, VV.1, VV.3). Where the tolerance of a test of this provision is below a relative 1e-5, a relative discrepancy of 1e-5 or more SHOULD be treated as a defect, not as rounding (NUMER.28, VV.1, VV.3).

#### STND.VVUQ.71 Independent derivative checks

Default, from CSQ2. Instantiates NUMER.28, VV.1, VV.3.

A complex-step check SHOULD use a step of 1e-200 in double precision on a code path shown safe for complex arithmetic, and agree to a relative 1e-10 (NUMER.28, VV.1, VV.3). A finite-difference check SHOULD use central differences over a step-size study, and agree to a relative 1e-6 at its best step (NUMER.28, VV.1, VV.3). In a precision other than double, the complex step SHOULD be the smallest whose product with the derivative does not underflow, confirmed by a step 100 times larger that gives the same derivative within the agreement of this provision (NUMER.28, VV.1, VV.3).

#### STND.VVUQ.72 Nonsmooth operations

Default, from CSQ2. Instantiates NUMER.29, INTPR.9, VV.1.

At an operation that is not differentiable everywhere, the derivative used SHOULD be one-sided, a subgradient, or a smoothed surrogate, with the sensitivity of the result to that choice checked (NUMER.29, INTPR.9, VV.1).

#### STND.VVUQ.73 Chaotic averages

Default, from CSQ2. Instantiates NUMER.29, INTPR.9, VV.1.

Derivatives of long-time averages of chaotic dynamics SHOULD be computed by a shadowing method or reported as not computed (NUMER.29, INTPR.9, VV.1).

#### STND.VVUQ.74 Derivatives of expectations

Default, from CSQ2. Instantiates NUMER.28, VV.1, VV.3.

Derivatives of expectations SHOULD use a pathwise estimator where the sampling is differentiable and a likelihood-ratio or measure-valued estimator where the sampled path branches, each with its statistical uncertainty (NUMER.28, VV.1, VV.3).

#### STND.VVUQ.75 Derivative cost

Default, from CSQ2. Instantiates NUMER.27, RSRC.4, DSGN.11, DSGN.16.

Where a reverse-mode or adjoint gradient costs more than ten times its forward computation, the cause SHOULD be investigated (NUMER.27, RSRC.4, DSGN.11, DSGN.16).

### Learned surrogates

#### STND.VVUQ.76 Learned surrogates

Default, from CSQ2. Instantiates NUMER.6, NUMER.13, VV.1, VV.6, INTPR.9, VV.5.

A learned surrogate on the path of a reported result SHOULD be verified on problems held out from its training, with its error stated against the size of its training set and its optimizer settings, and its sensitivity to random seeds stated (NUMER.6, NUMER.13, VV.1, VV.6, INTPR.9, VV.5). Its output uncertainty SHOULD include the error of its training optimization and of its finite training set (NUMER.13, INTPR.9, VV.5, VV.1). Its validation SHOULD use data independent of its training and calibration (NUMER.6, VV.1, VV.6).

#### STND.VVUQ.77 Fair comparison

Default, from CSQ2. Instantiates VV.1, RSRC.4.

A claim that a learned method outperforms a numerical method SHOULD rest on a comparison at equal accuracy or equal cost against an efficient numerical method, measured under the conditions that HW.22 states for a comparative performance claim (VV.1, RSRC.4).

### Continuous verification

#### STND.VVUQ.78 Continuous verification

Default, from CSQ2. Instantiates VV.8, RSRC.11, RSRC.12.

Each verification test of this standard whose evidence a change is able to affect SHOULD run before the change is relied upon, with its result kept with the revision it judges (VV.8, RSRC.11, RSRC.12).

### Execution paths

#### STND.VVUQ.79 Deterministic extrapolation fit

Default, from CSQ2. Instantiates VV.1, VV.3.

Where the comparison of an alternative execution path of deterministic results with its reference path covers only part of the regime of use (HW.17), the criterion for its extrapolation SHOULD fit by least squares the logarithm of the largest ratio of observed difference to the tolerance of HW.16, each difference measured as that tolerance measures it, against the extrapolation abscissa, at each of at least six problem sizes spanning a factor of at least sixteen (VV.1, VV.3). Where an observed difference of that fit is zero, the fit SHOULD use in its place the spacing of the less precise compared format at the largest magnitude among the compared reference values, measured as the tolerance of HW.16 measures it (VV.1).

#### STND.VVUQ.80 Stochastic extrapolation fit

Default, from CSQ2. Instantiates VV.1, VV.3.

Where the comparison of an alternative execution path of stochastic results with its reference path covers only part of the regime of use (HW.17), the criterion for its extrapolation SHOULD fit the estimated difference of each compared quantity, measured as the tolerance of HW.16 measures it, against the extrapolation abscissa, by least squares weighted by the inverse square of the standard error of each estimate, at each of at least six problem sizes spanning a factor of at least sixteen (VV.1, VV.3).

#### STND.VVUQ.81 Extrapolation acceptance

Default, from CSQ2. Instantiates VV.1, VV.3.

Where the upper limit of the one-sided 95 percent prediction interval of the fit of STND.VVUQ.79 at the largest problem size of the regime of use reaches zero, the criterion SHOULD reject the extrapolation (VV.1, VV.3). Where the two-sided 95 percent confidence interval of the fit of STND.VVUQ.80 at the largest problem size of the regime of use is not contained within the tolerance of HW.16, the criterion SHOULD reject the extrapolation (VV.1, VV.3).

## Revision History

| Revision | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-10-11 | Adopted. |
| 1.1 | 2026-10-11 | Minor amendment (GOV.41) after the review of its provision pairs and its cold review: STND.VVUQ.37 sets lambda by the probability its analysis supports, 2.72 for a product of n factors and the square root of 2 ln(40n) over one less the unit roundoff for an inner product; STND.VVUQ.40 asks for ten Latin hypercube replicates; STND.VVUQ.50 estimates the effect of a retained performance approximation by runs without it in the regime of each reported result it affects, at that result's discretization, and admits a bound by analysis only for other approximations; STND.VVUQ.61 checks every statistical uncertainty, tallies included, against the fraction recorded under NUMER.23, with estimates scaled by the square root of their sample counts; STND.VVUQ.70 treats a relative discrepancy of 1e-5 as a defect only where its test's tolerance is below 1e-5. |
| 1.2 | 2026-10-18 | Minor amendment (GOV.41), conforming on the adoption of HW: STND.VVUQ.77 measures a comparison of a learned and a numerical method under the conditions of HW.22; new STND.VVUQ.79 to STND.VVUQ.81, in a new section Execution paths, give the default extrapolation criterion for a comparison beyond the reach of the reference path (HW.17); the term Extrapolation abscissa is added. |
| 1.2.1 | 2026-10-19 | Editorial amendment (GOV.41): the informative Notes describe ML and MEAS as adopted; no obligation changes. |
| 1.3 | 2026-10-24 | Minor amendment (GOV.41): new STND.VVUQ.82 treats a difference between compared results that declared run-to-run variation explains, within the agreement of its tier, as no defect; discourages changes made only to remove it unless an acceptance criterion or the consequence class requires bitwise identity; and admits a deterministic mode as an option; new STND.VVUQ.83, binding on agents (GOV.48), forbids an agent to change or extend the work on its own initiative only to remove such a difference, and has it state each difference it leaves. |
| 1.4 | 2026-10-24 | Minor amendment (GOV.41): STND.VVUQ.63 states the outcome that a test battery decides, a published battery of statistical tests of randomness at least as demanding as the use of the generator requires, named with its revision in the record of the work, in place of naming one battery; the Notes say that batteries differ in power, name BigCrush, the battery that the provision named before, beside the smaller ones of its library, and cite ML.2 and MEAS.2 for the matters that ML and MEAS own; References lists ML and MEAS; and, as an editorial change, STND.VVUQ.2 and its row of the table of common quantities speak of a computation that continues from state saved by an earlier run, in place of a checkpoint and its restart. |
| 1.5 | 2026-10-28 | Minor amendment (GOV.41): a core of STND.VVUQ.1, STND.VVUQ.3, STND.VVUQ.5, STND.VVUQ.7, STND.VVUQ.13, STND.VVUQ.17, STND.VVUQ.62, STND.VVUQ.64, and STND.VVUQ.82 applies from CSQ3, and every other default from CSQ2; the Notes state the onset of the standard, which they did not before. |
| 1.5.1 | 2026-10-28 | Editorial amendment (GOV.41): the Purpose no longer names a research note that the project does not hold and a knowledge entry that was never made, and says that the table of sources in the Notes gives the source of each default number that rests on one; the Notes name the manuals of one code without their version numbers, and a sentence that narrated an earlier revision names the battery by its size; no obligation, permission, or defined meaning changes. |
