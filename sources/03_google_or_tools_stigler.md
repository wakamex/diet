# Source: The Stigler Diet Problem  |  OR-Tools  |  Google for Developers

- URL: https://developers.google.com/optimization/lp/stigler_diet
- Slug: 03_google_or_tools_stigler

---

[Skip to main content](https://developers.google.com/optimization/lp/stigler_diet#main-content)

[![Google OR-Tools](https://developers.google.com/static/optimization/images/orLogo.png)](https://developers.google.com/optimization)

- [GoogleOR-Tools](https://developers.google.com/optimization)

`/`

Language

- [English](https://developers.google.com/optimization/lp/stigler_diet)
- [Deutsch](https://developers.google.com/optimization/lp/stigler_diet?hl=de)
- [Español](https://developers.google.com/optimization/lp/stigler_diet?hl=es)
- [Español – América Latina](https://developers.google.com/optimization/lp/stigler_diet?hl=es-419)
- [Français](https://developers.google.com/optimization/lp/stigler_diet?hl=fr)
- [Indonesia](https://developers.google.com/optimization/lp/stigler_diet?hl=id)
- [Italiano](https://developers.google.com/optimization/lp/stigler_diet?hl=it)
- [Polski](https://developers.google.com/optimization/lp/stigler_diet?hl=pl)
- [Português – Brasil](https://developers.google.com/optimization/lp/stigler_diet?hl=pt-br)
- [Tiếng Việt](https://developers.google.com/optimization/lp/stigler_diet?hl=vi)
- [Türkçe](https://developers.google.com/optimization/lp/stigler_diet?hl=tr)
- [Русский](https://developers.google.com/optimization/lp/stigler_diet?hl=ru)
- [עברית](https://developers.google.com/optimization/lp/stigler_diet?hl=he)
- [العربيّة](https://developers.google.com/optimization/lp/stigler_diet?hl=ar)
- [فارسی](https://developers.google.com/optimization/lp/stigler_diet?hl=fa)
- [हिंदी](https://developers.google.com/optimization/lp/stigler_diet?hl=hi)
- [বাংলা](https://developers.google.com/optimization/lp/stigler_diet?hl=bn)
- [ภาษาไทย](https://developers.google.com/optimization/lp/stigler_diet?hl=th)
- [中文 – 简体](https://developers.google.com/optimization/lp/stigler_diet?hl=zh-cn)
- [中文 – 繁體](https://developers.google.com/optimization/lp/stigler_diet?hl=zh-tw)
- [日本語](https://developers.google.com/optimization/lp/stigler_diet?hl=ja)
- [한국어](https://developers.google.com/optimization/lp/stigler_diet?hl=ko)

Sign in

- [OR-Tools](https://developers.google.com/optimization)

- On this page
- [Solution using the linear solver](https://developers.google.com/optimization/lp/stigler_diet#solution_using_the_linear_solver)
  - [Import the linear solver wrapper](https://developers.google.com/optimization/lp/stigler_diet#import_the_linear_solver_wrapper)
  - [Data for the problem](https://developers.google.com/optimization/lp/stigler_diet#data_for_the_problem)
  - [Declare the LP solver](https://developers.google.com/optimization/lp/stigler_diet#declare_the_lp_solver)
  - [Create the variables](https://developers.google.com/optimization/lp/stigler_diet#create_the_variables)
  - [Define the constraints](https://developers.google.com/optimization/lp/stigler_diet#define_the_constraints)
  - [Create the objective](https://developers.google.com/optimization/lp/stigler_diet#create_the_objective)
  - [Invoke the solver](https://developers.google.com/optimization/lp/stigler_diet#invoke_the_solver)
  - [Display the solution](https://developers.google.com/optimization/lp/stigler_diet#display_the_solution)
  - [Complete code for the program](https://developers.google.com/optimization/lp/stigler_diet#complete_code_for_the_program)

- [Home](https://developers.google.com/)
- [Products](https://developers.google.com/products)
- [OR-Tools](https://developers.google.com/optimization)
- [Guides](https://developers.google.com/optimization/introduction)



 Send feedback



# The Stigler Diet Problem    Stay organized with collections      Save and categorize content based on your preferences.

- On this page
- [Solution using the linear solver](https://developers.google.com/optimization/lp/stigler_diet#solution_using_the_linear_solver)
  - [Import the linear solver wrapper](https://developers.google.com/optimization/lp/stigler_diet#import_the_linear_solver_wrapper)
  - [Data for the problem](https://developers.google.com/optimization/lp/stigler_diet#data_for_the_problem)
  - [Declare the LP solver](https://developers.google.com/optimization/lp/stigler_diet#declare_the_lp_solver)
  - [Create the variables](https://developers.google.com/optimization/lp/stigler_diet#create_the_variables)
  - [Define the constraints](https://developers.google.com/optimization/lp/stigler_diet#define_the_constraints)
  - [Create the objective](https://developers.google.com/optimization/lp/stigler_diet#create_the_objective)
  - [Invoke the solver](https://developers.google.com/optimization/lp/stigler_diet#invoke_the_solver)
  - [Display the solution](https://developers.google.com/optimization/lp/stigler_diet#display_the_solution)
  - [Complete code for the program](https://developers.google.com/optimization/lp/stigler_diet#complete_code_for_the_program)

![Spark icon](https://developers.google.com/_static/images/icons/spark.svg)

## Page Summary

outlined\_flag

- The Stigler Diet is a mathematical optimization problem that aims to find the cheapest combination of foods to meet daily nutritional needs.

- The problem uses linear programming techniques to minimize the cost of the diet while satisfying nutritional constraints.

- Data includes food prices, nutritional values, and minimum daily requirements for various nutrients.

- Solutions are found using optimization solvers like GLOP, providing the optimal food quantities and total cost.

- The Stigler Diet is a historical example of applying optimization in nutrition, but it's not intended as practical dietary advice.


In this section, we show how to solve a classic problem called the
[Stigler diet](http://en.wikipedia.org/wiki/Stigler_diet), named for economics
Nobel laureate George Stigler, who computed an inexpensive way to fulfill basic
nutritional needs given a set of foods. He posed this as a mathematical exercise
, not as eating recommendations, although the notion of computing optimal
nutrition has of [come into vogue](http://en.wikipedia.org/wiki/CRON-diet)
recently.

The Stigler diet mandated that these minimums be met:

**Nutrients list**

| Nutrient | Daily Recommended Intake |
| --- | --- |
| Calories | 3,000 calories |
| Protein | 70 grams |
| Calcium | .8 grams |
| Iron | 12 milligrams |
| Vitamin A | 5,000 IU |
| Thiamine (Vitamin B1) | 1.8 milligrams |
| Riboflavin (Vitamin B2) | 2.7 milligrams |
| Niacin | 18 milligrams |
| Ascorbic Acid (Vitamin C) | 75 milligrams |

The set of foods Stigler evaluated was a reflection of the time
(1944). The nutritional data below is per dollar, not per unit, so the
objective is to determine how many dollars to spend on each foodstuff.

**Commodities list**

| Commodity | Unit | 1939 price (cents) | Calories (kcal) | Protein (g) | Calcium (g) | Iron (mg) | Vitamin A (KIU) | Thiamine (mg) | Riboflavin (mg) | Niacin (mg) | Ascorbic Acid (mg) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Wheat Flour (Enriched) | 10 lb. | 36 | 44.7 | 1411 | 2 | 365 | 0 | 55.4 | 33.3 | 441 | 0 |
| Macaroni | 1 lb. | 14.1 | 11.6 | 418 | 0.7 | 54 | 0 | 3.2 | 1.9 | 68 | 0 |
| Wheat Cereal (Enriched) | 28 oz. | 24.2 | 11.8 | 377 | 14.4 | 175 | 0 | 14.4 | 8.8 | 114 | 0 |
| Corn Flakes | 8 oz. | 7.1 | 11.4 | 252 | 0.1 | 56 | 0 | 13.5 | 2.3 | 68 | 0 |
| Corn Meal | 1 lb. | 4.6 | 36.0 | 897 | 1.7 | 99 | 30.9 | 17.4 | 7.9 | 106 | 0 |
| Hominy Grits | 24 oz. | 8.5 | 28.6 | 680 | 0.8 | 80 | 0 | 10.6 | 1.6 | 110 | 0 |
| Rice | 1 lb. | 7.5 | 21.2 | 460 | 0.6 | 41 | 0 | 2 | 4.8 | 60 | 0 |
| Rolled Oats | 1 lb. | 7.1 | 25.3 | 907 | 5.1 | 341 | 0 | 37.1 | 8.9 | 64 | 0 |
| White Bread (Enriched) | 1 lb. | 7.9 | 15.0 | 488 | 2.5 | 115 | 0 | 13.8 | 8.5 | 126 | 0 |
| Whole Wheat Bread | 1 lb. | 9.1 | 12.2 | 484 | 2.7 | 125 | 0 | 13.9 | 6.4 | 160 | 0 |
| Rye Bread | 1 lb. | 9.1 | 12.4 | 439 | 1.1 | 82 | 0 | 9.9 | 3 | 66 | 0 |
| Pound Cake | 1 lb. | 24.8 | 8.0 | 130 | 0.4 | 31 | 18.9 | 2.8 | 3 | 17 | 0 |
| Soda Crackers | 1 lb. | 15.1 | 12.5 | 288 | 0.5 | 50 | 0 | 0 | 0 | 0 | 0 |
| Milk | 1 qt. | 11 | 6.1 | 310 | 10.5 | 18 | 16.8 | 4 | 16 | 7 | 177 |
| Evaporated Milk (can) | 14.5 oz. | 6.7 | 8.4 | 422 | 15.1 | 9 | 26 | 3 | 23.5 | 11 | 60 |
| Butter | 1 lb. | 30.8 | 10.8 | 9 | 0.2 | 3 | 44.2 | 0 | 0.2 | 2 | 0 |
| Oleomargarine | 1 lb. | 16.1 | 20.6 | 17 | 0.6 | 6 | 55.8 | 0.2 | 0 | 0 | 0 |
| Eggs | 1 doz. | 32.6 | 2.9 | 238 | 1.0 | 52 | 18.6 | 2.8 | 6.5 | 1 | 0 |
| Cheese (Cheddar) | 1 lb. | 24.2 | 7.4 | 448 | 16.4 | 19 | 28.1 | 0.8 | 10.3 | 4 | 0 |
| Cream | 1/2 pt. | 14.1 | 3.5 | 49 | 1.7 | 3 | 16.9 | 0.6 | 2.5 | 0 | 17 |
| Peanut Butter | 1 lb. | 17.9 | 15.7 | 661 | 1.0 | 48 | 0 | 9.6 | 8.1 | 471 | 0 |
| Mayonnaise | 1/2 pt. | 16.7 | 8.6 | 18 | 0.2 | 8 | 2.7 | 0.4 | 0.5 | 0 | 0 |
| Crisco | 1 lb. | 20.3 | 20.1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Lard | 1 lb. | 9.8 | 41.7 | 0 | 0 | 0 | 0.2 | 0 | 0.5 | 5 | 0 |
| Sirloin Steak | 1 lb. | 39.6 | 2.9 | 166 | 0.1 | 34 | 0.2 | 2.1 | 2.9 | 69 | 0 |
| Round Steak | 1 lb. | 36.4 | 2.2 | 214 | 0.1 | 32 | 0.4 | 2.5 | 2.4 | 87 | 0 |
| Rib Roast | 1 lb. | 29.2 | 3.4 | 213 | 0.1 | 33 | 0 | 0 | 2 | 0 | 0 |
| Chuck Roast | 1 lb. | 22.6 | 3.6 | 309 | 0.2 | 46 | 0.4 | 1 | 4 | 120 | 0 |
| Plate | 1 lb. | 14.6 | 8.5 | 404 | 0.2 | 62 | 0 | 0.9 | 0 | 0 | 0 |
| Liver (Beef) | 1 lb. | 26.8 | 2.2 | 333 | 0.2 | 139 | 169.2 | 6.4 | 50.8 | 316 | 525 |
| Leg of Lamb | 1 lb. | 27.6 | 3.1 | 245 | 0.1 | 20 | 0 | 2.8 | 3.9 | 86 | 0 |
| Lamb Chops (Rib) | 1 lb. | 36.6 | 3.3 | 140 | 0.1 | 15 | 0 | 1.7 | 2.7 | 54 | 0 |
| Pork Chops | 1 lb. | 30.7 | 3.5 | 196 | 0.2 | 30 | 0 | 17.4 | 2.7 | 60 | 0 |
| Pork Loin Roast | 1 lb. | 24.2 | 4.4 | 249 | 0.3 | 37 | 0 | 18.2 | 3.6 | 79 | 0 |
| Bacon | 1 lb. | 25.6 | 10.4 | 152 | 0.2 | 23 | 0 | 1.8 | 1.8 | 71 | 0 |
| Ham, smoked | 1 lb. | 27.4 | 6.7 | 212 | 0.2 | 31 | 0 | 9.9 | 3.3 | 50 | 0 |
| Salt Pork | 1 lb. | 16 | 18.8 | 164 | 0.1 | 26 | 0 | 1.4 | 1.8 | 0 | 0 |
| Roasting Chicken | 1 lb. | 30.3 | 1.8 | 184 | 0.1 | 30 | 0.1 | 0.9 | 1.8 | 68 | 46 |
| Veal Cutlets | 1 lb. | 42.3 | 1.7 | 156 | 0.1 | 24 | 0 | 1.4 | 2.4 | 57 | 0 |
| Salmon, Pink (can) | 16 oz. | 13 | 5.8 | 705 | 6.8 | 45 | 3.5 | 1 | 4.9 | 209 | 0 |
| Apples | 1 lb. | 4.4 | 5.8 | 27 | 0.5 | 36 | 7.3 | 3.6 | 2.7 | 5 | 544 |
| Bananas | 1 lb. | 6.1 | 4.9 | 60 | 0.4 | 30 | 17.4 | 2.5 | 3.5 | 28 | 498 |
| Lemons | 1 doz. | 26 | 1.0 | 21 | 0.5 | 14 | 0 | 0.5 | 0 | 4 | 952 |
| Oranges | 1 doz. | 30.9 | 2.2 | 40 | 1.1 | 18 | 11.1 | 3.6 | 1.3 | 10 | 1998 |
| Green Beans | 1 lb. | 7.1 | 2.4 | 138 | 3.7 | 80 | 69 | 4.3 | 5.8 | 37 | 862 |
| Cabbage | 1 lb. | 3.7 | 2.6 | 125 | 4.0 | 36 | 7.2 | 9 | 4.5 | 26 | 5369 |
| Carrots | 1 bunch | 4.7 | 2.7 | 73 | 2.8 | 43 | 188.5 | 6.1 | 4.3 | 89 | 608 |
| Celery | 1 stalk | 7.3 | 0.9 | 51 | 3.0 | 23 | 0.9 | 1.4 | 1.4 | 9 | 313 |
| Lettuce | 1 head | 8.2 | 0.4 | 27 | 1.1 | 22 | 112.4 | 1.8 | 3.4 | 11 | 449 |
| Onions | 1 lb. | 3.6 | 5.8 | 166 | 3.8 | 59 | 16.6 | 4.7 | 5.9 | 21 | 1184 |
| Potatoes | 15 lb. | 34 | 14.3 | 336 | 1.8 | 118 | 6.7 | 29.4 | 7.1 | 198 | 2522 |
| Spinach | 1 lb. | 8.1 | 1.1 | 106 | 0 | 138 | 918.4 | 5.7 | 13.8 | 33 | 2755 |
| Sweet Potatoes | 1 lb. | 5.1 | 9.6 | 138 | 2.7 | 54 | 290.7 | 8.4 | 5.4 | 83 | 1912 |
| Peaches (can) | No. 2 1/2 | 16.8 | 3.7 | 20 | 0.4 | 10 | 21.5 | 0.5 | 1 | 31 | 196 |
| Pears (can) | No. 2 1/2 | 20.4 | 3.0 | 8 | 0.3 | 8 | 0.8 | 0.8 | 0.8 | 5 | 81 |
| Pineapple (can) | No. 2 1/2 | 21.3 | 2.4 | 16 | 0.4 | 8 | 2 | 2.8 | 0.8 | 7 | 399 |
| Asparagus (can) | No. 2 | 27.7 | 0.4 | 33 | 0.3 | 12 | 16.3 | 1.4 | 2.1 | 17 | 272 |
| Green Beans (can) | No. 2 | 10 | 1.0 | 54 | 2 | 65 | 53.9 | 1.6 | 4.3 | 32 | 431 |
| Pork and Beans (can) | 16 oz. | 7.1 | 7.5 | 364 | 4 | 134 | 3.5 | 8.3 | 7.7 | 56 | 0 |
| Corn (can) | No. 2 | 10.4 | 5.2 | 136 | 0.2 | 16 | 12 | 1.6 | 2.7 | 42 | 218 |
| Peas (can) | No. 2 | 13.8 | 2.3 | 136 | 0.6 | 45 | 34.9 | 4.9 | 2.5 | 37 | 370 |
| Tomatoes (can) | No. 2 | 8.6 | 1.3 | 63 | 0.7 | 38 | 53.2 | 3.4 | 2.5 | 36 | 1253 |
| Tomato Soup (can) | 10 1/2 oz. | 7.6 | 1.6 | 71 | 0.6 | 43 | 57.9 | 3.5 | 2.4 | 67 | 862 |
| Peaches, Dried | 1 lb. | 15.7 | 8.5 | 87 | 1.7 | 173 | 86.8 | 1.2 | 4.3 | 55 | 57 |
| Prunes, Dried | 1 lb. | 9 | 12.8 | 99 | 2.5 | 154 | 85.7 | 3.9 | 4.3 | 65 | 257 |
| Raisins, Dried | 15 oz. | 9.4 | 13.5 | 104 | 2.5 | 136 | 4.5 | 6.3 | 1.4 | 24 | 136 |
| Peas, Dried | 1 lb. | 7.9 | 20.0 | 1367 | 4.2 | 345 | 2.9 | 28.7 | 18.4 | 162 | 0 |
| Lima Beans, Dried | 1 lb. | 8.9 | 17.4 | 1055 | 3.7 | 459 | 5.1 | 26.9 | 38.2 | 93 | 0 |
| Navy Beans, Dried | 1 lb. | 5.9 | 26.9 | 1691 | 11.4 | 792 | 0 | 38.4 | 24.6 | 217 | 0 |
| Coffee | 1 lb. | 22.4 | 0 | 0 | 0 | 0 | 0 | 4 | 5.1 | 50 | 0 |
| Tea | 1/4 lb. | 17.4 | 0 | 0 | 0 | 0 | 0 | 0 | 2.3 | 42 | 0 |
| Cocoa | 8 oz. | 8.6 | 8.7 | 237 | 3 | 72 | 0 | 2 | 11.9 | 40 | 0 |
| Chocolate | 8 oz. | 16.2 | 8.0 | 77 | 1.3 | 39 | 0 | 0.9 | 3.4 | 14 | 0 |
| Sugar | 10 lb. | 51.7 | 34.9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Corn Syrup | 24 oz. | 13.7 | 14.7 | 0 | 0.5 | 74 | 0 | 0 | 0 | 5 | 0 |
| Molasses | 18 oz. | 13.6 | 9.0 | 0 | 10.3 | 244 | 0 | 1.9 | 7.5 | 146 | 0 |
| Strawberry Preserves | 1 lb. | 20.5 | 6.4 | 11 | 0.4 | 7 | 0.2 | 0.2 | 0.4 | 3 | 0 |

Since the nutrients have all been normalized by price, our objective is simply
minimizing the sum of foods.

In 1944, Stigler calculated the best answer he could, noting with sadness:

> ...there does not appear to be any direct method of finding the minimum of a
> linear function subject to linear conditions.

He found a diet that cost $39.93 per year, in 1939 dollars. In 1947, Jack
Laderman used the simplex method (then, a recent invention!) to determine the
optimal solution. It took 120 man days of nine clerks on desk calculators to
arrive at the answer.

## Solution using the linear solver

The following sections present a program that solves the Stigler diet problem.

### Import the linear solver wrapper

Import the OR-Tools [linear solver wrapper](https://developers.google.com/optimization/mip/lp), an interface
for the \[GLOP\](/optimization/mip/glop0 linear solver, as shown below.

[Python](https://developers.google.com/optimization/lp/stigler_diet#python)[C++](https://developers.google.com/optimization/lp/stigler_diet#c++)[Java](https://developers.google.com/optimization/lp/stigler_diet#java)[C#](https://developers.google.com/optimization/lp/stigler_diet#c)More

```
from ortools.linear_solver import pywraplp
```

```
#include <array>
#include <cstddef>
#include <cstdlib>
#include <memory>
#include <string>
#include <utility>  // std::pair
#include <vector>

#include "absl/base/log_severity.h"
#include "absl/log/globals.h"
#include "absl/log/log.h"
#include "ortools/base/init_google.h"
#include "ortools/linear_solver/linear_solver.h"
```

```
import com.google.ortools.Loader;
import com.google.ortools.linearsolver.MPConstraint;
import com.google.ortools.linearsolver.MPObjective;
import com.google.ortools.linearsolver.MPSolver;
import com.google.ortools.linearsolver.MPVariable;
import java.util.ArrayList;
import java.util.List;
```

```
using System;
using System.Collections.Generic;
using Google.OrTools.LinearSolver;
```

### Data for the problem

The following code creates an array `nutrients` for the
[minimum nutrient requirements](https://developers.google.com/optimization/lp/stigler_diet#nutrients), and an
array `data` for the [nutritional data table](https://developers.google.com/optimization/lp/stigler_diet#data)
in any solution.

[Python](https://developers.google.com/optimization/lp/stigler_diet#python)[C++](https://developers.google.com/optimization/lp/stigler_diet#c++)[Java](https://developers.google.com/optimization/lp/stigler_diet#java)[C#](https://developers.google.com/optimization/lp/stigler_diet#c)More

```
# Nutrient minimums.
nutrients = [\
    ["Calories (kcal)", 3],\
    ["Protein (g)", 70],\
    ["Calcium (g)", 0.8],\
    ["Iron (mg)", 12],\
    ["Vitamin A (KIU)", 5],\
    ["Vitamin B1 (mg)", 1.8],\
    ["Vitamin B2 (mg)", 2.7],\
    ["Niacin (mg)", 18],\
    ["Vitamin C (mg)", 75],\
]

# Commodity, Unit, 1939 price (cents), Calories (kcal), Protein (g),
# Calcium (g), Iron (mg), Vitamin A (KIU), Vitamin B1 (mg), Vitamin B2 (mg),
# Niacin (mg), Vitamin C (mg)
data = [\
    # fmt: off\
  ['Wheat Flour (Enriched)', '10 lb.', 36, 44.7, 1411, 2, 365, 0, 55.4, 33.3, 441, 0],\
  ['Macaroni', '1 lb.', 14.1, 11.6, 418, 0.7, 54, 0, 3.2, 1.9, 68, 0],\
  ['Wheat Cereal (Enriched)', '28 oz.', 24.2, 11.8, 377, 14.4, 175, 0, 14.4, 8.8, 114, 0],\
  ['Corn Flakes', '8 oz.', 7.1, 11.4, 252, 0.1, 56, 0, 13.5, 2.3, 68, 0],\
  ['Corn Meal', '1 lb.', 4.6, 36.0, 897, 1.7, 99, 30.9, 17.4, 7.9, 106, 0],\
  ['Hominy Grits', '24 oz.', 8.5, 28.6, 680, 0.8, 80, 0, 10.6, 1.6, 110, 0],\
  ['Rice', '1 lb.', 7.5, 21.2, 460, 0.6, 41, 0, 2, 4.8, 60, 0],\
  ['Rolled Oats', '1 lb.', 7.1, 25.3, 907, 5.1, 341, 0, 37.1, 8.9, 64, 0],\
  ['White Bread (Enriched)', '1 lb.', 7.9, 15.0, 488, 2.5, 115, 0, 13.8, 8.5, 126, 0],\
  ['Whole Wheat Bread', '1 lb.', 9.1, 12.2, 484, 2.7, 125, 0, 13.9, 6.4, 160, 0],\
  ['Rye Bread', '1 lb.', 9.1, 12.4, 439, 1.1, 82, 0, 9.9, 3, 66, 0],\
  ['Pound Cake', '1 lb.', 24.8, 8.0, 130, 0.4, 31, 18.9, 2.8, 3, 17, 0],\
  ['Soda Crackers', '1 lb.', 15.1, 12.5, 288, 0.5, 50, 0, 0, 0, 0, 0],\
  ['Milk', '1 qt.', 11, 6.1, 310, 10.5, 18, 16.8, 4, 16, 7, 177],\
  ['Evaporated Milk (can)', '14.5 oz.', 6.7, 8.4, 422, 15.1, 9, 26, 3, 23.5, 11, 60],\
  ['Butter', '1 lb.', 30.8, 10.8, 9, 0.2, 3, 44.2, 0, 0.2, 2, 0],\
  ['Oleomargarine', '1 lb.', 16.1, 20.6, 17, 0.6, 6, 55.8, 0.2, 0, 0, 0],\
  ['Eggs', '1 doz.', 32.6, 2.9, 238, 1.0, 52, 18.6, 2.8, 6.5, 1, 0],\
  ['Cheese (Cheddar)', '1 lb.', 24.2, 7.4, 448, 16.4, 19, 28.1, 0.8, 10.3, 4, 0],\
  ['Cream', '1/2 pt.', 14.1, 3.5, 49, 1.7, 3, 16.9, 0.6, 2.5, 0, 17],\
  ['Peanut Butter', '1 lb.', 17.9, 15.7, 661, 1.0, 48, 0, 9.6, 8.1, 471, 0],\
  ['Mayonnaise', '1/2 pt.', 16.7, 8.6, 18, 0.2, 8, 2.7, 0.4, 0.5, 0, 0],\
  ['Crisco', '1 lb.', 20.3, 20.1, 0, 0, 0, 0, 0, 0, 0, 0],\
  ['Lard', '1 lb.', 9.8, 41.7, 0, 0, 0, 0.2, 0, 0.5, 5, 0],\
  ['Sirloin Steak', '1 lb.', 39.6, 2.9, 166, 0.1, 34, 0.2, 2.1, 2.9, 69, 0],\
  ['Round Steak', '1 lb.', 36.4, 2.2, 214, 0.1, 32, 0.4, 2.5, 2.4, 87, 0],\
  ['Rib Roast', '1 lb.', 29.2, 3.4, 213, 0.1, 33, 0, 0, 2, 0, 0],\
  ['Chuck Roast', '1 lb.', 22.6, 3.6, 309, 0.2, 46, 0.4, 1, 4, 120, 0],\
  ['Plate', '1 lb.', 14.6, 8.5, 404, 0.2, 62, 0, 0.9, 0, 0, 0],\
  ['Liver (Beef)', '1 lb.', 26.8, 2.2, 333, 0.2, 139, 169.2, 6.4, 50.8, 316, 525],\
  ['Leg of Lamb', '1 lb.', 27.6, 3.1, 245, 0.1, 20, 0, 2.8, 3.9, 86, 0],\
  ['Lamb Chops (Rib)', '1 lb.', 36.6, 3.3, 140, 0.1, 15, 0, 1.7, 2.7, 54, 0],\
  ['Pork Chops', '1 lb.', 30.7, 3.5, 196, 0.2, 30, 0, 17.4, 2.7, 60, 0],\
  ['Pork Loin Roast', '1 lb.', 24.2, 4.4, 249, 0.3, 37, 0, 18.2, 3.6, 79, 0],\
  ['Bacon', '1 lb.', 25.6, 10.4, 152, 0.2, 23, 0, 1.8, 1.8, 71, 0],\
  ['Ham, smoked', '1 lb.', 27.4, 6.7, 212, 0.2, 31, 0, 9.9, 3.3, 50, 0],\
  ['Salt Pork', '1 lb.', 16, 18.8, 164, 0.1, 26, 0, 1.4, 1.8, 0, 0],\
  ['Roasting Chicken', '1 lb.', 30.3, 1.8, 184, 0.1, 30, 0.1, 0.9, 1.8, 68, 46],\
  ['Veal Cutlets', '1 lb.', 42.3, 1.7, 156, 0.1, 24, 0, 1.4, 2.4, 57, 0],\
  ['Salmon, Pink (can)', '16 oz.', 13, 5.8, 705, 6.8, 45, 3.5, 1, 4.9, 209, 0],\
  ['Apples', '1 lb.', 4.4, 5.8, 27, 0.5, 36, 7.3, 3.6, 2.7, 5, 544],\
  ['Bananas', '1 lb.', 6.1, 4.9, 60, 0.4, 30, 17.4, 2.5, 3.5, 28, 498],\
  ['Lemons', '1 doz.', 26, 1.0, 21, 0.5, 14, 0, 0.5, 0, 4, 952],\
  ['Oranges', '1 doz.', 30.9, 2.2, 40, 1.1, 18, 11.1, 3.6, 1.3, 10, 1998],\
  ['Green Beans', '1 lb.', 7.1, 2.4, 138, 3.7, 80, 69, 4.3, 5.8, 37, 862],\
  ['Cabbage', '1 lb.', 3.7, 2.6, 125, 4.0, 36, 7.2, 9, 4.5, 26, 5369],\
  ['Carrots', '1 bunch', 4.7, 2.7, 73, 2.8, 43, 188.5, 6.1, 4.3, 89, 608],\
  ['Celery', '1 stalk', 7.3, 0.9, 51, 3.0, 23, 0.9, 1.4, 1.4, 9, 313],\
  ['Lettuce', '1 head', 8.2, 0.4, 27, 1.1, 22, 112.4, 1.8, 3.4, 11, 449],\
  ['Onions', '1 lb.', 3.6, 5.8, 166, 3.8, 59, 16.6, 4.7, 5.9, 21, 1184],\
  ['Potatoes', '15 lb.', 34, 14.3, 336, 1.8, 118, 6.7, 29.4, 7.1, 198, 2522],\
  ['Spinach', '1 lb.', 8.1, 1.1, 106, 0, 138, 918.4, 5.7, 13.8, 33, 2755],\
  ['Sweet Potatoes', '1 lb.', 5.1, 9.6, 138, 2.7, 54, 290.7, 8.4, 5.4, 83, 1912],\
  ['Peaches (can)', 'No. 2 1/2', 16.8, 3.7, 20, 0.4, 10, 21.5, 0.5, 1, 31, 196],\
  ['Pears (can)', 'No. 2 1/2', 20.4, 3.0, 8, 0.3, 8, 0.8, 0.8, 0.8, 5, 81],\
  ['Pineapple (can)', 'No. 2 1/2', 21.3, 2.4, 16, 0.4, 8, 2, 2.8, 0.8, 7, 399],\
  ['Asparagus (can)', 'No. 2', 27.7, 0.4, 33, 0.3, 12, 16.3, 1.4, 2.1, 17, 272],\
  ['Green Beans (can)', 'No. 2', 10, 1.0, 54, 2, 65, 53.9, 1.6, 4.3, 32, 431],\
  ['Pork and Beans (can)', '16 oz.', 7.1, 7.5, 364, 4, 134, 3.5, 8.3, 7.7, 56, 0],\
  ['Corn (can)', 'No. 2', 10.4, 5.2, 136, 0.2, 16, 12, 1.6, 2.7, 42, 218],\
  ['Peas (can)', 'No. 2', 13.8, 2.3, 136, 0.6, 45, 34.9, 4.9, 2.5, 37, 370],\
  ['Tomatoes (can)', 'No. 2', 8.6, 1.3, 63, 0.7, 38, 53.2, 3.4, 2.5, 36, 1253],\
  ['Tomato Soup (can)', '10 1/2 oz.', 7.6, 1.6, 71, 0.6, 43, 57.9, 3.5, 2.4, 67, 862],\
  ['Peaches, Dried', '1 lb.', 15.7, 8.5, 87, 1.7, 173, 86.8, 1.2, 4.3, 55, 57],\
  ['Prunes, Dried', '1 lb.', 9, 12.8, 99, 2.5, 154, 85.7, 3.9, 4.3, 65, 257],\
  ['Raisins, Dried', '15 oz.', 9.4, 13.5, 104, 2.5, 136, 4.5, 6.3, 1.4, 24, 136],\
  ['Peas, Dried', '1 lb.', 7.9, 20.0, 1367, 4.2, 345, 2.9, 28.7, 18.4, 162, 0],\
  ['Lima Beans, Dried', '1 lb.', 8.9, 17.4, 1055, 3.7, 459, 5.1, 26.9, 38.2, 93, 0],\
  ['Navy Beans, Dried', '1 lb.', 5.9, 26.9, 1691, 11.4, 792, 0, 38.4, 24.6, 217, 0],\
  ['Coffee', '1 lb.', 22.4, 0, 0, 0, 0, 0, 4, 5.1, 50, 0],\
  ['Tea', '1/4 lb.', 17.4, 0, 0, 0, 0, 0, 0, 2.3, 42, 0],\
  ['Cocoa', '8 oz.', 8.6, 8.7, 237, 3, 72, 0, 2, 11.9, 40, 0],\
  ['Chocolate', '8 oz.', 16.2, 8.0, 77, 1.3, 39, 0, 0.9, 3.4, 14, 0],\
  ['Sugar', '10 lb.', 51.7, 34.9, 0, 0, 0, 0, 0, 0, 0, 0],\
  ['Corn Syrup', '24 oz.', 13.7, 14.7, 0, 0.5, 74, 0, 0, 0, 5, 0],\
  ['Molasses', '18 oz.', 13.6, 9.0, 0, 10.3, 244, 0, 1.9, 7.5, 146, 0],\
  ['Strawberry Preserves', '1 lb.', 20.5, 6.4, 11, 0.4, 7, 0.2, 0.2, 0.4, 3, 0],\
    # fmt: on\
]
```

```
// Nutrient minimums.
const std::vector<std::pair<std::string, double>> nutrients = {
    {"Calories (kcal)", 3.0}, {"Protein (g)", 70.0},
    {"Calcium (g)", 0.8},     {"Iron (mg)", 12.0},
    {"Vitamin A (kIU)", 5.0}, {"Vitamin B1 (mg)", 1.8},
    {"Vitamin B2 (mg)", 2.7}, {"Niacin (mg)", 18.0},
    {"Vitamin C (mg)", 75.0}};

struct Commodity {
  std::string name;  //!< Commodity name
  std::string unit;  //!< Unit
  double price;      //!< 1939 price per unit (cents)
  //! Calories (kcal),
  //! Protein (g),
  //! Calcium (g),
  //! Iron (mg),
  //! Vitamin A (kIU),
  //! Vitamin B1 (mg),
  //! Vitamin B2 (mg),
  //! Niacin (mg),
  //! Vitamin C (mg)
  std::array<double, 9> nutrients;
};

std::vector<Commodity> data = {
    {"Wheat Flour (Enriched)",
     "10 lb.",
     36,
     {44.7, 1411, 2, 365, 0, 55.4, 33.3, 441, 0}},
    {"Macaroni", "1 lb.", 14.1, {11.6, 418, 0.7, 54, 0, 3.2, 1.9, 68, 0}},
    {"Wheat Cereal (Enriched)",
     "28 oz.",
     24.2,
     {11.8, 377, 14.4, 175, 0, 14.4, 8.8, 114, 0}},
    {"Corn Flakes", "8 oz.", 7.1, {11.4, 252, 0.1, 56, 0, 13.5, 2.3, 68, 0}},
    {"Corn Meal",
     "1 lb.",
     4.6,
     {36.0, 897, 1.7, 99, 30.9, 17.4, 7.9, 106, 0}},
    {"Hominy Grits",
     "24 oz.",
     8.5,
     {28.6, 680, 0.8, 80, 0, 10.6, 1.6, 110, 0}},
    {"Rice", "1 lb.", 7.5, {21.2, 460, 0.6, 41, 0, 2, 4.8, 60, 0}},
    {"Rolled Oats", "1 lb.", 7.1, {25.3, 907, 5.1, 341, 0, 37.1, 8.9, 64, 0}},
    {"White Bread (Enriched)",
     "1 lb.",
     7.9,
     {15.0, 488, 2.5, 115, 0, 13.8, 8.5, 126, 0}},
    {"Whole Wheat Bread",
     "1 lb.",
     9.1,
     {12.2, 484, 2.7, 125, 0, 13.9, 6.4, 160, 0}},
    {"Rye Bread", "1 lb.", 9.1, {12.4, 439, 1.1, 82, 0, 9.9, 3, 66, 0}},
    {"Pound Cake", "1 lb.", 24.8, {8.0, 130, 0.4, 31, 18.9, 2.8, 3, 17, 0}},
    {"Soda Crackers", "1 lb.", 15.1, {12.5, 288, 0.5, 50, 0, 0, 0, 0, 0}},
    {"Milk", "1 qt.", 11, {6.1, 310, 10.5, 18, 16.8, 4, 16, 7, 177}},
    {"Evaporated Milk (can)",
     "14.5 oz.",
     6.7,
     {8.4, 422, 15.1, 9, 26, 3, 23.5, 11, 60}},
    {"Butter", "1 lb.", 30.8, {10.8, 9, 0.2, 3, 44.2, 0, 0.2, 2, 0}},
    {"Oleomargarine", "1 lb.", 16.1, {20.6, 17, 0.6, 6, 55.8, 0.2, 0, 0, 0}},
    {"Eggs", "1 doz.", 32.6, {2.9, 238, 1.0, 52, 18.6, 2.8, 6.5, 1, 0}},
    {"Cheese (Cheddar)",
     "1 lb.",
     24.2,
     {7.4, 448, 16.4, 19, 28.1, 0.8, 10.3, 4, 0}},
    {"Cream", "1/2 pt.", 14.1, {3.5, 49, 1.7, 3, 16.9, 0.6, 2.5, 0, 17}},
    {"Peanut Butter",
     "1 lb.",
     17.9,
     {15.7, 661, 1.0, 48, 0, 9.6, 8.1, 471, 0}},
    {"Mayonnaise", "1/2 pt.", 16.7, {8.6, 18, 0.2, 8, 2.7, 0.4, 0.5, 0, 0}},
    {"Crisco", "1 lb.", 20.3, {20.1, 0, 0, 0, 0, 0, 0, 0, 0}},
    {"Lard", "1 lb.", 9.8, {41.7, 0, 0, 0, 0.2, 0, 0.5, 5, 0}},
    {"Sirloin Steak",
     "1 lb.",
     39.6,
     {2.9, 166, 0.1, 34, 0.2, 2.1, 2.9, 69, 0}},
    {"Round Steak", "1 lb.", 36.4, {2.2, 214, 0.1, 32, 0.4, 2.5, 2.4, 87, 0}},
    {"Rib Roast", "1 lb.", 29.2, {3.4, 213, 0.1, 33, 0, 0, 2, 0, 0}},
    {"Chuck Roast", "1 lb.", 22.6, {3.6, 309, 0.2, 46, 0.4, 1, 4, 120, 0}},
    {"Plate", "1 lb.", 14.6, {8.5, 404, 0.2, 62, 0, 0.9, 0, 0, 0}},
    {"Liver (Beef)",
     "1 lb.",
     26.8,
     {2.2, 333, 0.2, 139, 169.2, 6.4, 50.8, 316, 525}},
    {"Leg of Lamb", "1 lb.", 27.6, {3.1, 245, 0.1, 20, 0, 2.8, 3.9, 86, 0}},
    {"Lamb Chops (Rib)",
     "1 lb.",
     36.6,
     {3.3, 140, 0.1, 15, 0, 1.7, 2.7, 54, 0}},
    {"Pork Chops", "1 lb.", 30.7, {3.5, 196, 0.2, 30, 0, 17.4, 2.7, 60, 0}},
    {"Pork Loin Roast",
     "1 lb.",
     24.2,
     {4.4, 249, 0.3, 37, 0, 18.2, 3.6, 79, 0}},
    {"Bacon", "1 lb.", 25.6, {10.4, 152, 0.2, 23, 0, 1.8, 1.8, 71, 0}},
    {"Ham, smoked", "1 lb.", 27.4, {6.7, 212, 0.2, 31, 0, 9.9, 3.3, 50, 0}},
    {"Salt Pork", "1 lb.", 16, {18.8, 164, 0.1, 26, 0, 1.4, 1.8, 0, 0}},
    {"Roasting Chicken",
     "1 lb.",
     30.3,
     {1.8, 184, 0.1, 30, 0.1, 0.9, 1.8, 68, 46}},
    {"Veal Cutlets", "1 lb.", 42.3, {1.7, 156, 0.1, 24, 0, 1.4, 2.4, 57, 0}},
    {"Salmon, Pink (can)",
     "16 oz.",
     13,
     {5.8, 705, 6.8, 45, 3.5, 1, 4.9, 209, 0}},
    {"Apples", "1 lb.", 4.4, {5.8, 27, 0.5, 36, 7.3, 3.6, 2.7, 5, 544}},
    {"Bananas", "1 lb.", 6.1, {4.9, 60, 0.4, 30, 17.4, 2.5, 3.5, 28, 498}},
    {"Lemons", "1 doz.", 26, {1.0, 21, 0.5, 14, 0, 0.5, 0, 4, 952}},
    {"Oranges", "1 doz.", 30.9, {2.2, 40, 1.1, 18, 11.1, 3.6, 1.3, 10, 1998}},
    {"Green Beans", "1 lb.", 7.1, {2.4, 138, 3.7, 80, 69, 4.3, 5.8, 37, 862}},
    {"Cabbage", "1 lb.", 3.7, {2.6, 125, 4.0, 36, 7.2, 9, 4.5, 26, 5369}},
    {"Carrots", "1 bunch", 4.7, {2.7, 73, 2.8, 43, 188.5, 6.1, 4.3, 89, 608}},
    {"Celery", "1 stalk", 7.3, {0.9, 51, 3.0, 23, 0.9, 1.4, 1.4, 9, 313}},
    {"Lettuce", "1 head", 8.2, {0.4, 27, 1.1, 22, 112.4, 1.8, 3.4, 11, 449}},
    {"Onions", "1 lb.", 3.6, {5.8, 166, 3.8, 59, 16.6, 4.7, 5.9, 21, 1184}},
    {"Potatoes",
     "15 lb.",
     34,
     {14.3, 336, 1.8, 118, 6.7, 29.4, 7.1, 198, 2522}},
    {"Spinach", "1 lb.", 8.1, {1.1, 106, 0, 138, 918.4, 5.7, 13.8, 33, 2755}},
    {"Sweet Potatoes",
     "1 lb.",
     5.1,
     {9.6, 138, 2.7, 54, 290.7, 8.4, 5.4, 83, 1912}},
    {"Peaches (can)",
     "No. 2 1/2",
     16.8,
     {3.7, 20, 0.4, 10, 21.5, 0.5, 1, 31, 196}},
    {"Pears (can)",
     "No. 2 1/2",
     20.4,
     {3.0, 8, 0.3, 8, 0.8, 0.8, 0.8, 5, 81}},
    {"Pineapple (can)",
     "No. 2 1/2",
     21.3,
     {2.4, 16, 0.4, 8, 2, 2.8, 0.8, 7, 399}},
    {"Asparagus (can)",
     "No. 2",
     27.7,
     {0.4, 33, 0.3, 12, 16.3, 1.4, 2.1, 17, 272}},
    {"Green Beans (can)",
     "No. 2",
     10,
     {1.0, 54, 2, 65, 53.9, 1.6, 4.3, 32, 431}},
    {"Pork and Beans (can)",
     "16 oz.",
     7.1,
     {7.5, 364, 4, 134, 3.5, 8.3, 7.7, 56, 0}},
    {"Corn (can)", "No. 2", 10.4, {5.2, 136, 0.2, 16, 12, 1.6, 2.7, 42, 218}},
    {"Peas (can)",
     "No. 2",
     13.8,
     {2.3, 136, 0.6, 45, 34.9, 4.9, 2.5, 37, 370}},
    {"Tomatoes (can)",
     "No. 2",
     8.6,
     {1.3, 63, 0.7, 38, 53.2, 3.4, 2.5, 36, 1253}},
    {"Tomato Soup (can)",
     "10 1/2 oz.",
     7.6,
     {1.6, 71, 0.6, 43, 57.9, 3.5, 2.4, 67, 862}},
    {"Peaches, Dried",
     "1 lb.",
     15.7,
     {8.5, 87, 1.7, 173, 86.8, 1.2, 4.3, 55, 57}},
    {"Prunes, Dried",
     "1 lb.",
     9,
     {12.8, 99, 2.5, 154, 85.7, 3.9, 4.3, 65, 257}},
    {"Raisins, Dried",
     "15 oz.",
     9.4,
     {13.5, 104, 2.5, 136, 4.5, 6.3, 1.4, 24, 136}},
    {"Peas, Dried",
     "1 lb.",
     7.9,
     {20.0, 1367, 4.2, 345, 2.9, 28.7, 18.4, 162, 0}},
    {"Lima Beans, Dried",
     "1 lb.",
     8.9,
     {17.4, 1055, 3.7, 459, 5.1, 26.9, 38.2, 93, 0}},
    {"Navy Beans, Dried",
     "1 lb.",
     5.9,
     {26.9, 1691, 11.4, 792, 0, 38.4, 24.6, 217, 0}},
    {"Coffee", "1 lb.", 22.4, {0, 0, 0, 0, 0, 4, 5.1, 50, 0}},
    {"Tea", "1/4 lb.", 17.4, {0, 0, 0, 0, 0, 0, 2.3, 42, 0}},
    {"Cocoa", "8 oz.", 8.6, {8.7, 237, 3, 72, 0, 2, 11.9, 40, 0}},
    {"Chocolate", "8 oz.", 16.2, {8.0, 77, 1.3, 39, 0, 0.9, 3.4, 14, 0}},
    {"Sugar", "10 lb.", 51.7, {34.9, 0, 0, 0, 0, 0, 0, 0, 0}},
    {"Corn Syrup", "24 oz.", 13.7, {14.7, 0, 0.5, 74, 0, 0, 0, 5, 0}},
    {"Molasses", "18 oz.", 13.6, {9.0, 0, 10.3, 244, 0, 1.9, 7.5, 146, 0}},
    {"Strawberry Preserves",
     "1 lb.",
     20.5,
     {6.4, 11, 0.4, 7, 0.2, 0.2, 0.4, 3, 0}}};
```

```
// Nutrient minimums.
List<Object[]> nutrients = new ArrayList<>();
nutrients.add(new Object[] {"Calories (kcal)", 3.0});
nutrients.add(new Object[] {"Protein (g)", 70.0});
nutrients.add(new Object[] {"Calcium (g)", 0.8});
nutrients.add(new Object[] {"Iron (mg)", 12.0});
nutrients.add(new Object[] {"Vitamin A (kIU)", 5.0});
nutrients.add(new Object[] {"Vitamin B1 (mg)", 1.8});
nutrients.add(new Object[] {"Vitamin B2 (mg)", 2.7});
nutrients.add(new Object[] {"Niacin (mg)", 18.0});
nutrients.add(new Object[] {"Vitamin C (mg)", 75.0});

List<Object[]> data = new ArrayList<>();
data.add(new Object[] {"Wheat Flour (Enriched)", "10 lb.", 36,
    new double[] {44.7, 1411, 2, 365, 0, 55.4, 33.3, 441, 0}});
data.add(new Object[] {
    "Macaroni", "1 lb.", 14.1, new double[] {11.6, 418, 0.7, 54, 0, 3.2, 1.9, 68, 0}});
data.add(new Object[] {"Wheat Cereal (Enriched)", "28 oz.", 24.2,
    new double[] {11.8, 377, 14.4, 175, 0, 14.4, 8.8, 114, 0}});
data.add(new Object[] {
    "Corn Flakes", "8 oz.", 7.1, new double[] {11.4, 252, 0.1, 56, 0, 13.5, 2.3, 68, 0}});
data.add(new Object[] {
    "Corn Meal", "1 lb.", 4.6, new double[] {36.0, 897, 1.7, 99, 30.9, 17.4, 7.9, 106, 0}});
data.add(new Object[] {
    "Hominy Grits", "24 oz.", 8.5, new double[] {28.6, 680, 0.8, 80, 0, 10.6, 1.6, 110, 0}});
data.add(
    new Object[] {"Rice", "1 lb.", 7.5, new double[] {21.2, 460, 0.6, 41, 0, 2, 4.8, 60, 0}});
data.add(new Object[] {
    "Rolled Oats", "1 lb.", 7.1, new double[] {25.3, 907, 5.1, 341, 0, 37.1, 8.9, 64, 0}});
data.add(new Object[] {"White Bread (Enriched)", "1 lb.", 7.9,
    new double[] {15.0, 488, 2.5, 115, 0, 13.8, 8.5, 126, 0}});
data.add(new Object[] {"Whole Wheat Bread", "1 lb.", 9.1,
    new double[] {12.2, 484, 2.7, 125, 0, 13.9, 6.4, 160, 0}});
data.add(new Object[] {
    "Rye Bread", "1 lb.", 9.1, new double[] {12.4, 439, 1.1, 82, 0, 9.9, 3, 66, 0}});
data.add(new Object[] {
    "Pound Cake", "1 lb.", 24.8, new double[] {8.0, 130, 0.4, 31, 18.9, 2.8, 3, 17, 0}});
data.add(new Object[] {
    "Soda Crackers", "1 lb.", 15.1, new double[] {12.5, 288, 0.5, 50, 0, 0, 0, 0, 0}});
data.add(
    new Object[] {"Milk", "1 qt.", 11, new double[] {6.1, 310, 10.5, 18, 16.8, 4, 16, 7, 177}});
data.add(new Object[] {"Evaporated Milk (can)", "14.5 oz.", 6.7,
    new double[] {8.4, 422, 15.1, 9, 26, 3, 23.5, 11, 60}});
data.add(
    new Object[] {"Butter", "1 lb.", 30.8, new double[] {10.8, 9, 0.2, 3, 44.2, 0, 0.2, 2, 0}});
data.add(new Object[] {
    "Oleomargarine", "1 lb.", 16.1, new double[] {20.6, 17, 0.6, 6, 55.8, 0.2, 0, 0, 0}});
data.add(new Object[] {
    "Eggs", "1 doz.", 32.6, new double[] {2.9, 238, 1.0, 52, 18.6, 2.8, 6.5, 1, 0}});
data.add(new Object[] {"Cheese (Cheddar)", "1 lb.", 24.2,
    new double[] {7.4, 448, 16.4, 19, 28.1, 0.8, 10.3, 4, 0}});
data.add(new Object[] {
    "Cream", "1/2 pt.", 14.1, new double[] {3.5, 49, 1.7, 3, 16.9, 0.6, 2.5, 0, 17}});
data.add(new Object[] {
    "Peanut Butter", "1 lb.", 17.9, new double[] {15.7, 661, 1.0, 48, 0, 9.6, 8.1, 471, 0}});
data.add(new Object[] {
    "Mayonnaise", "1/2 pt.", 16.7, new double[] {8.6, 18, 0.2, 8, 2.7, 0.4, 0.5, 0, 0}});
data.add(new Object[] {"Crisco", "1 lb.", 20.3, new double[] {20.1, 0, 0, 0, 0, 0, 0, 0, 0}});
data.add(new Object[] {"Lard", "1 lb.", 9.8, new double[] {41.7, 0, 0, 0, 0.2, 0, 0.5, 5, 0}});
data.add(new Object[] {
    "Sirloin Steak", "1 lb.", 39.6, new double[] {2.9, 166, 0.1, 34, 0.2, 2.1, 2.9, 69, 0}});
data.add(new Object[] {
    "Round Steak", "1 lb.", 36.4, new double[] {2.2, 214, 0.1, 32, 0.4, 2.5, 2.4, 87, 0}});
data.add(
    new Object[] {"Rib Roast", "1 lb.", 29.2, new double[] {3.4, 213, 0.1, 33, 0, 0, 2, 0, 0}});
data.add(new Object[] {
    "Chuck Roast", "1 lb.", 22.6, new double[] {3.6, 309, 0.2, 46, 0.4, 1, 4, 120, 0}});
data.add(
    new Object[] {"Plate", "1 lb.", 14.6, new double[] {8.5, 404, 0.2, 62, 0, 0.9, 0, 0, 0}});
data.add(new Object[] {"Liver (Beef)", "1 lb.", 26.8,
    new double[] {2.2, 333, 0.2, 139, 169.2, 6.4, 50.8, 316, 525}});
data.add(new Object[] {
    "Leg of Lamb", "1 lb.", 27.6, new double[] {3.1, 245, 0.1, 20, 0, 2.8, 3.9, 86, 0}});
data.add(new Object[] {
    "Lamb Chops (Rib)", "1 lb.", 36.6, new double[] {3.3, 140, 0.1, 15, 0, 1.7, 2.7, 54, 0}});
data.add(new Object[] {
    "Pork Chops", "1 lb.", 30.7, new double[] {3.5, 196, 0.2, 30, 0, 17.4, 2.7, 60, 0}});
data.add(new Object[] {
    "Pork Loin Roast", "1 lb.", 24.2, new double[] {4.4, 249, 0.3, 37, 0, 18.2, 3.6, 79, 0}});
data.add(new Object[] {
    "Bacon", "1 lb.", 25.6, new double[] {10.4, 152, 0.2, 23, 0, 1.8, 1.8, 71, 0}});
data.add(new Object[] {
    "Ham, smoked", "1 lb.", 27.4, new double[] {6.7, 212, 0.2, 31, 0, 9.9, 3.3, 50, 0}});
data.add(new Object[] {
    "Salt Pork", "1 lb.", 16, new double[] {18.8, 164, 0.1, 26, 0, 1.4, 1.8, 0, 0}});
data.add(new Object[] {"Roasting Chicken", "1 lb.", 30.3,
    new double[] {1.8, 184, 0.1, 30, 0.1, 0.9, 1.8, 68, 46}});
data.add(new Object[] {
    "Veal Cutlets", "1 lb.", 42.3, new double[] {1.7, 156, 0.1, 24, 0, 1.4, 2.4, 57, 0}});
data.add(new Object[] {
    "Salmon, Pink (can)", "16 oz.", 13, new double[] {5.8, 705, 6.8, 45, 3.5, 1, 4.9, 209, 0}});
data.add(new Object[] {
    "Apples", "1 lb.", 4.4, new double[] {5.8, 27, 0.5, 36, 7.3, 3.6, 2.7, 5, 544}});
data.add(new Object[] {
    "Bananas", "1 lb.", 6.1, new double[] {4.9, 60, 0.4, 30, 17.4, 2.5, 3.5, 28, 498}});
data.add(
    new Object[] {"Lemons", "1 doz.", 26, new double[] {1.0, 21, 0.5, 14, 0, 0.5, 0, 4, 952}});
data.add(new Object[] {
    "Oranges", "1 doz.", 30.9, new double[] {2.2, 40, 1.1, 18, 11.1, 3.6, 1.3, 10, 1998}});
data.add(new Object[] {
    "Green Beans", "1 lb.", 7.1, new double[] {2.4, 138, 3.7, 80, 69, 4.3, 5.8, 37, 862}});
data.add(new Object[] {
    "Cabbage", "1 lb.", 3.7, new double[] {2.6, 125, 4.0, 36, 7.2, 9, 4.5, 26, 5369}});
data.add(new Object[] {
    "Carrots", "1 bunch", 4.7, new double[] {2.7, 73, 2.8, 43, 188.5, 6.1, 4.3, 89, 608}});
data.add(new Object[] {
    "Celery", "1 stalk", 7.3, new double[] {0.9, 51, 3.0, 23, 0.9, 1.4, 1.4, 9, 313}});
data.add(new Object[] {
    "Lettuce", "1 head", 8.2, new double[] {0.4, 27, 1.1, 22, 112.4, 1.8, 3.4, 11, 449}});
data.add(new Object[] {
    "Onions", "1 lb.", 3.6, new double[] {5.8, 166, 3.8, 59, 16.6, 4.7, 5.9, 21, 1184}});
data.add(new Object[] {
    "Potatoes", "15 lb.", 34, new double[] {14.3, 336, 1.8, 118, 6.7, 29.4, 7.1, 198, 2522}});
data.add(new Object[] {
    "Spinach", "1 lb.", 8.1, new double[] {1.1, 106, 0, 138, 918.4, 5.7, 13.8, 33, 2755}});
data.add(new Object[] {"Sweet Potatoes", "1 lb.", 5.1,
    new double[] {9.6, 138, 2.7, 54, 290.7, 8.4, 5.4, 83, 1912}});
data.add(new Object[] {"Peaches (can)", "No. 2 1/2", 16.8,
    new double[] {3.7, 20, 0.4, 10, 21.5, 0.5, 1, 31, 196}});
data.add(new Object[] {
    "Pears (can)", "No. 2 1/2", 20.4, new double[] {3.0, 8, 0.3, 8, 0.8, 0.8, 0.8, 5, 81}});
data.add(new Object[] {
    "Pineapple (can)", "No. 2 1/2", 21.3, new double[] {2.4, 16, 0.4, 8, 2, 2.8, 0.8, 7, 399}});
data.add(new Object[] {"Asparagus (can)", "No. 2", 27.7,
    new double[] {0.4, 33, 0.3, 12, 16.3, 1.4, 2.1, 17, 272}});
data.add(new Object[] {
    "Green Beans (can)", "No. 2", 10, new double[] {1.0, 54, 2, 65, 53.9, 1.6, 4.3, 32, 431}});
data.add(new Object[] {"Pork and Beans (can)", "16 oz.", 7.1,
    new double[] {7.5, 364, 4, 134, 3.5, 8.3, 7.7, 56, 0}});
data.add(new Object[] {
    "Corn (can)", "No. 2", 10.4, new double[] {5.2, 136, 0.2, 16, 12, 1.6, 2.7, 42, 218}});
data.add(new Object[] {
    "Peas (can)", "No. 2", 13.8, new double[] {2.3, 136, 0.6, 45, 34.9, 4.9, 2.5, 37, 370}});
data.add(new Object[] {
    "Tomatoes (can)", "No. 2", 8.6, new double[] {1.3, 63, 0.7, 38, 53.2, 3.4, 2.5, 36, 1253}});
data.add(new Object[] {"Tomato Soup (can)", "10 1/2 oz.", 7.6,
    new double[] {1.6, 71, 0.6, 43, 57.9, 3.5, 2.4, 67, 862}});
data.add(new Object[] {
    "Peaches, Dried", "1 lb.", 15.7, new double[] {8.5, 87, 1.7, 173, 86.8, 1.2, 4.3, 55, 57}});
data.add(new Object[] {
    "Prunes, Dried", "1 lb.", 9, new double[] {12.8, 99, 2.5, 154, 85.7, 3.9, 4.3, 65, 257}});
data.add(new Object[] {"Raisins, Dried", "15 oz.", 9.4,
    new double[] {13.5, 104, 2.5, 136, 4.5, 6.3, 1.4, 24, 136}});
data.add(new Object[] {
    "Peas, Dried", "1 lb.", 7.9, new double[] {20.0, 1367, 4.2, 345, 2.9, 28.7, 18.4, 162, 0}});
data.add(new Object[] {"Lima Beans, Dried", "1 lb.", 8.9,
    new double[] {17.4, 1055, 3.7, 459, 5.1, 26.9, 38.2, 93, 0}});
data.add(new Object[] {"Navy Beans, Dried", "1 lb.", 5.9,
    new double[] {26.9, 1691, 11.4, 792, 0, 38.4, 24.6, 217, 0}});
data.add(new Object[] {"Coffee", "1 lb.", 22.4, new double[] {0, 0, 0, 0, 0, 4, 5.1, 50, 0}});
data.add(new Object[] {"Tea", "1/4 lb.", 17.4, new double[] {0, 0, 0, 0, 0, 0, 2.3, 42, 0}});
data.add(
    new Object[] {"Cocoa", "8 oz.", 8.6, new double[] {8.7, 237, 3, 72, 0, 2, 11.9, 40, 0}});
data.add(new Object[] {
    "Chocolate", "8 oz.", 16.2, new double[] {8.0, 77, 1.3, 39, 0, 0.9, 3.4, 14, 0}});
data.add(new Object[] {"Sugar", "10 lb.", 51.7, new double[] {34.9, 0, 0, 0, 0, 0, 0, 0, 0}});
data.add(new Object[] {
    "Corn Syrup", "24 oz.", 13.7, new double[] {14.7, 0, 0.5, 74, 0, 0, 0, 5, 0}});
data.add(new Object[] {
    "Molasses", "18 oz.", 13.6, new double[] {9.0, 0, 10.3, 244, 0, 1.9, 7.5, 146, 0}});
data.add(new Object[] {"Strawberry Preserves", "1 lb.", 20.5,
    new double[] {6.4, 11, 0.4, 7, 0.2, 0.2, 0.4, 3, 0}});
```

```
// Nutrient minimums.
(String Name, double Value)[] nutrients =
    new[] { ("Calories (kcal)", 3.0), ("Protein (g)", 70.0),    ("Calcium (g)", 0.8),
            ("Iron (mg)", 12.0),      ("Vitamin A (kIU)", 5.0), ("Vitamin B1 (mg)", 1.8),
            ("Vitamin B2 (mg)", 2.7), ("Niacin (mg)", 18.0),    ("Vitamin C (mg)", 75.0) };

(String Name, String Unit, double Price, double[] Nutrients)[] data = new[] {
    ("Wheat Flour (Enriched)", "10 lb.", 36, new double[] { 44.7, 1411, 2, 365, 0, 55.4, 33.3, 441, 0 }),
    ("Macaroni", "1 lb.", 14.1, new double[] { 11.6, 418, 0.7, 54, 0, 3.2, 1.9, 68, 0 }),
    ("Wheat Cereal (Enriched)", "28 oz.", 24.2, new double[] { 11.8, 377, 14.4, 175, 0, 14.4, 8.8, 114, 0 }),
    ("Corn Flakes", "8 oz.", 7.1, new double[] { 11.4, 252, 0.1, 56, 0, 13.5, 2.3, 68, 0 }),
    ("Corn Meal", "1 lb.", 4.6, new double[] { 36.0, 897, 1.7, 99, 30.9, 17.4, 7.9, 106, 0 }),
    ("Hominy Grits", "24 oz.", 8.5, new double[] { 28.6, 680, 0.8, 80, 0, 10.6, 1.6, 110, 0 }),
    ("Rice", "1 lb.", 7.5, new double[] { 21.2, 460, 0.6, 41, 0, 2, 4.8, 60, 0 }),
    ("Rolled Oats", "1 lb.", 7.1, new double[] { 25.3, 907, 5.1, 341, 0, 37.1, 8.9, 64, 0 }),
    ("White Bread (Enriched)", "1 lb.", 7.9, new double[] { 15.0, 488, 2.5, 115, 0, 13.8, 8.5, 126, 0 }),
    ("Whole Wheat Bread", "1 lb.", 9.1, new double[] { 12.2, 484, 2.7, 125, 0, 13.9, 6.4, 160, 0 }),
    ("Rye Bread", "1 lb.", 9.1, new double[] { 12.4, 439, 1.1, 82, 0, 9.9, 3, 66, 0 }),
    ("Pound Cake", "1 lb.", 24.8, new double[] { 8.0, 130, 0.4, 31, 18.9, 2.8, 3, 17, 0 }),
    ("Soda Crackers", "1 lb.", 15.1, new double[] { 12.5, 288, 0.5, 50, 0, 0, 0, 0, 0 }),
    ("Milk", "1 qt.", 11, new double[] { 6.1, 310, 10.5, 18, 16.8, 4, 16, 7, 177 }),
    ("Evaporated Milk (can)", "14.5 oz.", 6.7, new double[] { 8.4, 422, 15.1, 9, 26, 3, 23.5, 11, 60 }),
    ("Butter", "1 lb.", 30.8, new double[] { 10.8, 9, 0.2, 3, 44.2, 0, 0.2, 2, 0 }),
    ("Oleomargarine", "1 lb.", 16.1, new double[] { 20.6, 17, 0.6, 6, 55.8, 0.2, 0, 0, 0 }),
    ("Eggs", "1 doz.", 32.6, new double[] { 2.9, 238, 1.0, 52, 18.6, 2.8, 6.5, 1, 0 }),
    ("Cheese (Cheddar)", "1 lb.", 24.2, new double[] { 7.4, 448, 16.4, 19, 28.1, 0.8, 10.3, 4, 0 }),
    ("Cream", "1/2 pt.", 14.1, new double[] { 3.5, 49, 1.7, 3, 16.9, 0.6, 2.5, 0, 17 }),
    ("Peanut Butter", "1 lb.", 17.9, new double[] { 15.7, 661, 1.0, 48, 0, 9.6, 8.1, 471, 0 }),
    ("Mayonnaise", "1/2 pt.", 16.7, new double[] { 8.6, 18, 0.2, 8, 2.7, 0.4, 0.5, 0, 0 }),
    ("Crisco", "1 lb.", 20.3, new double[] { 20.1, 0, 0, 0, 0, 0, 0, 0, 0 }),
    ("Lard", "1 lb.", 9.8, new double[] { 41.7, 0, 0, 0, 0.2, 0, 0.5, 5, 0 }),
    ("Sirloin Steak", "1 lb.", 39.6, new double[] { 2.9, 166, 0.1, 34, 0.2, 2.1, 2.9, 69, 0 }),
    ("Round Steak", "1 lb.", 36.4, new double[] { 2.2, 214, 0.1, 32, 0.4, 2.5, 2.4, 87, 0 }),
    ("Rib Roast", "1 lb.", 29.2, new double[] { 3.4, 213, 0.1, 33, 0, 0, 2, 0, 0 }),
    ("Chuck Roast", "1 lb.", 22.6, new double[] { 3.6, 309, 0.2, 46, 0.4, 1, 4, 120, 0 }),
    ("Plate", "1 lb.", 14.6, new double[] { 8.5, 404, 0.2, 62, 0, 0.9, 0, 0, 0 }),
    ("Liver (Beef)", "1 lb.", 26.8, new double[] { 2.2, 333, 0.2, 139, 169.2, 6.4, 50.8, 316, 525 }),
    ("Leg of Lamb", "1 lb.", 27.6, new double[] { 3.1, 245, 0.1, 20, 0, 2.8, 3.9, 86, 0 }),
    ("Lamb Chops (Rib)", "1 lb.", 36.6, new double[] { 3.3, 140, 0.1, 15, 0, 1.7, 2.7, 54, 0 }),
    ("Pork Chops", "1 lb.", 30.7, new double[] { 3.5, 196, 0.2, 30, 0, 17.4, 2.7, 60, 0 }),
    ("Pork Loin Roast", "1 lb.", 24.2, new double[] { 4.4, 249, 0.3, 37, 0, 18.2, 3.6, 79, 0 }),
    ("Bacon", "1 lb.", 25.6, new double[] { 10.4, 152, 0.2, 23, 0, 1.8, 1.8, 71, 0 }),
    ("Ham, smoked", "1 lb.", 27.4, new double[] { 6.7, 212, 0.2, 31, 0, 9.9, 3.3, 50, 0 }),
    ("Salt Pork", "1 lb.", 16, new double[] { 18.8, 164, 0.1, 26, 0, 1.4, 1.8, 0, 0 }),
    ("Roasting Chicken", "1 lb.", 30.3, new double[] { 1.8, 184, 0.1, 30, 0.1, 0.9, 1.8, 68, 46 }),
    ("Veal Cutlets", "1 lb.", 42.3, new double[] { 1.7, 156, 0.1, 24, 0, 1.4, 2.4, 57, 0 }),
    ("Salmon, Pink (can)", "16 oz.", 13, new double[] { 5.8, 705, 6.8, 45, 3.5, 1, 4.9, 209, 0 }),
    ("Apples", "1 lb.", 4.4, new double[] { 5.8, 27, 0.5, 36, 7.3, 3.6, 2.7, 5, 544 }),
    ("Bananas", "1 lb.", 6.1, new double[] { 4.9, 60, 0.4, 30, 17.4, 2.5, 3.5, 28, 498 }),
    ("Lemons", "1 doz.", 26, new double[] { 1.0, 21, 0.5, 14, 0, 0.5, 0, 4, 952 }),
    ("Oranges", "1 doz.", 30.9, new double[] { 2.2, 40, 1.1, 18, 11.1, 3.6, 1.3, 10, 1998 }),
    ("Green Beans", "1 lb.", 7.1, new double[] { 2.4, 138, 3.7, 80, 69, 4.3, 5.8, 37, 862 }),
    ("Cabbage", "1 lb.", 3.7, new double[] { 2.6, 125, 4.0, 36, 7.2, 9, 4.5, 26, 5369 }),
    ("Carrots", "1 bunch", 4.7, new double[] { 2.7, 73, 2.8, 43, 188.5, 6.1, 4.3, 89, 608 }),
    ("Celery", "1 stalk", 7.3, new double[] { 0.9, 51, 3.0, 23, 0.9, 1.4, 1.4, 9, 313 }),
    ("Lettuce", "1 head", 8.2, new double[] { 0.4, 27, 1.1, 22, 112.4, 1.8, 3.4, 11, 449 }),
    ("Onions", "1 lb.", 3.6, new double[] { 5.8, 166, 3.8, 59, 16.6, 4.7, 5.9, 21, 1184 }),
    ("Potatoes", "15 lb.", 34, new double[] { 14.3, 336, 1.8, 118, 6.7, 29.4, 7.1, 198, 2522 }),
    ("Spinach", "1 lb.", 8.1, new double[] { 1.1, 106, 0, 138, 918.4, 5.7, 13.8, 33, 2755 }),
    ("Sweet Potatoes", "1 lb.", 5.1, new double[] { 9.6, 138, 2.7, 54, 290.7, 8.4, 5.4, 83, 1912 }),
    ("Peaches (can)", "No. 2 1/2", 16.8, new double[] { 3.7, 20, 0.4, 10, 21.5, 0.5, 1, 31, 196 }),
    ("Pears (can)", "No. 2 1/2", 20.4, new double[] { 3.0, 8, 0.3, 8, 0.8, 0.8, 0.8, 5, 81 }),
    ("Pineapple (can)", "No. 2 1/2", 21.3, new double[] { 2.4, 16, 0.4, 8, 2, 2.8, 0.8, 7, 399 }),
    ("Asparagus (can)", "No. 2", 27.7, new double[] { 0.4, 33, 0.3, 12, 16.3, 1.4, 2.1, 17, 272 }),
    ("Green Beans (can)", "No. 2", 10, new double[] { 1.0, 54, 2, 65, 53.9, 1.6, 4.3, 32, 431 }),
    ("Pork and Beans (can)", "16 oz.", 7.1, new double[] { 7.5, 364, 4, 134, 3.5, 8.3, 7.7, 56, 0 }),
    ("Corn (can)", "No. 2", 10.4, new double[] { 5.2, 136, 0.2, 16, 12, 1.6, 2.7, 42, 218 }),
    ("Peas (can)", "No. 2", 13.8, new double[] { 2.3, 136, 0.6, 45, 34.9, 4.9, 2.5, 37, 370 }),
    ("Tomatoes (can)", "No. 2", 8.6, new double[] { 1.3, 63, 0.7, 38, 53.2, 3.4, 2.5, 36, 1253 }),
    ("Tomato Soup (can)", "10 1/2 oz.", 7.6, new double[] { 1.6, 71, 0.6, 43, 57.9, 3.5, 2.4, 67, 862 }),
    ("Peaches, Dried", "1 lb.", 15.7, new double[] { 8.5, 87, 1.7, 173, 86.8, 1.2, 4.3, 55, 57 }),
    ("Prunes, Dried", "1 lb.", 9, new double[] { 12.8, 99, 2.5, 154, 85.7, 3.9, 4.3, 65, 257 }),
    ("Raisins, Dried", "15 oz.", 9.4, new double[] { 13.5, 104, 2.5, 136, 4.5, 6.3, 1.4, 24, 136 }),
    ("Peas, Dried", "1 lb.", 7.9, new double[] { 20.0, 1367, 4.2, 345, 2.9, 28.7, 18.4, 162, 0 }),
    ("Lima Beans, Dried", "1 lb.", 8.9, new double[] { 17.4, 1055, 3.7, 459, 5.1, 26.9, 38.2, 93, 0 }),
    ("Navy Beans, Dried", "1 lb.", 5.9, new double[] { 26.9, 1691, 11.4, 792, 0, 38.4, 24.6, 217, 0 }),
    ("Coffee", "1 lb.", 22.4, new double[] { 0, 0, 0, 0, 0, 4, 5.1, 50, 0 }),
    ("Tea", "1/4 lb.", 17.4, new double[] { 0, 0, 0, 0, 0, 0, 2.3, 42, 0 }),
    ("Cocoa", "8 oz.", 8.6, new double[] { 8.7, 237, 3, 72, 0, 2, 11.9, 40, 0 }),
    ("Chocolate", "8 oz.", 16.2, new double[] { 8.0, 77, 1.3, 39, 0, 0.9, 3.4, 14, 0 }),
    ("Sugar", "10 lb.", 51.7, new double[] { 34.9, 0, 0, 0, 0, 0, 0, 0, 0 }),
    ("Corn Syrup", "24 oz.", 13.7, new double[] { 14.7, 0, 0.5, 74, 0, 0, 0, 5, 0 }),
    ("Molasses", "18 oz.", 13.6, new double[] { 9.0, 0, 10.3, 244, 0, 1.9, 7.5, 146, 0 }),
    ("Strawberry Preserves", "1 lb.", 20.5, new double[] { 6.4, 11, 0.4, 7, 0.2, 0.2, 0.4, 3, 0 })
};
```

### Declare the LP solver

The following code instantiates the `MPsolver` wrapper.

[Python](https://developers.google.com/optimization/lp/stigler_diet#python)[C++](https://developers.google.com/optimization/lp/stigler_diet#c++)[Java](https://developers.google.com/optimization/lp/stigler_diet#java)[C#](https://developers.google.com/optimization/lp/stigler_diet#c)More

```
# Instantiate a Glop solver and naming it.
solver = pywraplp.Solver.CreateSolver("GLOP")
if not solver:
    return
```

```
// Create the linear solver with the GLOP backend.
std::unique_ptr<MPSolver> solver(MPSolver::CreateSolver("GLOP"));
```

```
// Create the linear solver with the GLOP backend.
MPSolver solver = MPSolver.createSolver("GLOP");
if (solver == null) {
  System.out.println("Could not create solver GLOP");
  return;
}
```

```
// Create the linear solver with the GLOP backend.
Solver solver = Solver.CreateSolver("GLOP");
if (solver is null)
{
    return;
}
```

### Create the variables

The following code creates the variables for the problem.

[Python](https://developers.google.com/optimization/lp/stigler_diet#python)[C++](https://developers.google.com/optimization/lp/stigler_diet#c++)[Java](https://developers.google.com/optimization/lp/stigler_diet#java)[C#](https://developers.google.com/optimization/lp/stigler_diet#c)More

```
# Declare an array to hold our variables.
foods = [solver.NumVar(0.0, solver.infinity(), item[0]) for item in data]

print("Number of variables =", solver.NumVariables())
```

```
std::vector<MPVariable*> foods;
const double infinity = solver->infinity();
foods.reserve(data.size());
for (const Commodity& commodity : data) {
  foods.push_back(solver->MakeNumVar(0.0, infinity, commodity.name));
}
LOG(INFO) << "Number of variables = " << solver->NumVariables();
```

```
double infinity = java.lang.Double.POSITIVE_INFINITY;
List<MPVariable> foods = new ArrayList<>();
for (int i = 0; i < data.size(); ++i) {
  foods.add(solver.makeNumVar(0.0, infinity, (String) data.get(i)[0]));
}
System.out.println("Number of variables = " + solver.numVariables());
```

```
List<Variable> foods = new List<Variable>();
for (int i = 0; i < data.Length; ++i)
{
    foods.Add(solver.MakeNumVar(0.0, double.PositiveInfinity, data[i].Name));
}
Console.WriteLine($"Number of variables = {solver.NumVariables()}");
```

The method
[`MPSolver::MakeNumVar`](https://or-tools.github.io/docs/cpp/classoperations__research_1_1MPSolver.html)
creates one variable, `food[i]`, for each row of the table.
As mentioned previously, the nutritional data is per dollar, so `food[i]` is the
amount of money to spend on commodity `i`.

### Define the constraints

The constraints for Stigler diet require the total amount of the nutrients
provided by all foods to be at least the minimum requirement for each nutrient.
Next, we write these constraints as inequalities involving the arrays `data` and
`nutrients`, and the variables `food[i]`.

First, the amount of nutrient `i` provided by food `j` per dollar is
`data[j][i+3]` (we add 3 to the column index because the nutrient data begins in
the fourth column of `data`.) Since the amount of money to be spent on food `j`
is `food[j]`, the amount of nutrient `i` provided by food `j` is
\\(data\[j\]\[i+3\] \\cdot food\[j\]\\).
Finally, since the minimum requirement for nutrient `i` is `nutrients[i][1]`, we
can write constraint i as follows:

\\(
\\sum\_{j} data\[j\]\[i+3\] \\cdot food\[j\] \\geq nutrients\[i\]\[1\] \\;\\;\\;\\;\\; (1)
\\)

The following code defines these constraints.

[Python](https://developers.google.com/optimization/lp/stigler_diet#python)[C++](https://developers.google.com/optimization/lp/stigler_diet#c++)[Java](https://developers.google.com/optimization/lp/stigler_diet#java)[C#](https://developers.google.com/optimization/lp/stigler_diet#c)More

```
# Create the constraints, one per nutrient.
constraints = []
for i, nutrient in enumerate(nutrients):
    constraints.append(solver.Constraint(nutrient[1], solver.infinity()))
    for j, item in enumerate(data):
        constraints[i].SetCoefficient(foods[j], item[i + 3])

print("Number of constraints =", solver.NumConstraints())
```

```
// Create the constraints, one per nutrient.
std::vector<MPConstraint*> constraints;
for (std::size_t i = 0; i < nutrients.size(); ++i) {
  constraints.push_back(
      solver->MakeRowConstraint(nutrients[i].second, infinity));
  for (std::size_t j = 0; j < data.size(); ++j) {
    constraints.back()->SetCoefficient(foods[j], data[j].nutrients[i]);
  }
}
LOG(INFO) << "Number of constraints = " << solver->NumConstraints();
```

```
MPConstraint[] constraints = new MPConstraint[nutrients.size()];
for (int i = 0; i < nutrients.size(); ++i) {
  constraints[i] = solver.makeConstraint(
      (double) nutrients.get(i)[1], infinity, (String) nutrients.get(i)[0]);
  for (int j = 0; j < data.size(); ++j) {
    constraints[i].setCoefficient(foods.get(j), ((double[]) data.get(j)[3])[i]);
  }
  // constraints.add(constraint);
}
System.out.println("Number of constraints = " + solver.numConstraints());
```

```
List<Constraint> constraints = new List<Constraint>();
for (int i = 0; i < nutrients.Length; ++i)
{
    Constraint constraint =
        solver.MakeConstraint(nutrients[i].Value, double.PositiveInfinity, nutrients[i].Name);
    for (int j = 0; j < data.Length; ++j)
    {
        constraint.SetCoefficient(foods[j], data[j].Nutrients[i]);
    }
    constraints.Add(constraint);
}
Console.WriteLine($"Number of constraints = {solver.NumConstraints()}");
```

The Python method `Constraint` (corresponding to the C++ method
[`MPSolver::MakeRowConstraint`](https://or-tools.github.io/docs/cpp/classoperations__research_1_1MPSolver.html)
) creates the constraints for the problem. For each
`i`, `constraint(nutrients[i][1], solver.infinity)`

This creates a constraint in which a linear combination of the variables
`food[j]` (defined next) is greater than or equal to `nutrients[i][1]`.
The coefficients of the linear expression are defined by the method
[`MPConstraint::SetCoefficient`](https://or-tools.github.io/docs/cpp/classoperations__research_1_1MPConstraint.html)
as follows: `SetCoefficient(food[j], data[j][i+3]`

This sets the coefficient of `food[j]` to be `data[j][i+3]`.

Putting this all together, the code defines the constraints expressed in (1)
above.

### Create the objective

The following code defines the objective function for the problem.

[Python](https://developers.google.com/optimization/lp/stigler_diet#python)[C++](https://developers.google.com/optimization/lp/stigler_diet#c++)[Java](https://developers.google.com/optimization/lp/stigler_diet#java)[C#](https://developers.google.com/optimization/lp/stigler_diet#c)More

```
# Objective function: Minimize the sum of (price-normalized) foods.
objective = solver.Objective()
for food in foods:
    objective.SetCoefficient(food, 1)
objective.SetMinimization()
```

```
MPObjective* const objective = solver->MutableObjective();
for (size_t i = 0; i < data.size(); ++i) {
  objective->SetCoefficient(foods[i], 1);
}
objective->SetMinimization();
```

```
MPObjective objective = solver.objective();
for (int i = 0; i < data.size(); ++i) {
  objective.setCoefficient(foods.get(i), 1);
}
objective.setMinimization();
```

```
Objective objective = solver.Objective();
for (int i = 0; i < data.Length; ++i)
{
    objective.SetCoefficient(foods[i], 1);
}
objective.SetMinimization();
```

The objective function is the total cost of the food, which is the sum of the
variables `food[i]`.

The method
[`MPObjective::SetCoefficient`](https://or-tools.github.io/docs/cpp/classoperations__research_1_1MPObjective.html)
sets the coefficients of the objective function, which are all `1` in this case.
Finally, the
[`MPObjective::SetMinimization`](https://or-tools.github.io/docs/cpp/classoperations__research_1_1MPObjective.html)
declares this to be a minimization problem.

### Invoke the solver

The following code invokes the solver.

[Python](https://developers.google.com/optimization/lp/stigler_diet#python)[C++](https://developers.google.com/optimization/lp/stigler_diet#c++)[Java](https://developers.google.com/optimization/lp/stigler_diet#java)[C#](https://developers.google.com/optimization/lp/stigler_diet#c)More

```
print(f"Solving with {solver.SolverVersion()}")
status = solver.Solve()
```

```
const MPSolver::ResultStatus result_status = solver->Solve();
```

```
final MPSolver.ResultStatus resultStatus = solver.solve();
```

```
Solver.ResultStatus resultStatus = solver.Solve();
```

Glop solves the problem on a typical computer in less than 300 milliseconds:

### Display the solution

The following code displays the solution.

[Python](https://developers.google.com/optimization/lp/stigler_diet#python)[C++](https://developers.google.com/optimization/lp/stigler_diet#c++)[Java](https://developers.google.com/optimization/lp/stigler_diet#java)[C#](https://developers.google.com/optimization/lp/stigler_diet#c)More

```
# Check that the problem has an optimal solution.
if status != solver.OPTIMAL:
    print("The problem does not have an optimal solution!")
    if status == solver.FEASIBLE:
        print("A potentially suboptimal solution was found.")
    else:
        print("The solver could not solve the problem.")
        exit(1)

# Display the amounts (in dollars) to purchase of each food.
nutrients_result = [0] * len(nutrients)
print("\nAnnual Foods:")
for i, food in enumerate(foods):
    if food.solution_value() > 0.0:
        print("{}: ${}".format(data[i][0], 365.0 * food.solution_value()))
        for j, _ in enumerate(nutrients):
            nutrients_result[j] += data[i][j + 3] * food.solution_value()
print("\nOptimal annual price: ${:.4f}".format(365.0 * objective.Value()))

print("\nNutrients per day:")
for i, nutrient in enumerate(nutrients):
    print(
        "{}: {:.2f} (min {})".format(nutrient[0], nutrients_result[i], nutrient[1])
    )
```

```
// Check that the problem has an optimal solution.
if (result_status != MPSolver::OPTIMAL) {
  LOG(INFO) << "The problem does not have an optimal solution!";
  if (result_status == MPSolver::FEASIBLE) {
    LOG(INFO) << "A potentially suboptimal solution was found";
  } else {
    LOG(INFO) << "The solver could not solve the problem.";
    return;
  }
}

std::vector<double> nutrients_result(nutrients.size());
LOG(INFO) << "";
LOG(INFO) << "Annual Foods:";
for (std::size_t i = 0; i < data.size(); ++i) {
  if (foods[i]->solution_value() > 0.0) {
    LOG(INFO) << data[i].name << ": $"
              << std::to_string(365. * foods[i]->solution_value());
    for (std::size_t j = 0; j < nutrients.size(); ++j) {
      nutrients_result[j] +=
          data[i].nutrients[j] * foods[i]->solution_value();
    }
  }
}
LOG(INFO) << "";
LOG(INFO) << "Optimal annual price: $"
          << std::to_string(365. * objective->Value());
LOG(INFO) << "";
LOG(INFO) << "Nutrients per day:";
for (std::size_t i = 0; i < nutrients.size(); ++i) {
  LOG(INFO) << nutrients[i].first << ": "
            << std::to_string(nutrients_result[i]) << " (min "
            << std::to_string(nutrients[i].second) << ")";
}
```

```
// Check that the problem has an optimal solution.
if (resultStatus != MPSolver.ResultStatus.OPTIMAL) {
  System.err.println("The problem does not have an optimal solution!");
  if (resultStatus == MPSolver.ResultStatus.FEASIBLE) {
    System.err.println("A potentially suboptimal solution was found.");
  } else {
    System.err.println("The solver could not solve the problem.");
    return;
  }
}

// Display the amounts (in dollars) to purchase of each food.
double[] nutrientsResult = new double[nutrients.size()];
System.out.println("\nAnnual Foods:");
for (int i = 0; i < foods.size(); ++i) {
  if (foods.get(i).solutionValue() > 0.0) {
    System.out.println((String) data.get(i)[0] + ": $" + 365 * foods.get(i).solutionValue());
    for (int j = 0; j < nutrients.size(); ++j) {
      nutrientsResult[j] += ((double[]) data.get(i)[3])[j] * foods.get(i).solutionValue();
    }
  }
}
System.out.println("\nOptimal annual price: $" + 365 * objective.value());

System.out.println("\nNutrients per day:");
for (int i = 0; i < nutrients.size(); ++i) {
  System.out.println(
      nutrients.get(i)[0] + ": " + nutrientsResult[i] + " (min " + nutrients.get(i)[1] + ")");
}
```

```
// Check that the problem has an optimal solution.
if (resultStatus != Solver.ResultStatus.OPTIMAL)
{
    Console.WriteLine("The problem does not have an optimal solution!");
    if (resultStatus == Solver.ResultStatus.FEASIBLE)
    {
        Console.WriteLine("A potentially suboptimal solution was found.");
    }
    else
    {
        Console.WriteLine("The solver could not solve the problem.");
        return;
    }
}

// Display the amounts (in dollars) to purchase of each food.
double[] nutrientsResult = new double[nutrients.Length];
Console.WriteLine("\nAnnual Foods:");
for (int i = 0; i < foods.Count; ++i)
{
    if (foods[i].SolutionValue() > 0.0)
    {
        Console.WriteLine($"{data[i].Name}: ${365 * foods[i].SolutionValue():N2}");
        for (int j = 0; j < nutrients.Length; ++j)
        {
            nutrientsResult[j] += data[i].Nutrients[j] * foods[i].SolutionValue();
        }
    }
}
Console.WriteLine($"\nOptimal annual price: ${365 * objective.Value():N2}");

Console.WriteLine("\nNutrients per day:");
for (int i = 0; i < nutrients.Length; ++i)
{
    Console.WriteLine($"{nutrients[i].Name}: {nutrientsResult[i]:N2} (min {nutrients[i].Value})");
}
```

Here is the output of the program.

```
make rpy_stigler_diet
"/usr/bin/python3.11" ortools/linear_solver/samples/stigler_diet.py
Number of variables = 77
Number of constraints = 9

Annual Foods:
Wheat Flour (Enriched): $10.774457511918223
Liver (Beef): $0.6907834111074193
Cabbage: $4.093268864842877
Spinach: $1.8277960703546996
Navy Beans, Dried: $22.275425687243036

Optimal annual price: $39.6617

Nutrients per day:
Calories (kcal): 3.00 (min 3)
Protein (g): 147.41 (min 70)
Calcium (g): 0.80 (min 0.8)
Iron (mg): 60.47 (min 12)
Vitamin A (KIU): 5.00 (min 5)
Vitamin B1 (mg): 4.12 (min 1.8)
Vitamin B2 (mg): 2.70 (min 2.7)
Niacin (mg): 27.32 (min 18)
Vitamin C (mg): 75.00 (min 75)

Advanced usage:
Problem solved in  1  milliseconds
Problem solved in  14  iterations
```

### Complete code for the program

The complete code for the Stigler diet program is shown below.

[Python](https://developers.google.com/optimization/lp/stigler_diet#python)[C++](https://developers.google.com/optimization/lp/stigler_diet#c++)[Java](https://developers.google.com/optimization/lp/stigler_diet#java)[C#](https://developers.google.com/optimization/lp/stigler_diet#c)More

```
"""The Stigler diet problem.

A description of the problem can be found here:
https://en.wikipedia.org/wiki/Stigler_diet.
"""
from ortools.linear_solver import pywraplp

def main():
    """Entry point of the program."""
    # Instantiate the data problem.
    # Nutrient minimums.
    nutrients = [\
        ["Calories (kcal)", 3],\
        ["Protein (g)", 70],\
        ["Calcium (g)", 0.8],\
        ["Iron (mg)", 12],\
        ["Vitamin A (KIU)", 5],\
        ["Vitamin B1 (mg)", 1.8],\
        ["Vitamin B2 (mg)", 2.7],\
        ["Niacin (mg)", 18],\
        ["Vitamin C (mg)", 75],\
    ]

    # Commodity, Unit, 1939 price (cents), Calories (kcal), Protein (g),
    # Calcium (g), Iron (mg), Vitamin A (KIU), Vitamin B1 (mg), Vitamin B2 (mg),
    # Niacin (mg), Vitamin C (mg)
    data = [\
        # fmt: off\
      ['Wheat Flour (Enriched)', '10 lb.', 36, 44.7, 1411, 2, 365, 0, 55.4, 33.3, 441, 0],\
      ['Macaroni', '1 lb.', 14.1, 11.6, 418, 0.7, 54, 0, 3.2, 1.9, 68, 0],\
      ['Wheat Cereal (Enriched)', '28 oz.', 24.2, 11.8, 377, 14.4, 175, 0, 14.4, 8.8, 114, 0],\
      ['Corn Flakes', '8 oz.', 7.1, 11.4, 252, 0.1, 56, 0, 13.5, 2.3, 68, 0],\
      ['Corn Meal', '1 lb.', 4.6, 36.0, 897, 1.7, 99, 30.9, 17.4, 7.9, 106, 0],\
      ['Hominy Grits', '24 oz.', 8.5, 28.6, 680, 0.8, 80, 0, 10.6, 1.6, 110, 0],\
      ['Rice', '1 lb.', 7.5, 21.2, 460, 0.6, 41, 0, 2, 4.8, 60, 0],\
      ['Rolled Oats', '1 lb.', 7.1, 25.3, 907, 5.1, 341, 0, 37.1, 8.9, 64, 0],\
      ['White Bread (Enriched)', '1 lb.', 7.9, 15.0, 488, 2.5, 115, 0, 13.8, 8.5, 126, 0],\
      ['Whole Wheat Bread', '1 lb.', 9.1, 12.2, 484, 2.7, 125, 0, 13.9, 6.4, 160, 0],\
      ['Rye Bread', '1 lb.', 9.1, 12.4, 439, 1.1, 82, 0, 9.9, 3, 66, 0],\
      ['Pound Cake', '1 lb.', 24.8, 8.0, 130, 0.4, 31, 18.9, 2.8, 3, 17, 0],\
      ['Soda Crackers', '1 lb.', 15.1, 12.5, 288, 0.5, 50, 0, 0, 0, 0, 0],\
      ['Milk', '1 qt.', 11, 6.1, 310, 10.5, 18, 16.8, 4, 16, 7, 177],\
      ['Evaporated Milk (can)', '14.5 oz.', 6.7, 8.4, 422, 15.1, 9, 26, 3, 23.5, 11, 60],\
      ['Butter', '1 lb.', 30.8, 10.8, 9, 0.2, 3, 44.2, 0, 0.2, 2, 0],\
      ['Oleomargarine', '1 lb.', 16.1, 20.6, 17, 0.6, 6, 55.8, 0.2, 0, 0, 0],\
      ['Eggs', '1 doz.', 32.6, 2.9, 238, 1.0, 52, 18.6, 2.8, 6.5, 1, 0],\
      ['Cheese (Cheddar)', '1 lb.', 24.2, 7.4, 448, 16.4, 19, 28.1, 0.8, 10.3, 4, 0],\
      ['Cream', '1/2 pt.', 14.1, 3.5, 49, 1.7, 3, 16.9, 0.6, 2.5, 0, 17],\
      ['Peanut Butter', '1 lb.', 17.9, 15.7, 661, 1.0, 48, 0, 9.6, 8.1, 471, 0],\
      ['Mayonnaise', '1/2 pt.', 16.7, 8.6, 18, 0.2, 8, 2.7, 0.4, 0.5, 0, 0],\
      ['Crisco', '1 lb.', 20.3, 20.1, 0, 0, 0, 0, 0, 0, 0, 0],\
      ['Lard', '1 lb.', 9.8, 41.7, 0, 0, 0, 0.2, 0, 0.5, 5, 0],\
      ['Sirloin Steak', '1 lb.', 39.6, 2.9, 166, 0.1, 34, 0.2, 2.1, 2.9, 69, 0],\
      ['Round Steak', '1 lb.', 36.4, 2.2, 214, 0.1, 32, 0.4, 2.5, 2.4, 87, 0],\
      ['Rib Roast', '1 lb.', 29.2, 3.4, 213, 0.1, 33, 0, 0, 2, 0, 0],\
      ['Chuck Roast', '1 lb.', 22.6, 3.6, 309, 0.2, 46, 0.4, 1, 4, 120, 0],\
      ['Plate', '1 lb.', 14.6, 8.5, 404, 0.2, 62, 0, 0.9, 0, 0, 0],\
      ['Liver (Beef)', '1 lb.', 26.8, 2.2, 333, 0.2, 139, 169.2, 6.4, 50.8, 316, 525],\
      ['Leg of Lamb', '1 lb.', 27.6, 3.1, 245, 0.1, 20, 0, 2.8, 3.9, 86, 0],\
      ['Lamb Chops (Rib)', '1 lb.', 36.6, 3.3, 140, 0.1, 15, 0, 1.7, 2.7, 54, 0],\
      ['Pork Chops', '1 lb.', 30.7, 3.5, 196, 0.2, 30, 0, 17.4, 2.7, 60, 0],\
      ['Pork Loin Roast', '1 lb.', 24.2, 4.4, 249, 0.3, 37, 0, 18.2, 3.6, 79, 0],\
      ['Bacon', '1 lb.', 25.6, 10.4, 152, 0.2, 23, 0, 1.8, 1.8, 71, 0],\
      ['Ham, smoked', '1 lb.', 27.4, 6.7, 212, 0.2, 31, 0, 9.9, 3.3, 50, 0],\
      ['Salt Pork', '1 lb.', 16, 18.8, 164, 0.1, 26, 0, 1.4, 1.8, 0, 0],\
      ['Roasting Chicken', '1 lb.', 30.3, 1.8, 184, 0.1, 30, 0.1, 0.9, 1.8, 68, 46],\
      ['Veal Cutlets', '1 lb.', 42.3, 1.7, 156, 0.1, 24, 0, 1.4, 2.4, 57, 0],\
      ['Salmon, Pink (can)', '16 oz.', 13, 5.8, 705, 6.8, 45, 3.5, 1, 4.9, 209, 0],\
      ['Apples', '1 lb.', 4.4, 5.8, 27, 0.5, 36, 7.3, 3.6, 2.7, 5, 544],\
      ['Bananas', '1 lb.', 6.1, 4.9, 60, 0.4, 30, 17.4, 2.5, 3.5, 28, 498],\
      ['Lemons', '1 doz.', 26, 1.0, 21, 0.5, 14, 0, 0.5, 0, 4, 952],\
      ['Oranges', '1 doz.', 30.9, 2.2, 40, 1.1, 18, 11.1, 3.6, 1.3, 10, 1998],\
      ['Green Beans', '1 lb.', 7.1, 2.4, 138, 3.7, 80, 69, 4.3, 5.8, 37, 862],\
      ['Cabbage', '1 lb.', 3.7, 2.6, 125, 4.0, 36, 7.2, 9, 4.5, 26, 5369],\
      ['Carrots', '1 bunch', 4.7, 2.7, 73, 2.8, 43, 188.5, 6.1, 4.3, 89, 608],\
      ['Celery', '1 stalk', 7.3, 0.9, 51, 3.0, 23, 0.9, 1.4, 1.4, 9, 313],\
      ['Lettuce', '1 head', 8.2, 0.4, 27, 1.1, 22, 112.4, 1.8, 3.4, 11, 449],\
      ['Onions', '1 lb.', 3.6, 5.8, 166, 3.8, 59, 16.6, 4.7, 5.9, 21, 1184],\
      ['Potatoes', '15 lb.', 34, 14.3, 336, 1.8, 118, 6.7, 29.4, 7.1, 198, 2522],\
      ['Spinach', '1 lb.', 8.1, 1.1, 106, 0, 138, 918.4, 5.7, 13.8, 33, 2755],\
      ['Sweet Potatoes', '1 lb.', 5.1, 9.6, 138, 2.7, 54, 290.7, 8.4, 5.4, 83, 1912],\
      ['Peaches (can)', 'No. 2 1/2', 16.8, 3.7, 20, 0.4, 10, 21.5, 0.5, 1, 31, 196],\
      ['Pears (can)', 'No. 2 1/2', 20.4, 3.0, 8, 0.3, 8, 0.8, 0.8, 0.8, 5, 81],\
      ['Pineapple (can)', 'No. 2 1/2', 21.3, 2.4, 16, 0.4, 8, 2, 2.8, 0.8, 7, 399],\
      ['Asparagus (can)', 'No. 2', 27.7, 0.4, 33, 0.3, 12, 16.3, 1.4, 2.1, 17, 272],\
      ['Green Beans (can)', 'No. 2', 10, 1.0, 54, 2, 65, 53.9, 1.6, 4.3, 32, 431],\
      ['Pork and Beans (can)', '16 oz.', 7.1, 7.5, 364, 4, 134, 3.5, 8.3, 7.7, 56, 0],\
      ['Corn (can)', 'No. 2', 10.4, 5.2, 136, 0.2, 16, 12, 1.6, 2.7, 42, 218],\
      ['Peas (can)', 'No. 2', 13.8, 2.3, 136, 0.6, 45, 34.9, 4.9, 2.5, 37, 370],\
      ['Tomatoes (can)', 'No. 2', 8.6, 1.3, 63, 0.7, 38, 53.2, 3.4, 2.5, 36, 1253],\
      ['Tomato Soup (can)', '10 1/2 oz.', 7.6, 1.6, 71, 0.6, 43, 57.9, 3.5, 2.4, 67, 862],\
      ['Peaches, Dried', '1 lb.', 15.7, 8.5, 87, 1.7, 173, 86.8, 1.2, 4.3, 55, 57],\
      ['Prunes, Dried', '1 lb.', 9, 12.8, 99, 2.5, 154, 85.7, 3.9, 4.3, 65, 257],\
      ['Raisins, Dried', '15 oz.', 9.4, 13.5, 104, 2.5, 136, 4.5, 6.3, 1.4, 24, 136],\
      ['Peas, Dried', '1 lb.', 7.9, 20.0, 1367, 4.2, 345, 2.9, 28.7, 18.4, 162, 0],\
      ['Lima Beans, Dried', '1 lb.', 8.9, 17.4, 1055, 3.7, 459, 5.1, 26.9, 38.2, 93, 0],\
      ['Navy Beans, Dried', '1 lb.', 5.9, 26.9, 1691, 11.4, 792, 0, 38.4, 24.6, 217, 0],\
      ['Coffee', '1 lb.', 22.4, 0, 0, 0, 0, 0, 4, 5.1, 50, 0],\
      ['Tea', '1/4 lb.', 17.4, 0, 0, 0, 0, 0, 0, 2.3, 42, 0],\
      ['Cocoa', '8 oz.', 8.6, 8.7, 237, 3, 72, 0, 2, 11.9, 40, 0],\
      ['Chocolate', '8 oz.', 16.2, 8.0, 77, 1.3, 39, 0, 0.9, 3.4, 14, 0],\
      ['Sugar', '10 lb.', 51.7, 34.9, 0, 0, 0, 0, 0, 0, 0, 0],\
      ['Corn Syrup', '24 oz.', 13.7, 14.7, 0, 0.5, 74, 0, 0, 0, 5, 0],\
      ['Molasses', '18 oz.', 13.6, 9.0, 0, 10.3, 244, 0, 1.9, 7.5, 146, 0],\
      ['Strawberry Preserves', '1 lb.', 20.5, 6.4, 11, 0.4, 7, 0.2, 0.2, 0.4, 3, 0],\
        # fmt: on\
    ]

    # Instantiate a Glop solver and naming it.
    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        return

    # Declare an array to hold our variables.
    foods = [solver.NumVar(0.0, solver.infinity(), item[0]) for item in data]

    print("Number of variables =", solver.NumVariables())

    # Create the constraints, one per nutrient.
    constraints = []
    for i, nutrient in enumerate(nutrients):
        constraints.append(solver.Constraint(nutrient[1], solver.infinity()))
        for j, item in enumerate(data):
            constraints[i].SetCoefficient(foods[j], item[i + 3])

    print("Number of constraints =", solver.NumConstraints())

    # Objective function: Minimize the sum of (price-normalized) foods.
    objective = solver.Objective()
    for food in foods:
        objective.SetCoefficient(food, 1)
    objective.SetMinimization()

    print(f"Solving with {solver.SolverVersion()}")
    status = solver.Solve()

    # Check that the problem has an optimal solution.
    if status != solver.OPTIMAL:
        print("The problem does not have an optimal solution!")
        if status == solver.FEASIBLE:
            print("A potentially suboptimal solution was found.")
        else:
            print("The solver could not solve the problem.")
            exit(1)

    # Display the amounts (in dollars) to purchase of each food.
    nutrients_result = [0] * len(nutrients)
    print("\nAnnual Foods:")
    for i, food in enumerate(foods):
        if food.solution_value() > 0.0:
            print("{}: ${}".format(data[i][0], 365.0 * food.solution_value()))
            for j, _ in enumerate(nutrients):
                nutrients_result[j] += data[i][j + 3] * food.solution_value()
    print("\nOptimal annual price: ${:.4f}".format(365.0 * objective.Value()))

    print("\nNutrients per day:")
    for i, nutrient in enumerate(nutrients):
        print(
            "{}: {:.2f} (min {})".format(nutrient[0], nutrients_result[i], nutrient[1])
        )

    print("\nAdvanced usage:")
    print(f"Problem solved in {solver.wall_time():d} milliseconds")
    print(f"Problem solved in {solver.iterations():d} iterations")

if __name__ == "__main__":
    main()
```

```
// The Stigler diet problem.
#include <array>
#include <cstddef>
#include <cstdlib>
#include <memory>
#include <string>
#include <utility>  // std::pair
#include <vector>

#include "absl/base/log_severity.h"
#include "absl/log/globals.h"
#include "absl/log/log.h"
#include "ortools/base/init_google.h"
#include "ortools/linear_solver/linear_solver.h"

namespace operations_research {
void StiglerDiet() {
  // Nutrient minimums.
  const std::vector<std::pair<std::string, double>> nutrients = {
      {"Calories (kcal)", 3.0}, {"Protein (g)", 70.0},
      {"Calcium (g)", 0.8},     {"Iron (mg)", 12.0},
      {"Vitamin A (kIU)", 5.0}, {"Vitamin B1 (mg)", 1.8},
      {"Vitamin B2 (mg)", 2.7}, {"Niacin (mg)", 18.0},
      {"Vitamin C (mg)", 75.0}};

  struct Commodity {
    std::string name;  //!< Commodity name
    std::string unit;  //!< Unit
    double price;      //!< 1939 price per unit (cents)
    //! Calories (kcal),
    //! Protein (g),
    //! Calcium (g),
    //! Iron (mg),
    //! Vitamin A (kIU),
    //! Vitamin B1 (mg),
    //! Vitamin B2 (mg),
    //! Niacin (mg),
    //! Vitamin C (mg)
    std::array<double, 9> nutrients;
  };

  std::vector<Commodity> data = {
      {"Wheat Flour (Enriched)",
       "10 lb.",
       36,
       {44.7, 1411, 2, 365, 0, 55.4, 33.3, 441, 0}},
      {"Macaroni", "1 lb.", 14.1, {11.6, 418, 0.7, 54, 0, 3.2, 1.9, 68, 0}},
      {"Wheat Cereal (Enriched)",
       "28 oz.",
       24.2,
       {11.8, 377, 14.4, 175, 0, 14.4, 8.8, 114, 0}},
      {"Corn Flakes", "8 oz.", 7.1, {11.4, 252, 0.1, 56, 0, 13.5, 2.3, 68, 0}},
      {"Corn Meal",
       "1 lb.",
       4.6,
       {36.0, 897, 1.7, 99, 30.9, 17.4, 7.9, 106, 0}},
      {"Hominy Grits",
       "24 oz.",
       8.5,
       {28.6, 680, 0.8, 80, 0, 10.6, 1.6, 110, 0}},
      {"Rice", "1 lb.", 7.5, {21.2, 460, 0.6, 41, 0, 2, 4.8, 60, 0}},
      {"Rolled Oats", "1 lb.", 7.1, {25.3, 907, 5.1, 341, 0, 37.1, 8.9, 64, 0}},
      {"White Bread (Enriched)",
       "1 lb.",
       7.9,
       {15.0, 488, 2.5, 115, 0, 13.8, 8.5, 126, 0}},
      {"Whole Wheat Bread",
       "1 lb.",
       9.1,
       {12.2, 484, 2.7, 125, 0, 13.9, 6.4, 160, 0}},
      {"Rye Bread", "1 lb.", 9.1, {12.4, 439, 1.1, 82, 0, 9.9, 3, 66, 0}},
      {"Pound Cake", "1 lb.", 24.8, {8.0, 130, 0.4, 31, 18.9, 2.8, 3, 17, 0}},
      {"Soda Crackers", "1 lb.", 15.1, {12.5, 288, 0.5, 50, 0, 0, 0, 0, 0}},
      {"Milk", "1 qt.", 11, {6.1, 310, 10.5, 18, 16.8, 4, 16, 7, 177}},
      {"Evaporated Milk (can)",
       "14.5 oz.",
       6.7,
       {8.4, 422, 15.1, 9, 26, 3, 23.5, 11, 60}},
      {"Butter", "1 lb.", 30.8, {10.8, 9, 0.2, 3, 44.2, 0, 0.2, 2, 0}},
      {"Oleomargarine", "1 lb.", 16.1, {20.6, 17, 0.6, 6, 55.8, 0.2, 0, 0, 0}},
      {"Eggs", "1 doz.", 32.6, {2.9, 238, 1.0, 52, 18.6, 2.8, 6.5, 1, 0}},
      {"Cheese (Cheddar)",
       "1 lb.",
       24.2,
       {7.4, 448, 16.4, 19, 28.1, 0.8, 10.3, 4, 0}},
      {"Cream", "1/2 pt.", 14.1, {3.5, 49, 1.7, 3, 16.9, 0.6, 2.5, 0, 17}},
      {"Peanut Butter",
       "1 lb.",
       17.9,
       {15.7, 661, 1.0, 48, 0, 9.6, 8.1, 471, 0}},
      {"Mayonnaise", "1/2 pt.", 16.7, {8.6, 18, 0.2, 8, 2.7, 0.4, 0.5, 0, 0}},
      {"Crisco", "1 lb.", 20.3, {20.1, 0, 0, 0, 0, 0, 0, 0, 0}},
      {"Lard", "1 lb.", 9.8, {41.7, 0, 0, 0, 0.2, 0, 0.5, 5, 0}},
      {"Sirloin Steak",
       "1 lb.",
       39.6,
       {2.9, 166, 0.1, 34, 0.2, 2.1, 2.9, 69, 0}},
      {"Round Steak", "1 lb.", 36.4, {2.2, 214, 0.1, 32, 0.4, 2.5, 2.4, 87, 0}},
      {"Rib Roast", "1 lb.", 29.2, {3.4, 213, 0.1, 33, 0, 0, 2, 0, 0}},
      {"Chuck Roast", "1 lb.", 22.6, {3.6, 309, 0.2, 46, 0.4, 1, 4, 120, 0}},
      {"Plate", "1 lb.", 14.6, {8.5, 404, 0.2, 62, 0, 0.9, 0, 0, 0}},
      {"Liver (Beef)",
       "1 lb.",
       26.8,
       {2.2, 333, 0.2, 139, 169.2, 6.4, 50.8, 316, 525}},
      {"Leg of Lamb", "1 lb.", 27.6, {3.1, 245, 0.1, 20, 0, 2.8, 3.9, 86, 0}},
      {"Lamb Chops (Rib)",
       "1 lb.",
       36.6,
       {3.3, 140, 0.1, 15, 0, 1.7, 2.7, 54, 0}},
      {"Pork Chops", "1 lb.", 30.7, {3.5, 196, 0.2, 30, 0, 17.4, 2.7, 60, 0}},
      {"Pork Loin Roast",
       "1 lb.",
       24.2,
       {4.4, 249, 0.3, 37, 0, 18.2, 3.6, 79, 0}},
      {"Bacon", "1 lb.", 25.6, {10.4, 152, 0.2, 23, 0, 1.8, 1.8, 71, 0}},
      {"Ham, smoked", "1 lb.", 27.4, {6.7, 212, 0.2, 31, 0, 9.9, 3.3, 50, 0}},
      {"Salt Pork", "1 lb.", 16, {18.8, 164, 0.1, 26, 0, 1.4, 1.8, 0, 0}},
      {"Roasting Chicken",
       "1 lb.",
       30.3,
       {1.8, 184, 0.1, 30, 0.1, 0.9, 1.8, 68, 46}},
      {"Veal Cutlets", "1 lb.", 42.3, {1.7, 156, 0.1, 24, 0, 1.4, 2.4, 57, 0}},
      {"Salmon, Pink (can)",
       "16 oz.",
       13,
       {5.8, 705, 6.8, 45, 3.5, 1, 4.9, 209, 0}},
      {"Apples", "1 lb.", 4.4, {5.8, 27, 0.5, 36, 7.3, 3.6, 2.7, 5, 544}},
      {"Bananas", "1 lb.", 6.1, {4.9, 60, 0.4, 30, 17.4, 2.5, 3.5, 28, 498}},
      {"Lemons", "1 doz.", 26, {1.0, 21, 0.5, 14, 0, 0.5, 0, 4, 952}},
      {"Oranges", "1 doz.", 30.9, {2.2, 40, 1.1, 18, 11.1, 3.6, 1.3, 10, 1998}},
      {"Green Beans", "1 lb.", 7.1, {2.4, 138, 3.7, 80, 69, 4.3, 5.8, 37, 862}},
      {"Cabbage", "1 lb.", 3.7, {2.6, 125, 4.0, 36, 7.2, 9, 4.5, 26, 5369}},
      {"Carrots", "1 bunch", 4.7, {2.7, 73, 2.8, 43, 188.5, 6.1, 4.3, 89, 608}},
      {"Celery", "1 stalk", 7.3, {0.9, 51, 3.0, 23, 0.9, 1.4, 1.4, 9, 313}},
      {"Lettuce", "1 head", 8.2, {0.4, 27, 1.1, 22, 112.4, 1.8, 3.4, 11, 449}},
      {"Onions", "1 lb.", 3.6, {5.8, 166, 3.8, 59, 16.6, 4.7, 5.9, 21, 1184}},
      {"Potatoes",
       "15 lb.",
       34,
       {14.3, 336, 1.8, 118, 6.7, 29.4, 7.1, 198, 2522}},
      {"Spinach", "1 lb.", 8.1, {1.1, 106, 0, 138, 918.4, 5.7, 13.8, 33, 2755}},
      {"Sweet Potatoes",
       "1 lb.",
       5.1,
       {9.6, 138, 2.7, 54, 290.7, 8.4, 5.4, 83, 1912}},
      {"Peaches (can)",
       "No. 2 1/2",
       16.8,
       {3.7, 20, 0.4, 10, 21.5, 0.5, 1, 31, 196}},
      {"Pears (can)",
       "No. 2 1/2",
       20.4,
       {3.0, 8, 0.3, 8, 0.8, 0.8, 0.8, 5, 81}},
      {"Pineapple (can)",
       "No. 2 1/2",
       21.3,
       {2.4, 16, 0.4, 8, 2, 2.8, 0.8, 7, 399}},
      {"Asparagus (can)",
       "No. 2",
       27.7,
       {0.4, 33, 0.3, 12, 16.3, 1.4, 2.1, 17, 272}},
      {"Green Beans (can)",
       "No. 2",
       10,
       {1.0, 54, 2, 65, 53.9, 1.6, 4.3, 32, 431}},
      {"Pork and Beans (can)",
       "16 oz.",
       7.1,
       {7.5, 364, 4, 134, 3.5, 8.3, 7.7, 56, 0}},
      {"Corn (can)", "No. 2", 10.4, {5.2, 136, 0.2, 16, 12, 1.6, 2.7, 42, 218}},
      {"Peas (can)",
       "No. 2",
       13.8,
       {2.3, 136, 0.6, 45, 34.9, 4.9, 2.5, 37, 370}},
      {"Tomatoes (can)",
       "No. 2",
       8.6,
       {1.3, 63, 0.7, 38, 53.2, 3.4, 2.5, 36, 1253}},
      {"Tomato Soup (can)",
       "10 1/2 oz.",
       7.6,
       {1.6, 71, 0.6, 43, 57.9, 3.5, 2.4, 67, 862}},
      {"Peaches, Dried",
       "1 lb.",
       15.7,
       {8.5, 87, 1.7, 173, 86.8, 1.2, 4.3, 55, 57}},
      {"Prunes, Dried",
       "1 lb.",
       9,
       {12.8, 99, 2.5, 154, 85.7, 3.9, 4.3, 65, 257}},
      {"Raisins, Dried",
       "15 oz.",
       9.4,
       {13.5, 104, 2.5, 136, 4.5, 6.3, 1.4, 24, 136}},
      {"Peas, Dried",
       "1 lb.",
       7.9,
       {20.0, 1367, 4.2, 345, 2.9, 28.7, 18.4, 162, 0}},
      {"Lima Beans, Dried",
       "1 lb.",
       8.9,
       {17.4, 1055, 3.7, 459, 5.1, 26.9, 38.2, 93, 0}},
      {"Navy Beans, Dried",
       "1 lb.",
       5.9,
       {26.9, 1691, 11.4, 792, 0, 38.4, 24.6, 217, 0}},
      {"Coffee", "1 lb.", 22.4, {0, 0, 0, 0, 0, 4, 5.1, 50, 0}},
      {"Tea", "1/4 lb.", 17.4, {0, 0, 0, 0, 0, 0, 2.3, 42, 0}},
      {"Cocoa", "8 oz.", 8.6, {8.7, 237, 3, 72, 0, 2, 11.9, 40, 0}},
      {"Chocolate", "8 oz.", 16.2, {8.0, 77, 1.3, 39, 0, 0.9, 3.4, 14, 0}},
      {"Sugar", "10 lb.", 51.7, {34.9, 0, 0, 0, 0, 0, 0, 0, 0}},
      {"Corn Syrup", "24 oz.", 13.7, {14.7, 0, 0.5, 74, 0, 0, 0, 5, 0}},
      {"Molasses", "18 oz.", 13.6, {9.0, 0, 10.3, 244, 0, 1.9, 7.5, 146, 0}},
      {"Strawberry Preserves",
       "1 lb.",
       20.5,
       {6.4, 11, 0.4, 7, 0.2, 0.2, 0.4, 3, 0}}};

  // Create the linear solver with the GLOP backend.
  std::unique_ptr<MPSolver> solver(MPSolver::CreateSolver("GLOP"));

  std::vector<MPVariable*> foods;
  const double infinity = solver->infinity();
  foods.reserve(data.size());
  for (const Commodity& commodity : data) {
    foods.push_back(solver->MakeNumVar(0.0, infinity, commodity.name));
  }
  LOG(INFO) << "Number of variables = " << solver->NumVariables();

  // Create the constraints, one per nutrient.
  std::vector<MPConstraint*> constraints;
  for (std::size_t i = 0; i < nutrients.size(); ++i) {
    constraints.push_back(
        solver->MakeRowConstraint(nutrients[i].second, infinity));
    for (std::size_t j = 0; j < data.size(); ++j) {
      constraints.back()->SetCoefficient(foods[j], data[j].nutrients[i]);
    }
  }
  LOG(INFO) << "Number of constraints = " << solver->NumConstraints();

  MPObjective* const objective = solver->MutableObjective();
  for (size_t i = 0; i < data.size(); ++i) {
    objective->SetCoefficient(foods[i], 1);
  }
  objective->SetMinimization();

  const MPSolver::ResultStatus result_status = solver->Solve();

  // Check that the problem has an optimal solution.
  if (result_status != MPSolver::OPTIMAL) {
    LOG(INFO) << "The problem does not have an optimal solution!";
    if (result_status == MPSolver::FEASIBLE) {
      LOG(INFO) << "A potentially suboptimal solution was found";
    } else {
      LOG(INFO) << "The solver could not solve the problem.";
      return;
    }
  }

  std::vector<double> nutrients_result(nutrients.size());
  LOG(INFO) << "";
  LOG(INFO) << "Annual Foods:";
  for (std::size_t i = 0; i < data.size(); ++i) {
    if (foods[i]->solution_value() > 0.0) {
      LOG(INFO) << data[i].name << ": $"
                << std::to_string(365. * foods[i]->solution_value());
      for (std::size_t j = 0; j < nutrients.size(); ++j) {
        nutrients_result[j] +=
            data[i].nutrients[j] * foods[i]->solution_value();
      }
    }
  }
  LOG(INFO) << "";
  LOG(INFO) << "Optimal annual price: $"
            << std::to_string(365. * objective->Value());
  LOG(INFO) << "";
  LOG(INFO) << "Nutrients per day:";
  for (std::size_t i = 0; i < nutrients.size(); ++i) {
    LOG(INFO) << nutrients[i].first << ": "
              << std::to_string(nutrients_result[i]) << " (min "
              << std::to_string(nutrients[i].second) << ")";
  }

  LOG(INFO) << "";
  LOG(INFO) << "Advanced usage:";
  LOG(INFO) << "Problem solved in " << solver->wall_time() << " milliseconds";
  LOG(INFO) << "Problem solved in " << solver->iterations() << " iterations";
}
}  // namespace operations_research

int main(int argc, char** argv) {
  InitGoogle(argv[0], &argc, &argv, true);
  absl::SetStderrThreshold(absl::LogSeverityAtLeast::kInfo);
  operations_research::StiglerDiet();
  return EXIT_SUCCESS;
}
```

```
// The Stigler diet problem.
package com.google.ortools.linearsolver.samples;
import com.google.ortools.Loader;
import com.google.ortools.linearsolver.MPConstraint;
import com.google.ortools.linearsolver.MPObjective;
import com.google.ortools.linearsolver.MPSolver;
import com.google.ortools.linearsolver.MPVariable;
import java.util.ArrayList;
import java.util.List;

/** Stigler diet example. */
public final class StiglerDiet {
  public static void main(String[] args) {
    Loader.loadNativeLibraries();
    // Nutrient minimums.
    List<Object[]> nutrients = new ArrayList<>();
    nutrients.add(new Object[] {"Calories (kcal)", 3.0});
    nutrients.add(new Object[] {"Protein (g)", 70.0});
    nutrients.add(new Object[] {"Calcium (g)", 0.8});
    nutrients.add(new Object[] {"Iron (mg)", 12.0});
    nutrients.add(new Object[] {"Vitamin A (kIU)", 5.0});
    nutrients.add(new Object[] {"Vitamin B1 (mg)", 1.8});
    nutrients.add(new Object[] {"Vitamin B2 (mg)", 2.7});
    nutrients.add(new Object[] {"Niacin (mg)", 18.0});
    nutrients.add(new Object[] {"Vitamin C (mg)", 75.0});

    List<Object[]> data = new ArrayList<>();
    data.add(new Object[] {"Wheat Flour (Enriched)", "10 lb.", 36,
        new double[] {44.7, 1411, 2, 365, 0, 55.4, 33.3, 441, 0}});
    data.add(new Object[] {
        "Macaroni", "1 lb.", 14.1, new double[] {11.6, 418, 0.7, 54, 0, 3.2, 1.9, 68, 0}});
    data.add(new Object[] {"Wheat Cereal (Enriched)", "28 oz.", 24.2,
        new double[] {11.8, 377, 14.4, 175, 0, 14.4, 8.8, 114, 0}});
    data.add(new Object[] {
        "Corn Flakes", "8 oz.", 7.1, new double[] {11.4, 252, 0.1, 56, 0, 13.5, 2.3, 68, 0}});
    data.add(new Object[] {
        "Corn Meal", "1 lb.", 4.6, new double[] {36.0, 897, 1.7, 99, 30.9, 17.4, 7.9, 106, 0}});
    data.add(new Object[] {
        "Hominy Grits", "24 oz.", 8.5, new double[] {28.6, 680, 0.8, 80, 0, 10.6, 1.6, 110, 0}});
    data.add(
        new Object[] {"Rice", "1 lb.", 7.5, new double[] {21.2, 460, 0.6, 41, 0, 2, 4.8, 60, 0}});
    data.add(new Object[] {
        "Rolled Oats", "1 lb.", 7.1, new double[] {25.3, 907, 5.1, 341, 0, 37.1, 8.9, 64, 0}});
    data.add(new Object[] {"White Bread (Enriched)", "1 lb.", 7.9,
        new double[] {15.0, 488, 2.5, 115, 0, 13.8, 8.5, 126, 0}});
    data.add(new Object[] {"Whole Wheat Bread", "1 lb.", 9.1,
        new double[] {12.2, 484, 2.7, 125, 0, 13.9, 6.4, 160, 0}});
    data.add(new Object[] {
        "Rye Bread", "1 lb.", 9.1, new double[] {12.4, 439, 1.1, 82, 0, 9.9, 3, 66, 0}});
    data.add(new Object[] {
        "Pound Cake", "1 lb.", 24.8, new double[] {8.0, 130, 0.4, 31, 18.9, 2.8, 3, 17, 0}});
    data.add(new Object[] {
        "Soda Crackers", "1 lb.", 15.1, new double[] {12.5, 288, 0.5, 50, 0, 0, 0, 0, 0}});
    data.add(
        new Object[] {"Milk", "1 qt.", 11, new double[] {6.1, 310, 10.5, 18, 16.8, 4, 16, 7, 177}});
    data.add(new Object[] {"Evaporated Milk (can)", "14.5 oz.", 6.7,
        new double[] {8.4, 422, 15.1, 9, 26, 3, 23.5, 11, 60}});
    data.add(
        new Object[] {"Butter", "1 lb.", 30.8, new double[] {10.8, 9, 0.2, 3, 44.2, 0, 0.2, 2, 0}});
    data.add(new Object[] {
        "Oleomargarine", "1 lb.", 16.1, new double[] {20.6, 17, 0.6, 6, 55.8, 0.2, 0, 0, 0}});
    data.add(new Object[] {
        "Eggs", "1 doz.", 32.6, new double[] {2.9, 238, 1.0, 52, 18.6, 2.8, 6.5, 1, 0}});
    data.add(new Object[] {"Cheese (Cheddar)", "1 lb.", 24.2,
        new double[] {7.4, 448, 16.4, 19, 28.1, 0.8, 10.3, 4, 0}});
    data.add(new Object[] {
        "Cream", "1/2 pt.", 14.1, new double[] {3.5, 49, 1.7, 3, 16.9, 0.6, 2.5, 0, 17}});
    data.add(new Object[] {
        "Peanut Butter", "1 lb.", 17.9, new double[] {15.7, 661, 1.0, 48, 0, 9.6, 8.1, 471, 0}});
    data.add(new Object[] {
        "Mayonnaise", "1/2 pt.", 16.7, new double[] {8.6, 18, 0.2, 8, 2.7, 0.4, 0.5, 0, 0}});
    data.add(new Object[] {"Crisco", "1 lb.", 20.3, new double[] {20.1, 0, 0, 0, 0, 0, 0, 0, 0}});
    data.add(new Object[] {"Lard", "1 lb.", 9.8, new double[] {41.7, 0, 0, 0, 0.2, 0, 0.5, 5, 0}});
    data.add(new Object[] {
        "Sirloin Steak", "1 lb.", 39.6, new double[] {2.9, 166, 0.1, 34, 0.2, 2.1, 2.9, 69, 0}});
    data.add(new Object[] {
        "Round Steak", "1 lb.", 36.4, new double[] {2.2, 214, 0.1, 32, 0.4, 2.5, 2.4, 87, 0}});
    data.add(
        new Object[] {"Rib Roast", "1 lb.", 29.2, new double[] {3.4, 213, 0.1, 33, 0, 0, 2, 0, 0}});
    data.add(new Object[] {
        "Chuck Roast", "1 lb.", 22.6, new double[] {3.6, 309, 0.2, 46, 0.4, 1, 4, 120, 0}});
    data.add(
        new Object[] {"Plate", "1 lb.", 14.6, new double[] {8.5, 404, 0.2, 62, 0, 0.9, 0, 0, 0}});
    data.add(new Object[] {"Liver (Beef)", "1 lb.", 26.8,
        new double[] {2.2, 333, 0.2, 139, 169.2, 6.4, 50.8, 316, 525}});
    data.add(new Object[] {
        "Leg of Lamb", "1 lb.", 27.6, new double[] {3.1, 245, 0.1, 20, 0, 2.8, 3.9, 86, 0}});
    data.add(new Object[] {
        "Lamb Chops (Rib)", "1 lb.", 36.6, new double[] {3.3, 140, 0.1, 15, 0, 1.7, 2.7, 54, 0}});
    data.add(new Object[] {
        "Pork Chops", "1 lb.", 30.7, new double[] {3.5, 196, 0.2, 30, 0, 17.4, 2.7, 60, 0}});
    data.add(new Object[] {
        "Pork Loin Roast", "1 lb.", 24.2, new double[] {4.4, 249, 0.3, 37, 0, 18.2, 3.6, 79, 0}});
    data.add(new Object[] {
        "Bacon", "1 lb.", 25.6, new double[] {10.4, 152, 0.2, 23, 0, 1.8, 1.8, 71, 0}});
    data.add(new Object[] {
        "Ham, smoked", "1 lb.", 27.4, new double[] {6.7, 212, 0.2, 31, 0, 9.9, 3.3, 50, 0}});
    data.add(new Object[] {
        "Salt Pork", "1 lb.", 16, new double[] {18.8, 164, 0.1, 26, 0, 1.4, 1.8, 0, 0}});
    data.add(new Object[] {"Roasting Chicken", "1 lb.", 30.3,
        new double[] {1.8, 184, 0.1, 30, 0.1, 0.9, 1.8, 68, 46}});
    data.add(new Object[] {
        "Veal Cutlets", "1 lb.", 42.3, new double[] {1.7, 156, 0.1, 24, 0, 1.4, 2.4, 57, 0}});
    data.add(new Object[] {
        "Salmon, Pink (can)", "16 oz.", 13, new double[] {5.8, 705, 6.8, 45, 3.5, 1, 4.9, 209, 0}});
    data.add(new Object[] {
        "Apples", "1 lb.", 4.4, new double[] {5.8, 27, 0.5, 36, 7.3, 3.6, 2.7, 5, 544}});
    data.add(new Object[] {
        "Bananas", "1 lb.", 6.1, new double[] {4.9, 60, 0.4, 30, 17.4, 2.5, 3.5, 28, 498}});
    data.add(
        new Object[] {"Lemons", "1 doz.", 26, new double[] {1.0, 21, 0.5, 14, 0, 0.5, 0, 4, 952}});
    data.add(new Object[] {
        "Oranges", "1 doz.", 30.9, new double[] {2.2, 40, 1.1, 18, 11.1, 3.6, 1.3, 10, 1998}});
    data.add(new Object[] {
        "Green Beans", "1 lb.", 7.1, new double[] {2.4, 138, 3.7, 80, 69, 4.3, 5.8, 37, 862}});
    data.add(new Object[] {
        "Cabbage", "1 lb.", 3.7, new double[] {2.6, 125, 4.0, 36, 7.2, 9, 4.5, 26, 5369}});
    data.add(new Object[] {
        "Carrots", "1 bunch", 4.7, new double[] {2.7, 73, 2.8, 43, 188.5, 6.1, 4.3, 89, 608}});
    data.add(new Object[] {
        "Celery", "1 stalk", 7.3, new double[] {0.9, 51, 3.0, 23, 0.9, 1.4, 1.4, 9, 313}});
    data.add(new Object[] {
        "Lettuce", "1 head", 8.2, new double[] {0.4, 27, 1.1, 22, 112.4, 1.8, 3.4, 11, 449}});
    data.add(new Object[] {
        "Onions", "1 lb.", 3.6, new double[] {5.8, 166, 3.8, 59, 16.6, 4.7, 5.9, 21, 1184}});
    data.add(new Object[] {
        "Potatoes", "15 lb.", 34, new double[] {14.3, 336, 1.8, 118, 6.7, 29.4, 7.1, 198, 2522}});
    data.add(new Object[] {
        "Spinach", "1 lb.", 8.1, new double[] {1.1, 106, 0, 138, 918.4, 5.7, 13.8, 33, 2755}});
    data.add(new Object[] {"Sweet Potatoes", "1 lb.", 5.1,
        new double[] {9.6, 138, 2.7, 54, 290.7, 8.4, 5.4, 83, 1912}});
    data.add(new Object[] {"Peaches (can)", "No. 2 1/2", 16.8,
        new double[] {3.7, 20, 0.4, 10, 21.5, 0.5, 1, 31, 196}});
    data.add(new Object[] {
        "Pears (can)", "No. 2 1/2", 20.4, new double[] {3.0, 8, 0.3, 8, 0.8, 0.8, 0.8, 5, 81}});
    data.add(new Object[] {
        "Pineapple (can)", "No. 2 1/2", 21.3, new double[] {2.4, 16, 0.4, 8, 2, 2.8, 0.8, 7, 399}});
    data.add(new Object[] {"Asparagus (can)", "No. 2", 27.7,
        new double[] {0.4, 33, 0.3, 12, 16.3, 1.4, 2.1, 17, 272}});
    data.add(new Object[] {
        "Green Beans (can)", "No. 2", 10, new double[] {1.0, 54, 2, 65, 53.9, 1.6, 4.3, 32, 431}});
    data.add(new Object[] {"Pork and Beans (can)", "16 oz.", 7.1,
        new double[] {7.5, 364, 4, 134, 3.5, 8.3, 7.7, 56, 0}});
    data.add(new Object[] {
        "Corn (can)", "No. 2", 10.4, new double[] {5.2, 136, 0.2, 16, 12, 1.6, 2.7, 42, 218}});
    data.add(new Object[] {
        "Peas (can)", "No. 2", 13.8, new double[] {2.3, 136, 0.6, 45, 34.9, 4.9, 2.5, 37, 370}});
    data.add(new Object[] {
        "Tomatoes (can)", "No. 2", 8.6, new double[] {1.3, 63, 0.7, 38, 53.2, 3.4, 2.5, 36, 1253}});
    data.add(new Object[] {"Tomato Soup (can)", "10 1/2 oz.", 7.6,
        new double[] {1.6, 71, 0.6, 43, 57.9, 3.5, 2.4, 67, 862}});
    data.add(new Object[] {
        "Peaches, Dried", "1 lb.", 15.7, new double[] {8.5, 87, 1.7, 173, 86.8, 1.2, 4.3, 55, 57}});
    data.add(new Object[] {
        "Prunes, Dried", "1 lb.", 9, new double[] {12.8, 99, 2.5, 154, 85.7, 3.9, 4.3, 65, 257}});
    data.add(new Object[] {"Raisins, Dried", "15 oz.", 9.4,
        new double[] {13.5, 104, 2.5, 136, 4.5, 6.3, 1.4, 24, 136}});
    data.add(new Object[] {
        "Peas, Dried", "1 lb.", 7.9, new double[] {20.0, 1367, 4.2, 345, 2.9, 28.7, 18.4, 162, 0}});
    data.add(new Object[] {"Lima Beans, Dried", "1 lb.", 8.9,
        new double[] {17.4, 1055, 3.7, 459, 5.1, 26.9, 38.2, 93, 0}});
    data.add(new Object[] {"Navy Beans, Dried", "1 lb.", 5.9,
        new double[] {26.9, 1691, 11.4, 792, 0, 38.4, 24.6, 217, 0}});
    data.add(new Object[] {"Coffee", "1 lb.", 22.4, new double[] {0, 0, 0, 0, 0, 4, 5.1, 50, 0}});
    data.add(new Object[] {"Tea", "1/4 lb.", 17.4, new double[] {0, 0, 0, 0, 0, 0, 2.3, 42, 0}});
    data.add(
        new Object[] {"Cocoa", "8 oz.", 8.6, new double[] {8.7, 237, 3, 72, 0, 2, 11.9, 40, 0}});
    data.add(new Object[] {
        "Chocolate", "8 oz.", 16.2, new double[] {8.0, 77, 1.3, 39, 0, 0.9, 3.4, 14, 0}});
    data.add(new Object[] {"Sugar", "10 lb.", 51.7, new double[] {34.9, 0, 0, 0, 0, 0, 0, 0, 0}});
    data.add(new Object[] {
        "Corn Syrup", "24 oz.", 13.7, new double[] {14.7, 0, 0.5, 74, 0, 0, 0, 5, 0}});
    data.add(new Object[] {
        "Molasses", "18 oz.", 13.6, new double[] {9.0, 0, 10.3, 244, 0, 1.9, 7.5, 146, 0}});
    data.add(new Object[] {"Strawberry Preserves", "1 lb.", 20.5,
        new double[] {6.4, 11, 0.4, 7, 0.2, 0.2, 0.4, 3, 0}});

    // Create the linear solver with the GLOP backend.
    MPSolver solver = MPSolver.createSolver("GLOP");
    if (solver == null) {
      System.out.println("Could not create solver GLOP");
      return;
    }

    double infinity = java.lang.Double.POSITIVE_INFINITY;
    List<MPVariable> foods = new ArrayList<>();
    for (int i = 0; i < data.size(); ++i) {
      foods.add(solver.makeNumVar(0.0, infinity, (String) data.get(i)[0]));
    }
    System.out.println("Number of variables = " + solver.numVariables());

    MPConstraint[] constraints = new MPConstraint[nutrients.size()];
    for (int i = 0; i < nutrients.size(); ++i) {
      constraints[i] = solver.makeConstraint(
          (double) nutrients.get(i)[1], infinity, (String) nutrients.get(i)[0]);
      for (int j = 0; j < data.size(); ++j) {
        constraints[i].setCoefficient(foods.get(j), ((double[]) data.get(j)[3])[i]);
      }
      // constraints.add(constraint);
    }
    System.out.println("Number of constraints = " + solver.numConstraints());

    MPObjective objective = solver.objective();
    for (int i = 0; i < data.size(); ++i) {
      objective.setCoefficient(foods.get(i), 1);
    }
    objective.setMinimization();

    final MPSolver.ResultStatus resultStatus = solver.solve();

    // Check that the problem has an optimal solution.
    if (resultStatus != MPSolver.ResultStatus.OPTIMAL) {
      System.err.println("The problem does not have an optimal solution!");
      if (resultStatus == MPSolver.ResultStatus.FEASIBLE) {
        System.err.println("A potentially suboptimal solution was found.");
      } else {
        System.err.println("The solver could not solve the problem.");
        return;
      }
    }

    // Display the amounts (in dollars) to purchase of each food.
    double[] nutrientsResult = new double[nutrients.size()];
    System.out.println("\nAnnual Foods:");
    for (int i = 0; i < foods.size(); ++i) {
      if (foods.get(i).solutionValue() > 0.0) {
        System.out.println((String) data.get(i)[0] + ": $" + 365 * foods.get(i).solutionValue());
        for (int j = 0; j < nutrients.size(); ++j) {
          nutrientsResult[j] += ((double[]) data.get(i)[3])[j] * foods.get(i).solutionValue();
        }
      }
    }
    System.out.println("\nOptimal annual price: $" + 365 * objective.value());

    System.out.println("\nNutrients per day:");
    for (int i = 0; i < nutrients.size(); ++i) {
      System.out.println(
          nutrients.get(i)[0] + ": " + nutrientsResult[i] + " (min " + nutrients.get(i)[1] + ")");
    }

    System.out.println("\nAdvanced usage:");
    System.out.println("Problem solved in " + solver.wallTime() + " milliseconds");
    System.out.println("Problem solved in " + solver.iterations() + " iterations");
  }

  private StiglerDiet() {}
}
```

```
// The Stigler diet problem.
using System;
using System.Collections.Generic;
using Google.OrTools.LinearSolver;

public class StiglerDiet
{
    static void Main()
    {
        // Nutrient minimums.
        (String Name, double Value)[] nutrients =
            new[] { ("Calories (kcal)", 3.0), ("Protein (g)", 70.0),    ("Calcium (g)", 0.8),
                    ("Iron (mg)", 12.0),      ("Vitamin A (kIU)", 5.0), ("Vitamin B1 (mg)", 1.8),
                    ("Vitamin B2 (mg)", 2.7), ("Niacin (mg)", 18.0),    ("Vitamin C (mg)", 75.0) };

        (String Name, String Unit, double Price, double[] Nutrients)[] data = new[] {
            ("Wheat Flour (Enriched)", "10 lb.", 36, new double[] { 44.7, 1411, 2, 365, 0, 55.4, 33.3, 441, 0 }),
            ("Macaroni", "1 lb.", 14.1, new double[] { 11.6, 418, 0.7, 54, 0, 3.2, 1.9, 68, 0 }),
            ("Wheat Cereal (Enriched)", "28 oz.", 24.2, new double[] { 11.8, 377, 14.4, 175, 0, 14.4, 8.8, 114, 0 }),
            ("Corn Flakes", "8 oz.", 7.1, new double[] { 11.4, 252, 0.1, 56, 0, 13.5, 2.3, 68, 0 }),
            ("Corn Meal", "1 lb.", 4.6, new double[] { 36.0, 897, 1.7, 99, 30.9, 17.4, 7.9, 106, 0 }),
            ("Hominy Grits", "24 oz.", 8.5, new double[] { 28.6, 680, 0.8, 80, 0, 10.6, 1.6, 110, 0 }),
            ("Rice", "1 lb.", 7.5, new double[] { 21.2, 460, 0.6, 41, 0, 2, 4.8, 60, 0 }),
            ("Rolled Oats", "1 lb.", 7.1, new double[] { 25.3, 907, 5.1, 341, 0, 37.1, 8.9, 64, 0 }),
            ("White Bread (Enriched)", "1 lb.", 7.9, new double[] { 15.0, 488, 2.5, 115, 0, 13.8, 8.5, 126, 0 }),
            ("Whole Wheat Bread", "1 lb.", 9.1, new double[] { 12.2, 484, 2.7, 125, 0, 13.9, 6.4, 160, 0 }),
            ("Rye Bread", "1 lb.", 9.1, new double[] { 12.4, 439, 1.1, 82, 0, 9.9, 3, 66, 0 }),
            ("Pound Cake", "1 lb.", 24.8, new double[] { 8.0, 130, 0.4, 31, 18.9, 2.8, 3, 17, 0 }),
            ("Soda Crackers", "1 lb.", 15.1, new double[] { 12.5, 288, 0.5, 50, 0, 0, 0, 0, 0 }),
            ("Milk", "1 qt.", 11, new double[] { 6.1, 310, 10.5, 18, 16.8, 4, 16, 7, 177 }),
            ("Evaporated Milk (can)", "14.5 oz.", 6.7, new double[] { 8.4, 422, 15.1, 9, 26, 3, 23.5, 11, 60 }),
            ("Butter", "1 lb.", 30.8, new double[] { 10.8, 9, 0.2, 3, 44.2, 0, 0.2, 2, 0 }),
            ("Oleomargarine", "1 lb.", 16.1, new double[] { 20.6, 17, 0.6, 6, 55.8, 0.2, 0, 0, 0 }),
            ("Eggs", "1 doz.", 32.6, new double[] { 2.9, 238, 1.0, 52, 18.6, 2.8, 6.5, 1, 0 }),
            ("Cheese (Cheddar)", "1 lb.", 24.2, new double[] { 7.4, 448, 16.4, 19, 28.1, 0.8, 10.3, 4, 0 }),
            ("Cream", "1/2 pt.", 14.1, new double[] { 3.5, 49, 1.7, 3, 16.9, 0.6, 2.5, 0, 17 }),
            ("Peanut Butter", "1 lb.", 17.9, new double[] { 15.7, 661, 1.0, 48, 0, 9.6, 8.1, 471, 0 }),
            ("Mayonnaise", "1/2 pt.", 16.7, new double[] { 8.6, 18, 0.2, 8, 2.7, 0.4, 0.5, 0, 0 }),
            ("Crisco", "1 lb.", 20.3, new double[] { 20.1, 0, 0, 0, 0, 0, 0, 0, 0 }),
            ("Lard", "1 lb.", 9.8, new double[] { 41.7, 0, 0, 0, 0.2, 0, 0.5, 5, 0 }),
            ("Sirloin Steak", "1 lb.", 39.6, new double[] { 2.9, 166, 0.1, 34, 0.2, 2.1, 2.9, 69, 0 }),
            ("Round Steak", "1 lb.", 36.4, new double[] { 2.2, 214, 0.1, 32, 0.4, 2.5, 2.4, 87, 0 }),
            ("Rib Roast", "1 lb.", 29.2, new double[] { 3.4, 213, 0.1, 33, 0, 0, 2, 0, 0 }),
            ("Chuck Roast", "1 lb.", 22.6, new double[] { 3.6, 309, 0.2, 46, 0.4, 1, 4, 120, 0 }),
            ("Plate", "1 lb.", 14.6, new double[] { 8.5, 404, 0.2, 62, 0, 0.9, 0, 0, 0 }),
            ("Liver (Beef)", "1 lb.", 26.8, new double[] { 2.2, 333, 0.2, 139, 169.2, 6.4, 50.8, 316, 525 }),
            ("Leg of Lamb", "1 lb.", 27.6, new double[] { 3.1, 245, 0.1, 20, 0, 2.8, 3.9, 86, 0 }),
            ("Lamb Chops (Rib)", "1 lb.", 36.6, new double[] { 3.3, 140, 0.1, 15, 0, 1.7, 2.7, 54, 0 }),
            ("Pork Chops", "1 lb.", 30.7, new double[] { 3.5, 196, 0.2, 30, 0, 17.4, 2.7, 60, 0 }),
            ("Pork Loin Roast", "1 lb.", 24.2, new double[] { 4.4, 249, 0.3, 37, 0, 18.2, 3.6, 79, 0 }),
            ("Bacon", "1 lb.", 25.6, new double[] { 10.4, 152, 0.2, 23, 0, 1.8, 1.8, 71, 0 }),
            ("Ham, smoked", "1 lb.", 27.4, new double[] { 6.7, 212, 0.2, 31, 0, 9.9, 3.3, 50, 0 }),
            ("Salt Pork", "1 lb.", 16, new double[] { 18.8, 164, 0.1, 26, 0, 1.4, 1.8, 0, 0 }),
            ("Roasting Chicken", "1 lb.", 30.3, new double[] { 1.8, 184, 0.1, 30, 0.1, 0.9, 1.8, 68, 46 }),
            ("Veal Cutlets", "1 lb.", 42.3, new double[] { 1.7, 156, 0.1, 24, 0, 1.4, 2.4, 57, 0 }),
            ("Salmon, Pink (can)", "16 oz.", 13, new double[] { 5.8, 705, 6.8, 45, 3.5, 1, 4.9, 209, 0 }),
            ("Apples", "1 lb.", 4.4, new double[] { 5.8, 27, 0.5, 36, 7.3, 3.6, 2.7, 5, 544 }),
            ("Bananas", "1 lb.", 6.1, new double[] { 4.9, 60, 0.4, 30, 17.4, 2.5, 3.5, 28, 498 }),
            ("Lemons", "1 doz.", 26, new double[] { 1.0, 21, 0.5, 14, 0, 0.5, 0, 4, 952 }),
            ("Oranges", "1 doz.", 30.9, new double[] { 2.2, 40, 1.1, 18, 11.1, 3.6, 1.3, 10, 1998 }),
            ("Green Beans", "1 lb.", 7.1, new double[] { 2.4, 138, 3.7, 80, 69, 4.3, 5.8, 37, 862 }),
            ("Cabbage", "1 lb.", 3.7, new double[] { 2.6, 125, 4.0, 36, 7.2, 9, 4.5, 26, 5369 }),
            ("Carrots", "1 bunch", 4.7, new double[] { 2.7, 73, 2.8, 43, 188.5, 6.1, 4.3, 89, 608 }),
            ("Celery", "1 stalk", 7.3, new double[] { 0.9, 51, 3.0, 23, 0.9, 1.4, 1.4, 9, 313 }),
            ("Lettuce", "1 head", 8.2, new double[] { 0.4, 27, 1.1, 22, 112.4, 1.8, 3.4, 11, 449 }),
            ("Onions", "1 lb.", 3.6, new double[] { 5.8, 166, 3.8, 59, 16.6, 4.7, 5.9, 21, 1184 }),
            ("Potatoes", "15 lb.", 34, new double[] { 14.3, 336, 1.8, 118, 6.7, 29.4, 7.1, 198, 2522 }),
            ("Spinach", "1 lb.", 8.1, new double[] { 1.1, 106, 0, 138, 918.4, 5.7, 13.8, 33, 2755 }),
            ("Sweet Potatoes", "1 lb.", 5.1, new double[] { 9.6, 138, 2.7, 54, 290.7, 8.4, 5.4, 83, 1912 }),
            ("Peaches (can)", "No. 2 1/2", 16.8, new double[] { 3.7, 20, 0.4, 10, 21.5, 0.5, 1, 31, 196 }),
            ("Pears (can)", "No. 2 1/2", 20.4, new double[] { 3.0, 8, 0.3, 8, 0.8, 0.8, 0.8, 5, 81 }),
            ("Pineapple (can)", "No. 2 1/2", 21.3, new double[] { 2.4, 16, 0.4, 8, 2, 2.8, 0.8, 7, 399 }),
            ("Asparagus (can)", "No. 2", 27.7, new double[] { 0.4, 33, 0.3, 12, 16.3, 1.4, 2.1, 17, 272 }),
            ("Green Beans (can)", "No. 2", 10, new double[] { 1.0, 54, 2, 65, 53.9, 1.6, 4.3, 32, 431 }),
            ("Pork and Beans (can)", "16 oz.", 7.1, new double[] { 7.5, 364, 4, 134, 3.5, 8.3, 7.7, 56, 0 }),
            ("Corn (can)", "No. 2", 10.4, new double[] { 5.2, 136, 0.2, 16, 12, 1.6, 2.7, 42, 218 }),
            ("Peas (can)", "No. 2", 13.8, new double[] { 2.3, 136, 0.6, 45, 34.9, 4.9, 2.5, 37, 370 }),
            ("Tomatoes (can)", "No. 2", 8.6, new double[] { 1.3, 63, 0.7, 38, 53.2, 3.4, 2.5, 36, 1253 }),
            ("Tomato Soup (can)", "10 1/2 oz.", 7.6, new double[] { 1.6, 71, 0.6, 43, 57.9, 3.5, 2.4, 67, 862 }),
            ("Peaches, Dried", "1 lb.", 15.7, new double[] { 8.5, 87, 1.7, 173, 86.8, 1.2, 4.3, 55, 57 }),
            ("Prunes, Dried", "1 lb.", 9, new double[] { 12.8, 99, 2.5, 154, 85.7, 3.9, 4.3, 65, 257 }),
            ("Raisins, Dried", "15 oz.", 9.4, new double[] { 13.5, 104, 2.5, 136, 4.5, 6.3, 1.4, 24, 136 }),
            ("Peas, Dried", "1 lb.", 7.9, new double[] { 20.0, 1367, 4.2, 345, 2.9, 28.7, 18.4, 162, 0 }),
            ("Lima Beans, Dried", "1 lb.", 8.9, new double[] { 17.4, 1055, 3.7, 459, 5.1, 26.9, 38.2, 93, 0 }),
            ("Navy Beans, Dried", "1 lb.", 5.9, new double[] { 26.9, 1691, 11.4, 792, 0, 38.4, 24.6, 217, 0 }),
            ("Coffee", "1 lb.", 22.4, new double[] { 0, 0, 0, 0, 0, 4, 5.1, 50, 0 }),
            ("Tea", "1/4 lb.", 17.4, new double[] { 0, 0, 0, 0, 0, 0, 2.3, 42, 0 }),
            ("Cocoa", "8 oz.", 8.6, new double[] { 8.7, 237, 3, 72, 0, 2, 11.9, 40, 0 }),
            ("Chocolate", "8 oz.", 16.2, new double[] { 8.0, 77, 1.3, 39, 0, 0.9, 3.4, 14, 0 }),
            ("Sugar", "10 lb.", 51.7, new double[] { 34.9, 0, 0, 0, 0, 0, 0, 0, 0 }),
            ("Corn Syrup", "24 oz.", 13.7, new double[] { 14.7, 0, 0.5, 74, 0, 0, 0, 5, 0 }),
            ("Molasses", "18 oz.", 13.6, new double[] { 9.0, 0, 10.3, 244, 0, 1.9, 7.5, 146, 0 }),
            ("Strawberry Preserves", "1 lb.", 20.5, new double[] { 6.4, 11, 0.4, 7, 0.2, 0.2, 0.4, 3, 0 })
        };

        // Create the linear solver with the GLOP backend.
        Solver solver = Solver.CreateSolver("GLOP");
        if (solver is null)
        {
            return;
        }

        List<Variable> foods = new List<Variable>();
        for (int i = 0; i < data.Length; ++i)
        {
            foods.Add(solver.MakeNumVar(0.0, double.PositiveInfinity, data[i].Name));
        }
        Console.WriteLine($"Number of variables = {solver.NumVariables()}");

        List<Constraint> constraints = new List<Constraint>();
        for (int i = 0; i < nutrients.Length; ++i)
        {
            Constraint constraint =
                solver.MakeConstraint(nutrients[i].Value, double.PositiveInfinity, nutrients[i].Name);
            for (int j = 0; j < data.Length; ++j)
            {
                constraint.SetCoefficient(foods[j], data[j].Nutrients[i]);
            }
            constraints.Add(constraint);
        }
        Console.WriteLine($"Number of constraints = {solver.NumConstraints()}");

        Objective objective = solver.Objective();
        for (int i = 0; i < data.Length; ++i)
        {
            objective.SetCoefficient(foods[i], 1);
        }
        objective.SetMinimization();

        Solver.ResultStatus resultStatus = solver.Solve();

        // Check that the problem has an optimal solution.
        if (resultStatus != Solver.ResultStatus.OPTIMAL)
        {
            Console.WriteLine("The problem does not have an optimal solution!");
            if (resultStatus == Solver.ResultStatus.FEASIBLE)
            {
                Console.WriteLine("A potentially suboptimal solution was found.");
            }
            else
            {
                Console.WriteLine("The solver could not solve the problem.");
                return;
            }
        }

        // Display the amounts (in dollars) to purchase of each food.
        double[] nutrientsResult = new double[nutrients.Length];
        Console.WriteLine("\nAnnual Foods:");
        for (int i = 0; i < foods.Count; ++i)
        {
            if (foods[i].SolutionValue() > 0.0)
            {
                Console.WriteLine($"{data[i].Name}: ${365 * foods[i].SolutionValue():N2}");
                for (int j = 0; j < nutrients.Length; ++j)
                {
                    nutrientsResult[j] += data[i].Nutrients[j] * foods[i].SolutionValue();
                }
            }
        }
        Console.WriteLine($"\nOptimal annual price: ${365 * objective.Value():N2}");

        Console.WriteLine("\nNutrients per day:");
        for (int i = 0; i < nutrients.Length; ++i)
        {
            Console.WriteLine($"{nutrients[i].Name}: {nutrientsResult[i]:N2} (min {nutrients[i].Value})");
        }

        Console.WriteLine("\nAdvanced usage:");
        Console.WriteLine($"Problem solved in {solver.WallTime()} milliseconds");
        Console.WriteLine($"Problem solved in {solver.Iterations()} iterations");
    }
}
```



 Send feedback



Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-03-18 UTC.


Need to tell us more?






\[\[\["Easy to understand","easyToUnderstand","thumb-up"\],\["Solved my problem","solvedMyProblem","thumb-up"\],\["Other","otherUp","thumb-up"\]\],\[\["Missing the information I need","missingTheInformationINeed","thumb-down"\],\["Too complicated / too many steps","tooComplicatedTooManySteps","thumb-down"\],\["Out of date","outOfDate","thumb-down"\],\["Samples / code issue","samplesCodeIssue","thumb-down"\],\["Other","otherDown","thumb-down"\]\],\["Last updated 2026-03-18 UTC."\],\[\],\["The core content outlines the Stigler diet problem, aiming to find the least expensive food combination to meet minimum daily nutrient requirements. This involves a dataset of 77 food commodities, each with price and nutritional values (calories, protein, vitamins, etc.). Minimum daily requirements are specified for nine nutrients. The problem is solved using linear programming and the OR-Tools library, with code in Python, C++, Java, and C#, to minimize total cost while satisfying constraints. Outputs show the optimal food quantities, total cost, and nutrient intake.\\n"\]\]



Info


Chat


API