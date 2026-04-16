# Source: 02_stiglers_diet_problem_revisited_2001

- URL: https://mate.unipv.it/~gualandi/famo2conti/papers/stigler.pdf
- Slug: 02_stiglers_diet_problem_revisited_2001

---

This article was downloaded by: \[2.36.53.253\] On: 03 October 2015, At: 05:36 Publisher: Institute for Operations Research and the Management Sciences (INFORMS) INFORMS is located in Maryland, USA

# Operations Research

Publication details, including instructions for authors and subscription information: [http://pubsonline.informs.org](http://pubsonline.informs.org/)

# Stigler's Diet Problem Revisited

Susan Garner Garille, Saul I. Gass,

## To cite this article:

Susan Garner Garille, Saul I. Gass, (2001) Stigler's Diet Problem Revisited. Operations Research 49(1):1-13. http:// dx.doi.org/10.1287/opre.49.1.1.11187

## Full terms and conditions of use: [http://pubsonline.informs.org/page/terms-and-conditions](http://pubsonline.informs.org/page/terms-and-conditions)

This article may be used only for the purposes of research, teaching, and/or private study. Commercial use or systematic downloading (by robots or other automatic processes) is prohibited without explicit Publisher approval, unless otherwise noted. For more information, contact [permissions@informs.org](mailto:permissions@informs.org).

The Publisher does not warrant or guarantee the article’s accuracy, completeness, merchantability, fitness for a particular purpose, or non-infringement. Descriptions of, or references to, products or publications, or inclusion of an advertisement in this article, neither constitutes nor implies a guarantee, endorsement, or support of claims made of that product, publication, or service.

## © 2001 INFORMS

## Please scroll down for article—it is on subsequent pages

INFORMS is the largest professional society in the world for professionals in the fields of operations research, management science, and analytics. For more information on INFORMS, its publications, membership, or meetings visit [http://www.informs.org](http://www.informs.org/)

* * *

Downloaded from informs.org by \[2.36.53.253\] on 03 October 2015, at 05:36 . For personal use only, all rights reserved.

STIGLER’S DIET PROBLEM REVISITED

SUSAN GARNER GARILLE AND SAUL I. GASS

SUSAN GARNER GARILLE AND SAUL I. GASS
University of Maryland, College Park, Maryland 20742
[susan.garille@ey.com](mailto:susan.garille@ey.com) • [sgass@rhsmith.umd.edu](mailto:sgass@rhsmith.umd.edu)

(Received June 1999; revision received October 1999; accepted December 1999)

We review Stigler’s diet problem, its impact on linear programming and operations research, and we determine minimum cost diets using
updated nutritional and cost data. We also discuss how Stigler’s diet problem formulation and its extensions have, over the years, influenced
dietitians and nutritionists in their search for more wholesome but cost-effective diets.

n his book The Man Who Ate Everything, Jeffrey
ISteingarten (1998), the food editor for Vogue magazine,
notes (p. 33):

notes (p. 33):
Years ago I read somewhere that the absolutely
cheapest survival diet consists of peanut butter, whole wheat bread, nonfat dry milk and a
vitamin pill.

into something palatable?” he states (p. 43):
The problem looked like child’s play. All I needed
was a list of all foods, five thousand or ten thousand
of them; nutritional information about each food and
its cost; a personal computer with a statistics program installed; and somebody to type the first two
things into the third. The mathematical problem is
generally referred to as linear programming, and the
routine commonly used to solve it is the Simplex
Method, which somebody once tried to teach me in
graduate school long, long ago (emphasis added).
You simply ask the computer to choose a group
of foods that collectively satisfy your list of nutritional requirements while absolutely minimizing the
overall cost. It’s like the simultaneous equations we
learned to solve in high school, but much more complicated. Yet with a personal computer, the whole
problem should take just a few minutes to solve. I
planned to patent the answer as the Simplex Subsis-
Downloaded from informs.org by \[2.36.53.253\] on 03 October 2015, at 05:36 . For personal use only, all rights reserved. tence Diet.

pre-linear programming times, used a set of simultaneous
(9 × 77) linear inequalities (greater than or equal to) to
find a low-cost diet that met nutrient and caloric requirements. In this paper, we review Stigler’s diet problem, its
impact on linear programming and operations research, and
we determine minimum cost diets using updated nutritional
and cost data. We also discuss how Stigler’s diet problem
formulation and its extensions have, over the years, influenced dietitians and nutritionists in their search for more
wholesome but cost-effective diets.

1.0. STIGLER’S DIET PROBLEM

1.0. STIGLER’S DIET PROBLEM
Stigler posed the following problem: For a moderately
active man (economist) weighing 154 pounds, how much of
each of 77 foods should be eaten on a daily basis so that the
man’s intake of nine nutrients (including calories) will be at
least equal to the recommended dietary allowances (RDAs)
suggested by the National Research Council in 1943, with
the cost of the diet being minimal? RDAs “!!! are the levels of intake of essential nutrients that, on the basis of scientific knowledge, are judged by the Food and Nutrition
board to be adequate to meet the known nutrient needs of
practically all healthy persons” (National Research Council 1989). Stigler’s RDAs of interest were calories, protein,
calcium, iron, vitamin A, thiamine, riboflavin, niacin, and
ascorbic acid. Table 1 lists the values of these RDAs for
the man in question. Stigler obtained the nutrient content
of his 77 foods from a 1940 U.S. Department of Agricul-
Downloaded from informs.org by \[2.36.53.253\] on 03 October 2015, at 05:36 . For personal use only, all rights reserved. ture (USDA) publication as well as from a privately printed
1944 book (Chatfield and Adams 1940, Bowes and Church
1944). Stigler (1945, p. 308) commented on “!!! the tentativeness of these figures,” and lamented “!!! the almost
infinite complexity of a refined and accurate assessment of
nutritive value of a diet.”

Subject classifications: Agriculture/food: human diet. Linear programming.
Area of review: OR chronicle.

Area of review: OR chronicle.
0030-364X/01/4901-0001 $05.00
1526-5463 electronic ISSN

* * *

Downloaded from informs.org by \[2.36.53.253\] on 03 October 2015, at 05:36 . For personal use only, all rights reserved.

2/Garille and Gass
Table 1. 1943 RDAs for a moderately active 154-pound
man.

| Nutrient | RDA |
| --- | --- |
| Calories | 3000 kcalories |
| Protein | 70 grams |
| Calcium | 0.8 grams |
| Iron | 12 milligrams |
| Vitamin A | 5000 IU |
| Thiamine(Vitamin B1) | 1.8 milligrams |
| Riboflavin(Vitamin B2) | 2.7 milligrams |
| Niacin | 18 milligrams |
| Ascorbic Acid(Vitamin C) | 75 milligrams |

$$
\\mathrm {B} \_ {1})
$$

$$
\\mathrm {B} \_ {2})
$$

The basic linear-programming diet problem model is
given by Min cX, subject to AX ≥ b, X ≥ 0, where c is a
vector of prices for the foods X, each column of the matrix
A contains the nutrient content of the corresponding food,
and the vector b is the set of lower bounds for the RDAs.
Stigler’s limit of 77 foods was because of the need for associated price data, and such data were available for these
more or less representative foods for both 1939 and 1945.
As Stigler (1945, p. 309) commented, “It is beyond question that with a fuller list the minimum cost of meeting the
National Research Council’s allowances could be reduced,
possibly by a substantial amount.” The food prices, collected by the Bureau of Labor Statistics, were averages
across many large cities. Stigler’s “minimum” cost diets,
using average prices gathered in August of each year, are
given in Table 2. Note that total costs are annual costs and
the food quantities are for the full year (to be divided into
365.25 days). Much has been said about the inadequacy of
Stigler’s minimal subsistence diets in terms of palatability,
variety, and overall adequacy. From an operations research
perspective, Stigler’s diet problem is a prime example of
an OR model that faithfully describes the real-world situation but whose solution validity is close to zero. As Stigler
(1945, p. 312) cautioned, “No one recommends these diets
for anyone, let alone everyone.” Also, Lancaster (1992,
p. 61) in her article describing the evolution of the diet
model into the more acceptable menu-planning approach,

$$
A X \\geq b, X \\geq 0
$$

|  | August 1939 |  | August 1945 |  |
| --- | --- | --- | --- | --- |
| Food | Annual Quantity | Annual Cost | Annual Quantity | Annual Cost |
| Wheat Flour | 370 lb. | $13.33 | 535 lb. | $34.43 |
| Evaporated Milk | 57 cans | 3.84 | — | — |
| Cabbage | 111 lb. | 4.11 | 107 lb. | 5.23 |
| Spinach | 23 lb. | 1.85 | 13 lb. | 1.56 |
| Dried Navy Beans | 285 lb. | 16.80 | — | — |
| Pancake Flour | — | — | 134 lb. | 13.08 |
| Beef Liver | — | — | 25 lb. | 5.48 |
| Total Annual Cost |  | $39.93 |  | $59.88 |
| Total Daily Cost |  | $0.109 |  | $0.135 |

observed, “The solution to the least-cost diet is the equivalent of the human dog biscuit.” Credit must be given to
the diet problem, however, in that it was the precursor of a
wide variety of successful linear-programming applications
dealing with cattle and chicken feed, fertilizer, and general
ingredient mix problems. As we shall see, the concept of a
minimum cost diet for humans does serve as a baseline for
governmental funding and school lunch planning.

governmental funding and school lunch planning.
Stigler used trial and error, and mathematical insight and
agility to solve his (9 × 77) set of inequalities. Based on
cost and nutrient content, he was able to “weed” the original 77 foods down to 15 as the eliminated foods were
dominated by those in the list of 15. (The 15 foods had
no meat except beef liver and excluded all sugars, beverages, and patented cereals.) Stigler’s diet for 1939 data
cost $39.93 per year (daily cost of $0.1093) and included
varying amounts of wheat flour, evaporated milk, cabbage,
spinach, and dried navy beans (Stigler 1945). Stigler’s 1939
diet problem was the first “large-scale” problem that was
solved using the simplex method (Dantzig 1963, 1990).
In 1947, nine clerks, using hand-operated desk calculators, pivoted away for 120 clerk-days and found the linearprogramming (LP) minimum cost of $39.69 (daily cost of
$0.1087). Stigler knew what he was doing! The LP solution
foods were from Stigler’s reduced list and were the same
except that a small amount of beef liver in the LP solution
caused 57 cans of evaporated milk to disappear. These solutions had excesses (surplus) in niacin, thiamine, protein,
and iron. If no excesses are allowed (equality constrained
problem), the yearly cost increases to $49.40 (daily cost
of $0.1352) and includes varying amounts of wheat flour,
cornmeal, evaporated milk, peanut butter, lard, beef liver,
cabbage, potatoes, spinach, and dried navy beans (corn
meal, peanut butter, and lard were not in Stigler’s reduced
list of foods). These nine foods represent an optimal basic
feasible solution to the (9 × 77) equality system (Dantzig
1963). Adjusted for inflation to April 1998, the cost of the
1939 LP diet increases from $39.69 to $466.69. Table 3
contrasts the Stigler and the LP solutions for 1939.

2.0. RELATED DIET PROBLEM FORMULATIONS

* * *

Downloaded from informs.org by \[2.36.53.253\] on 03 October 2015, at 05:36 . For personal use only, all rights reserved.

Table 3. Stigler and linear programming annual diets, August 1939.

|  | Stigler一1939 |  | LP Simplex-Excess |  | LP Simplex-No Excess |  |
| --- | --- | --- | --- | --- | --- | --- |
| Food | Annual Quantity | Annual Cost | Annual Quantity | Annual Cost | Annual Quantity | Annual Cost |
| Wheat Flour | 370 lb. | $13.33 | 299 lb. | $10.78 | 184 lb. | $6.62 |
| Evaporated Milk | 57 cans | 3.84 | - | - | 246 cans | 16.48 |
| Cabbage | 111 lb. | 4.11 | 111 lb. | 4.10 | 91.1 lb. | 3.37 |
| Spinach | 23 lb. | 1.85 | 23 lb. | 1.83 | 2.96 lb. | 0.24 |
| Dried Navy Beans | 285 lb. | 16.80 | 378 lb. | 22.29 | - | - |
| Beef Liver | - | - | 2.57 lb. | 0.69 | 20.8 lb. | 5.57 |
| Peanut Butter | - | - | - | - | 0.67 lb. | 0.12 |
| Corn Meal | - | - | - | - | 135 lb. | 6.21 |
| Lard | - | - | - | - | 90.9 lb. | 8.91 |
| Potatoes | - | - | - | - | 82.9 lb. | 1.88 |
| Total Annual Cost(1939 $) |  | $39.93 |  | $39.69 |  | $49.40 |
| Total Daily Cost(1939 $) |  | $0.1093 |  | $0.1087 |  | $0.1352 |
| Total Daily Cost(1998 $) |  | $1.285 |  | $1.278 |  | $1.590 |

3.0. STIGLER’S DIET PROBLEM REVISITED

to $745.13 per person per year for April 1998).
Beckmann (1960) reported on a model and solution using
the same nine nutrients as Stigler, but with RDA values
updated to 1958. He used a different set of foods and different sources for their nutrient content, with food prices

ferent sources for their nutrient content, with food prices
as found in Providence, Rhode Island in the fall of 1959
(Beckmann was at Brown University). He solved two problems, both for a 45-year-old male, one at the 3000-calorie
level and the other for 2200 calories. The optimal 3000-
calorie Beckmann diet included soybean meal, beef liver,
lard, and frozen orange juice and had a daily cost of $0.216
per day or an annual cost of $78.99 (adjusted to $440.46
for April 1998).
Downloaded from informs.org by \[2.36.53.253\] on 03 October 2015, at 05:36 . For personal use only, all rights reserved.

ferent sources for their nutrient content, with food prices
as found in Providence, Rhode Island in the fall of 1959
(Beckmann was at Brown University). He solved two problems, both for a 45-year-old male, one at the 3000-calorie
level and the other for 2200 calories. The optimal 3000-
calorie Beckmann diet included soybean meal, beef liver,
lard, and frozen orange juice and had a daily cost of $0.216
per day or an annual cost of $78.99 (adjusted to $440.46
Downloaded from informs.org by \[2.36.53.253\] on 03 October 2015, at 05:36 . For personal use only, all rights reserved.

Since 1939, the National Research Council has extended
the number of nutrients that should be included as RDAs
when determining a diet. We used these RDAs in developing a set of extended Stigler diet problems that include the
full set of RDAs and the updated values of the prices and
nutrient content of the 77 foods. For the extended problems,
we set upper bounds for those nutrients that are known to
be toxic or undesirable above certain levels. The extended
set of RDAs is given in Table 4. Further, although not incorporated into the diet constraints, we did check the result-

Table 4. 1989 RDAs (tci = total calcium intake).

| Nutrient | RDA25-50 Years Old |  | Upper Bound |
| --- | --- | --- | --- |
| Male | Female |  |  |
| Calories(kcal) | 2,900 | 2,200 |  |
| Protein(g) | 6.3 | 50 | 126 |
| Calcium(g) | 0.8 | 0.8 | 2.5 |
| Iron(mg) | 10 | 15 | 19,750 |
| VitaminA(μgRE) | 1,000 | 800 | 15,000 |
| Thiamine(mg)(VitaminB1) | 1.5 | 1.1 |  |
| Riboflavin(mg)(VitaminB2) | 1.7 | 1.3 |  |
| Niacin(mg) | 19 | 15 | 10,000 |
| Ascorbic Acid(mg)(VitaminC) | 60 | 60 |  |
| VitaminD(IU) | 200 | 200 | 1000 |
| VitaminE(mg-α-RE) | 10 | 8 |  |
| VitaminK(μg) | 80 | 65 |  |
| VitaminB6(mg) | 2 | 1.6 | 209 |
| Folate(μg) | 200 | 180 | 20,000 |
| VitaminB12(μg) | 2 | 2 |  |
| Phosphorous(mg) | 800 | 800 | 2×tci |
| Magnesium(mg) | 350 | 280 |  |
| Zinc(mg) | 15 | 12 | 15 |
| Iodine(μg) | 150 | 150 |  |
| Selenium(μg) | 70 | 55 | 5,000 |

$$
(\\mu \\mathrm {g} \\mathrm {R E})
$$

$$
\\mathrm {B} \_ {1})
$$

$$
\\mathrm {B} \_ {2})
$$

$$
\\mathrm {B} \_ {6} (\\mathrm {m g})
$$

$$
\\mathrm {n B} \_ {1 2} (\\mu \\mathrm {g})
$$

* * *

Downloaded from informs.org by \[2.36.53.253\] on 03 October 2015, at 05:36 . For personal use only, all rights reserved.

4/Garille and Gass
ing diets to see if they meet the minimum and maximum
bounds of other nutrients of interest as well as the bounds
for dietary concerns such as cholesterol. These items and
their values are shown in Table 5 (National Research Council 1989).

cil 1989).
Stigler’s RDAs were for an active 154-pound man,
assumed from his article to be Stigler himself. The NRC
RDAs are given for different sex and age groups, with
median heights and weights for each group. Today’s 154-
pound man would fall into the 15–18-year-old or 19–24-
year-old age group. Stigler, who was born in 1911, would
have been 33 years old at the time he did his study in
1944–1945. We decided to use the RDAs for a 25–50-yearold-man, although this age group has the median weight of
174 pounds. This weight is a bit higher than Stigler’s male,
but we believe that it was his intention to pick an average
male for his diet, and the 25–50-year-old group best fits
that objective. We also solved the updated diet problem for
a women in the 25–50-year-old age group. In both cases,
we use calorie requirements for a light to moderately active
man or woman. Here “light” activity includes “!!! walking
on a level surface 2.5 to 3 miles per hour, garage work,
electrical trades, carpentry, restaurant trades, house cleaning, child care, golfing, sailing, and table tennis”; “moderate” activity includes “!!! walking 3.5 to 4 mph, weeding
and hoeing, carrying a load, cycling, tennis, and dancing”
(National Research Council 1989). The average OR man or
woman is, we believe, included in these definitions.

woman is, we believe, included in these definitions.
Our ability to measure accurately the nutrient content
of foods has improved greatly since the mid 1940s. Further, we now find that many foods are fortified (e.g., corn
flakes, one of Stigler’s foods). The new nutrient content for
the updated problems was taken from Pennington (1998),
which is the 17th edition of one of the sources used by
Stigler. Most of the data used are cited as coming from the
current U.S. Department of Agriculture handbooks, while
some—like corn flakes and peanut butter—came from food
companies and trade associations. In an attempt to make the
problem more realistic, we used nutritive content of foods
in the form they would most likely be eaten; for example,

| Nutrient | Lower Bound | Upper Bound |
| --- | --- | --- |
| Pantothenic Acid | 4mg |  |
| Sodium | 500mg |  |
| Potassium | 2,000mg | 18,000mg |
| Copper | 1.5mg |  |
| Manganese | 2mg | 5mg |
| Fat |  | 0.3×TCI |
| Saturated Fatty Acids |  | 0.1×TCI |
| Carbohydrates | 0.125×TCI |  |
| Polyunsaturated Fatty Acids | 0.07×TCI | 0.1×TCI |
| Dietary Fiber | 12g |  |
| Cholesterol |  | 0.125×TCI |

$$
0\. 3 \\times \\mathrm {T C I}
$$

$$
0\. 1 \\times \\mathrm {T C I}
$$

$$
0\. 1 2 5 \\times \\mathrm {T C I}
$$

$$
0\. 1 \\times \\mathrm {T C I}
$$

$$
0\. 0 7 \\times \\mathrm {T C I}
$$

$$
0\. 1 2 5 \\times \\mathrm {T C I}
$$

cooked rice instead of raw rice, the latter being used by
Stigler.

Stigler.
The 77 foods that Stigler included in his diet were all
included in the commodity list for which the Bureau of
Labor Statistics (BLS) collected retail price information.
Our hope was that the BLS would still be collecting prices
for the Stigler list. However, the current BLS list includes
around 30 of the 77 foods, with the list changing depending
on what foods are included in the Consumer Price Index.
To be consistent with respect to time and place, and upon
the recommendation of a USDA economist, we fell back
on the strategy used by Smith and Beckmann: We determined prices from the Giant Foods supermarket chain in
the Washington, DC area for April 1998.

The 77 foods that Stigler included in his diet were all
included in the commodity list for which the Bureau of
Labor Statistics (BLS) collected retail price information.
Our hope was that the BLS would still be collecting prices
for the Stigler list. However, the current BLS list includes
around 30 of the 77 foods, with the list changing depending
on what foods are included in the Consumer Price Index.
To be consistent with respect to time and place, and upon
the recommendation of a USDA economist, we fell back
on the strategy used by Smith and Beckmann: We determined prices from the Giant Foods supermarket chain in
the Washington, DC area for April 1998.

mined prices from the Giant Foods supermarket chain in
the Washington, DC area for April 1998.
There were problems with trying to make an exact match
between Stigler’s foods and the current listing of foods.
Stigler’s list came from the BLS publication Retail Prices
of Foods, 1923–1936, which includes average price quotations of 51 large cities in 1939 and 56 cities in 1944. It
proved difficult to exactly match the foods in the old BLS
list and those cited in the new Pennington list. Again, in our
attempt to be more realistic than Stigler, where Stigler had
raw eggs, we had to decide between some form of a cooked
egg, e.g., fried, hard-boiled, scrambled. In such cases, we
chose the one that was “healthier” or easier to prepare.
Our resulting list of 77 foods then had to be matched with
the foods available at the Giant. If the food selected from
Pennington was a brand name, we priced it accordingly.
Otherwise, we chose the least expensive brand in the least
expensive form. Our pricing task was somewhat relieved as
the Giant posts prices per measured unit. A listing showing
the food matches between Stigler, Pennington, and Giant
is given in Appendix A. In essence, a food Stigler matched
to a food in Pennington for its nutrient content was in turn
matched to a Giant food for its price.

4.0. SOLUTIONS TO THE UPDATED AND
EXTENDED STIGLER’S DIET PROBLEMS

scratch, we would attempt
ous flaws faced and described by both Stigler (1945) and
Dantzig (1963, 1990). First, the new list of foods would be
more extensive. There are many inexpensive, nutrient-rich
foods that could be included. Also, Stigler’s list includes
foods that are uncommon in the kitchens of the 1990s, e.g.,
lard, Crisco. Certainly, one would now favor vegetable oil
or olive oil. Second, it was recognized from the start that
nutrient consumption and nutrient usage may not be linear
for all, if any, nutrients. The Stigler diet model assumes
that there are no interactions between foods nor interactions between nutrients. That is, the quantity of a nutrient
Downloaded from informs.org by \[2.36.53.253\] on 03 October 2015, at 05:36 . For personal use only, all rights reserved. consumed by eating a specified amount of a certain food is
exactly the quantity of that nutrient that will be used by the
body. This is the basic assumption that allows us to cast the
diet problem as a linear-programming problem. We know
of no other diet evaluation process that does otherwise.

attempt to repair some of the obvious flaws faced and described by both Stigler (1945) and
Dantzig (1963, 1990). First, the new list of foods would be
more extensive. There are many inexpensive, nutrient-rich
foods that could be included. Also, Stigler’s list includes
foods that are uncommon in the kitchens of the 1990s, e.g.,
lard, Crisco. Certainly, one would now favor vegetable oil
or olive oil. Second, it was recognized from the start that
nutrient consumption and nutrient usage may not be linear
for all, if any, nutrients. The Stigler diet model assumes
that there are no interactions between foods nor interactions between nutrients. That is, the quantity of a nutrient
Downloaded from informs.org by \[2.36.53.253\] on 03 October 2015, at 05:36 . For personal use only, all rights reserved. consumed by eating a specified amount of a certain food is
exactly the quantity of that nutrient that will be used by the
body. This is the basic assumption that allows us to cast the
diet problem as a linear-programming problem. We know
of no other diet evaluation process that does otherwise.

of no other diet evaluation process that does otherwise.

EXTENDED STIGLER’S DIET PROBLEMS
As the new data sets were entered into spreadsheets, it
was convenient to use the linear-programming spreadsheet

* * *

Downloaded from informs.org by \[2.36.53.253\] on 03 October 2015, at 05:36 . For personal use only, all rights reserved.

$$
\\mathrm {M i n} X
$$

Min X
subject to d ≤ AX ≤ b$

$$
d \\leq A X \\leq b,
$$

$$
X \\geq 0,
$$

X ≥ 0$
where d is a vector of nutrient RDA lower bounds and b
is a vector of nutrient RDA upper bounds. As the entries
(aij) of matrix A contain the number of grams per dollar
for nutrient i in food j, the variables X = %xj& are then
the dollar values of food j to buy. The objective function is then just the minimization of the total sum of the
food purchases. We solved diet problems for five different
sets of data: (1) updated Stigler’s problem for a 25–50-
year-old man and (2) for a 25–50-year-old woman; (3) the
extended Stigler problem where we incorporate constraints
for all of the current RDAs for a 25–50-year-old man and
(4) 25–50-year-old woman; and (5) Stigler’s problem using
current RDAs and food nutrient contents, but with 1939
food prices. Also, for each of these problems, we solved
for a minimum cost diet where no excess nutrients were
allowed. Recall that we use 365.25 days in a year to compute the annual costs. We next discuss the solution to each
problem.

$$
X = \\left(x \_ {i}\\right)
$$

$$
j,
$$

$$
\\left(a \_ {i j}\\right)
$$

Garille and Gass / 5
within the upper bounds; while in the last two solutions,
we allow no excess nutrients, that is, the lower bounds are
met exactly.

Updated Stigler’s Diet Problem
Here we give the optimal solution diets using the nutrients considered by Stigler but current data for RDAs, food
prices, and food nutrient content. Lower bounds were used
for the following nutrients: calories, protein, vitamin A,
vitamin C, thiamine, riboflavin, niacin, calcium, and iron.
Upper bounds were used for the following nutrients: protein, vitamin A, niacin, calcium, and iron. In the first two
solutions described below, we allow for excess nutrients

Updated Stigler’s Diet Problem

$$
\\mathrm {B} \_ {6},
$$

$$
\\mathrm {B} \_ {1 2},
$$

25–50-year-old man (excess nutrients). The optimal
solution diet for a 25–50-year-old man has an annual cost
of $412.26 ($1.13 daily). Each day it consists of 5.68 cups
of wheat flour, 17.5 fluid ounces of milk, 0.710 of an
orange, and 0.335 of a carrot. The annual costs are shown in
Table 6 and the corresponding annual quantities are shown
in Table 7. For the extended set of 1989 RDAs (Table 4)
and suggested 1989 nutrient intakes (Table 5), the following minimum requirements are not satisfied by this diet:
polyunsaturated fatty acids, vitamin B , vitamin B6 12, pantothenic acid, sodium, potassium, magnesium, zinc, copper,
iodine, vitamin E, and vitamin K. No upper limits were
exceeded. This diet provides servings (or portions of servings) from the following food groups established by the
USDA: milk group (milk), vegetable group (carrots), fruit
group (oranges), grain product group (wheat flour). Of the
foods in this diet, only wheat flour is common with Stigler’s
reduced list of foods.

25–50-year-old woman (excess nutrients). The optimal
solution diet for a 25–50-year-old woman has an annual
cost of $354.05 ($0.97 daily). Each day it consists of 4.12
cups of wheat flour, 18.3 fluid ounces of milk, 0.718 of
an orange, and 0.229 of a carrot. The annual costs are
shown in Table 6 and the corresponding annual quantities
are shown in Table 7. The following minimum requirements
are not satisfied with this diet: polyunsaturated fatty acids,
vitamin B6, sodium, potassium, magnesium, zinc, copper,
iodine, vitamin E, and vitamin K. No upper limits were
exceeded. This diet provides servings (or portions of servings) from the following food groups established by the
USDA: milk group (milk), vegetable group (carrots), fruit
group (oranges), grain product group (wheat flour). Of the

Table 6. Optimal updated and extended excess diets: annual costs (April 1998 prices).

|  | Stigler Update |  | Extended Stigler |  |
| --- | --- | --- | --- | --- |
|  | 25-50-Year-Old | 25-50-Year-Old | 25-50-Year-Old | 25-50-Year-Old |
| Food | Male | Female | Male | Female |
| Wheat Flour | $228.53 | $165.72 | $52.93 | $45.33 |
| Rolled Oats | - | - | $50.69 | $62.00 |
| Milk | $138.52 | $145.20 | $126.81 | $132.03 |
| Peanut Butter | - | - | $123.38 | $105.86 |
| Lard | - | - | $83.06 | $29.57 |
| Beef Liver | - | - | $0.50 | $0.33 |
| Bananas | - | - | $95.82 | $64.84 |
| Oranges | $37.47 | $37.84 | $4.34 | $12.35 |
| Cabbage | - | - | $19.94 | $15.82 |
| Carrots | $7.74 | $5.29 | $7.25 | $5.05 |
| Potatoes | - | - | $31.44 | $31.27 |
| Pork and Beans | - | - | $55.11 | $30.82 |
| Total Cost(Annual) | $412.26 | $354.05 | $651.27 | $535.27 |
| Total Cost(Daily) | $1.1287 | $0.9694 | $1.7831 | $1.4655 |

RIGHTSLINK
Camarillo Clearness Center

$$
\\mathrm {B} \_ {6}
$$

* * *

Downloaded from informs.org by \[2.36.53.253\] on 03 October 2015, at 05:36 . For personal use only, all rights reserved.

6/Garille and Gass
Table 7. Optimal updated and extended excess diets: annual quantities.

|  | Stigler Update |  | Extended Stigler |  |
| --- | --- | --- | --- | --- |
| Food | 25-50-Year-Old Male | 25-50-Year-Old Female | 25-50-Year-Old Male | 25-50-year-Old Female |
| Wheat Flour (lb.) | 571 | 414 | 132 | 113 |
| Rolled Oats (lb.) | - | - | 85.9 | 105 |
| Milk (qt.) | 198 | 207 | 181 | 189 |
| Peanut Butter (lb.) | - | - | 49.8 | 42.7 |
| Lard (lb.) | - | - | 76.2 | 27.1 |
| Beef Liver (lb.) | - | - | 0.251 | 0.166 |
| Bananas (lb.) | - | - | 162 | 110 |
| Oranges (lb.) | 74.9 | 75.7 | 8.68 | 24.7 |
| Cabbage (lb.) | - | - | 39.9 | 31.6 |
| Carrots (lb.) | 19.4 | 13.3 | 18.2 | 12.7 |
| Potatoes (lb.) | - | - | 62.9 | 62.5 |
| Pork and Beans (lb.) | - | - | 108 | 60.4 |

foods in this diet, only wheat flour is common with Stigler’s
reduced list of foods.

vitamin A, vitamin C, thiamine, riboflavin, niacin, calcium,
and iron.
25–50-year-old man (no excess nutrients). The optimal
solution diet has an annual cost of $522.30 ($1.43 daily).
The diet consists of wheat flour, milk, peanut butter, lard,
bacon, roasting chicken, oranges, carrots, and molasses.
The annual costs and quantities are shown in Table 8.
The following minimum requirements are not satisfied with
this diet: carbohydrates, polyunsaturated fatty acids, dietary
fiber, vitamin B6, pantothenic acid, zinc, copper, manganese, iodine, selenium, vitamin E, and vitamin K. No
requirements are exceeded. This diet provides servings (or
portions of servings) from all six of the food groups established by the USDA: fats, oils, and sweets group (peanut

$$
\\mathrm {B} \_ {6},
$$

butter, lard, molasses), milk group (milk), meats and beans
group (bacon, roasting chicken), vegetable group (carrots),
fruit group (oranges), grain product group (wheat flour).
Of the foods in this diet, only wheat flour is common with
Stigler’s reduced list of foods.

group (oranges), grain product group (wheat flour). Of the
Table 8. Optimal updated no excess diets (April 1998 prices).

25–50-year-old woman (no excess nutrients). The optimal solution diet has an annual cost of $461.72 ($1.26
daily). The diet consists of wheat flour, milk, beef liver,
roasting chicken, oranges, carrots, pork and beans, sugar,
and molasses. The annual costs and quantities are shown
in Table 8. The requirements for the following nutrients are not met by this diet: polyunsaturated fatty acids,
dietary fiber, vitamin B6, vitamin B12, folate, phosphorus,
zinc, copper, iodine, selenium, vitamin D, vitamin E, and
vitamin K. This diet provides servings (or portions of servings) from all six of the food groups established by the
USDA: fats, oils, and sweets group (sugar, molasses), milk
group (milk), meats and beans group (beef liver, roasting
chicken, pork and beans), vegetable group (carrots), fruit
group (oranges), grain product group (wheat flour). Of the

$$
\\mathrm {B} \_ {1 2}
$$

|  | 20-50-Year-Old Male |  | 25-50-Year-Old Female |  |
| --- | --- | --- | --- | --- |
| Food | Annual Quantity | Annual Cost | Annual Quantity | Annual Cost |
| Wheat Flour | 99.2 lb. | $39.69 | 71.3 lb. | $28.50 |
| Milk | 190 qt. | $133.03 | 127 qt. | $88.94 |
| Peanut Butter | 13.4 lb. | $33.18 | - | - |
| Lard | 143 lb. | $155.45 | - | - |
| Beef Liver | - | - | 0.43 lb. | $0.85 |
| Bacon | 16.7 lb. | $16.52 | - | - |
| Roasting Chicken | 72.7 lb. | $57.42 | 78.5 lb. | $61.99 |
| Oranges | 75.2 lb. | $37.62 | 73.6 lb. | $36.82 |
| Carrots | 19.1 lb. | $7.62 | 14.2 lb. | $5.66 |
| Pork and Beans | - | - | 76.4 lb. | $38.96 |
| Sugar | - | - | 210 lb. | $92.43 |
| Molasses | 14.0 qt. | $41.77 | 36.1 qt. | $107.57 |
| Total Cost(Annual) |  | $522.30 |  | $461.72 |
| Total Cost(Daily) |  | $1.4300 |  | $1.2641 |

$$
\\mathrm {B} \_ {6}
$$

* * *

Downloaded from informs.org by \[2.36.53.253\] on 03 October 2015, at 05:36 . For personal use only, all rights reserved.

Extended Stigler’s Diet Problem

Extended Stigler’s Diet Problem
This problem uses current
and food nutrient content with more nutrients than Stigler
considered. Lower bounds were incorporated for the following nutrients: calories, protein, vitamin A, vitamin D,
vitamin E, vitamin K, vitamin C, thiamin, riboflavin, niacin,
vitamin B6, folate, vitamin B12
nesium, iron, zinc, iodine, and selenium. In addition, upper

Extended Stigler’s Diet Problem
current data for RDAs, food prices,
and food nutrient content with more nutrients than Stigler
considered. Lower bounds were incorporated for the following nutrients: calories, protein, vitamin A, vitamin D,
vitamin E, vitamin K, vitamin C, thiamin, riboflavin, niacin,
, folate, vitamin B12, calcium, phosphorus, magnesium, iron, zinc, iodine, and selenium. In addition, upper

nesium, iron, zinc, iodine, and selenium. In addition, upper
bounds were formulated for the following nutrients: protein, vitamin A, vitamin D, niacin, vitamin B6, folate, calcium, phosphorus, iron, zinc, and selenium. The resultant
linear-programming model has 31 constraints and 77 foods.

$$
\\mathrm {B} \_ {1 2}
$$

$$
\\mathrm {B} \_ {6};
$$

linear-programming model has 31 constraints and 77 foods.
25–50-year-old man (extended). The optimal solution
diet has an annual cost of $651.27 ($1.78 daily). Each
day it consists of: 1.31 cups of wheat flour, 1.32 cups of
rolled oats, 16.0 fluid ounces of milk, 3.86 tablespoons of
peanut butter, 7.28 tablespoons of lard, 0.0108 ounces of
beef liver, 1.77 bananas, 0.0824 of an orange, 0.707 cup
of shredded cabbage, 0.314 of a carrot, 0.387 of a potato,
and 0.530 cup of pork and beans. The annual costs are
shown in Table 6 and the corresponding annual quantities
are shown in Table 7. The following minimum requirements
are not satisfied with this diet: carbohydrates, polyunsaturated fatty acids, and copper. The upper limit for manganese
was exceeded. This diet provides servings (or portions of
servings) from all of the six food groups established by the
USDA: fats, oils, and sweets group (peanut butter, lard),
milk group (milk), meats and beans group (beef liver, pork
and beans), vegetables group (cabbage, carrots, potato),
fruit group (bananas, oranges), grain product group (wheat
flour, rolled oats). The following foods from this diet are
common with Stigler’s diet reduced list: wheat flour, beef
liver, cabbage, and potatoes.

liver, cabbage, and potatoes.
25–50-year-old woman
tion diet has an annual
Each day it consists of:
cups of rolled oats, 1.67 fluid ounces of milk, 3.31 tablespoons of peanut butter, 2.59 tablespoons of lard, 0.00724
ounces of beef liver, 1.20 bananas, 0.234 of an orange,
0.561 cup of shredded cabbage, 0.219 of a carrot, 0.384
of a potato, and 0.297 cup of pork and beans. The annual
costs are shown in Table 6 and the corresponding annual
Downloaded from informs.org by \[2.36.53.253\] on 03 October 2015, at 05:36 . For personal use only, all rights reserved.
quantities are shown in Table 7. The following minimum
requirements are not satisfied with this diet: polyunsaturated fatty acids and copper. The upper limit for manganese
was exceeded. This diet provides servings (or portions of
servings) from all of the six food groups established by the
USDA: fats, oils, and sweets group (peanut butter, lard),

liver, cabbage, and potatoes.
woman (extended). The optimal soluannual cost of $535.27 ($1.47 daily).
of: 1.13 cups of wheat flour, 1.61
cups of rolled oats, 1.67 fluid ounces of milk, 3.31 tablespoons of peanut butter, 2.59 tablespoons of lard, 0.00724
ounces of beef liver, 1.20 bananas, 0.234 of an orange,
0.561 cup of shredded cabbage, 0.219 of a carrot, 0.384
of a potato, and 0.297 cup of pork and beans. The annual
costs are shown in Table 6 and the corresponding annual
Downloaded from informs.org by \[2.36.53.253\] on 03 October 2015, at 05:36 . For personal use only, all rights reserved.
quantities are shown in Table 7. The following minimum
requirements are not satisfied with this diet: polyunsaturated fatty acids and copper. The upper limit for manganese
was exceeded. This diet provides servings (or portions of
servings) from all of the six food groups established by the
USDA: fats, oils, and sweets group (peanut butter, lard),

USDA: fats, oils, and sweets group (peanut butter, lard),
milk group (milk), meats and beans group (beef liver, pork
and beans), vegetable group (cabbage, carrots, potato), fruit
group (bananas, oranges), grain product group (wheat flour,

Garille and Gass / 7
Stigler’s reduced list: wheat flour, beef liver, cabbage, and
potatoes.

potatoes.
When the no excess nutrient condition was applied to
the extended diet problem, there were no feasible diets for
either the man or woman. For all our diets, it is cheaper to
feed a woman than a man.

RIGHTSLINK

Semi-Updated Stigler’s Diet Problem

Semi-Updated Stigler’s Diet Problem
In this version of the problem, we solved Stigler’s original
problem using current data for the RDAs (for a 25–50-yearold light to moderately active man) and for the updated
nutritive values of foods, but with 1939 food prices. The
problem had only the nine inequality constraints, one each
for the nine nutrients considered by Stigler. The constraints
in this problem are the same as the constraints in the
updated Stigler’s problem discussed above.

updated Stigler’s problem discussed above.
To solve this problem, some food units of measurement
needed to be converted from what Stigler used. The prices
collected in April 1998 from the Giant supermarket were
all given per pound, except for the prices for milk, evaporated milk, cream, corn syrup, and molasses, which were
in quarts. Some of the conversions were quite clear. For
example, the unit for the following items in the 1939 data
was ounces (oz.): wheat cereal, corn flakes, hominy grits,
raisins, cocoa, and chocolate. These were readily converted
to pounds. More involved conversions dealt with foods
1
in cans (a 14-ounce can of evaporated milk was used
2
by Stigler), eggs (a dozen was the unit measure used by
Stigler), and carrots (a bunch was Stigler’s unit).

5.0. APPLICATIONS OF THE MINIMUM COST DIET

5.0. APPLICATIONS OF THE MINIMUM COST DIET
One might wonder about the real-world use of the minimum cost diet as originally posed by Stigler. We have
already noted how monotonous this diet would be if consumed on a regular basis. Stigler (1945) compared the

$$
1 4 \\frac {1}{2}
$$

by Stigler), eggs (a dozen was the unit measure used by
Stigler), and carrots (a bunch was Stigler’s unit).
The optimal solution to the semi-updated excess Stigler

The optimal solution to the semi-updated excess Stigler
diet problem was $40.92 annually in 1939 ($481.16 in
April 1998). The annual costs and quantities are shown

diet problem was $40.92 annually in 1939 ($481.16 in
April 1998). The annual costs and quantities are shown
in Table 9 and Table 10, respectively. The semi-updated
excess diet included wheat flour, evaporated milk, cabbage,
and sweet potatoes—a different diet than Stigler’s original,
which included spinach and navy beans but no sweet potatoes. The following minimum requirements are not satis-

fied with this diet: polyunsaturated fatty acids, vitamin B ,
vitamin B12, pantothenic acid, sodium, potassium, magnesium, zinc, copper, iodine, vitamin D, and vitamin E. The
upper limit for manganese was exceeded. This diet provides servings (or portions of servings) from the following
USDA food groups: milk group (evaporated milk), vegetable group (cabbage, sweet potatoes), grain product group
(wheat flour). All the foods in this diet are also on Stigler’s
reduced list of foods. As shown
Downloaded from informs.org by \[2.36.53.253\] on 03 October 2015, at 05:36 . For personal use only, all rights reserved. cost of this diet is just $0.99 more than the annual cost of
Stigler’s 1939 diet and $1.23 more than the annual cost of
Dantzig’s 1939 simplex LP solution diet. Tables 9 and 10
also show the semi-updated no excess solution.

fied with this diet: polyunsaturated fatty acids, vitamin B ,6
, pantothenic acid, sodium, potassium, magnesium, zinc, copper, iodine, vitamin D, and vitamin E. The
upper limit for manganese was exceeded. This diet provides servings (or portions of servings) from the following
USDA food groups: milk group (evaporated milk), vegetable group (cabbage, sweet potatoes), grain product group
(wheat flour). All the foods in this diet are also on Stigler’s
in Table 9, the annual
Downloaded from informs.org by \[2.36.53.253\] on 03 October 2015, at 05:36 . For personal use only, all rights reserved. cost of this diet is just $0.99 more than the annual cost of
Stigler’s 1939 diet and $1.23 more than the annual cost of
Dantzig’s 1939 simplex LP solution diet. Tables 9 and 10
also show the semi-updated no excess solution.

$$
\\mathrm {B} \_ {1 2}
$$

* * *

Downloaded from informs.org by \[2.36.53.253\] on 03 October 2015, at 05:36 . For personal use only, all rights reserved.

8/Garille and Gass
Table 9. Solutions to Stigler’s original and semi-updated diet problems: annual costs for August 1939.

| Food | Stigler(Original) | LP SimplexExcessNutrients(Original) | LP SimplexNo ExcessNutrients(Original) | LP SimplexSemi-UpdatedExcessNutrients | LP SimplexSemi-UpdatedNo ExcessNutrients |
| --- | --- | --- | --- | --- | --- |
| Wheat Flour | $13.33 | $10.78 | $6.61 | $19.98 | $2.90 |
| Corn Meal | - | - | $6.22 | - | - |
| Rolled Oats | - | - | - | - | $3.79 |
| Evaporated Milk | $3.84 | - | $16.48 | $14.46 | $16.01 |
| Peanut Butter | - | - | $0.12 | - | $11.42 |
| Lard | - | - | $8.91 | - | $11.15 |
| Beef Liver | - | $0.69 | $5.57 | - | $0.35 |
| Cabbage | $4.11 | $4.10 | $3.37 | $4.64 | $3.33 |
| Potatoes | - | - | $1.88 | - | $2.19 |
| Spinach | $1.85 | $1.83 | $0.24 | - | - |
| Dried Navy Beans | $16.80 | $22.29 | - | - | - |
| Sweet Potatoes | - | - | - | $1.84 | $1.52 |
| Total Daily Cost(1939 $) | $0.1093 | $0.1087 | $0.1352 | $0.1120 | $0.1442 |
| Total Daily Cost(1998 $) | $1.285 | $1.278 | $1.590 | $1.317 | $1.695 |
| Total Annual Cost(1939 $) | $39.93 | $39.69 | $49.40 | $40.92 | $52.56 |
| Total Annual Cost(1998 $) | $469.52 | $466.69 | $580.87 | $481.16 | $619.08 |

yearly cost of his diet ($39.93) with the costs of diets proposed by “professional dieticians.” The diets cited all cost
two to three times as much as his minimum cost diet. He
explained the differences in terms of palatability, variety,
prestige value of various foods, and other cultural facets of
consumption. This, he felt, led the dieticians to emphasize
meats and the inclusion of sugar. (In this regard, Stigler
1939, p. 314 commented, “Tax supported bureaucrats and
professors may also have another reason for certain of their
practices.”) Without making drastic modifications to the
basic diet problem, such minimum cost diets will never
prove to be acceptable. In his discussion of the diet problem, Gass (1958) noted that any new model would have to
enable more foods to be in the minimum solution (as is the
case of our extended Stigler problem), involve taste prefer-
Table 10. Solutions to Stigler’s original and semi-updated diet problems: annual quantities.

ences (with weights that can be introduced into the objective function), and by forcing foods in by lower bounds.
Also, another approach would be to subdivide the problem
into smaller diet problems, each of which would involve
a single class of food. This may be a reasonable approach
using the six food groups of the USDA’s Food Guide Pyramid (Pennington 1998).

Table 10. Solutions to Stigler’s original and semi-updated diet problems: annual quantities.

| Food | Stigler(Original) | LP SimplexExcessNutrients(Original) | LP SimplexNo ExcessNutrients(Original) | LP SimplexSemi-UpdatedExcessNutrients | LP SimplexSemi-UpdatedNo ExcessNutrients |
| --- | --- | --- | --- | --- | --- |
| Wheat Flour(lb.) | 370 | 299 | 184 | 555 | 80.6 |
| Corn Meal(lb.) | — | — | 135 | — | — |
| Rolled Oats(lb.) | — | — | — | — | 53.4 |
| Evaporated Milk(cans) | 57 | — | 246 | 215 | 239 |
| Peanut Butter(lb.) | — | — | 0.67 | — | 63.8 |
| Lard(lb.) | — | — | 90.9 | — | 114 |
| Beef Liver(lb.) | — | 2.57 | 20.8 | — | 1.29 |
| Cabbage(lb.) | 111 | 111 | 91.1 | 125 | 89.9 |
| Potatoes(lb.) | — | — | 82.9 | — | 96.6 |
| Spinach(lb.) | 23 | 23 | 2.96 | — | — |
| Dried Navy Beans(lb.) | 285 | 378 | — | — | — |
| Sweet Potatoes(lb.) | — | — | — | 36.1 | 29.8 |

mid (Pennington 1998).
Stigler’s diet problem and its modifications are ideal
for the classroom. In constructing such a model, the student learns about the rigors of data collection (its magnitude and need for accuracy and consistency), the need
for validating a model in a real-world setting, and the
need to run various scenarios and perform sensitivity
studies. Gass (1985) suggests student exercises using the
eight basic RDAs and calories and for constructing food

* * *

Downloaded from informs.org by \[2.36.53.253\] on 03 October 2015, at 05:36 . For personal use only, all rights reserved.

mixes for cats and dogs.
reports on his classroom-oriented
of selecting a menu
1994, Liberatore and
Web site, [http://www.mcs.anl.gov/otc/Guide/SIREV/](http://www.mcs.anl.gov/otc/Guide/SIREV/), contains data and formats that enable students to try their hand
at forming a diet that satisfies given levels of RDAs.

dogs. More recently, Bosch (1993)
classroom-oriented diet problem in terms
from McDonald’s (also see Erkut
Nydick 1999). The NEOS (1999)
Web site, [http://www.mcs.anl.gov/otc/Guide/SIREV/](http://www.mcs.anl.gov/otc/Guide/SIREV/), contains data and formats that enable students to try their hand
at forming a diet that satisfies given levels of RDAs.

Web site, [http://www.mcs.anl.gov/otc/Guide/SIREV/](http://www.mcs.anl.gov/otc/Guide/SIREV/), contains data and formats that enable students to try their hand
at forming a diet that satisfies given levels of RDAs.
Obvious deficiencies in the minimum cost diet have
led investigators to apply the power of linear and integer
programming to the development of more realistic models of human diets (minimum cost feed diets for cattle
and chicken seem to be devoured by the recipients; Jewell 1960). In particular, pioneering work in menu planning,
or computer-assisted menu planning, is described in Balintfy (1975). The history of this progress is reviewed in
Lancaster (1992). There are, however, some ongoing applications of modified diet models that can trace their lineage
back to Stigler and linear programming. We next describe
two such applications: (1) the thrifty Food Plan, a subsistence dietary approach developed by the USDA Agricultural Research Service that is used to determine the number
of food stamps to issue to Food Stamp Program recipients;
and (2) the rules imposed by the USDA on school dietitians
and related diet/menu software that ensures that publicschool students will receive nutritious school lunches.

The Thrifty Food Plan

The Thrifty Food Plan
The Thrifty Food Plan (TFP) was originally developed
by the Agricultural Research Service (ARS) in 1974–1975
(Kerr et al. 1984). As noted in ARS (1975): “This plan

specifies the amounts of foods of different
groups) that families might use to provide nutritious diets
for family members.” Here, chief dietary concerns, besides
the usual RDA and related constraints, were palatability
and variety. The TFP model finds “!!! the combination of
food groups !!! that represents as little change from the
food consumption pattern as required to meet the nutritional
goals at a given cost” (ASR 1975). The basis for current
family food consumption patterns was obtained by surveying households in 1965–1966, with an update conducted
1983\. Suggested diets are given for the different sex–age
categories determined by the National Research Council
for the given RDAs. The Center for Nutrition Policy and
Promotion is currently revising the TFP model so it will
include the most recent dietary guidelines (1989 RDAs) and
recommendations (food pyramid).

different types (food
groups) that families might use to provide nutritious diets
for family members.” Here, chief dietary concerns, besides
the usual RDA and related constraints, were palatability
and variety. The TFP model finds “!!! the combination of
food groups !!! that represents as little change from the
food consumption pattern as required to meet the nutritional
goals at a given cost” (ASR 1975). The basis for current
family food consumption patterns was obtained by surveying households in 1965–1966, with an update conducted
1983\. Suggested diets are given for the different sex–age
categories determined by the National Research Council
for the given RDAs. The Center for Nutrition Policy and
Promotion is currently revising the TFP model so it will
include the most recent dietary guidelines (1989 RDAs) and

nutritive values. (Note that these are not the food groups
established by the USDA.)
Constraints relative to each group were incorporated in
the model. Except for the groups fats/oils, sugars/sweets,

Garille and Gass
and soft drinks, no more than twice the amount of the food

Garille and Gass / 9
and soft drinks, no more than twice the amount of the food

and soft drinks, no more than twice the amount of the food
consumption pattern for each food group was allowed, and
no less than half of the food consumption pattern for each

no less than half of the food consumption pattern for each
food group was allowed. For the fats and sugars, no more
than the established food consumption pattern was allowed.
No more than half the food consumption pattern amount of
soft drinks were allowed in the diet. Also, upper and lower
limits on the ratio of the amount of flour to the amount of
leavening agents and seasonings were imposed.

no less than half of the food consumption pattern for each
food group was allowed. For the fats and sugars, no more
than the established food consumption pattern was allowed.
No more than half the food consumption pattern amount of
soft drinks were allowed in the diet. Also, upper and lower
limits on the ratio of the amount of flour to the amount of
leavening agents and seasonings were imposed.

leavening agents and seasonings were imposed.
The 1974 values of the RDAs were used. The model set
lower limits for 5% above the RDA for the following nutrients: calories, protein, calcium, iron, vitamin A, thiamine,
riboflavin, niacin, vitamin B12, and vitamin C. These exaggerated upper limits allow for some waste of edible food.
The model set lower limits of 80% of the RDA for magnesium and vitamin B6 and set an upper limit for calories
of 10% above the RDA. An upper limit was also set for fat
intake: No more than 40% of the calories came from fat.
A cholesterol limit was also imposed in that no weekly diet
for any person could contain more than four eggs (ARS
1975).

$$
\\mathrm {B} \_ {1 2}
$$

$$
\\mathrm {B} \_ {6}
$$

1975).
The TFP model does not minimize cost but minimizes a
deviation measure from present consumption patterns. Cost
is included and limited by a constraint. Maximum costs are
set for each sex–age category. To determine these maximum costs, two “preplans” were computed first. One preplan diet was the least-cost diet and the other was a diet
with no cost limit. These preplans were determined using
the quadratic programming model. Equitable costs were
determined for the categories by subtracting a constant proportion of the difference between costs for the two preplans
from the cost of the more expensive preplan. The proportion used was set to result in the per-capita cost of the
“economy plan” (ARS 1975).

“economy plan” (ARS 1975).
The monthly cost of the 1975 thrifty plan for a 20–54-
year-old male was $49.20 ($162.16 in April 1998), and for
a 20–54-year-old female the cost was $39.90 ($131.50 in
April 1998) (USDA 1983). The annual costs were $590.40
($1945.88 in April 1988) and $478.80 ($1578.06), respectively. The diet is given in terms of the number of units
from each food group that should be consumed to obtain
sufficient nutrients within the budget of the thrift plan. The
weekly diet consists of a set of foods that offers a variety
of foods and appears to be an improvement with respect to
palatability. We summarize the weekly thrift-plan diets and
associated monthly costs for men and women in Table 11.

The monthly cost of the 1975 thrifty plan for a 20–54-
year-old male was $49.20 ($162.16 in April 1998), and for
a 20–54-year-old female the cost was $39.90 ($131.50 in
April 1998) (USDA 1983). The annual costs were $590.40
($1945.88 in April 1988) and $478.80 ($1578.06), respectively. The diet is given in terms of the number of units
from each food group that should be consumed to obtain
sufficient nutrients within the budget of the thrift plan. The
weekly diet consists of a set of foods that offers a variety
of foods and appears to be an improvement with respect to
palatability. We summarize the weekly thrift-plan diets and
associated monthly costs for men and women in Table 11.

School Lunch Menu Planning

* * *

Downloaded from informs.org by \[2.36.53.253\] on 03 October 2015, at 05:36 . For personal use only, all rights reserved.

10 / Garille and Gass
Table 11. Weekly Thrift Plan Diets 1975—monthly costs.

| Food Group | Male20-54-Year-Old | Female20-54-Year-Old |
| --- | --- | --- |
| Milk, Cheese, Ice Cream | 2.57 quarts | 2.81 quarts |
| Meat, Poultry, Fish | 3.03 pounds | 2.41 pounds |
| Eggs | 4 | 4 |
| Dry Beans and Peas,Nuts | 0.44 pounds | 0.27 pounds |
| Dark-Green,Deep-YellowVegetables | 0.39 pounds | 0.52 pounds |
| Citrus Fruit,Tomatoes | 1.80 | 1.86 |
| Potatoes | 2.02 pounds | 1.51 pounds |
| Other Vegetables,Fruit | 3.69 pounds | 3.39 pounds |
| Cereal | 0.89 pounds | 0.90 pounds |
| Flour | 0.92 pounds | 0.67 pounds |
| Bread | 2.29 pounds | 1.41 pounds |
| Other Bakery Products | 1.33 pounds | 0.67 pounds |
| Fats,Oils | 0.95 pounds | 0.57 pounds |
| Sugar,Sweets | 0.86 pounds | 0.57 pounds |
| Accessories:Coffee,Tea,Soft Drinks,Juices,etc. | 1.24 pounds | 1.18 pounds |
| Monthly/Annual Cost1975 | $49.20/$590.40 | $39.90/$478.80 |
| Updated April 1998 | $162.16/$1,945.88 | $131.50/$1,578.06 |
| Monthly/Annual Cost1997 | $118.40/$1,420.80 | $106.80/$1,281.60 |
| Updated April 1998 | $119.88/$1,438.53 | $108.13/$1,297.59 |

issued by the USDA.
Schools have until school year 1998/99 to comply with
the most current recommendations of the Dietary Guidelines for Americans. School lunches, measured over one
week, must provide one-third of the RDAs for protein,

Dietary Guidelines” (USDA 1975).
Analyzed and revised every five years since their development in the late 1970s, the Dietary Guidelines for
Americans are issued by the USDA and the Department of
Health and Human Services. In 1990, the Dietary Guidelines recommended that people eat a variety of foods; maintain a healthy weight; choose a diet with plenty of vegetables, fruits, and grain products; and use sugar and sodium
in moderation. The Dietary Guidelines also recommended
diets that are low in fat, saturated fat, and cholesterol so
that over time fat comprises 30% or less of caloric intake
and saturated fat less than 10 percent of total calories for
persons two years of age and older (USDA 1995).

vitamin A, vitamin C, iron, calcium, and calories. School
lunch planners need only consider these nutrients because
studies have shown that these are the nutrients in which
U.S. children are most likely to be deficient. Also, if the
RDAs for these nutrients are met, the probability is high
that the RDAs for other nutrients will also be met. In addition to the RDA constraints, no more than 30% of the total
calories in the lunches may come from fat and no more
than 10% of the total calories may come from saturated fat
(USDA/CNP 1998). One of the ways school systems can
meet these objectives is by using computer-based software
with the generic name of NuMenus.

with the generic name of NuMenus.
NuMenus “!!! is a computer-based menu planning system which allows menus to be planned without conforming to specific food components or quantity requirements.
Approved software analyzes the nutrient content of foods
prepared for school meals and enables the menu planner
to adjust portion sizes and food components as needed to
achieve compliance with nutrition standards. While menu
planners are not bound by strict component and quantity
requirements, they must, nonetheless, ensure that children
are offered an entree, milk, and at least one other food
item” (USDA 1998).

6.0. SUMMARY
The statement and early solution of Stigler’s diet problem
predates much of what we now call operations research. Its

6.0. SUMMARY

* * *

Downloaded from informs.org by \[2.36.53.253\] on 03 October 2015, at 05:36 . For personal use only, all rights reserved.

influence on OR, however, has been early and extensive;
its contributions cut across OR theory, computation, and
application. The hand-computed solution of Stigler’s original (9 × 77) problem, done in 1947, helped prove that the
simplex method would work in practice. The concept of a
diet or blending problem led the way to many minimumcost applications: cattle and chicken feed, chemical and
fertilizer blending. The inadequacy of the Stigler’s diet
problem to produce a nutritious and palatable human diet
caused researchers to extend the approach to menu planning, which in turn raised new research questions in integer and goal programming. The diet problem has proved
to be a pedagogical paradigm. Students at all levels readily
understand the problem. The linear-programming model of
the basic diet problem can be used to explain just about
all linear programming assumptions and concepts (additivity, proportionality, nonnegativity, sensitivity analysis, duality). Student field projects involving the diet problem illustrate the difficulties of data collection (accuracy, consistency). It is a classic example of a “correct” mathematical
model of a real-world problem that does not produce a valid
solution.

solution.
Stigler’s pre-linear programming approach to the modeling of a human diet—that is, the recognition that a diet can
be expressed as constrained linear system (one that assumes
additivity and proportionality intake of dietary nutrients)—

Garille and Gass / 11
forms the basis for how we now (1) evaluate the nutritional content of diets for school children, (2) plan menus
for institutions (hospitals, jails), and in general, (3) manage
food-systems. Although the minimum-cost diets we determined in our extended Stigler’s diet model were more varied and more nutritious than Stigler’s original diet, we do
not suggest that such diets be followed. They do, however,
represent low-cost baseline diets against which other nutritionally correct diets can be compared.

tionally correct diets can be compared.
The diet conscious reader may wish to pick up the challenge posed by Steingarten (1998, p. 45):

lenge posed by Steingarten (1998, p. 45):
Now it’s your job and mine to make something
delicious out of our Simplex Subsistence Diet. Just
remember: This is as close to the theoretically cheapest diet that will keep you alive and well nourished.
Even if we add an extra ounce of sugar, a cup of
coffee, and a little olive oil to make our lives more
scrumptious, we can still beat the USDA and Thrifty
Food Plan at its own game.

Food Plan at its own game.
The so-challenged reader may wish to try Chef Daniel
Boulard’s menu for “swiss chard and bean soup with ricotta
toast,” which Steingarten includes in his book. He notes that
this soup “!!! uncannily mirrors our Simplex Subsistence
Diet.” In 1993, it would have served four as a complete
supper at $1.76 a person (Steingarten 1998, p. 45–47). Bon
appétit!

APPENDIX A.

$$
0 ^ {\\prime \\prime}
$$

Stigler Name Bowes & Church’s Food Values Name
Wheat Flour Wheat flour, white, all purpose, enriched
Macaroni Macaroni, enriched, cooked
Wheat cereal Farina, cooked, enriched
Corn flakes Corn flakes, Kellogg’s
Corn meal Cornmeal, yellow, degermed, enriched Quaker
Hominy grits Corn grits, regular/quick, enriched, cooked
Rice White rice, long grain, enriched, cooked
Rolled oats Oats, regular/quick/instant, dry
White bread Bread, white
Whole wheat bread Bread, whole wheat
Rye bread Bread, rye, American
Pound cake Cake, pound, golden, from mix, Betty Crocker
Soda crackers Cracker, oyster & soup, Keebler
Milk Milk, lowfat, 2% fat
Evaporated milk Milk, evaporated, canned, Carnation
Butter Butter
Oleomargarine Margarine, Fleischmann’s, stick
Downloaded from informs.org by \[2.36.53.253\] on 03 October 2015, at 05:36 . For personal use only, all rights reserved. Eggs Egg, chicken, boiled, hard/soft
Cheese Cheese, cheddar
Cream Light (coffee/table) cream
Peanut butter Peanut butter, creamy, Jif
Mayonnaise Mayonnaise, Best Foods/Hellman’s
Crisco Shortening, Crisco, regular/butter flavor
Lard Animal fats, lard (pork fat), raw

Bowes & Church’s Food Values Name
Wheat flour, white, all purpose, enriched
Macaroni, enriched, cooked
Farina, cooked, enriched
Corn flakes, Kellogg’s
Cornmeal, yellow, degermed, enriched Quaker
Corn grits, regular/quick, enriched, cooked
White rice, long grain, enriched, cooked
Oats, regular/quick/instant, dry
Bread, whole wheat
Bread, rye, American
Cake, pound, golden, from mix, Betty Crocker
Cracker, oyster & soup, Keebler
Milk, lowfat, 2% fat
Milk, evaporated, canned, Carnation
Margarine, Fleischmann’s, stick
Downloaded from informs.org by \[2.36.53.253\] on 03 October 2015, at 05:36 . For personal use only, all rights reserved. Egg, chicken, boiled, hard/soft
Cheese, cheddar
Light (coffee/table) cream
Peanut butter, creamy, Jif
Mayonnaise, Best Foods/Hellman’s
Shortening, Crisco, regular/butter flavor
Animal fats, lard (pork fat), raw

Crisco Shortening, Crisco, regular/butter flavor
Lard Animal fats, lard (pork fat), raw
Sirloin steak Top sirloin, separable lean, choice, broiled,
′′
0 fat trim

′′
0 fat trim
Round steak Round, eye of, separable lean, roasted, choice,
′′
0 fat trim

$$
0 ^ {\\prime \\prime}
$$

Super G stone ground whole wheat graham flour
Super G elbow macaroni (enriched)
Farina enriched creamy hot wheat cereal
Kellogg’s corn flakes
Quaker yellow corn meal
Quaker instant grits—original
Super G long grain white rice (bulk)
Quaker Oats rolled oats (bulk)
Super G enriched white sandwich bread
Home Pride wheat bread
Super G seedless Jewish rye bread
Betty Crocker pound cake mix
Super G soup and oyster crackers
Super G 2% milk fat reduced fat milk
Carnation evaporated milk (canned)
Super G regular butter quarters
Fleischmann’s original spread sticks
Downloaded from informs.org by \[2.36.53.253\] on 03 October 2015, at 05:36 . For personal use only, all rights reserved. Super G A medium eggs
Super G Wisconsin sharp cheddar cheese
Super G table cream
Jif creamy peanut butter
Hellmann’s mayonnaise
Crisco all-vegetable shortening
Esskay lard
Top sirloin steak boneless choice (meat)

Giant Name

Beef eye round steak choice (meat)

* * *

Downloaded from informs.org by \[2.36.53.253\] on 03 October 2015, at 05:36 . For personal use only, all rights reserved.

Rib roast Rib, small end (ribs 10-12), separable lean,
′′
choice, roasted, 1/4 fat trim
Chuck roast Chuck arm pot roast, separable lean, braised,
′′
choice, 0 fat trim
Plate Beef, flank, choice, separable lean & fat, braised,
′′
0 fat trim
Liver Liver, beef, braised
Leg of lamb Lamb, domestic, leg, shank half, choice, roasted,
separable lean
Lamb chops Lamb, domestic, rib, separable lean, choice,
broiled
Pork chops Pork, center loin (loin chops/roasts), separable
lean, roasted
Pork loin roast Pork, center loin (loin chops/roasts), separable
lean, roasted
Bacon Bacon, cured, broiled/pan fried (unit = yield from
1 pound raw)
Ham Ham, cured (fully cooked as purchased) lean (4–
5% fat), roasted
Salt pork Belly, pork, raw
Roasting chicken Chicken, roaster, light & dark meat w/skin,
roasted
Veal cutlets Veal, loin, separable lean braised
Salmon Salmon, pink, canned, Libby’s
Apples Apple, raw, with skin
Bananas Banana, raw
Lemons Lemon, raw
Oranges Orange, navel, raw
Green beans Green beans (snap beans) boiled
Cabbage Cabbage, green, raw
Carrots Carrots, raw
Celery Celery, raw
Lettuce Lettuce, iceberg, raw
Onions Onions, raw
Potatoes Potato, baked, with skin
Spinach Spinach, raw
Sweet potatoes Sweet potato baked, with skin
Peaches Peaches, canned, heavy syrup
Pears Pears, canned, heavy pack
Pineapple Pineapple, canned, heavy syrup
Asparagus Asparagus, canned
Green beans Green beans (snap beans) canned
Pork and beans Pork and beans, in tomato sauce, canned
Corn Corn, yellow, canned
Peas Peas, green, canned
Tomatoes Tomato, red, whole, peeled, canned
Tomato soup Soup, tomato
Peaches, dried Peaches, dried, sulphured
Prunes, dried Prunes, dried
Raisins, dried Raisins, seedless
Peas, dried Peas, split, boiled
Lima beans, dried Lima beans, baby, boiled, mature
Navy beans, dried Navy beans, boiled
Coffee Coffee, brewed
Tea Tea, brewed, black, 3 minutes
Cocoa Cocoa, unsweetened, dry powder, Hershey
Downloaded from informs.org by \[2.36.53.253\] on 03 October 2015, at 05:36 . For personal use only, all rights reserved.
Chocolate Baking chocolate, unsweetened
Sugar Sugar, white, granulated
Corn syrup Syrup, corn, dark
Molasses Molasses
Strawberry preserves Jam/preserves

Beef rib roast small end choice (meat) bone in
Beef chuck blade roast (w/bone)
Beef flank steak (meat)
Fresh baby beef liver
semi boneless lamb leg choice (meat)
Lamb rib chops choice (meat)
Pork loin roast
Pork loin sirloin roast
Generic sliced bacon
Mash’s fully cooked smoked ham
Hormel cured salt pork
All Natural fresh chicken
Veal cutlet—boneless (meat)
Season pink salmon (canned)
McIntosh apples
Bananas
Lemons
California navel oranges
Green beans
Green cabbage
Wm. Bolthouse Farms cold water carrots
Celery hearts
Iceberg lettuce
Yellow onions
US #1 baking potatoes
Spinach
US #1 red sweet potatoes
Super G halves yellow cling peaches in heavy syrup
Super G Bartlett pear halves in heavy syrup
Super G sliced pineapple in heavy syrup
Super G all green asparagus cut spears
Super G cut green beans
Super G pork and beans in tomato sauce
Super G whole kernel golden corn
Super G sweet peas
Super G California whole peeled tomatoes
Campbell’s tomato soup
Ann’s House of Nuts dried peaches (bulk)
Ann’s House of Nuts whole prunes (bulk)
Ann’s House of Nuts seedless dark raisins (bulk)
Goya green split peas
Goya No. 1 grade baby lima beans
Goya No. 1 grade navy beans
Super G coffee
Super G tea bags
Hershey’s cocoa
Downloaded from informs.org by \[2.36.53.253\] on 03 October 2015, at 05:36 . For personal use only, all rights reserved.
Hershey’s baking chocolate—unsweetened
Super G granulated sugar (bulk)
Karo dark corn syrup
King Po-T-Rik molasses
Super G strawberry preserves

* * *

Downloaded from informs.org by \[2.36.53.253\] on 03 October 2015, at 05:36 . For personal use only, all rights reserved.

REFERENCES

Agricultural Research Service. 1975. The Thrifty Food Plan. U.S.
Department of Agriculture, Hyattsville, MD.
Balintfy, J. L. 1975. A mathematical programming system for

Balintfy, J. L. 1975. A
food management applications. Interfaces 6 13–31.
. 1979\. The cost of decent subsistence. Management Sci.
25(10) 980–989.
, S. R. Rook, S. Taj. 1996. The index of decent subsistence.
Socio-Econom. Planning Sci. 30(4) 237–244.
Beckmann, M. J. 1960. On the determination of an adequate diet.
Trabajos de Estadidtica 11 139–142.
Bosch, R. A. 1993. Big Mac attack. OR/MS Today 20(4) 30–31.
Bowes, A. D., C. F. Church. 1994. Food values of portions commonly used. Privately printed, 5th edition, Philadelphia, PA.
Chatfield, C., G.
American Food Materials. Circular No. 549, U.S. Department of Agriculture, Washington, DC.
Czyzyk, J., T. Wisniewski, S. J. Wright. 1999. Optimization case
studies in NEOS guide. SIAM Rev. 41(1) 148–163.
Dantzig, G. B. 1990. The diet problem. Interfaces 20(4) 43–47.
. 1963\. Linear
University Press, Princeton, NJ.
Erkut, E. 1994. Big Mac attack revisited. OR/MS Today 21(3)
50–52.
Gass, S. I. 1958. Linear Programming: Methods and Applications.
McGraw-Hill Book Company, New York.
. 1984\. Linear Programming: Methods and Applications. 5th
Edition, McGraw-Hill Book Company, New York.
Jewell, W. S. 1960. A classroom example of linear programming,
lesson no. 2. Oper. Res. 8(4) 565–570.
Kerr, R. L., B. B. Peterkin, A. S. Blum, L. E. Cleveland. 1984.
USDA 1983 Thrifty Food Plans. Family Econom. Rev. 1 18–
25.
Lancaster, L. M. 1992. The history of the application of mathematical programming to menu planning. Eur. J. Oper. Res.
57 339–347.

1975. A mathematical programming system for
      food management applications. Interfaces 6 13–31.
      . 1979\. The cost of decent subsistence. Management Sci.
      25(10) 980–989.
      , S. R. Rook, S. Taj. 1996. The index of decent subsistence.
      Socio-Econom. Planning Sci. 30(4) 237–244.
      Beckmann, M. J. 1960. On the determination of an adequate diet.
      Trabajos de Estadidtica 11 139–142.
      Bosch, R. A. 1993. Big Mac attack. OR/MS Today 20(4) 30–31.
      Bowes, A. D., C. F. Church. 1994. Food values of portions commonly used. Privately printed, 5th edition, Philadelphia, PA.
      Adams. 1940. Proximate Composition of
      American Food Materials. Circular No. 549, U.S. Department of Agriculture, Washington, DC.
      Czyzyk, J., T. Wisniewski, S. J. Wright. 1999. Optimization case
      studies in NEOS guide. SIAM Rev. 41(1) 148–163.
      Dantzig, G. B. 1990. The diet problem. Interfaces 20(4) 43–47.
      Linear Programming and Extensions. Princeton
      University Press, Princeton, NJ.
      Erkut, E. 1994. Big Mac attack revisited. OR/MS Today 21(3)
      Gass, S. I. 1958. Linear Programming: Methods and Applications.
      McGraw-Hill Book Company, New York.
      . 1984\. Linear Programming: Methods and Applications. 5th
      Edition, McGraw-Hill Book Company, New York.
      Jewell, W. S. 1960. A classroom example of linear programming,
      lesson no. 2. Oper. Res. 8(4) 565–570.
      Kerr, R. L., B. B. Peterkin, A. S. Blum, L. E. Cleveland. 1984.
      USDA 1983 Thrifty Food Plans. Family Econom. Rev. 1 18–
      Lancaster, L. M. 1992. The history of the application of mathematical programming to menu planning. Eur. J. Oper. Res.

Garille and Gass / 13
Liberatore, M. J., R. L. Nydick. 1999. Breaking the mold—a new
approach to teaching the first MBA course in management
science. Interfaces 29(4) 99–116.
National Research Council. 1989. Recommended Dietary
Allowances. 10th edition, National Research Council Press,
Washington, DC.
Pennington, J. A. T. 1998. Bowes and Church’s Food Values of Portions Commonly Used. 17th edition, Lippincottt,
Philadelphia, PA.
Smith, V. E. 1963. Electronic Computation of Human Diets.
Michigan State University, Lansing, MI.
Steingarten, J. 1998. The Man Who Ate Everything. A. A. Knopf,
New York.
Stigler, G. 1945. The cost of subsistence. J. Farm Econom. 25
303–314.
USDA. 1983. The Thrifty Food Plan, 1983. Consumer Nutrition
Division, Human Nutrition Information Service, U.S. Department of Agricultute, Hyattsville, MD.
. 1994\. School Food Service Software System: Specifications
and Functional Requirements Document. Food and Nutrition
Service, Washington, DC.
. 1998\. Team Nutrition—USDA’s School Meal Initiative
for Healthy School Meals: Menu Planning and Recipes
for Schools. % [http://www.nal.gov:8001/menu/mealpla.htm&](http://www.nal.gov:8001/menu/mealpla.htm&),
22 May 1998, Washington, DC.
. Agriculture Food and Nutrition Service. 1995. Child Nutrition Programs: School Meal Initiatives for Healthy Children.
Final Rule, Federal Register: Washington, DC, 60
. Center for Nutrition and Policy Promotion. 1998.
National School Lunch Program'Q(’s and'A(’s.
% [http://www.usda.gov/fcs/cnp/school∼2.htm&](http://www.usda.gov/fcs/cnp/school%E2%88%BC2.htm&), 26 May 1998,
Washington, DC.
. NuMenus. 1998. Approved Software Packages for
NuMenus, Assisted NuMenus and State Monitoring of
Foods Based Menus. % [http://www.nal.usda.gov:8001/menu/](http://www.nal.usda.gov:8001/menu/)
softwr2.html&, 22 May 1998, Washington, DC.