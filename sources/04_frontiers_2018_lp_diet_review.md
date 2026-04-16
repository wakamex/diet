# Source: Frontiers | A Review of the Use of Linear Programming to Optimize Diets, Nutritiously, Economically and Environmentally

- URL: https://www.frontiersin.org/articles/10.3389/fnut.2018.00048/full
- Slug: 04_frontiers_2018_lp_diet_review

---

## REVIEW article

Front. Nutr., 20 June 2018

Sec. Nutrition and Sustainable Diets

Volume 5 - 2018 \| [https://doi.org/10.3389/fnut.2018.00048](https://doi.org/10.3389/fnut.2018.00048)

# A Review of the Use of Linear Programming to Optimize Diets, Nutritiously, Economically and Environmentally

- [CV\\
\\
Corné van Dooren \*](https://loop.frontiersin.org/people/517103)

- Voedingscentrum, The Netherlands Nutrition Centre, Den Haag, Netherlands


Article metrics

[View details](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#metrics)

144

Citations

95,6k

Views

8,5k

Downloads

A correction has been applied to this article in:

1. Corrigendum: A Review of the Use of Linear Programming to Optimize Diets, Nutritiously, Economically and Environmentally

1. [Read correction](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2022.850033/full)

## Abstract

The “Diet Problem” (the search of a low-cost diet that would meet the nutritional needs of a US Army soldier) is characterized by a long history, whereas most solutions for comparable diet problems were developed in 2000 or later, during which computers with large calculation capacities became widely available and linear programming (LP) tools were developed. Based on the selected literature (52 papers), LP can be applied to a variety of diet problems, from food aid, national food programmes, and dietary guidelines to individual issues. This review describes the developments in the search for constraints. After nutritional constraints, costs constraints, acceptability constraints and ecological constraints were introduced. The 12 studies that apply ecological constraints were analyzed and compared in detail. Most studies have used nutritional constraints and cost constraints in the analysis of dietary problems and solutions, but such research begin showing weaknesses under situations featuring a small number of food items and/or nutritional constraints. Introducing acceptability constraints is recommended, but no study has provided the ultimate solution to calculating acceptability. Future possibilities lie in finding LP solutions for diets by combining nutritional, costs, ecological and acceptability constraints. LP is an important tool for environmental optimization and shows considerable potential as an instrument for finding solutions to a variety of very complex diet problems.

## Introduction: the diet problem

### Aim

Nutrition is affected by numerous environmental and societal causes. Although the diet problems were already urgent during World War II, the challenge of feeding the world in a healthy and sustainable manner will only become more urgent ( [1](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B1)). Herforth et al. ( [2](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B2)) proposed a “simple framework based on three domains: nutritional quality, economic viability, and environmental sustainability”. This paper answered their proposal by including the three domains in an integrated way ( [2](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B2)). It is expected that LP makes it possible to model these domains across disciplines.

This paper reviews the application of linear programming to optimize diets with nutritional, economic, and environmental constraints. There are three main reasons for studying the application of LP to diets in greater depth:

- Linear programming is thought to be “the ideal tool to rigorously convert precise nutrient constraints into food combinations” ( [3](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B3)).

- Maillot et al. ( [4](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B4)) stated that most food-based dietary guidelines assume that people eating according guidelines are receiving all recommended nutrients. However, in practice this is not always true ( [4](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B4)). So, LP could be helpful to support development of dietary guidelines that fulfill all nutritional requirements.

- Macdiarmid ( [5](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B5)) observed that healthy diets have not always lower environmental impacts. She assumed that LP is able to suggest diets and products with lower environmental impacts than the impacts of diets assessed through scenario type studies ( [5](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B5)).


The goal of this review is to analyse if the application of LP since 2000 provided acceptable diet solutions in practice, especially when environmental constraints were introduced.

### Definition

Linear Programming (LP) can be used to solve questions on matching diets to nutritional and other additional constraints with a minimum amount of changes. Linear programming is a mathematical technique that allows the generation of optimal solutions that satisfy several constraints at once ( [6](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B6)).

### History

The first studies applying LP to diets were published between 1950 and 1960 ( [7](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B7)). The search for diet solutions started with Jerry Cornfield, who formulated “The Diet Problem” for the Army during World War II (1941–1945), in search of a low-cost diet that would meet the nutritional needs of a soldier. The economist George Stigler, endeavored optimization techniques to establish the cheapest diet delivering enough energy, proteins, vitamins, and minerals ( [8](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B8)). According to Buttriss et al., this diet should be composed by the available list of 77 US foods of which the costs and nutrient composition were measured: “Stigler could not find the exact solution to this problem, which turned out to be incredibly complex. The Stigler “Diet Problem” is a typical question of resource optimization or, in mathematical terms, of minimization of a linear function subject to multiple linear constraints, also called linear programming” ( [9](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B9)).

For the duration of World War II, the Air Force and other parts of the army were hiring mathematicians to solve the important diet problem and to plan affordable meals. Among the researchers involved in solving this problem was George Dantzig. He proposed a new algorithm he had developed. It took him until 1947, being the first to deliver the correct mathematical result ( [9](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B9), [10](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B10)). Dantzig tested his model on his own diet, constructing a database with 50 foods. He wanted to reduce his caloric intake to 1,500 kcal and programmed an objective function to maximize the feeling of being full (operationalized as the weight per unit minus the weight of its water content). The solution he found was a weird diet with 200 bouillon cubes per day. This was possible because the former nutritional requirements didn't show a limit to the amount of salt. These results led to upper bounds being added to LP for the first time ( [10](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B10)). Until now the approach has been used in many ways to design individual diets as well as population diets ( [4](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B4)). The problem of the diet is interesting, because it is difficult to optimize the function of phenomenon like the diet, as it is composed of several variables: energy density, water content, macronutrients, micronutrients, bioactive substances, and contaminants. This paper gives an overview of those applications.

### Calculation methods

This review focus on optimization through the application of linear programming. This section explains the background of this method. The result of a LP problem shrinks to discover the optimum worth (maximum or minimum, liable to the problem) of the linear equation (named the “objective function”):

f=c1x1+…+cnxnf=c1x1+…+cnxn

The function is conditional on different constraints, stated as inequalities (see Figure [1](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#F1)). According mathematicians “the basic assumption in this method is that the various relationships between demand and availability are linear.” To obtain the solution, “it is necessary to find the solution of the system of linear inequalities (that is, the set of _n_-values of the variables xi that simultaneously satisfies all the inequalities). The objective function is then evaluated by substituting the values of xi in the equation that defines _f_ “(Encyclopedia Britannica, accessed June 2nd, 2017).

Figure 1

Concept of linear programming: The constraints (xi; purple lines) result in a feasible solution set (yellow area). The objective function (k; yellow line) results in the highest possible solution at the edge of the solution area.

Mathematician Cornfield started to find solutions for the Diet Problem by constructing an Input-Output model. His colleague Hoffenberg suggested using the simplex method (a standard method of maximizing a linear function of several variables). In 1947, a team took 120-man days to find a solution using the simplex method. A few years later, Dantzig introduced a linear program and started using an IBM 701 computer in the early 1950s ( [10](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B10)). The development of diet solutions was highly dependent on the development of computers with a high calculation capacity. The laborious computations necessary for LP were only possible at the time when fast computer technologies became available ( [3](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B3)).

Solving such complex problem subjected to several constraints either to optimize the daily energy allowance, macro and micronutrient intakes, or constraints on economic issues (price, income) and environmental issues (greenhouse gas emissions, energy use, land use, exposure to contaminants). Authors assume that constraints, such as price and nutrient content are linearly related to food weight ( [11](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B11)), but this could be a simplification of the reality. Micronutrients (e.g., advised daily intake vs. toxicity of Iodine) or costs (e.g., price elasticity) could be non-linear. There are several open problems in the theory of linear programming, for instance the strongly polynomial-time performance in the number of constraints and the number of variables. Besides linear optimization functions, several authors suggest using quadratic functions for optimization on popularity or acceptability ( [12](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B12)– [14](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B14)).

## Materials and methods

### Literature review

In this systematic literature review we selected—in line with the PRISMA protocol (Figure [2](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#F2))—literature on Pubmed: full text articles with “linear programming” and “nutrition” in the title or as key word, published between 2000 and 2014, including review papers ( _n_ = 81). The selection was narrowed by adding “diet” as key word ( _n_ = 51). We included through the snowball search approach additional related citations from these articles and from Mertens at al.'s review article ( [15](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B15)), and additional studies using environmental constraints published in 2015–2016, resulting in a total of _n_ = 71\. The records were screened on ground of title, aims and abstract. This resulted in the exclusion of 19 papers, based on the following criteria: non-English language, single nutrient, clinical study, or methodological paper. The total number of studies included for analysis are 52. A short overview of the studies is given in Appendix A. Since the time of “The Diet Problem,” LP has been applied in different sciences, but until 2003 it was rarely applied to questions of human nutrition ( [3](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B3)). This review describes the historical developments and improvements of the application of linear programming (LP) in diets since 2000. Five studies applying quadratic programming (QP) are also considered. Detailed focus was on diet studies with ecological constraints ( _n_ = 12). An extraction table (Table [1](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#T1))

Figure 2

Selection of papers through the PRISMA protocol for systematic literature research.

Table 1

| **Study** | **Goal** | **Outcome** | **Comment** |
| :-- | :-- | :-- | :-- |
| ( [13](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B13)) | To assess the impact of diet change on the blue and green water footprints of food consumption | Green water: −6, −11, −15, −21%. Blue water: −4, −6, −9, −14%. Halving animal protein saves water for the diet of an additional 1.8 billion people | Recommended diet per country not specified |
| ( [16](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B16)) | Estimate likely changes in diet under healthy eating guidelines and their consequences for the agricultural sector | Increase of 131.4% in gross margins; increase land use of oats, potatoes, fruits, and vegs; decrease use of sugar beet, milk, beef, sheep, beans, and some cereals |  |
| ( [17](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B17)) | Whether a reduction in GHGEs can be achieved while meeting dietary requirements | 2.43 kg CO2eq/d (−36%) and GBP 29.-/wk | No drinks included |
| ( [18](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B18)) (Spain) | To determine whether it is possible to develop corresponding diet recommendations in other countries; to analyse the difficulties of integrating data from multiple sources | 25% reduction in GHGe: 2,710g CO2e/day. Costs € 3.48 (unchanged) | Ignored the effect of alcohol and drinks |
| ( [18](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B18)) (Sweden) |  | 25% reduction in GHGe: 4,295g CO2e/day. Costs SEK 44.07 (−0.57) | All diets show reduction in total amount of meat and increase in legumes and bread/ pasta/ potatoes |
| ( [18](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B18)) (France) |  | 25% reduction in GHGe: 2,609g CO2e/day. Costs € 4.36 (−0.54) |  |
| ( [19](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B19)) | Ensuring food security in the context of rising food prices and environmental constraints | 5.98 kg CO2eq/d and NZ$ 6.75 | No drinks included |
| ( [20](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B20)) | To find low climate impact diets that are affordable yet fulfill all nutritional requirements | 1.58 kg CO2eq/day and € 2.57 |  |
| ( [21](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B21)) | Demonstrate a method that is able to identify diets with reduced environmental impact and that are more similar to the current diet than predetermined scenarios | 30% less environmental impact (0.29 pt pReCiPe) | Diet compared with (pesco)vegetarian, vegan, closest healthy |
| ( [22](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B22)) | To model the specific reductions in food-related GHGEs that could be achieved while meeting international dietary recommendations and minimizing deviation from the current diet | WHO guidelines −17% GHGE, realistic modifications −40% GHGE (fewer animal products and processed snacks, more fruit, vegetables, and cereals) | More than 40% is unlikely without radical change |
| ( [23](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B23)) | To assess the compatibility between reduction of diet-related GHGEs and nutritional adequacy, acceptability and affordability dimensions | GHGE reductions up to 30%; higher GHGE reductions decreased diet cost but also diet quality with major shifts in diet | 3 levels of nutritional constraints; stepwise 10% GHGE reduction; aggregation into food groups with new Euclidean distance method |
| ( [24](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B24)) | To investigate the diversity in dietary changes needed to achieve a healthy diet and a healthy diet with lower GHGEs by taking into account each individual's current diet and then minimizing the changes they need to make | Only 7.5% of people achieved healthy diet and 4.6% sustainable diet; 15 and 27% reduction in GHGEs, respectively; healthy diets alone do not produce substantial reductions in GHGEs | 4 step model; using 7–10 new items, 95% met health or GHGE constraints; sodium most difficult nutrient to meet; healthy diets alone do not produce substantial reductions in GHGE |
| ( [25](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B25)) | To identify a healthy, greener and cheaper diet based on current consumption patterns | More than 50% CO2 reduction for 3 diets to 8.3 kg CO2/wk; 10 euro/wk cost reduction (25%) for the low cost diet |  |
| ( [26](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B26)) | To demonstrate that linear programming can be used to define nutritionally healthy, environmentally friendly, and culturally acceptable diets, using the Low Lands as an example | Optimized Low Lands Diet results in a lower environmental impact than the Mediterranean and New Nordic Diet; GHGEs are 2.60 kg CO2eq/day and LU 2.86 m2\*year/day | Retrospective study about optimizing the traditional Low Lands Diet |

Overview of the 12 diet studies with both nutritional and ecological constraints.

_The table gives details about the goal, outcomes and comments_.

was constructed, including study aim, main outcome, objective function, used programme, applied nutritional, economic and ecological constraints, number of food items included, and study population (country, age, gender).

### Computer programs

Among the LP pioneers were Soden and Fletcher from the University of Salford UK. Their principles of LP were already clear in 1992 and still in use. They were far ahead of their time by using an objective function based on individual food preferences. They developed a computer program named “Microdiet System, 1990” in collaboration with practicing dieticians, which was used in some leading UK hospitals ( [27](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B27)). Guided by the philosophy of goal programming, they described a “computational method for constructing individually acceptable diets by modifying a chosen diet to meet nutritional requirements.” They demonstrated the effects of imposing different nutrient requirements ( _n_ = 4) on small food quantities ( _n_ = 25) on a sample diet and described techniques which can ensure that the modified diet will be acceptable to the individual. The starting point in the calculation was the person's current dietary intake. This was modified using LP methods which use vectors to make the smallest changes to the food quantities to meet specific targets. Sequential modification was introduced to identify changes that are acceptable to the individual ( [27](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B27)). Their maximum capacity was a problem with 100 foods and 30 constraints. Based on this analysis, Fletcher et al. developed a computational method able to construct individually acceptable diets by means of LP ( [28](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B28)).

The advent of powerful personal computers made an LP function accessible in widespread computer programmes, for example Microsoft Excel®. Also other spreadsheet programmes now provide a simple solver function that can be used for LP ( [11](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B11)). Briend et al. ( [3](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B3)) described in detail how to apply this function in Excel. An LP module was also incorporated in diet analysis programs, of which “Nutrisurvey” is a free example ( [http://www.nutrisurvey.de/lp/lp.htm](http://www.nutrisurvey.de/lp/lp.htm)) ( [3](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B3)).

Since 1975, a computerized programming model with a quadratic mathematical function has been available as part of the Thrifty Food Plan (TFP) in the USA ( [29](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B29)). The group of Lino designed a Microsoft Excel application in 2008, which permits “one to more easily evaluate the official USDA food plans or to create a new benchmark food plan that meets one's own chosen nutrition policy goals” ( [30](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B30)). Gao et al. were among the first to apply Quadratic Programming (QP) in diets. They used SAS (Version 8.02) for the calculations, and exported the data to Microsoft Excel. QP used Microsoft Excel SOLVER developed by Frontline Systems ( [31](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B31)). The European HELENA study also applied QP to optimize diets from Food Frequency Questionnaires. The solutions were acquired through the use of LINGO Hyper (Release 10.0, LINDO Systems Inc., USA) ( [32](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B32)).

LP and QP are also available in the statistical software R 2012 through a GNU Linear Programming Kit implemented in the IpSolveAPI package (or “Rglpk”). Macdiarmid in the UK was one of the first to use the software for LP in diets for the calculations of WWF Livewell Plate ( [17](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B17), [33](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B33)). Macdiarmid states that “this mathematical method optimizes an outcome which is a linear function of several variables that can be controlled (e.g., the amount of food eaten), while subject to a number of constraints (e.g., dietary requirements)” ( [33](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B33)).

Blonk Consultants in the Netherlands developed their own software Optimeal®, which was used in the LP studies of Van Dooren et al. ( [20](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B20), [26](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B26)). The tool supports LP and QP and has several options to customize the goal function, such as a proxy of popularity and different measures for distance. Optimeal is programmed in Matlab Compiler 7.16.

## Results

### Nutritional constraints: from food plans to dietary guidelines

This review includes 52 optimization studies with nutritional constraints, of which 17 without other constraints.

At the start of this millennium, the French group lead by Nicole Darmon, Elaine Ferguson (New Zealand), and André Briend started to apply LP in food aid. They demonstrated in Malawi that it was possible to satisfy nutritional recommendations for children 3–6 y during the harvest season using LP through the Microdiet software with a small distance from the native diet. But, in the non-harvest period, the availability of riboflavin and zinc was improved ( [34](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B34)). Later, Ferguson and her team ( [35](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B35)) were active in Indonesia, applying LP to develop complementary feeding recommendations to apply in specific populations with a diet with micronutrient deficiencies ( [35](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B35)).

Inspired by the results of Darmon, Ferguson, and Briend, the UN World Food Programme and Save the Children started applying LP, a few years later. A user-friendly Excel solver function was developed for practitioners by Save the Children UK. With this spreadsheet, LP has been used in many developing countries to assess to what extent economic constraints contribute to the nutrition problems. For this purpose, the organizations have gathered prices of food products from a couple of countries (i.e., Zambia, Mozambique, Djibouti, Bangladesh, Tanzania, and Niger). They called it the “Cost of the Diet” tool. In the tool, the following data were included:

- World Food Composition Database,

- recommended nutrient requirements (WHO data for different ages, gender, and physiological conditions), and

- food prices per 100 g per country.


Romeo Frega et al. published a case study applying the tool in Mozambique to determine cost-effective fortification strategies ( [36](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B36)).

In the meantime, the French group worked together with Adam Drewnowski from the University of Washington to apply LP in the USA. The French study applied LP to create food plans that meets critical dietary recommendations advised by the World Cancer Research Fund ( [37](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B37)). Consumption constraints were included to prevent food plans from advising unreasonable amounts of food from a food group (Much more stringent than the USDA TFP). Consumption data were taken from a 161 representative men and women in the Pacific Northwest. For this group, achieving cancer prevention recommendations required little modification of their current diets (lower in refined grains and higher in vegetables and fruits) and had small impacts on the cost and quality of the diet. However, to meet all nutritional needs it was necessary to highly increase the volume and change the food intake patterns. Costs were considered, but not as a constraint (diet costs rose from $ 6.95/day to $ 8.03/day for women). These applications demonstrated that optimization models deliver an sophisticated mathematical solution to check whether different subgroups achieve different dietary guidelines (in the USA) ( [38](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B38)). Metzgar et al. ( [39](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B39)) did the same for a Paleolithic diet on a limited budget. Many consumers with a limited income have a low budget to buy food. This paper used the USDA data sets of the TFP. The results show that a Paleolithic diet is possible within the defined constraints. Nevertheless, the diet is too low in calcium and some other micronutrients. A 9.3% increase in spending was needed ( [39](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B39)).

Darmon et al. ( [40](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B40)) went into greater depth, testing the compatibility between nutrient profiling and recommendations based on nutrients by using LP. The option of modeling diets satisfying 40 nutrient constraints (“healthy models”) was tested. Healthy diets could be modeled using foods from the most favorable nutrient profile class, but unhealthy diets could not be modeled within an accurate scope of energy consumption. Darmon's conclusion was that a “few key nutrients (protein, fiber, saturated fatty acids, added sugars, sodium, vitamin C, calcium, iron) can be used to predict the ability of a given food to facilitate—or to impair—a large number of nutrient recommendations” ( [40](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B40)).

In line with Darmon, Clervieulle assessed the validity of five different European nutrient profiling systems (i.e., Choices, Keyhole, French Agency for Food, Environmental and Occupational Health and Safety (AFSSA), European Commission (EC) system, and FoodProfiler). For each profiling system, construct validity was assessed by testing whether unhealthy foods (identified as non-eligible) results in unhealthy diets and healthy foods (those identified as eligible by the system) results in healthy diets. The AFSSA, EC, and FoodProfiler systems were proved to be valid, though some food products appeared to be misclassified. The two other systems failed. One important result was that, “it was possible to design healthy diets with eligible products and unhealthy diets with non-eligible products” ( [41](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B41)).

The huge efforts in France resulted in the use of LP to develop dietary reference intakes as early as 2001 ( [42](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B42)). Several studies have been conducted using data from a French representative dietary survey (ASPCC survey). All these studies have similar results and demonstrate that meeting nutritional requirements is difficult. But it is possible by using regular foods, by applying common nutritional recommendations ( [42](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B42), [43](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B43)). Thus far, most studies using LP on diets focus exclusively on nutritional constraints ( [38](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B38), [39](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B39), [44](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B44)– [46](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B46)). The studies of Ferguson et al. ( [44](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B44), [45](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B45)) for example, were done to revise Food-Based Dietary Guidelines or to upgrade Food Aid. LP could be helpful to support development of dietary guidelines that fulfill all nutritional requirements.

### Economic constraints: food aid

Twenty of the studies included used economic constraints, five of them where focussed on food aid, 15 on applications in developed countries, of which three especially on the Thrifty Food Plan and two of them included also ecological constraints. The Diet Problem was originally designed to find low costs solutions for feeding soldiers ( [10](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B10)). LP can also be applied to identify the lowest cost nutritionally adequate diet when providing food aid, as costs and nutrient content of foods are linearly associated to the weight of foods ( [11](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B11)). Mathematical optimization models have long indicated ( [7](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B7), [8](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B8)) that diets high in nutrients could be found very cheap ( [47](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B47)).

LP was found to be very helpful in food aid programs. For example, Ryan et al. designed an LP tool to compose “novel ready-to-use therapeutic food” for malnourished children. They systematically surveyed international and national crop and food databases and took the example of ingredients locally available in Ethiopia. The cost of the optimized formulation was only $0.12 per 100 g, more than 40% cheaper than the available ready-to-use therapeutic food ( [48](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B48)). Dibari et al. also published LP solutions for East Africa ( [49](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B49)). LP can also be applied to calculate the lowest price for an additional food supplement necessary to reach an adequate diet. It can similarly be used to calculate what families save compared to the expenses by the donor after distributing a food supplement, for example in rural Chad ( [11](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B11)). The same group stated that LP can help during the complementary feeding period. In a review article, Briend et al. informed pediatricians and public health professionals about this tool ( [3](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B3)). Ferguson et al. addressed the diets of young children living in disadvantaged environments, for instance in Indonesia. They combined LP with goal programming. The study resulted in a number of optimal CFRs for the local population, giving insights in their most important “problem nutrients” ( [45](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B45)).

From food aid in Africa, the next step was to apply LP to poor families and food banks in developed countries. Earlier, Briend and Darmon described an approach based on cost minimization by LP (in Excel) to determine which nutrients may be below recommended intakes in poor families in France ( [50](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B50)). In 2007 Rambeloson et al. started a study on food banks in France, to assess the nutritional quality of the food distributed and to identify applicable changes to improve it. All 2004 data were collected for food aid donated by French food banks. LP was used to find the minimum changes necessary to meet the French dietary recommendations. The actual donation was improved by adding new foods into the food aid boxes ( [46](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B46)). These examples demonstrate that cheap food is not always nutritionally adequate food. This has also been found in studies which only applied cost constraints.

### Economic constraints: costs vs. nutrients in developed countries

Although food aid was an important application of LP, the approach is not only useful for poor countries and disadvantaged citizens. Briend continued his work on LP in France, together with Darmon and Ferguson. Their focus was on the interactions between economic constraints and unhealthy diets. The study demonstrated that adding a cost constraint could result in diets with lower nutrient densities, with preferences comparable to the diets of low socioeconomic groups ( [51](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B51)). This suggests that, when cost constraints affect food choices, LP resulted in an energy dense diet to maintain French dietary patterns ( [52](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B52)). Next, Darmon et al. used LP to calculate the effect of a cost constraint on the available food choices for French women, to reach a healthy diet ( [53](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B53)). Drewnowski and Spencer also found that reducing the costs of diets in LP models “leads to high-fat, energy-dense diets that are similar in composition to those consumed by low-income groups. Such diets are more affordable than more healthy diets based on lean meats, fish, fresh vegetables, and fruit” ( [54](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B54)).

In 2007, Matthieu Maillot joined the French research team with new publications on cost constraints. For the first time, LP was applied on a large dataset of people, in this case a representative sample of French adults in the INCA data set (1999, _n_ = 1,332) ( [55](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B55)). Maillot et al. developed LP models to propose diets that satisfied higher nutritional constraints at minimum price. Their found agreement between LP and nutrient profiling indicates that “LP is a useful tool for testing nutrient profiling systems and validating the concept” ( [56](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B56)). The work of Maillot et al. also concluded that “calculating the minimum cost of a nutritious diet needs to take social and cultural factors into account” ( [47](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B47)). One of the studies performed in France also looked at the costs and found a 55% increase in costs for the nutritionally optimal diet, from € 2.75 to € 4.24 per 2,000 kcal ( [46](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B46)). Similar work done by Maillot and Drewnowski in the US (2010) on optimizing the size of the servings and energy density also showed an increase in costs (to between $ 4.40 and $ 5.50/day, an increase of $ 0.10–1.20) ( [57](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B57)).

Finally, LP with cost constraints has been applied to specific dietary requirements. Raffensperger ( [58](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B58)) used LP to study the lowest available cost of a low-carbohydrate diet in New Zealand. Introducing constraints for carbohydrate and fat, resulted in a big, non-linear increase of cost. The study identified, within a low-carbohydrate, low-fat diet, which nutrients had the biggest effect on cost: The optimum diet cost NZ$ 14/day, with energy, calcium, and fiber being the most expensive nutrients ( [58](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B58)). LP demonstrated to be an applicable tool to rigorously convert precise nutrient constraints into food combinations.

### The example of the thrifty food plan (TFP)

Of the 20 studies with economic constraints, 3 used the Thrifty Food Plan as an example. Forty years ago, the USDA developed the TFP to solve the problem of selecting a healthy diet for low-income groups. This dietary optimization program composed diets that fits within the constraints, using the 4,800 most popular foods. Since 1975, the TFP has been the most successful program providing healthful and minimal-cost meal plans and market baskets for consumers with a limited budget: more than 28 million. The TFP was updated in 1983, 1999, and 2006 ( [29](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B29)). The researchers used 15 nutritional constraints (essential nutrients with official RDAs). In 1999, Lino et al. found that a family of four spent 23% of their income on unhealthy foods. In contrast with other studies, it was possible to increase the healthy components without changing the budget ( [29](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B29)). USDA met simultaneously food group constraints, a cost constraint, and other constraints ( [30](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B30)). The 2006 revision of the market baskets could meet food intake recommendations of the MyPyramid Food Guidance System (e.g., for fruit, vegetables, and milk). However, none of the market baskets was able to meet the sodium guideline, so sodium was limited for each age-gender group ( [59](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B59)).

Wilde and Llobrera evaluated the TFP framework using constraints on food groups (e.g., meat, vegetables) or nutrients (e.g., saturated fat, calcium). It was possible to find nutritious diets for adult women with the TFP budget of $ 4.98/day, but it required a substantial change from current diets, or using nutrition standards in place of food category standards based on MyPyramid. This paper is interesting for future applications, because the authors introduced a stepwise approach, with the cost constraint increasing in steps of $0.05 ( [30](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B30)). This stepwise approach is also applicable for other constraints and recently applied by Kramer et al. ( [12](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B12)).

### Twelve studies with ecological constraints

The next step in the application of LP was the introduction of ecological constraints. Several studies—for instance in UK, and New Zealand—have successfully applied LP to optimize diets ( [4](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B4), [19](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B19), [33](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B33), [38](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B38), [39](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B39), [44](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B44), [46](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B46), [47](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B47), [57](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B57)). This section gives an overview of the 12 studies which have applied ecological constraints to 14 diets between 2000 and 2016 ( [13](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B13), [16](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B16)– [26](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B26)). The studies are summarized in [Table 1](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#T1).

Macdiarmid et al. were the first to use greenhouse gas emissions (GHGEs) as constraint. They found a realistic diet that could produce a 25 to 36% decrease in GHGEs ( [17](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B17), [33](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B33)). Their study suggested that future work would need to integrate wider issues of sustainability into the modeling process and develop broader dietary advice ( [33](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B33)). In the same period, Vieux et al. ( [60](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B60)) designed a low-impact diet using not LP but a scenario, with 12% lower GHGEs (3.60 kg CO2eq/day) ( [60](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B60)). The studies of Macdiarmid et al. ( [17](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B17), [33](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B33)) and Vieux et al. ( [60](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B60)) have drawbacks, as their diets include a low number of foods (82, 73 respectively\]. The study by Van Dooren ( [20](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B20)) included 206 most consumed Dutch food products, which is more realistic. It looked not only at GHGEs as an environmental parameter, but also at land use, energy use and ReCiPe score, which combines the three other parameters in an overall ecological pressure score. Later, Vieux et al. ( [61](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B61)) improved and expanded the French dataset to 391 products. He did not use LP, but looked for associations between GHGEs and nutritional quality ( [61](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B61)).

Macdiarmid et al.'s work modeling diets using LP methodology was supported by WWF in the United Kingdom with the goal of optimizing the nutritional quality of recommended diets and simultaneously reducing the diet-related GHGEs ( [17](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B17), [33](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B33)). This method was also applied by WWF to program the national diets of France, Spain, and Sweden, using local available datasets and nutritional constraints ( [18](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B18), [62](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B62)). The same kind of modeling was applied in a New Zealand study ( [19](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B19)). Diets were first modeled without acceptability constraints. Then they applied diets with popular foods consumed by the population, with realistic amounts as constraints. They also applied constraints for food costs, energy intake, macronutrients, and micronutrients ( [9](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B9)– [11](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B11), [15](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B15), [17](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B17), [20](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B20), [26](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B26)– [36](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B36), [38](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B38)– [40](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B40)) from national dietary recommended intakes. The optimized UK diets could result in 90% reductions in GHGEs, but the diet included only 7 foods and no drinks (and without emissions of the consumption phase). But this diet was without acceptability constraints (see section The Need for Acceptability Constraints) ( [33](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B33)). The New Zealand study demonstrated similar reductions in GHGEs ( [19](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B19)). The introduction of acceptability constraints in the UK model resulted in a diet incorporating 52 of the 82 typical food groups, without removing the groups meat or dairy, that met dietary recommendations and a 36% GHGEs reduction. The cost to the consumer did not increase. The modeled diets in France, Spain, and Sweden demonstrated similar results ( [18](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B18)). The New Zealand study optimized 16 diets for nutritional adequacy, cost, and GHGEs ( [19](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B19)). The latter study was of limited practical value, because the diets only include 14 to 19 foods, and drinks were not considered. The two studies of Van Dooren ( [20](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B20), [26](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B26)) are more extensive, because they used 33 nutrients instead of 16 ( [17](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B17)) or 18 ( [19](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B19)). In conclusion, LP makes it possible to propose diets with lower impacts than diet scenario studies.

Based on nutrition recommendations, Donati et al. identified three different 7-day diets for the healthy Italian adult population (young adults from a high school in Parma, _n_ = 104), characterized by different targets and optimizing different impacts: first the lowest cost diet (Minimum Cost Diet), then the Environmentally Sustainable Diet obtained by reducing the three environmental indicators (GHGEs, water consumption, and land use). Finally, the Sustainable Diet was recognized to reach simultaneously environmental and cost constraints. Donati et al. used 544 food items, but only 9 nutritional constraints ( [25](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B25)). The added value of the study is the use of multiple environmental parameters and new acceptability constraints. They created a new constraint modeling the connection between matching food groups (biscuits as a complement with coffee or tea). To make the results more accurate, they argued that “at the same time, it is unlikely for some foods to be eaten during the same meal. For instance, it is not usual to eat both beef and fish. In modeling consumption behavior to reflect real world eating habits, the model incorporates an ‘alternative’ constraint avoiding the combination of certain food items in the same meal” ( [25](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B25)). Despite these acceptability constraints, the volume of the diets almost doubled.

### Combining economic and ecological constraints

Nelson et al. ( [63](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B63)) stated that: “There is limited and inconsistent evidence as to whether sustainable diets are more or less expensive than average diets” ( [63](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B63)). Some LP studies added evidence.

The 2013 New Zealand study was the first study applying three types of constraints: nutritional, economic and ecological (GHGEs). The result was a monotonous diet containing 10 to 19 foods (selected from a database of 76 foods) ( [19](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B19)). This study showed that the more food products and the higher the acceptability, the more expensive the diet was. Auestad and Fulgoni reviewed the results: “When the modeled diets included meals more familiar to New Zealanders, the cost tended to be higher than for the other optimized diets” ( [64](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B64)). Concluding that: “Future research using this or similar approaches should also consider other aspects of environmental impacts (e.g., land use, water quality, food waste, and biodiversity), supply and pricing, including subsidies for farmers, and other social and economic aspects of sustainability” ( [64](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B64)).

Van Dooren et al. ( [20](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B20)) confirmed that costs increase when nutritional constraints are exclusively used. In contrast, adding environmental constraints decreased costs ( [20](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B20)). In the second step of Van Dooren et al.'s optimization, they found that costs were not increased compared to the current Dutch diet, but reduced to € 3.20. This is substantially lower than the cost for the British Livewell 2020 diet ( [33](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B33)): £ 29 per person per week (about € 4.80 a day), based on mid-range supermarket prices in August 2010. This may be due to differences in price levels, or differences in dietary patterns between the two countries. While € 3.20 is at the same price level as that found in a French study ( [4](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B4)), that study excluded drinks and did not include GHGEs as a constraint. The optimized French diets are monotonous and are expected to have a low social acceptability. Lastly, a New Zealand study resulted in a cheaper diet (about € 1.92–2.44) ( [19](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B19)). Though, these cheaper diets consist of low quantities of fruits and vegetables.

### Possibilities with quadratic programming

Although “Linear programming” was the selection criterium for this review, several selected diet studies were also using QP ( [31](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B31), [32](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B32), [51](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B51), [65](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B65)). For example, Jalava et al. ( [13](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B13)) assessed water footprints of diets after stepwise optimization (blue and green water, Table [1](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#T1)). They used QP to calculate stepwise the changes in diet gradually limit the percentage of animal protein to 50, 25, 12.5, and 0 of the total protein consumption of worldwide regions. Although QP is an optimization method ( [14](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B14)), the goal was to find a diet that encounter the dietary guidelines per scenario with the lowest number of changes in the menu (retaining the typical diet for each country). The four applied scenarios resulted in reductions for the blue water footprint of 4, 6, 9, and 14. The original diet was assigned as the optimization objective. QP resulted in estimated cost for any scenario. Therefore, the result was close to the traditional, culturally acceptable diet and fulfilled the nutritional constraints ( [13](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B13)). QP has advantages over LP when the goal is to find small changes on population level.

## Discussion

### Combining more constraints

Most studies have used nutritional constraints and cost constraints in the analysis of dietary problems and solutions, but such research begin showing weaknesses under situations featuring a small number of food items and/or nutritional constraints. The number of nutritional constraints vary from 5 to 37, which could have a major impact on the results of the studies: the lesser the number of constraints, the higher the risk of inadequacy of nutrient intake of the nutrients not considered. Even with a high number of nutritional constraints, bioavailability of nutrients (e.g., iron, amino acids) and phytochemicals are not considered. This could partly be solved by adding constraints on certain food groups rich in phytochemicals, e.g., fruits, vegetables, and fish. Future possibilities lie in finding LP solutions for diets by combining nutritional, costs, ecological and acceptability constraints. Evaluating the limited number of studies using LP on diets, we conclude that the studies of Wilson et al. ( [19](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B19)) and van Dooren et al. ( [20](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B20)) were unique in combining three dimensions: nutrients, GHGEs, and costs. Future LP diet studies should combine all three of these constraints.

### Comparability of ecological studies

The most important challenge to improve future LP diet studies with ecological constraints, is to build bigger databases with more foods and more environmental data, with improved quality and consistency of the data.

Although the papers cited above ( [33](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B33), [66](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B66)) observed substantial reductions in GHGEs, it is striking that they found much higher emission levels—in absolute terms—than the Dutch study ( [20](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B20)). The found emission of 1.56 kg CO2eq/day is lesser than the 3.6–4.2 kg for France and 3.77–5.02 kg for the UK (Macdiarmid also calculated a very limited diet with a 70% reduction in GHGEs, resulting in 1.74 kg CO2eq, which is still higher than the Dutch results). On the other hand, one of Wilson et al.'s results in New Zealand is comparable: 1.62 kg CO2eq, but without drinks ( [19](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B19)). These differences may be explained by different methods used to calculate GHGEs per product or variances in food cultures and preferences. This approves the preferability of a “country-by-country approach” ( [20](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B20)); outcomes should not be extrapolated from one country to another, because of the differences in availability of reliable data, dietary patterns, and the climate impact of products ( [20](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B20)).

Table [2](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#T2) makes it clear that the studies differ in number of food items (13–544; an indication of the completeness of diets), the size of the population, the number of nutritional constraints (5–33; an indication of the nutritional quality of the diets), the selected economic and ecological constraints, and the solutions to make the outcomes culturally acceptable.

Table 2

| **Study** | **Country/region** | **Individual/population** | **Diet of** | **No. of food items** | **No. of food groups** | **Programme** | **Optimization on (objective function)** | **Nutritional constraints** | **Economic constraints** | **Ecological constraints** | **Other parameters calculated** | **Acceptability constraints** |
| :-- | :-- | :-- | :-- | :-: | :-: | :-- | :-- | :-: | :-- | :-- | :-- | :-- |
| ( [13](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B13)) | 176 countries | Pop. | National food supply FAO |  | 13 | ? Quadratic | Minimize change in diets | 5 | x | Blue and Green Water | Overeating + food deficiency | No change in fish, spices, and stimulants; no increase of alcohol and sugar; stepwise decrease of animal protein: 50, 25, 12.5, 0%. |
| ( [16](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B16)) | England and Wales | Pop. | Households |  | 167 | ? Quadratic. See Srinivasan et al. ( [67](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B67)) | Minimize changes % in diet, + expenditure changes | 13 | x | Land Use | Cost of labor |  |
| ( [17](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B17)) | United Kingdom |  | Women, 19–50 y | 52/82 |  | GNU kit implemented in Rglpk of R statistical software | GHGE (?) | 16 | British pounds | GHGEs |  |  |
| ( [18](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B18)) | Spain | Pop. |  | 277 |  | Rglpk package | Minimum GHGE (> 25% reduction) | 17 | Only as outcome | GHGEs | Costs | Amounts consumed in particular food groups > 60–80% of the current average consumption |
|  | Sweden | Pop. |  | 88 |  | Rglpk package | Minimum GHGE (> 25% reduction) | 21 | Only as outcome | GHGEs | Costs |  |
|  | France | Pop. |  | 68 | 13 | Solver in Excel | \> 25% reduction GHGE | 13 | Only as outcome | GHGEs | Costs | On particular portion sizes for each food and minimal departure from the average diet |
| ( [19](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B19)) | New Zealand |  | Males, 16 diets | 76 | 14–18 | Excel, R language | Nutritional requirements (?) | 17 | NZ$ | GHGEs | Food waste UK |  |
| ( [20](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B20)) | NL |  | Males and females 31–50 y | 206 |  | Optimeal (Matlab) | Popularity (kg) | 33 | Euros | GHGEs | Land use + ReCiPe score |  |
| ( [21](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B21)) | NL | Ind. | Females 31–50 y | 207 |  | Optimeal (Matlab) | Penalty score on popularity (kg) | 37 | x | pReCiPe | GHGE + Land Use + Energy Use | Penalty score <100; no constraints on food groups |
| ( [22](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B22)) | UK | Pop. | Adult males and females |  | 42 (148 sub) | Software R 2012, package Alabama. Nonlinear with Augmented Langrangian method. | Squared deviations in “loss of welfare” from current diet | 14 | x | GHGEs |  | Stepwise reduction 10–70%; max. 50% deviation is acceptable; loss of welfare: expenditure shares/own-price elasticities |
| ( [23](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B23)) | France | Pop. | French INCA2 dietary survey, adults _n_ = 1,899 | 402 | 8 | Statistical software package SAS version 9.4 | Minimizing the total departure between the diets at food item and group level | 33 | Only as outcome | GHGEs | Mean adequacy ratio; Mean excess ratio; Solid energy density | Total weight (80–120%), <90th percentile for foods and food groups |
| ( [24](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B24)) | UK | Pop. | UK National Diet and Nutrition Survey, adults _n_ = 1491 |  | 134 | GNU Linear Programming Kit implemented in IpSolveAPI package of R stat software. | Minimizing the changes to their current intake | 27 | x | GHGEs (−25%) |  | 1\. gradual changes (≤50%) to amount of any foods currently eaten. 2. New foods were added. 3. Greater reductions (≤75%). 4. foods were removed |
| ( [25](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B25)) | Italy, Parma | Sub-pop. | Young adults (18–20y) high school _n_ = 104 | 544 |  | ? Multi-Objective Linear Programming | Minimizes both consumer expenditure and environmental impact | 9 | Euro | GHGEs, Land Use, water footprint | Simultaneously 3 | 1\. Food portion, 2. Food consumption frequency, 3. Food association, 4. Food alternative |
| ( [26](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B26)) | NL | Pop. | Male adults (31–50 y), historical | 206 |  | Optimeal (Matlab) | Popularity (kg) | 33 | x | GHGEs, Land Use combined | Distance in Health Score; No. of products added, eliminated and changed | Popularity (normalized value of the total food consumption based on weight) |

Twelve diet studies with nutritional and ecological constraints.

_The table gives details about the goal, objective function, selected population group, program, number of food items, and outcomes_.

### The need for acceptability constraints

One of the attempts to make outcomes culturally acceptable, is the introduction of acceptability constraints. Six studies demonstrated good examples of those constraints. From the first studies of Dantzig to date, researchers have struggled with the unrealistic outcomes of LP solutions. It was expected that adding acceptability constraints could help to prevent this. A good example is Maillot et al.'s (

[43](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B43)

) study, whose objective was “to assess the feasibility of achieving a set of 30 nutrient recommendations at the individual level and to characterize factors associated with feasibility.” The diets of all participants the French national food consumption survey (

_n_

= 1,171) were optimized. For everyone, departure from his/her recorded diet was minimized:

- Only foods reported in his/her weekly diet record were used to fulfill a set of nutritional constraints.

- Acceptability constraints guaranteed warranted accurate portions and patterns. For any given food, upper limit on the quantity was defined by the 95th percentile of consumer intake.

- To keep away from unacceptable quantities of food, the optimized diet should be lower than 115% of the weight eaten per week.

- Model feasibility was calculated for all diets.


The vitamin D constraint was the most difficult to fulfill, followed by sodium, magnesium, and saturated fatty acids. The new approach resulted in a “method for identifying nutrient levels that need to be carefully evaluated when establishing recommendations” ( [43](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B43)).

However, the use of cultural acceptability constraints limits finding solutions. In 2016 Parlesak et al. collected average prices for 312 foods available within Copenhagen, Denmark. They calculated five different cost-minimized food baskets for a family of four. The food baskets that met food based dietary guidelines was twice the price. Introducing cultural acceptability constraints increased the cost three times. So, variety in the diet and cultural acceptability has a price ( [68](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B68)).

Thompson et al. ( [18](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B18)) also struggled with the issue of acceptability and used a lot of trial and error. In their study at least 30% of the most popular foods were retained. They also put an upper bound on most foods and removed foods with smaller amounts in the diet, as well as less healthy options such as full-fat milk. They applied lower bounds of consumption, particularly on popular foods. For example, bread, potatoes and pasta have comparable GHGEs and prices, but the model will try to optimize one of the products for cultural reasons: for instance, consumption of potatoes was limited in Spain and pasta in Sweden ( [18](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B18)).

Other examples of the improvement of LP methodology were demonstrated in literature by using more nutritional constraints ( [47](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B47)) and selecting most frequently consumed foods ( [4](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B4), [69](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B69)). Maillot et al. improved LP models by using a goal function to maximize most frequently consumed foods, without replacing more than five products from the current diet ( [4](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B4)). Van Dooren et al. ( [20](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B20)) implemented this by using a unique objective function, maximizing the most consumed food products based on weight and minimizing absolute change in portions. For example, in the men's diet 50 of the 83 products were kept unchanged in number of calculated portions, and in the women's 55 of the 73 products. The Optimeal tool calculated a change in portions for 8 foods for men and 7 for women. Finally, 9 new food items were added to the men's diet and 8 to the women's (unsalted peanuts, pear, kale, sauerkraut, lentils, marrowfats, soy drink, mackerel, and mussels). Nevertheless, the diet was almost vegetarian, with less portions of meat and dairy. Likewise, new products such as soy drink, marrowfats and lentils were added to the diet, which are not consumed by the majority of the Dutch population ( [20](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B20)). A reality check is needed to determine if this would be acceptable for consumers.

Tyszler et al. ( [21](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B21)) described the application of a penalty score as acceptability constraint in more detail. The metric for changes was measured by a penalty score based on the popularity of foods. More specifically, “the number of servings changed in each food is multiplied by a normalization of the total quantity of that food (grams) previously consumed” according to the dietary survey ( [21](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B21)). Tyszler et al. explained: “The penalty score can be interpreted as a measure of distance between diets. The reasoning behind this modeling is that diets which are like the current one is more likely to be accepted by most of the population than more extreme diets.” The results of their study are shown in Figure [3](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#F3): “the closer a diet is to the frontier line, the more similar it is to the current diet, while being healthy” ( [21](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B21)). The “Closest healthy” and the “30% less” environmental impact diet (expressed as Recipe-scores; Recipe is a unit used in LCA methods) are, by definition, on the frontier. The figure indicates that, if the goal of the optimization is a diet with lower environmental load Vegetarian or Vegan are not the only options. There are many other solutions to this diet problem with a smaller number of adaptations in the diet ( [21](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B21)). Introducing acceptability constraints is recommended, but no study has provided the ultimate solution to calculating acceptability.

Figure 3

Example of the application of acceptability constraints and the effects on the environmental impact of different diet scenarios (M, males; F, females). The lower the penalty score is, the closer the diet is to the current diet and the more acceptable ( [21](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B21)). The red line is called the “possibilities frontier.” It indicates the possibilities with the lowest penalty score for a certain environmental constraint ( [21](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B21)).

### Proven value of LP in diet studies

Although the Diet Problem has a long history, most diet solutions are from 2000 or later, as computers with larger calculation capacity became widely available and LP tools were developed. The literature shows that LP can be applied to a variety of diet problems: from food aid, national food programs, dietary guidelines, to individual solutions. In supporting dietary guidelines, LP has proven its value in many ways. Most studies have used nutritional constraints combined with cost constraints. Studies showed weaknesses when the number of food items and/or nutritional constraints were low. However, even when the number of constraints is increased, LP is not always able to find solutions. Nutritional constraints should reflect at least the national dietary guidelines. In defining affordable diets and investigating the relationship between cost and health, LP studies provided insightful contradictions. LP shows that cheaper and healthier foods can be found easily, but when price becomes a constraint, often a shift occurs to unusual food unless the right constraints are chosen. LP can produce solutions that are not realistic for the population, especially when cultural acceptability is not considered. Introducing acceptability constraints is recommended, but none of the studies provide the ultimate solution for calculating acceptability. LP can play a role in the future developments on acceptance of changes and personalized food.

### Choice of function and tool

Table [2](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#T2) demonstrated that the analyzed studies are not always clear about the choice of their programming tool and objective function. Arnould et al. ( [16](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B16)) and Javala et al. ( [13](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B13)) seems to apply QP, but that is not even clear. Macdiarmid et al. ( [17](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B17)) and Wilson et al. ( [19](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/full#B19)) did not describe where the optimization is based on (GHGEs or nutritional requirements?). It should be expected that the methods are clearly described. The older software tools (Rglpk package, R stat software and Solver in Excel) are still in use and seem to function well, but because of the complexity of the diet problem, more sophisticated and tailor-made tools are built for specific application (Optimeal and Cost of the Diet-tool). Further development is needed to implement acceptability constraints.

Quadratic Programming has many advantages over LP when you want small changes on population level. QP differs from LP in that the functions are not linear but quadratic. An inherent limitation of LP is that it limits the amount of changes, while sometimes a wider range of small changes in products can give more useful solutions, e.g., when changing diets on population level. QP have this advantage above LP.

## Conclusions

LP could be helpful to support development of dietary guidelines that fulfill all nutritional requirements. LP also demonstrated to be an applicable tool to conscientiously convert predefined nutrient constraints into diets with unpredictable food combinations. Most studies have used nutritional constraints and cost constraints in the analysis of dietary problems and solutions, but such research begin showing weaknesses under situations featuring a small number of food items and/or nutritional constraints. Introducing acceptability constraints is recommended, but no study has provided the ultimate solution to calculating acceptability. Only 12 studies applied and introduced ecological constraints (and of these, only two also included cost constraints). These studies showed that the environmental impacts of diets can be halved, staying within the existing nutritional constraints. LP makes it possible to propose diets with lower impacts than diet scenario studies. In other words, LP is an important tool for environmental optimization and has a lot of potential. Important is consistency in methodology to derive environmental figures (full scope) and completeness of constraints. Future possibilities lie in finding LP solutions for diets by combining nutritional, cost, ecological, and acceptability constraints. LP is clearly a very helpful instrument for finding solutions to a variety of very complex diet problems.

## Statements

### Author contributions

The author confirms being the sole contributor of this work and approved it for publication.

### Acknowledgments

Thanks to Harry Aiking and Hans Blonk for their critical comments on the concept of this paper.

### Conflict of interest

The author declares that the research was conducted in the absence of any commercial or financial relationships that could be construed as a potential conflict of interest.

## References

- 1.





FAO. _How to Feed the World in 2050_. Rome: FAO (2010).



  - [Google Scholar](http://scholar.google.com/scholar_lookup?publication_year=2010&journal=How+to+Feed+the+World+in+2050)

- 2.





HerforthAFrongilloEASassiFMcLeanMSArabiMTiradoCet al. Toward an integrated approach to nutritional quality, environmental sustainability, and economic viability: research and measurement gaps. _Ann N Y Acad Sci._ (2016) 1332:1–21. 10.1111/nyas.12552



  - [Pubmed Abstract](https://pubmed.ncbi.nlm.nih.gov/25351044)
  - [CrossRef](https://doi.org/10.1111/nyas.12552)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=A.%2BHerforth&author=EA.%2BFrongillo&author=F.%2BSassi&author=MS.%2BMcLean&author=M.%2BArabi&author=C.%2BTirado&publication_year=2016&title=Toward%2Ban%2Bintegrated%2Bapproach%2Bto%2Bnutritional%2Bquality%2C%2Benvironmental%2Bsustainability%2C%2Band%2Beconomic%2Bviability%3A%2Bresearch%2Band%2Bmeasurement%2Bgaps&journal=Ann+N+Y+Acad+Sci.&volume=1332&pages=1-21)

- 3.





BriendADarmonNFergusonEErhardtJG. Linear programming: a mathematical tool for analyzing and optimizing children's diets during the complementary feeding period. _J Pediatr Gastroenterol Nutr._ (2003) 36:12–22. 10.1097/00005176-200301000-00006



  - [Pubmed Abstract](https://pubmed.ncbi.nlm.nih.gov/12499991)
  - [CrossRef](https://doi.org/10.1097/00005176-200301000-00006)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=A.%2BBriend&author=N.%2BDarmon&author=E.%2BFerguson&author=JG.%2BErhardt&publication_year=2003&title=Linear%2Bprogramming%3A%2Ba%2Bmathematical%2Btool%2Bfor%2Banalyzing%2Band%2Boptimizing%2Bchildren%27s%2Bdiets%2Bduring%2Bthe%2Bcomplementary%2Bfeeding%2Bperiod&journal=J+Pediatr+Gastroenterol+Nutr.&volume=36&pages=12-22)

- 4.





MaillotMVieuxFAmiotMJDarmonN. Individual diet modeling translates nutrient recommendations into realistic and individual-specific food choices. _Am J Clin Nutr._ (2010) 91:421–30. 10.3945/ajcn.2009.28426



  - [Pubmed Abstract](https://pubmed.ncbi.nlm.nih.gov/19939986)
  - [CrossRef](https://doi.org/10.3945/ajcn.2009.28426)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=M.%2BMaillot&author=F.%2BVieux&author=MJ.%2BAmiot&author=N.%2BDarmon&publication_year=2010&title=Individual%2Bdiet%2Bmodeling%2Btranslates%2Bnutrient%2Brecommendations%2Binto%2Brealistic%2Band%2Bindividual-specific%2Bfood%2Bchoices&journal=Am+J+Clin+Nutr.&volume=91&pages=421-30)

- 5.





MacdiarmidJI. Is a healthy diet an environmentally sustainable diet? _Proc Nutr Soc._ (2013) 72:13–20. 10.1017/S0029665112002893



  - [Pubmed Abstract](https://pubmed.ncbi.nlm.nih.gov/23186839)
  - [CrossRef](https://doi.org/10.1017/S0029665112002893)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=JI.%2BMacdiarmid&publication_year=2013&title=Is%2Ba%2Bhealthy%2Bdiet%2Ban%2Benvironmentally%2Bsustainable%2Bdiet%3F&journal=Proc+Nutr+Soc.&volume=72&pages=13-20)

- 6.





DantzigGBThapaMN. _Linear Programming 1: Introduction_. New York, NY: Springer-Verlag (1997).



  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=GB.%2BDantzig&author=MN.%2BThapa&publication_year=1997&journal=Linear+Programming+1%3A+Introduction)

- 7.





SmithVE. Linear programming models for the determination of palatable human diets. _J Farm Econ._ (1959) 41:272–83. 10.2307/1235154



  - [CrossRef](https://doi.org/10.2307/1235154)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=VE.%2BSmith&publication_year=1959&title=Linear%2Bprogramming%2Bmodels%2Bfor%2Bthe%2Bdetermination%2Bof%2Bpalatable%2Bhuman%2Bdiets&journal=J+Farm+Econ.&volume=41&pages=272-83)

- 8.





StiglerGJ. The cost of subsistence. _J Farm Econ._ (1945) 7:303–14. 10.2307/1231810



  - [CrossRef](https://doi.org/10.2307/1231810)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=GJ.%2BStigler&publication_year=1945&title=The%2Bcost%2Bof%2Bsubsistence&journal=J+Farm+Econ.&volume=7&pages=303-14)

- 9.





ButtrissJLBriendADarmonNFergusonELMaillotMLluchA. Diet modelling: how it can inform the development of dietary recommendations and public health policy. _Nutr Bull._ (2014) 39:115–25. 10.1111/nbu.12076



  - [CrossRef](https://doi.org/10.1111/nbu.12076)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=JL.%2BButtriss&author=A.%2BBriend&author=N.%2BDarmon&author=EL.%2BFerguson&author=M.%2BMaillot&author=A.%2BLluch&publication_year=2014&title=Diet%2Bmodelling%3A%2Bhow%2Bit%2Bcan%2Binform%2Bthe%2Bdevelopment%2Bof%2Bdietary%2Brecommendations%2Band%2Bpublic%2Bhealth%2Bpolicy&journal=Nutr+Bull.&volume=39&pages=115-25)

- 10.





DantzigGB. The diet problem. _Interfaces_. (1990) 20:43–7. 10.1287/inte.20.4.43



  - [CrossRef](https://doi.org/10.1287/inte.20.4.43)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=GB.%2BDantzig&publication_year=1990&title=The%2Bdiet%2Bproblem&journal=Interfaces&volume=20&pages=43-7)

- 11.





BriendAFergusonEDarmonN. Local food price analysis by linear programming: a new approach to assess the economic value of fortified food supplements. _Food Nutr Bull._ (2001) 22:184–9. 10.1177/156482650102200210



  - [CrossRef](https://doi.org/10.1177/156482650102200210)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=A.%2BBriend&author=E.%2BFerguson&author=N.%2BDarmon&publication_year=2001&title=Local%2Bfood%2Bprice%2Banalysis%2Bby%2Blinear%2Bprogramming%3A%2Ba%2Bnew%2Bapproach%2Bto%2Bassess%2Bthe%2Beconomic%2Bvalue%2Bof%2Bfortified%2Bfood%2Bsupplements&journal=Food+Nutr+Bull.&volume=22&pages=184-9)

- 12.





KramerGFHTyszlerMVeerPvtBlonkH. Decreasing the overall environmental impact of the Dutch diet: how to find healthy and sustainable diets with limited changes. _Public Health Nutr_. (2017) 20:1699–709. 10.1017/S1368980017000349



  - [Pubmed Abstract](https://pubmed.ncbi.nlm.nih.gov/28318463)
  - [CrossRef](https://doi.org/10.1017/S1368980017000349)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=GFH.%2BKramer&author=M.%2BTyszler&author=Pvt.%2BVeer&author=H.%2BBlonk&publication_year=2017&title=Decreasing%2Bthe%2Boverall%2Benvironmental%2Bimpact%2Bof%2Bthe%2BDutch%2Bdiet%3A%2Bhow%2Bto%2Bfind%2Bhealthy%2Band%2Bsustainable%2Bdiets%2Bwith%2Blimited%2Bchanges&journal=Public+Health+Nutr&volume=20&pages=1699-709)

- 13.





JalavaMKummuMPorkkaMSiebertSVarisO. Diet change—a solution to reduce water use? _Envir Res Lett._ (2014) 9:074016. 10.1088/1748-9326/9/7/074016



  - [CrossRef](https://doi.org/10.1088/1748-9326/9/7/074016)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=M.%2BJalava&author=M.%2BKummu&author=M.%2BPorkka&author=S.%2BSiebert&author=O.%2BVaris&publication_year=2014&title=Diet%2Bchange%E2%80%94a%2Bsolution%2Bto%2Breduce%2Bwater%2Buse%3F&journal=Envir+Res+Lett.&volume=9)

- 14.





NocedalJWrightS. _Numerical Optimization_. New York, NY: Springer-Verlag (1999).



  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=J.%2BNocedal&author=S.%2BWright&publication_year=1999&journal=Numerical+Optimization)

- 15.





MertensEvan't VeerPHiddinkGJSteijnsJMJMKuijstenA. Operationalising the health aspects of sustainable diets: a review. _Public Health Nutr._ (2017) 20:739–57. 10.1017/S1368980016002664



  - [Pubmed Abstract](https://pubmed.ncbi.nlm.nih.gov/27819199)
  - [CrossRef](https://doi.org/10.1017/S1368980016002664)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=E.%2BMertens&author=P.%2Bvan%27t%2BVeer&author=GJ.%2BHiddink&author=JMJM.%2BSteijns&author=A.%2BKuijsten&publication_year=2017&title=Operationalising%2Bthe%2Bhealth%2Baspects%2Bof%2Bsustainable%2Bdiets%3A%2Ba%2Breview&journal=Public+Health+Nutr.&volume=20&pages=739-57)

- 16.





ArnoultMHJonesPJTranterRBTiffinRTraillWBTzanopoulosJ. Modelling the likely impact of healthy eating guidelines on agricultural production and land use in England and Wales. _Land Use Policy_ (2010) 27:1046–55. 10.1016/j.landusepol.2010.02.001



  - [CrossRef](https://doi.org/10.1016/j.landusepol.2010.02.001)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=MH.%2BArnoult&author=PJ.%2BJones&author=RB.%2BTranter&author=R.%2BTiffin&author=WB.%2BTraill&author=J.%2BTzanopoulos&publication_year=2010&title=Modelling%2Bthe%2Blikely%2Bimpact%2Bof%2Bhealthy%2Beating%2Bguidelines%2Bon%2Bagricultural%2Bproduction%2Band%2Bland%2Buse%2Bin%2BEngland%2Band%2BWales&journal=Land+Use+Policy&volume=27&pages=1046-55)

- 17.





MacdiarmidJIKyleJHorganGWLoeJFyfeCJohnstoneAet al. Sustainable diets for the future: can we contribute to reducing greenhouse gas emissions by eating a healthy diet? _Am J Clin Nutr._ (2012) 96:632–9. 10.3945/ajcn.112.038729



  - [Pubmed Abstract](https://pubmed.ncbi.nlm.nih.gov/22854399)
  - [CrossRef](https://doi.org/10.3945/ajcn.112.038729)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=JI.%2BMacdiarmid&author=J.%2BKyle&author=GW.%2BHorgan&author=J.%2BLoe&author=C.%2BFyfe&author=A.%2BJohnstone&publication_year=2012&title=Sustainable%2Bdiets%2Bfor%2Bthe%2Bfuture%3A%2Bcan%2Bwe%2Bcontribute%2Bto%2Breducing%2Bgreenhouse%2Bgas%2Bemissions%2Bby%2Beating%2Ba%2Bhealthy%2Bdiet%3F&journal=Am+J+Clin+Nutr.&volume=96&pages=632-9)

- 18.





ThompsonSGowerRDarmonNVieuxFMurphy-BokernDMaillotM. _A Balance of Healthy and Sustainable Food Choices for France, Spain, and Sweden_. London: World Wildlife Fund UK (2013).



  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=S.%2BThompson&author=R.%2BGower&author=N.%2BDarmon&author=F.%2BVieux&author=D.%2BMurphy-Bokern&author=M.%2BMaillot&publication_year=2013&journal=A+Balance+of+Healthy+and+Sustainable+Food+Choices+for+France%2C+Spain%2C+and+Sweden)

- 19.





WilsonNNghiemNNi MhurchuCEylesHBakerMGBlakelyT. Foods and dietary patterns that are healthy, low-cost, and environmentally sustainable: a case study of optimization modeling for New Zealand. _PLoS ONE_ (2013) 8:27. 10.1371/journal.pone.0059648



  - [Pubmed Abstract](https://pubmed.ncbi.nlm.nih.gov/23544082)
  - [CrossRef](https://doi.org/10.1371/journal.pone.0059648)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=N.%2BWilson&author=N.%2BNghiem&author=C.%2BNi%2BMhurchu&author=H.%2BEyles&author=MG.%2BBaker&author=T.%2BBlakely&publication_year=2013&title=Foods%2Band%2Bdietary%2Bpatterns%2Bthat%2Bare%2Bhealthy%2C%2Blow-cost%2C%2Band%2Benvironmentally%2Bsustainable%3A%2Ba%2Bcase%2Bstudy%2Bof%2Boptimization%2Bmodeling%2Bfor%2BNew%2BZealand&journal=PLoS+ONE&volume=8)

- 20.





van DoorenCTyszlerMKramerGAikingH. Combining low price, low climate impact and high nutritional value in one shopping basket through diet optimization by linear programming. _Sustainability_ (2015) 7:12837. 10.3390/su70912837



  - [CrossRef](https://doi.org/10.3390/su70912837)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=C.%2Bvan%2BDooren&author=M.%2BTyszler&author=G.%2BKramer&author=H.%2BAiking&publication_year=2015&title=Combining%2Blow%2Bprice%2C%2Blow%2Bclimate%2Bimpact%2Band%2Bhigh%2Bnutritional%2Bvalue%2Bin%2Bone%2Bshopping%2Bbasket%2Bthrough%2Bdiet%2Boptimization%2Bby%2Blinear%2Bprogramming&journal=Sustainability&volume=7)

- 21.





TyszlerMKramerGBlonkH. Just eating healthier is not enough: studying the environmental impact of different diet scenarios for Dutch women (31–50 years old) by linear programming. _Int J Life Cycle Assess._ (2016) 21:701–9. 10.1007/s11367-015-0981-9



  - [CrossRef](https://doi.org/10.1007/s11367-015-0981-9)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=M.%2BTyszler&author=G.%2BKramer&author=H.%2BBlonk&publication_year=2016&title=Just%2Beating%2Bhealthier%2Bis%2Bnot%2Benough%3A%2Bstudying%2Bthe%2Benvironmental%2Bimpact%2Bof%2Bdifferent%2Bdiet%2Bscenarios%2Bfor%2BDutch%2Bwomen%2B%2831%E2%80%9350%2Byears%2Bold%29%2Bby%2Blinear%2Bprogramming&journal=Int+J+Life+Cycle+Assess.&volume=21&pages=701-9)

- 22.





GreenRMilnerJDangourADHainesAChalabiZMarkandyaAet al. The potential to reduce greenhouse gas emissions in the UK through healthy and realistic dietary change. _Clim Change_ (2015) 129:253–65. 10.1007/s10584-015-1329-y



  - [CrossRef](https://doi.org/10.1007/s10584-015-1329-y)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=R.%2BGreen&author=J.%2BMilner&author=AD.%2BDangour&author=A.%2BHaines&author=Z.%2BChalabi&author=A.%2BMarkandya&publication_year=2015&title=The%2Bpotential%2Bto%2Breduce%2Bgreenhouse%2Bgas%2Bemissions%2Bin%2Bthe%2BUK%2Bthrough%2Bhealthy%2Band%2Brealistic%2Bdietary%2Bchange&journal=Clim+Change&volume=129&pages=253-65)

- 23.





PerignonMMassetGFerrariGBarreTVieuxFMaillotMet al. How low can dietary greenhouse gas emissions be reduced without impairing nutritional adequacy, affordability and acceptability of the diet? A modelling study to guide sustainable food choices. _Public Health Nutr._ (2016) 6:1–13. 10.1017/S1368980016000653



  - [CrossRef](https://doi.org/10.1017/S1368980016000653)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=M.%2BPerignon&author=G.%2BMasset&author=G.%2BFerrari&author=T.%2BBarre&author=F.%2BVieux&author=M.%2BMaillot&publication_year=2016&title=How%2Blow%2Bcan%2Bdietary%2Bgreenhouse%2Bgas%2Bemissions%2Bbe%2Breduced%2Bwithout%2Bimpairing%2Bnutritional%2Badequacy%2C%2Baffordability%2Band%2Bacceptability%2Bof%2Bthe%2Bdiet%3F%2BA%2Bmodelling%2Bstudy%2Bto%2Bguide%2Bsustainable%2Bfood%2Bchoices&journal=Public+Health+Nutr.&volume=6&pages=1-13)

- 24.





HorganGWPerrinAWhybrowSMacdiarmidJI. Achieving dietary recommendations and reducing greenhouse gas emissions: modelling diets to minimise the change from current intakes. _Int J Behav Nutr Phys Act_. 201613:46. 10.1186/s12966-016-0370-1



  - [Pubmed Abstract](https://pubmed.ncbi.nlm.nih.gov/27056829)
  - [CrossRef](https://doi.org/10.1186/s12966-016-0370-1)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=GW.%2BHorgan&author=A.%2BPerrin&author=S.%2BWhybrow&author=JI.%2BMacdiarmid&publication_year=2016&title=Achieving%2Bdietary%2Brecommendations%2Band%2Breducing%2Bgreenhouse%2Bgas%2Bemissions%3A%2Bmodelling%2Bdiets%2Bto%2Bminimise%2Bthe%2Bchange%2Bfrom%2Bcurrent%2Bintakes&journal=Int+J+Behav+Nutr+Phys+Act&volume=13)

- 25.





DonatiMMenozziDZighettiCRosiAZinettiAScazzinaF. Towards a sustainable diet combining economic, environmental and nutritional objectives. _Appetite_ (2016) 106:48–57. 10.1016/j.appet.2016.02.151



  - [Pubmed Abstract](https://pubmed.ncbi.nlm.nih.gov/26921487)
  - [CrossRef](https://doi.org/10.1016/j.appet.2016.02.151)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=M.%2BDonati&author=D.%2BMenozzi&author=C.%2BZighetti&author=A.%2BRosi&author=A.%2BZinetti&author=F.%2BScazzina&publication_year=2016&title=Towards%2Ba%2Bsustainable%2Bdiet%2Bcombining%2Beconomic%2C%2Benvironmental%2Band%2Bnutritional%2Bobjectives&journal=Appetite&volume=106&pages=48-57)

- 26.





van DoorenCAikingH. Defining a nutritionally healthy, environmentally friendly, and culturally acceptable low lands diet. _Int J Life Cycle Assess_. (2016) 21:688–700. 10.1007/s11367-015-1007-3



  - [CrossRef](https://doi.org/10.1007/s11367-015-1007-3)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=C.%2Bvan%2BDooren&author=H.%2BAiking&publication_year=2016&title=Defining%2Ba%2Bnutritionally%2Bhealthy%2C%2Benvironmentally%2Bfriendly%2C%2Band%2Bculturally%2Bacceptable%2Blow%2Blands%2Bdiet&journal=Int+J+Life+Cycle+Assess&volume=21&pages=688-700)

- 27.





SodenPMFletcherLR. Modifying diets to satisfy nutritional requirements using linear programming. _Br J Nutr._ (1992) 68:565–72. 10.1079/BJN19920115



  - [Pubmed Abstract](https://pubmed.ncbi.nlm.nih.gov/1493126)
  - [CrossRef](https://doi.org/10.1079/BJN19920115)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=PM.%2BSoden&author=LR.%2BFletcher&publication_year=1992&title=Modifying%2Bdiets%2Bto%2Bsatisfy%2Bnutritional%2Brequirements%2Busing%2Blinear%2Bprogramming&journal=Br+J+Nutr.&volume=68&pages=565-72)

- 28.





FletcherLRSodenPMZinoberASI. Linear programming techniques for the construction of palatable human diets. _J Op Res Soc._ (1994) 45:489–96. 10.1057/jors.1994.76



  - [CrossRef](https://doi.org/10.1057/jors.1994.76)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=LR.%2BFletcher&author=PM.%2BSoden&author=ASI.%2BZinober&publication_year=1994&title=Linear%2Bprogramming%2Btechniques%2Bfor%2Bthe%2Bconstruction%2Bof%2Bpalatable%2Bhuman%2Bdiets&journal=J+Op+Res+Soc.&volume=45&pages=489-96)

- 29.





Staff at the Center for Nutrition Policy and PromotionLinoM. The thrifty food plan, 1999: revisions of the market baskets. _Family Econ Nutr Rev_. (2001) 13:50–63.



  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=M.%2BLino&publication_year=2001&title=The%2Bthrifty%2Bfood%2Bplan%2C%2B1999%3A%2Brevisions%2Bof%2Bthe%2Bmarket%2Bbaskets&journal=Family+Econ+Nutr+Rev&volume=13&pages=50-63)

- 30.





WildePELlobreraJ. Using the thrifty food plan to assess the cost of a nutritious diet. _J Cons Affairs_ (2009) 43:274–304. 10.1111/j.1745-6606.2009.01140.x



  - [CrossRef](https://doi.org/10.1111/j.1745-6606.2009.01140.x)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=PE.%2BWilde&author=J.%2BLlobrera&publication_year=2009&title=Using%2Bthe%2Bthrifty%2Bfood%2Bplan%2Bto%2Bassess%2Bthe%2Bcost%2Bof%2Ba%2Bnutritious%2Bdiet&journal=J+Cons+Affairs&volume=43&pages=274-304)

- 31.





GaoXWildePELichtensteinAHTuckerKL. The 2005 USDA food guide pyramid is associated with more adequate nutrient intakes within energy constraints than the 1992 pyramid. _J Nutr._ (2006) 136:1341–6. 10.1093/jn/136.5.1341



  - [Pubmed Abstract](https://pubmed.ncbi.nlm.nih.gov/16614427)
  - [CrossRef](https://doi.org/10.1093/jn/136.5.1341)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=X.%2BGao&author=PE.%2BWilde&author=AH.%2BLichtenstein&author=KL.%2BTucker&publication_year=2006&title=The%2B2005%2BUSDA%2Bfood%2Bguide%2Bpyramid%2Bis%2Bassociated%2Bwith%2Bmore%2Badequate%2Bnutrient%2Bintakes%2Bwithin%2Benergy%2Bconstraints%2Bthan%2Bthe%2B1992%2Bpyramid&journal=J+Nutr.&volume=136&pages=1341-6)

- 32.





MaesLVereeckenCAGedrichKRiekenKSichert-HellertWDe BourdeaudhuijIet al. A feasibility study of using a diet optimization approach in a web-based computer-tailoring intervention for adolescents. _Int J Obes._ (2008) 32:186. 10.1038/ijo.2008.186



  - [Pubmed Abstract](https://pubmed.ncbi.nlm.nih.gov/19011657)
  - [CrossRef](https://doi.org/10.1038/ijo.2008.186)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=L.%2BMaes&author=CA.%2BVereecken&author=K.%2BGedrich&author=K.%2BRieken&author=W.%2BSichert-Hellert&author=I.%2BDe%2BBourdeaudhuij&publication_year=2008&title=A%2Bfeasibility%2Bstudy%2Bof%2Busing%2Ba%2Bdiet%2Boptimization%2Bapproach%2Bin%2Ba%2Bweb-based%2Bcomputer-tailoring%2Bintervention%2Bfor%2Badolescents&journal=Int+J+Obes.&volume=32)

- 33.





MacdiarmidJKyleJHorganGLoeJFyfeCJohnstoneAet al. _Livewell: A Balance of Healthy and Sustainable Food Choices_. Aberdeen: WWF, Rowett Institute of Nutrition and Health (2011).



  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=J.%2BMacdiarmid&author=J.%2BKyle&author=G.%2BHorgan&author=J.%2BLoe&author=C.%2BFyfe&author=A.%2BJohnstone&publication_year=2011&journal=Livewell%3A+A+Balance+of+Healthy+and+Sustainable+Food+Choices)

- 34.





DarmonNFergusonEBriendA. Linear and nonlinear programming to optimize the nutrient density of a population's diet: an example based on diets of preschool children in rural Malawi. _Am J Clin Nutr._ (2002) 75:245–53. 10.1093/ajcn/75.2.245



  - [Pubmed Abstract](https://pubmed.ncbi.nlm.nih.gov/11815314)
  - [CrossRef](https://doi.org/10.1093/ajcn/75.2.245)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=N.%2BDarmon&author=E.%2BFerguson&author=A.%2BBriend&publication_year=2002&title=Linear%2Band%2Bnonlinear%2Bprogramming%2Bto%2Boptimize%2Bthe%2Bnutrient%2Bdensity%2Bof%2Ba%2Bpopulation%27s%2Bdiet%3A%2Ban%2Bexample%2Bbased%2Bon%2Bdiets%2Bof%2Bpreschool%2Bchildren%2Bin%2Brural%2BMalawi&journal=Am+J+Clin+Nutr.&volume=75&pages=245-53)

- 35.





SantikaOFahmidaUFergusonEL. Development of food-based complementary feeding recommendations for 9- to 11-month-old peri-urban Indonesian infants using linear programming. _J Nutr._ (2009) 139:135–41. 10.3945/jn.108.092270



  - [Pubmed Abstract](https://pubmed.ncbi.nlm.nih.gov/19056658)
  - [CrossRef](https://doi.org/10.3945/jn.108.092270)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=O.%2BSantika&author=U.%2BFahmida&author=EL.%2BFerguson&publication_year=2009&title=Development%2Bof%2Bfood-based%2Bcomplementary%2Bfeeding%2Brecommendations%2Bfor%2B9-%2Bto%2B11-month-old%2Bperi-urban%2BIndonesian%2Binfants%2Busing%2Blinear%2Bprogramming&journal=J+Nutr.&volume=139&pages=135-41)

- 36.





FregaRLanfrancoJGDe GreveSBernardiniSGeniezPGredeNet al. What linear programming contributes: world food programme experience with the “cost of the diet” tool. _Food Nutr Bull._ (2012) 33(3 Suppl.):S228–34. 10.1177/15648265120333S212



  - [CrossRef](https://doi.org/10.1177/15648265120333S212)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=R.%2BFrega&author=JG.%2BLanfranco&author=S.%2BDe%2BGreve&author=S.%2BBernardini&author=P.%2BGeniez&author=N.%2BGrede&publication_year=2012&title=What%2Blinear%2Bprogramming%2Bcontributes%3A%2Bworld%2Bfood%2Bprogramme%2Bexperience%2Bwith%2Bthe%2B%E2%80%9Ccost%2Bof%2Bthe%2Bdiet%E2%80%9D%2Btool&journal=Food+Nutr+Bull.)

- 37.





World Cancer Research Fund/American Institute for Cancer Research. _Food, Nutrition, Physical Activity, and the Prevention of Cancer: A Global Perspective_. Washington DC: AICR (2007).



  - [Google Scholar](http://scholar.google.com/scholar_lookup?publication_year=2007&journal=Food%2C+Nutrition%2C+Physical+Activity%2C+and+the+Prevention+of+Cancer%3A+A+Global+Perspective)

- 38.





MassetGMonsivaisPMaillotMDarmonNDrewnowskiA. Diet optimization methods can help translate dietary guidelines into a cancer prevention food plan. _J Nutr._ (2009) 139:1541–8. 10.3945/jn.109.104398



  - [Pubmed Abstract](https://pubmed.ncbi.nlm.nih.gov/19535422)
  - [CrossRef](https://doi.org/10.3945/jn.109.104398)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=G.%2BMasset&author=P.%2BMonsivais&author=M.%2BMaillot&author=N.%2BDarmon&author=A.%2BDrewnowski&publication_year=2009&title=Diet%2Boptimization%2Bmethods%2Bcan%2Bhelp%2Btranslate%2Bdietary%2Bguidelines%2Binto%2Ba%2Bcancer%2Bprevention%2Bfood%2Bplan&journal=J+Nutr.&volume=139&pages=1541-8)

- 39.





MetzgarMRideoutTCFontes-VillalbaMKuipersRS. The feasibility of a Paleolithic diet for low-income consumers. _Nutr Res._ (2011) 31:444–51. 10.1016/j.nutres.2011.05.008



  - [Pubmed Abstract](https://pubmed.ncbi.nlm.nih.gov/21745626)
  - [CrossRef](https://doi.org/10.1016/j.nutres.2011.05.008)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=M.%2BMetzgar&author=TC.%2BRideout&author=M.%2BFontes-Villalba&author=RS.%2BKuipers&publication_year=2011&title=The%2Bfeasibility%2Bof%2Ba%2BPaleolithic%2Bdiet%2Bfor%2Blow-income%2Bconsumers&journal=Nutr+Res.&volume=31&pages=444-51)

- 40.





DarmonNVieuxFMaillotMVolatierJ-LMartinA. Nutrient profiles discriminate between foods according to their contribution to nutritionally adequate diets: a validation study using linear programming and the SAIN,LIM system. _Am J Clin Nutr._ (2009) 89:1227–36. 10.3945/ajcn.2008.26465



  - [Pubmed Abstract](https://pubmed.ncbi.nlm.nih.gov/19211815)
  - [CrossRef](https://doi.org/10.3945/ajcn.2008.26465)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=N.%2BDarmon&author=F.%2BVieux&author=M.%2BMaillot&author=J-L.%2BVolatier&author=A.%2BMartin&publication_year=2009&title=Nutrient%2Bprofiles%2Bdiscriminate%2Bbetween%2Bfoods%2Baccording%2Bto%2Btheir%2Bcontribution%2Bto%2Bnutritionally%2Badequate%2Bdiets%3A%2Ba%2Bvalidation%2Bstudy%2Busing%2Blinear%2Bprogramming%2Band%2Bthe%2BSAIN%2CLIM%2Bsystem&journal=Am+J+Clin+Nutr.&volume=89&pages=1227-36)

- 41.





ClerfeuilleEVieuxFLluchADarmonNRolf-PedersenN. Assessing the construct validity of five nutrient profiling systems using diet modeling with linear programming. _Eur J Clin Nutr._ (2013) 67:1003–5. 10.1038/ejcn.2013.95



  - [Pubmed Abstract](https://pubmed.ncbi.nlm.nih.gov/23695210)
  - [CrossRef](https://doi.org/10.1038/ejcn.2013.95)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=E.%2BClerfeuille&author=F.%2BVieux&author=A.%2BLluch&author=N.%2BDarmon&author=N.%2BRolf-Pedersen&publication_year=2013&title=Assessing%2Bthe%2Bconstruct%2Bvalidity%2Bof%2Bfive%2Bnutrient%2Bprofiling%2Bsystems%2Busing%2Bdiet%2Bmodeling%2Bwith%2Blinear%2Bprogramming&journal=Eur+J+Clin+Nutr.&volume=67&pages=1003-5)

- 42.





MartinA. The “apports nutritionnels conseilles (ANC)” for the French population. _Reprod Nutr Dev._ (2001) 41:119–28. 10.1051/rnd:2001100



  - [Pubmed Abstract](https://pubmed.ncbi.nlm.nih.gov/11434516)
  - [CrossRef](https://doi.org/10.1051/rnd:2001100)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=A.%2BMartin&publication_year=2001&title=The%2B%E2%80%9Capports%2Bnutritionnels%2Bconseilles%2B%28ANC%29%E2%80%9D%2Bfor%2Bthe%2BFrench%2Bpopulation&journal=Reprod+Nutr+Dev.&volume=41&pages=119-28)

- 43.





MaillotMVieuxFFergusonEFVolatierJLAmiotMJDarmonN. To meet nutrient recommendations, most French adults need to expand their habitual food repertoire. _J Nutr._ (2009) 139:1721–7. 10.3945/jn.109.107318



  - [Pubmed Abstract](https://pubmed.ncbi.nlm.nih.gov/19625703)
  - [CrossRef](https://doi.org/10.3945/jn.109.107318)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=M.%2BMaillot&author=F.%2BVieux&author=EF.%2BFerguson&author=JL.%2BVolatier&author=MJ.%2BAmiot&author=N.%2BDarmon&publication_year=2009&title=To%2Bmeet%2Bnutrient%2Brecommendations%2C%2Bmost%2BFrench%2Badults%2Bneed%2Bto%2Bexpand%2Btheir%2Bhabitual%2Bfood%2Brepertoire&journal=J+Nutr.&volume=139&pages=1721-7)

- 44.





FergusonELDarmonNBriendAPremachandraIM. Food-based dietary guidelines can be developed and tested using linear programming analysis. _J Nutr._ (2004) 134:951–7. 10.1093/jn/134.4.951



  - [Pubmed Abstract](https://pubmed.ncbi.nlm.nih.gov/15051853)
  - [CrossRef](https://doi.org/10.1093/jn/134.4.951)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=EL.%2BFerguson&author=N.%2BDarmon&author=A.%2BBriend&author=IM.%2BPremachandra&publication_year=2004&title=Food-based%2Bdietary%2Bguidelines%2Bcan%2Bbe%2Bdeveloped%2Band%2Btested%2Busing%2Blinear%2Bprogramming%2Banalysis&journal=J+Nutr.&volume=134&pages=951-7)

- 45.





FergusonELDarmonNFahmidaUFitriyantiSHarperTBPremachandraIM. Design of optimal food-based complementary feeding recommendations and identification of key “problem nutrients” using goal programming. _J Nutr._ (2006) 136:2399–404. 10.1093/jn/136.9.2399



  - [Pubmed Abstract](https://pubmed.ncbi.nlm.nih.gov/16920861)
  - [CrossRef](https://doi.org/10.1093/jn/136.9.2399)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=EL.%2BFerguson&author=N.%2BDarmon&author=U.%2BFahmida&author=S.%2BFitriyanti&author=TB.%2BHarper&author=IM.%2BPremachandra&publication_year=2006&title=Design%2Bof%2Boptimal%2Bfood-based%2Bcomplementary%2Bfeeding%2Brecommendations%2Band%2Bidentification%2Bof%2Bkey%2B%E2%80%9Cproblem%2Bnutrients%E2%80%9D%2Busing%2Bgoal%2Bprogramming&journal=J+Nutr.&volume=136&pages=2399-404)

- 46.





RambelosonZJDarmonNFergusonEL. Linear programming can help identify practical solutions to improve the nutritional quality of food aid. _Public Health Nutr._ (2008) 11:395–404. 10.1017/S1368980007000511



  - [Pubmed Abstract](https://pubmed.ncbi.nlm.nih.gov/17666136)
  - [CrossRef](https://doi.org/10.1017/S1368980007000511)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=ZJ.%2BRambeloson&author=N.%2BDarmon&author=EL.%2BFerguson&publication_year=2008&title=Linear%2Bprogramming%2Bcan%2Bhelp%2Bidentify%2Bpractical%2Bsolutions%2Bto%2Bimprove%2Bthe%2Bnutritional%2Bquality%2Bof%2Bfood%2Baid&journal=Public+Health+Nutr.&volume=11&pages=395-404)

- 47.





MaillotMDarmonNDrewnowskiA. Are the lowest-cost healthful food plans culturally and socially acceptable? _Public Health Nutr._ (2010) 13:1178–85. 10.1017/S1368980009993028



  - [Pubmed Abstract](https://pubmed.ncbi.nlm.nih.gov/20105388)
  - [CrossRef](https://doi.org/10.1017/S1368980009993028)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=M.%2BMaillot&author=N.%2BDarmon&author=A.%2BDrewnowski&publication_year=2010&title=Are%2Bthe%2Blowest-cost%2Bhealthful%2Bfood%2Bplans%2Bculturally%2Band%2Bsocially%2Bacceptable%3F&journal=Public+Health+Nutr.&volume=13&pages=1178-85)

- 48.





RyanKNAdamsKPVostiSAOrdizMICimoEDManaryMJ. A comprehensive linear programming tool to optimize formulations of ready-to-use therapeutic foods: an application to Ethiopia. _Am J Clin Nutr._ (2014) 100:1551–8. 10.3945/ajcn.114.090670



  - [Pubmed Abstract](https://pubmed.ncbi.nlm.nih.gov/25411290)
  - [CrossRef](https://doi.org/10.3945/ajcn.114.090670)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=KN.%2BRyan&author=KP.%2BAdams&author=SA.%2BVosti&author=MI.%2BOrdiz&author=ED.%2BCimo&author=MJ.%2BManary&publication_year=2014&title=A%2Bcomprehensive%2Blinear%2Bprogramming%2Btool%2Bto%2Boptimize%2Bformulations%2Bof%2Bready-to-use%2Btherapeutic%2Bfoods%3A%2Ban%2Bapplication%2Bto%2BEthiopia&journal=Am+J+Clin+Nutr.&volume=100&pages=1551-8)

- 49.





DibariFDiop elHICollinsSSealA. Low-cost, ready-to-use therapeutic foods can be designed using locally available commodities with the aid of linear programming. _J Nutr._ (2012) 142:955–61. 10.3945/jn.111.1569483



  - [Pubmed Abstract](https://pubmed.ncbi.nlm.nih.gov/22457396)
  - [CrossRef](https://doi.org/10.3945/jn.111.1569483)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=F.%2BDibari&author=HI.%2BDiop%2Bel&author=S.%2BCollins&author=A.%2BSeal&publication_year=2012&title=Low-cost%2C%2Bready-to-use%2Btherapeutic%2Bfoods%2Bcan%2Bbe%2Bdesigned%2Busing%2Blocally%2Bavailable%2Bcommodities%2Bwith%2Bthe%2Baid%2Bof%2Blinear%2Bprogramming&journal=J+Nutr.&volume=142&pages=955-61)

- 50.





BriendADarmonN. Determining limiting nutrients by linear programming: a new approach to predict insufficient intakes from complementary foods. _Pediatrics_ (2000) 106(Suppl. 4):1288–9.



  - [Pubmed Abstract](https://pubmed.ncbi.nlm.nih.gov/11061835)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=A.%2BBriend&author=N.%2BDarmon&publication_year=2000&title=Determining%2Blimiting%2Bnutrients%2Bby%2Blinear%2Bprogramming%3A%2Ba%2Bnew%2Bapproach%2Bto%2Bpredict%2Binsufficient%2Bintakes%2Bfrom%2Bcomplementary%2Bfoods&journal=Pediatrics&volume=106&pages=1288-9)

- 51.





DarmonNFergusonELBriendA. A cost constraint alone has adverse effects on food selection and nutrient density: an analysis of human diets by linear programming. _J Nutr._ (2002) 132:3764–71. 10.1093/jn/132.12.3764



  - [Pubmed Abstract](https://pubmed.ncbi.nlm.nih.gov/12468621)
  - [CrossRef](https://doi.org/10.1093/jn/132.12.3764)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=N.%2BDarmon&author=EL.%2BFerguson&author=A.%2BBriend&publication_year=2002&title=A%2Bcost%2Bconstraint%2Balone%2Bhas%2Badverse%2Beffects%2Bon%2Bfood%2Bselection%2Band%2Bnutrient%2Bdensity%3A%2Ban%2Banalysis%2Bof%2Bhuman%2Bdiets%2Bby%2Blinear%2Bprogramming&journal=J+Nutr.&volume=132&pages=3764-71)

- 52.





DarmonNFergusonEBriendA. Do economic constraints encourage the selection of energy dense diets? _Appetite_ (2003) 41:315–22. 10.1016/S0195-6663(03)00113-2



  - [Pubmed Abstract](https://pubmed.ncbi.nlm.nih.gov/14637330)
  - [CrossRef](https://doi.org/10.1016/S0195-6663(03)00113-2)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=N.%2BDarmon&author=E.%2BFerguson&author=A.%2BBriend&publication_year=2003&title=Do%2Beconomic%2Bconstraints%2Bencourage%2Bthe%2Bselection%2Bof%2Benergy%2Bdense%2Bdiets%3F&journal=Appetite&volume=41&pages=315-22)

- 53.





DarmonNFergusonELBriendA. Impact of a cost constraint on nutritionally adequate food choices for French women: an analysis by linear programming. _J Nutr Educ Behav._ (2006) 38:82–90. 10.1016/j.jneb.2005.11.028



  - [Pubmed Abstract](https://pubmed.ncbi.nlm.nih.gov/16595286)
  - [CrossRef](https://doi.org/10.1016/j.jneb.2005.11.028)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=N.%2BDarmon&author=EL.%2BFerguson&author=A.%2BBriend&publication_year=2006&title=Impact%2Bof%2Ba%2Bcost%2Bconstraint%2Bon%2Bnutritionally%2Badequate%2Bfood%2Bchoices%2Bfor%2BFrench%2Bwomen%3A%2Ban%2Banalysis%2Bby%2Blinear%2Bprogramming&journal=J+Nutr+Educ+Behav.&volume=38&pages=82-90)

- 54.





DrewnowskiASpecterS. Poverty and obesity: the role of energy density and energy costs. _Am J Clin Nutr._ (2004) 79:6–16. 10.1093/ajcn/79.1.6



  - [Pubmed Abstract](https://pubmed.ncbi.nlm.nih.gov/14684391)
  - [CrossRef](https://doi.org/10.1093/ajcn/79.1.6)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=A.%2BDrewnowski&author=S.%2BSpecter&publication_year=2004&title=Poverty%2Band%2Bobesity%3A%2Bthe%2Brole%2Bof%2Benergy%2Bdensity%2Band%2Benergy%2Bcosts&journal=Am+J+Clin+Nutr.&volume=79&pages=6-16)

- 55.





MaillotMDarmonNVieuxFDrewnowskiA. Low energy density and high nutritional quality are each associated with higher diet costs in French adults. _Am J Clin Nutr._ (2007) 86:690–6. 10.1093/ajcn/86.3.690



  - [Pubmed Abstract](https://pubmed.ncbi.nlm.nih.gov/17823434)
  - [CrossRef](https://doi.org/10.1093/ajcn/86.3.690)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=M.%2BMaillot&author=N.%2BDarmon&author=F.%2BVieux&author=A.%2BDrewnowski&publication_year=2007&title=Low%2Benergy%2Bdensity%2Band%2Bhigh%2Bnutritional%2Bquality%2Bare%2Beach%2Bassociated%2Bwith%2Bhigher%2Bdiet%2Bcosts%2Bin%2BFrench%2Badults&journal=Am+J+Clin+Nutr.&volume=86&pages=690-6)

- 56.





MaillotMFergusonELDrewnowskiADarmonN. Nutrient profiling can help identify foods of good nutritional quality for their price: a validation study with linear programming. _J Nutr._ (2008) 138:1107–13. 10.1093/jn/138.6.1107



  - [Pubmed Abstract](https://pubmed.ncbi.nlm.nih.gov/18492842)
  - [CrossRef](https://doi.org/10.1093/jn/138.6.1107)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=M.%2BMaillot&author=EL.%2BFerguson&author=A.%2BDrewnowski&author=N.%2BDarmon&publication_year=2008&title=Nutrient%2Bprofiling%2Bcan%2Bhelp%2Bidentify%2Bfoods%2Bof%2Bgood%2Bnutritional%2Bquality%2Bfor%2Btheir%2Bprice%3A%2Ba%2Bvalidation%2Bstudy%2Bwith%2Blinear%2Bprogramming&journal=J+Nutr.&volume=138&pages=1107-13)

- 57.





MaillotMDrewnowskiA. Energy allowances for solid fats and added sugars in nutritionally adequate U.S. diets estimated at 17–33% by a linear programming model. _J Nutr._ (2011) 141:333–40. 10.3945/jn.110.131920



  - [Pubmed Abstract](https://pubmed.ncbi.nlm.nih.gov/21178090)
  - [CrossRef](https://doi.org/10.3945/jn.110.131920)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=M.%2BMaillot&author=A.%2BDrewnowski&publication_year=2011&title=Energy%2Ballowances%2Bfor%2Bsolid%2Bfats%2Band%2Badded%2Bsugars%2Bin%2Bnutritionally%2Badequate%2BU.S.%2Bdiets%2Bestimated%2Bat%2B17%E2%80%9333%25%2Bby%2Ba%2Blinear%2Bprogramming%2Bmodel&journal=J+Nutr.&volume=141&pages=333-40)

- 58.





RaffenspergerJF. The least-cost low-carbohydrate diet is expensive. _Nutr Res._ (2008) 28:6–12. 10.1016/j.nutres.2007.10.002



  - [Pubmed Abstract](https://pubmed.ncbi.nlm.nih.gov/19083381)
  - [CrossRef](https://doi.org/10.1016/j.nutres.2007.10.002)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=JF.%2BRaffensperger&publication_year=2008&title=The%2Bleast-cost%2Blow-carbohydrate%2Bdiet%2Bis%2Bexpensive&journal=Nutr+Res.&volume=28&pages=6-12)

- 59.





CarlsonALinoMFungweT. _The Low-Cost, Moderate-Cost, and Liberal Food Plans, 2007 (CNPP-20)_. Washington DC: U.S. Department of Agriculture, Center for Nutrition Policy and Promotion (2007).



  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=A.%2BCarlson&author=M.%2BLino&author=T.%2BFungwe&publication_year=2007&journal=The+Low-Cost%2C+Moderate-Cost%2C+and+Liberal+Food+Plans%2C+2007+%28CNPP-20%29)

- 60.





VieuxFDarmonNTouaziDSolerLG. Greenhouse gas emissions of self-selected individual diets in France: changing the diet structure or consuming less? _Ecol Econ._ (2012) 75:91–101. 10.1016/j.ecolecon.2012.01.003



  - [CrossRef](https://doi.org/10.1016/j.ecolecon.2012.01.003)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=F.%2BVieux&author=N.%2BDarmon&author=D.%2BTouazi&author=LG.%2BSoler&publication_year=2012&title=Greenhouse%2Bgas%2Bemissions%2Bof%2Bself-selected%2Bindividual%2Bdiets%2Bin%2BFrance%3A%2Bchanging%2Bthe%2Bdiet%2Bstructure%2Bor%2Bconsuming%2Bless%3F&journal=Ecol+Econ.&volume=75&pages=91-101)

- 61.





VieuxFSolerL-GTouaziDDarmonN. High nutritional quality is not associated with low greenhouse gas emissions in self-selected diets of French adults. _Am J Clin Nutr_. (2013) 97:569–83. 10.3945/ajcn.112.035105



  - [Pubmed Abstract](https://pubmed.ncbi.nlm.nih.gov/23364012)
  - [CrossRef](https://doi.org/10.3945/ajcn.112.035105)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=F.%2BVieux&author=L-G.%2BSoler&author=D.%2BTouazi&author=N.%2BDarmon&publication_year=2013&title=High%2Bnutritional%2Bquality%2Bis%2Bnot%2Bassociated%2Bwith%2Blow%2Bgreenhouse%2Bgas%2Bemissions%2Bin%2Bself-selected%2Bdiets%2Bof%2BFrench%2Badults&journal=Am+J+Clin+Nutr&volume=97&pages=569-83)

- 62.





KramerGVan DoorenC. _Food Patterns and Dietary Recommendations in Spain, France and Sweden_. London: World Wildlife Fund (2012).



  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=G.%2BKramer&author=C.%2BVan%2BDooren&publication_year=2012&journal=Food+Patterns+and+Dietary+Recommendations+in+Spain%2C+France+and+Sweden)

- 63.





NelsonMEHammMWHuFBAbramsSAGriffinTS. Alignment of healthy dietary patterns and environmental sustainability: a systematic review. _Adv Nutr._ (2016) 7:1005–25. 10.3945/an.116.012567



  - [Pubmed Abstract](https://pubmed.ncbi.nlm.nih.gov/28140320)
  - [CrossRef](https://doi.org/10.3945/an.116.012567)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=ME.%2BNelson&author=MW.%2BHamm&author=FB.%2BHu&author=SA.%2BAbrams&author=TS.%2BGriffin&publication_year=2016&title=Alignment%2Bof%2Bhealthy%2Bdietary%2Bpatterns%2Band%2Benvironmental%2Bsustainability%3A%2Ba%2Bsystematic%2Breview&journal=Adv+Nutr.&volume=7&pages=1005-25)

- 64.





AuestadNFulgoniVL. What current literature tells us about sustainable diets: emerging research linking dietary patterns, environmental sustainability, and economics. _Adv Nutr._ (2015) 6:19–36. 10.3945/an.114.005694



  - [Pubmed Abstract](https://pubmed.ncbi.nlm.nih.gov/25593141)
  - [CrossRef](https://doi.org/10.3945/an.114.005694)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=N.%2BAuestad&author=VL.%2BFulgoni&publication_year=2015&title=What%2Bcurrent%2Bliterature%2Btells%2Bus%2Babout%2Bsustainable%2Bdiets%3A%2Bemerging%2Bresearch%2Blinking%2Bdietary%2Bpatterns%2C%2Benvironmental%2Bsustainability%2C%2Band%2Beconomics&journal=Adv+Nutr.&volume=6&pages=19-36)

- 65.





CarlsonALinoMGerriorSABasiotisPP. _The Low-Cost, Moderate-Cost, and Liberal Food Plans: 2003 Administrative Report. Contract No.: CNPP-13_. Center for Nutrition Policy and Promotion, U.S. Department of Agriculture (2003).



  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=A.%2BCarlson&author=M.%2BLino&author=SA.%2BGerrior&author=PP.%2BBasiotis&publication_year=2003&journal=The+Low-Cost%2C+Moderate-Cost%2C+and+Liberal+Food+Plans%3A+2003+Administrative+Report.+Contract+No.%3A+CNPP-13)

- 66.





VieuxFDarmonNTouaziDLGS. _Food Consumption and Greenhouse Gas Emissions: Changing Food Consumption Patterns or Consuming Less?_ FENS: Madrid (2011).



  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=F.%2BVieux&author=N.%2BDarmon&author=D.%2BTouazi&author=S.%2BLG&publication_year=2011&journal=Food+Consumption+and+Greenhouse+Gas+Emissions%3A+Changing+Food+Consumption+Patterns+or+Consuming+Less%3F)

- 67.





SrinivasanCSIrzXShankarB. An assessment of the potential consumption impacts of WHO dietary norms in OECD countries. _Food Policy_ (2006) 31:53–77. 10.1016/j.foodpol.2005.08.002



  - [CrossRef](https://doi.org/10.1016/j.foodpol.2005.08.002)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=CS.%2BSrinivasan&author=X.%2BIrz&author=B.%2BShankar&publication_year=2006&title=An%2Bassessment%2Bof%2Bthe%2Bpotential%2Bconsumption%2Bimpacts%2Bof%2BWHO%2Bdietary%2Bnorms%2Bin%2BOECD%2Bcountries&journal=Food+Policy&volume=31&pages=53-77)

- 68.





ParlesakATetensIDejgård JensenJSmedSGabrijelčičBlenkuš MRaynerMet al. Use of linear programming to develop cost-minimized nutritionally adequate health promoting food baskets. _PLoS ONE_ (2016) 11:e0163411. 10.1371/journal.pone.0163411



  - [Pubmed Abstract](https://pubmed.ncbi.nlm.nih.gov/27760131)
  - [CrossRef](https://doi.org/10.1371/journal.pone.0163411)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=A.%2BParlesak&author=I.%2BTetens&author=J.%2BDejg%C3%A5rd%2BJensen&author=S.%2BSmed&author=Blenku%C5%A1%2BM.%2BGabrijel%C4%8Di%C4%8D&author=M.%2BRayner&publication_year=2016&title=Use%2Bof%2Blinear%2Bprogramming%2Bto%2Bdevelop%2Bcost-minimized%2Bnutritionally%2Badequate%2Bhealth%2Bpromoting%2Bfood%2Bbaskets&journal=PLoS+ONE&volume=11)

- 69.





MaillotMIssaCVieuxFLaironDDarmonN. The shortest way to reach nutritional goals is to adopt Mediterranean food choices: evidence from computer-generated personalized diets. _Am J Clin Nutr._ (2011) 94:1127–37. 10.3945/ajcn.111.016501



  - [Pubmed Abstract](https://pubmed.ncbi.nlm.nih.gov/21900460)
  - [CrossRef](https://doi.org/10.3945/ajcn.111.016501)
  - [Google Scholar](http://scholar.google.com/scholar_lookup?author=M.%2BMaillot&author=C.%2BIssa&author=F.%2BVieux&author=D.%2BLairon&author=N.%2BDarmon&publication_year=2011&title=The%2Bshortest%2Bway%2Bto%2Breach%2Bnutritional%2Bgoals%2Bis%2Bto%2Badopt%2BMediterranean%2Bfood%2Bchoices%3A%2Bevidence%2Bfrom%2Bcomputer-generated%2Bpersonalized%2Bdiets&journal=Am+J+Clin+Nutr.&volume=94&pages=1127-37)

## Appendix

TABLE A1

| **Reference** | **Year** | **LP or QP** | **Constraints** | **Comments** |
| :-- | :-: | :-: | :-: | :-: |
|  |  |  | **Nutrients** | **Costs** | **Environment** | **Acceptability** |  |
| --- | --- | --- | :-: | :-: | :-: | :-: | --- |
| 50 | 2000 | LP | N |  |  | A | A corresponds to portion size |
| 11 | 2001 | LP | N |  |  | A | A corresponds to portion size |
| 29 | 2001 | LP | N |  |  | A | A corresponds to portion size |
| 42 | 2001 | LP | N |  |  |  |  |
| 34 | 2002 | LP | N |  |  | A | A corresponds to portion size |
| 51 | 2002 | QP | N | C |  | A | A corresponds to portion size |
| 3 | 2003 | Review |  |  |  |  |  |
| 52 | 2003 | LP | N | C |  | A | A corresponds to portion size |
| 65 | 2003 | QP | N |  |  | A | A corresponds to portion size |
| 44 | 2004 | LP | N |  |  | A | A corresponds to portion size |
| 54 | 2004 | LP | N | C |  |  |  |
| 31 | 2006 | QP | N |  |  | A | A corresponds to portion size |
| 45 | 2006 | LP | N | C |  | A | A corresponds to portion size |
| 53 | 2006 | LP | N | C |  |  |  |
| 55 | 2007 | LP |  |  |  |  | It does not perform optimization |
| 59 | 2007 | LP | N | C |  | A | A corresponds to portion size and the amount to be consumed |
| 32 | 2008 | QP | N |  |  |  |  |
| 46 | 2008 | LP | N | C |  |  |  |
| 56 | 2008 | LP | N |  |  | A | The author explicitly states that it includes nutrient (N) and acceptability restrictions (A) |
| 58 | 2008 | LP | N |  |  |  |  |
| 30 | 2009 | LP | N | C |  |  |  |
| 35 | 2009 | LP | N | C |  | A | A corresponds to the deviation from current consumption. And at least one of the 4 models developed includes cost constraints (C) |
| 38 | 2009 | LP | N |  |  |  |  |
| 40 | 2009 | LP | N |  |  | A | A corresponds to portion size |
| 43 | 2009 | LP | N |  |  | A |  |
| 4 | 2009 | LP | N |  |  | A |  |
| 47 | 2010 | LP | N |  |  |  |  |
| 16 | 2010 | LP | N |  | E |  |  |
| 33 | 2010 | LP | N | C |  |  |  |
| 39 | 2011 | LP | N | C |  |  | The author explicitly states that it includes cost restrictions (C) |
| 57 | 2011 | LP | N |  |  | A | A corresponds to the deviation from current consumption |
| 69 | 2011 | LP | N |  |  |  | It does not include acceptability in the restrictions |
| 17 | 2012 | LP | N |  |  |  |  |
| 36 | 2012 | LP | N |  |  | A | A corresponds to portion size |
| 49 | 2012 | LP | N | C |  |  |  |
| 41 | 2013 | LP | N |  |  |  |  |
| 19 | 2013 | LP | N | C | E |  |  |
| 18 | 2013 | LP |  |  |  |  | It was not possible to access |
| 9 | 2014 | LP | N |  |  | A | A corresponds to the deviation from current consumption |
| 48 | 2014 | LP | N |  |  |  | It does not include cost restrictions; it mentions that it can be included in the developed tool |
| 13 | 2014 | QP | N |  |  | A | A corresponds to the deviation from current consumption |
| 20 | 2015 | LP | N | C | E | A | A corresponds to the deviation from current consumption |
| 22 | 2015 | LP | N |  | E |  |  |
| 15 | 2016 | Review |  |  |  |  |  |
| 26 | 2016 | LP | N |  | E | A | A corresponds to the deviation from current consumption |
| 12 | 2016 | LP | N |  | E | A | A corresponds to the deviation from current consumption |
| 23 | 2016 | LP | N |  | E |  |  |
| 25 | 2016 | LP | N |  | E | A | A corresponds to the deviation from current consumption |
| 24 | 2016 | LP | N |  | E |  |  |
| 68 | 2016 | LP | N |  |  | A | Costs included in the objective function, not in the restrictions |
| 21 | 2016 | LP | N |  | E | A |  |

Short overview of the reviewed papers, year published, type of programming (linear or quadratic) and constraints used.

## Summary

Keywords

sustainable diet, linear programming, diet costs, nutritional quality, environmental constraints (EC)

Citation

van Dooren C (2018) A Review of the Use of Linear Programming to Optimize Diets, Nutritiously, Economically and Environmentally. _Front. Nutr._ 5:48. doi: [10.3389/fnut.2018.00048](http://dx.doi.org/10.3389/fnut.2018.00048)

Received

16 January 2018

Accepted

14 May 2018

Published

21 June 2018

Volume

5 - 2018

Edited by

Uma Tiwari, Institute of Technology, Sligo, Ireland

Reviewed by

Aida Turrini, Consiglio per la Ricerca in Agricoltura e l'Analisi dell'Economia Agraria (CREA), Italy; Marisa Porrini, Università degli Studi di Milano, Italy

Updates

![Crossmark icon](https://www.frontiersin.org/ap-2024/images/crossmark_color.webp)
Check for updates

Copyright

© 2018 van Dooren.

This is an open-access article distributed under the terms of the [Creative Commons Attribution License (CC BY)](http://creativecommons.org/licenses/by/4.0/). The use, distribution or reproduction in other forums is permitted, provided the original author(s) and the copyright owner are credited and that the original publication in this journal is cited, in accordance with accepted academic practice. No use, distribution or reproduction is permitted which does not comply with these terms.

**\*Correspondence:** Corné van Dooren [dooren@voedingscentrum.nl](mailto:dooren@voedingscentrum.nl)

This article was submitted to Nutrition and Environmental Sustainability, a section of the journal Frontiers in Nutrition

Disclaimer

All claims expressed in this article are solely those of the authors and do not necessarily represent those of their affiliated organizations, or those of the publisher, the editors and the reviewers. Any product that may be evaluated in this article or claim that may be made by its manufacturer is not guaranteed or endorsed by the publisher.

## Outline

## Figures

## Cite article

Copy to clipboard

Citation

Copy citation

Export citation file

- [BibTex](https://public-pages-files-2025.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/bibTex)
- [EndNote](https://public-pages-files-2025.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/endNote)
- [Reference Manager](https://public-pages-files-2025.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/reference)
- [Simple Text file](https://public-pages-files-2025.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2018.00048/text)

## Article metrics

Share on WeChat

Scan with WeChat to share this article