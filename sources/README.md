# Literature corpus

20 papers and articles pulled via Firecrawl early in the project to
ground the pipeline design. Organized here so future readers (and future
me) can find the relevant prior work without re-searching.

## Foundation (the Stigler lineage)

| # | Source | Year | Why it matters |
|---|---|---|---|
| 01 | [Wikipedia — Stigler diet](01_wikipedia_stigler_diet.md) | living | Canonical summary of the 1945 problem + optimal-basket table (wheat flour 370 lb/yr, evap milk 57 cans, cabbage 111 lb, spinach 23 lb, navy beans 285 lb). |
| 06 | [Cambridge stats lab — Diet Problem history](06_cambridge_diet_history.md) | living | Short narrative of Stigler 1945 → Dantzig/Laderman 1947 → modern LP. The "9 clerks × 120 man-days" figure comes from here. |
| 02 | [Garille & Gass — *Stigler's Diet Problem Revisited*](02_stiglers_diet_problem_revisited_2001.md) | 2001 | The canonical 20th-century revisit. Re-solves with Dantzig's simplex, adds palatability constraints, updates prices + RDAs to 1990s. Our plan's framing leans heavily on this. |
| 17 | [Grokipedia — Stigler diet](17_grokipedia_stigler_diet.md) | living | Secondary summary; occasional fact-checks. |

## Modern LP diet reviews

| # | Source | Year | Why it matters |
|---|---|---|---|
| 04 | [Frontiers in Nutrition — *A Review of the Use of LP to Optimize Diets*](04_frontiers_2018_lp_diet_review.md) | 2018 | Most-cited review of LP-diet applications. Surveys cost, nutrition, environmental, and cultural-acceptability formulations. |
| 08 | [Wiley *Journal of Optimization* — systematic review](08_wiley_2023_systematic_review_lp_diet.md) | 2023 | Systematic review of LP-diet techniques, formulation taxonomies, and open problems. |
| 07 | [Springer *Archives of Computational Methods* — Balancing Health, Sustainability, and Culture](07_springer_2025_balancing_health_sustainability.md) | 2025 | Most recent review; frames diet optimization as a multi-objective problem. |

## Multi-objective / sustainability extensions

| # | Source | Year | Why it matters |
|---|---|---|---|
| 09 | [MDPI *Sustainability* — *Low Price, Low Climate Impact, High Nutrition*](09_mdpi_2015_low_price_low_climate.md) | 2015 | Three-objective LP (cost + GHG + nutrition) on Swedish consumption data. Inspired many follow-ups. |
| 11 | [ScienceDirect — Brazilian company carbon-footprint meals](11_brazilian_carbon_footprint_meals.md) | 2022 | Corporate-cafeteria LP minimizing carbon footprint under nutrition constraints. |
| 14 | [PMC — Spanish multi-objective nutrition/env/economics](14_pmc_spanish_multi_objective_diet.md) | 2020 | Spanish adult population dataset; Pareto frontier across three objectives. |
| 15 | [PMC — Planetary-boundaries diet LP](15_pmc_planetary_boundaries_diet.md) | 2024 | Individual-level LP with EAT-Lancet-style planetary-boundary constraints. |
| 12 | [arXiv — Decision-space diversity in MOEA for diet](12_arxiv_2025_decision_space_diversity.md) | 2025 | Hamming-distance decision-space uniformity for multi-objective evolutionary algorithms on diet problems. |
| 13 | [Frontiers — *Multi-objective optimization of national dietary guidelines*](13_frontiers_2026_multi_objective_national_diet.md) | 2026 | National-scale nutrition/environment/economy multi-objective framing. |

## Planetary Health Diet (EAT-Lancet)

| # | Source | Year | Why it matters |
|---|---|---|---|
| 10 | [Wikipedia — Planetary health diet](10_wikipedia_planetary_health_diet.md) | living | Summary of the EAT-Lancet 2019 / 2025 Commission diet. |
| 19 | [EAT-Lancet Summary Report](19_eat_lancet_summary_report.md) | 2019/2025 | Official commission summary. 2.0 estimates 15 M annual lives saved (up from 11.6 M). |
| 20 | [EAT-Lancet — Planetary Health Diet page](20_eat_lancet_planetary_health_diet.md) | 2019 | Reference food ranges (grams/day per category). Useful for v3 if we add a planetary-diet constraint set. |

## Tutorials + tooling

| # | Source | Year | Why it matters |
|---|---|---|---|
| 03 | [Google OR-Tools — Stigler Diet tutorial](03_google_or_tools_stigler.md) | living | Standard modern LP-Stigler implementation. Reference for the simplex formulation. |
| 05 | [NEOS Guide — Diet Problem](05_neos_guide_diet_problem.md) | living | NEOS server's case-study page. |
| 16 | [Google Research Blog — *Sudoku, LP, and the Ten-Cent Diet*](16_google_blog_2014_ten_cent_diet.md) | 2014 | The blog post that popularized Stigler-Dantzig modernization for developers. |
| 18 | [MIT BLOSSOMS — *Optimizing Your Diet*](18_mit_blossoms_optimizing_diet.md) | living | High-school-level introduction; useful for framing the "shadow price" intuition. |

## Where this pipeline differs from the literature

| Dimension | Standard in the literature | This pipeline |
|---|---|---|
| Prices | National averages, BLS APR, or static | **Per-store live** via Kroger Products API (3 real stores) + Walmart Affiliate (national) |
| Food representation | Abstracted food categories | **Real shoppable SKUs** (Kroger productIds + Walmart itemIds) |
| Dietary modes | Usually single-mode | **5 modes** (omnivore → vegan) in one solve |
| Supplements | Treated as out-of-scope | **Toggleable variant** showing supplement arbitrage |
| Infeasibility handling | Bare "infeasible" | **Phase-1 LP diagnostic** naming the blocking nutrients |
| Shadow prices | Rarely surfaced | **First-class output** per binding constraint |
| Palatability cap | Typically added (Garille & Gass 2001) | **None** — Stigler-pure LP |
| Environmental objective | Increasingly standard (EAT-Lancet 2019+, MDPI 2015, Brazilian 2022) | **Not yet** — deferred to v3 |
| Update cadence | One-shot analysis | **Daily** via GitHub Action |
| Transparency | Paper + one solution | Full catalog + solver diagnostics + source code |
