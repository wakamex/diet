# Source: The Diet Problem - NEOS Guide

- URL: https://neos-guide.org/case-studies/om/the-diet-problem/
- Slug: 05_neos_guide_diet_problem

---

[Skip to content](https://neos-guide.org/case-studies/om/the-diet-problem/#main "Skip to content")

The goal of the **diet problem** is to select a set of foods that will satisfy a set of daily nutritional requirement at minimum cost. The problem is formulated as a **linear program** where the objective is to minimize cost and the constraints are to satisfy the specified nutritional requirements. The diet problem constraints typically regulate the number of calories and the amount of vitamins, minerals, fats, sodium, and cholesterol in the diet. While the mathematical formulation is simple, the solution may not be palatable! The nutritional requirements can be met without regard for taste or variety, so consider the output before digging into a meal from an “optimal” menu!

## History

The diet problem was one of the first optimization problems studied in the 1930s and 1940s. The problem was motivated by the Army’s desire to minimize the cost of feeding GIs in the field while still providing a healthy diet. One of the early researchers to study the problem was George Stigler, who made an educated guess of an optimal solution using a heuristic method. His guess for the cost of an optimal diet was $39.93 per year (1939 prices). In the fall of 1947, Jack Laderman of the Mathematical Tables Project of the National Bureau of Standards used the newly developed simplex method to solve Stigler’s model. As the first “large scale” computation in optimization, the linear program consisted of nine equations in 77 unknowns. It took nine clerks using hand-operated desk calculators 120 man days to solve for the optimal solution of $39.69. Stigler’s guess was off by only $0.24 per year!

## Problem Statement

Given a set of foods, along with the nutrient information for each food and the cost per serving of each food, the objective of the diet problem is to select the number of servings of each food to purchase (and consume) so as to minimize the cost of the food while meeting the specified nutritional requirements. Typically, the nutritional requirements are expressed as a minimum and a maximum allowable level for each nutritional component. Other constraints such a minimum and/or maximum number of servings may be included to improve the quality of the menu.

Consider the following simple example (from [The Diet Problem: A WWW-based Interactive Case Study in Linear Programming](http://ftp.mcs.anl.gov/pub/tech_reports/reports/P602.pdf)). Suppose there are three foods available, corn, milk, and bread, and there are restrictions on the number of calories (between 2000 and 2250) and the amount of Vitamin A (between 5000 and 50,000). The first table lists, for each food, the cost per serving, the amount of Vitamin A per serving, and the number of calories per serving.

|     |     |     |     |
| --- | --- | --- | --- |
| **Food** | **Cost per serving** | **Vitamin A** | **Calories** |
| Corn | $0.18 | 107 | 72 |
| 2% Milk | $0.23 | 500 | 121 |
| Wheat Bread | $0.05 | 0 | 65 |

Suppose that the maximum number of servings is 10. Then, the optimal solution for the problem is 1.94 servings of corn, 10 servings of milk, and 10 servings of bread with a total cost of $3.15. The total amount of Vitamin A is 5208 and the total number of calories is 2000.

## Diet Problem Solver

![](https://neos-guide.org/wp-content/uploads/2022/05/Foodisammunition.jpg)

The objective of the diet problem is to select a set of foods that will satisfy a set of daily nutritional requirements at minimum cost. To create your own optimized menu, select the foods that you would like to consider in your menu and specify the nutritional constraints that you would like to satisfy. You might be surprised at the contents of an optimized menu!

|     |     |
| --- | --- |
| Enter your email address if you want the solver solution log: |  |
| The solution will output in a pop-up window. Please allow pop-ups to ensure it appears correctly. |

### Food Selection

- Mark the checkbox next to each food that you would like to consider in your menu. Note that you are more likely to get a solution if you select more food choices.
- Edit the "Min" and "Max" values if you would like to change the defaults for the number of servings of each food from Min = 0 and Max = 10.

|     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- |
|  |
| Select | Name | Serving | Price/Serving ($) | Min | Max |
|  | Frozen Broccoli | 10 Oz Pkg | 0.16 |  |  |
|  | Carrots, Raw | 1/2 Cup Shredded | 0.07 |  |  |
|  | Celery, Raw | 1 Stalk | 0.04 |  |  |
|  | Frozen Corn | 1/2 Cup | 0.18 |  |  |
|  | Lettuce, Iceberg,Raw | 1 Leaf | 0.02 |  |  |
|  | Peppers, Sweet, Raw | 1 Pepper | 0.53 |  |  |
|  | Potatoes, Baked | 1/2 Cup | 0.06 |  |  |
|  | Tofu | 1/4 block | 0.31 |  |  |
|  | Roasted Chicken | 1 lb chicken | 0.84 |  |  |
|  | Spaghetti W/ Sauce | 1 1/2 Cup | 0.78 |  |  |
|  | Tomato,Red,Ripe,Raw | 1 Tomato, 2-3/5 In | 0.27 |  |  |
|  | Apple, Raw, w/Skin | 1 Fruit,3/Lb,Wo/Rf | 0.24 |  |  |
|  | Banana | 1 Fruit | 0.15 |  |  |
|  | Grapes | 10 Grapes | 0.32 |  |  |
|  | Kiwifruit, Raw, Fresh | 1 Medium | 0.49 |  |  |
|  | Oranges | 1 Medium, 2-5/8 Diam | 0.15 |  |  |
|  | Bagels | 1 Oz | 0.16 |  |  |
|  | Wheat Bread | 1 Sl | 0.05 |  |  |
|  | White Bread | 1 Sl | 0.06 |  |  |
|  | Oatmeal Cookies | 1 Cookie | 0.09 |  |  |
|  | Apple Pie | 1 Oz | 0.16 |  |  |
|  | Chocolate Chip Cookies | 1 Cookie | 0.03 |  |  |
|  | Butter, Regular | 1 Pat | 0.05 |  |  |
|  | Cheddar Cheese | 1 Oz | 0.25 |  |  |
|  | 3.3% Fat, Whole Milk | 1 C | 0.16 |  |  |
|  | 2% Lowfat Milk | 1 C | 0.23 |  |  |
|  | Skim Milk | 1 C | 0.13 |  |  |
|  | Poached Eggs | Lrg Egg | 0.08 |  |  |
|  | Scrambled Eggs | 1 Egg | 0.11 |  |  |
|  | Bologna, Turkey | 1 Oz | 0.15 |  |  |
|  | Frankfurter, Beef | 1 Frankfurter | 0.27 |  |  |
|  | Ham, Sliced, Extralean | 1 Sl,6-1/4x4x1/16 In | 0.33 |  |  |
|  | Kielbasa, Pork | 1 Sl,6x3-3/4x1/16 In | 0.15 |  |  |
|  | Cap'N Crunch | 1 Oz | 0.31 |  |  |
|  | Cheerios | 1 Oz | 0.28 |  |  |
|  | Corn Flakes, Kellogg'S | 1 Oz | 0.28 |  |  |
|  | Raisin Bran, Kellogg'S | 1.3 Oz | 0.34 |  |  |
|  | Rice Krispies | 1 Oz | 0.32 |  |  |
|  | Special K | 1 Oz | 0.38 |  |  |
|  | Oatmeal | 1 C | 0.82 |  |  |
|  | Malt-O-Meal, Choc | 1 C | 0.52 |  |  |
|  | Pizza w/Pepperoni | 1 Slice | 0.44 |  |  |
|  | Taco | 1 Small Taco | 0.59 |  |  |
|  | Hamburger w/Toppings | 1 Burger | 0.83 |  |  |
|  | Hotdog, Plain | 1 Hotdog | 0.31 |  |  |
|  | Couscous | 1/2 Cup | 0.39 |  |  |
|  | White Rice | 1/2 Cup | 0.08 |  |  |
|  | Macaroni, cooked | 1/2 Cup | 0.17 |  |  |
|  | Peanut Butter | 2 Tbsp | 0.07 |  |  |
|  | Pork | 4 Oz | 0.81 |  |  |
|  | Sardines in Oil | 2 Sardines | 0.45 |  |  |
|  | White Tuna in Water | 3 Oz | 0.69 |  |  |
|  | Popcorn, Air-Popped | 1 Oz | 0.04 |  |  |
|  | Potato Chips, BBQ | 1 Oz | 0.22 |  |  |
|  | Pretzels | 1 Oz | 0.12 |  |  |
|  | Tortilla Chips | 1 Oz | 0.19 |  |  |
|  | Chicken Noodle Soup | 1 C (8 Fl Oz) | 0.39 |  |  |
|  | Splt Pea&Ham Soup | 1 C (8 Fl Oz) | 0.67 |  |  |
|  | Veggie Beef Soup | 1 C (8 Fl Oz) | 0.71 |  |  |
|  | New Eng Clam Chwd | 1 C (8 Fl Oz) | 0.75 |  |  |
|  | Tomato Soup | 1 C (8 Fl Oz) | 0.39 |  |  |
|  | New Eng Clam Chwd, w/Mlk | 1 C (8 Fl Oz) | 0.99 |  |  |
|  | Crm Mshrm Soup, w/Mlk | 1 C (8 Fl Oz) | 0.65 |  |  |
|  | Bean Bacon Soup, w/Watr | 1 C (8 Fl Oz) | 0.67 |  |  |

### Nutritional Requirements

- Unselect the checkbox next to any nutrients that you do not want to consider.
- Edit the "Min" and "Max" values for the nutrient levels if you would like to change them from their defaults.

|     |     |     |     |     |
| --- | --- | --- | --- | --- |
|  |
| Select | Name | Unit | Min | Max |
|  | Calories | cal |  |  |
|  | Cholesterol | mg |  |  |
|  | Total\_Fat | g |  |  |
|  | Sodium | mg |  |  |
|  | Carbohydrates | g |  |  |
|  | Dietary\_Fiber | g |  |  |
|  | Protein | g |  |  |
|  | Vit\_A | IU |  |  |
|  | Vit\_C | IU |  |  |
|  | Calcium | mg |  |  |
|  | Iron | mg |  |  |

**Nutrition information for each food**

|     |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Name | Calories | Cholesterol | Total\_Fat | Sodium | Carbohydrates | Dietary\_Fiber | Protein | Vit\_A | Vit\_C | Calcium | Iron |
| Frozen Broccoli | 73.8 | 0.0 | 0.8 | 68.2 | 13.6 | 8.5 | 8.0 | 5867.4 | 160.2 | 159.0 | 2.3 |
| Carrots, Raw | 23.7 | 0.0 | 0.1 | 19.2 | 5.6 | 1.6 | 0.6 | 15471.0 | 5.1 | 14.9 | 0.3 |
| Celery, Raw | 6.4 | 0.0 | 0.1 | 34.8 | 1.5 | 0.7 | 0.3 | 53.6 | 2.8 | 16.0 | 0.2 |
| Frozen Corn | 72.2 | 0.0 | 0.6 | 2.5 | 17.1 | 2.0 | 2.5 | 106.6 | 5.2 | 3.3 | 0.3 |
| Lettuce, Iceberg,Raw | 2.6 | 0.0 | 0.0 | 1.8 | 0.4 | 0.3 | 0.2 | 66.0 | 0.8 | 3.8 | 0.1 |
| Peppers, Sweet, Raw | 20.0 | 0.0 | 0.1 | 1.5 | 4.8 | 1.3 | 0.7 | 467.7 | 66.1 | 6.7 | 0.3 |
| Potatoes, Baked | 171.5 | 0.0 | 0.2 | 15.2 | 39.9 | 3.2 | 3.7 | 0.0 | 15.6 | 22.7 | 4.3 |
| Tofu | 88.2 | 0.0 | 5.5 | 8.1 | 2.2 | 1.4 | 9.4 | 98.6 | 0.1 | 121.8 | 6.2 |
| Roasted Chicken | 277.4 | 129.9 | 10.8 | 125.6 | 0.0 | 0.0 | 42.2 | 77.4 | 0.0 | 21.9 | 1.8 |
| Spaghetti W/ Sauce | 358.2 | 0.0 | 12.3 | 1237.1 | 58.3 | 11.6 | 8.2 | 3055.2 | 27.9 | 80.2 | 2.3 |
| Tomato,Red,Ripe,Raw | 25.8 | 0.0 | 0.4 | 11.1 | 5.7 | 1.4 | 1.0 | 766.3 | 23.5 | 6.2 | 0.6 |
| Apple, Raw, w/Skin | 81.4 | 0.0 | 0.5 | 0.0 | 21.0 | 3.7 | 0.3 | 73.1 | 7.9 | 9.7 | 0.2 |
| Banana | 104.9 | 0.0 | 0.5 | 1.1 | 26.7 | 2.7 | 1.2 | 92.3 | 10.4 | 6.8 | 0.4 |
| Grapes | 15.1 | 0.0 | 0.1 | 0.5 | 4.1 | 0.2 | 0.2 | 24.0 | 1.0 | 3.4 | 0.1 |
| Kiwifruit, Raw, Fresh | 46.4 | 0.0 | 0.3 | 3.8 | 11.3 | 2.6 | 0.8 | 133.0 | 74.5 | 19.8 | 0.3 |
| Oranges | 61.6 | 0.0 | 0.2 | 0.0 | 15.4 | 3.1 | 1.2 | 268.6 | 69.7 | 52.4 | 0.1 |
| Bagels | 78.0 | 0.0 | 0.5 | 151.4 | 15.1 | 0.6 | 3.0 | 0.0 | 0.0 | 21.0 | 1.0 |
| Wheat Bread | 65.0 | 0.0 | 1.0 | 134.5 | 12.4 | 1.3 | 2.2 | 0.0 | 0.0 | 10.8 | 0.7 |
| White Bread | 65.0 | 0.0 | 1.0 | 132.5 | 11.8 | 1.1 | 2.3 | 0.0 | 0.0 | 26.2 | 0.8 |
| Oatmeal Cookies | 81.0 | 0.0 | 3.3 | 68.9 | 12.4 | 0.6 | 1.1 | 2.9 | 0.1 | 6.7 | 0.5 |
| Apple Pie | 67.2 | 0.0 | 3.1 | 75.4 | 9.6 | 0.5 | 0.5 | 35.2 | 0.9 | 3.1 | 0.1 |
| Chocolate Chip Cookies | 78.1 | 5.1 | 4.5 | 57.8 | 9.3 | 0.0 | 0.9 | 101.8 | 0.0 | 6.2 | 0.4 |
| Butter, Regular | 35.8 | 10.9 | 4.1 | 41.3 | 0.0 | 0.0 | 0.0 | 152.9 | 0.0 | 1.2 | 0.0 |
| Cheddar Cheese | 112.7 | 29.4 | 9.3 | 173.7 | 0.4 | 0.0 | 7.0 | 296.5 | 0.0 | 202.0 | 0.2 |
| 3.3% Fat, Whole Milk | 149.9 | 33.2 | 8.1 | 119.6 | 11.4 | 0.0 | 8.0 | 307.4 | 2.3 | 291.3 | 0.1 |
| 2% Lowfat Milk | 121.2 | 18.3 | 4.7 | 121.8 | 11.7 | 0.0 | 8.1 | 500.2 | 2.3 | 296.7 | 0.1 |
| Skim Milk | 85.5 | 4.4 | 0.4 | 126.2 | 11.9 | 0.0 | 8.4 | 499.8 | 2.4 | 302.3 | 0.1 |
| Poached Eggs | 74.5 | 211.5 | 5.0 | 140.0 | 0.6 | 0.0 | 6.2 | 316.0 | 0.0 | 24.5 | 0.7 |
| Scrambled Eggs | 99.6 | 211.2 | 7.3 | 168.0 | 1.3 | 0.0 | 6.7 | 409.2 | 0.1 | 42.6 | 0.7 |
| Bologna, Turkey | 56.4 | 28.1 | 4.3 | 248.9 | 0.3 | 0.0 | 3.9 | 0.0 | 0.0 | 23.8 | 0.4 |
| Frankfurter, Beef | 141.8 | 27.4 | 12.8 | 461.7 | 0.8 | 0.0 | 5.4 | 0.0 | 10.8 | 9.0 | 0.6 |
| Ham, Sliced, Extralean | 37.1 | 13.3 | 1.4 | 405.1 | 0.3 | 0.0 | 5.5 | 0.0 | 7.4 | 2.0 | 0.2 |
| Kielbasa, Pork | 80.6 | 17.4 | 7.1 | 279.8 | 0.6 | 0.0 | 3.4 | 0.0 | 5.5 | 11.4 | 0.4 |
| Cap'N Crunch | 119.6 | 0.0 | 2.6 | 213.3 | 23.0 | 0.5 | 1.4 | 40.6 | 0.0 | 4.8 | 7.5 |
| Cheerios | 111.0 | 0.0 | 1.8 | 307.6 | 19.6 | 2.0 | 4.3 | 1252.2 | 15.1 | 48.6 | 4.5 |
| Corn Flakes, Kellogg'S | 110.5 | 0.0 | 0.1 | 290.5 | 24.5 | 0.7 | 2.3 | 1252.2 | 15.1 | 0.9 | 1.8 |
| Raisin Bran, Kellogg'S | 115.1 | 0.0 | 0.7 | 204.4 | 27.9 | 4.0 | 4.0 | 1250.2 | 0.0 | 12.9 | 16.8 |
| Rice Krispies | 112.2 | 0.0 | 0.2 | 340.8 | 24.8 | 0.4 | 1.9 | 1252.2 | 15.1 | 4.0 | 1.8 |
| Special K | 110.8 | 0.0 | 0.1 | 265.5 | 21.3 | 0.7 | 5.6 | 1252.2 | 15.1 | 8.2 | 4.5 |
| Oatmeal | 145.1 | 0.0 | 2.3 | 2.3 | 25.3 | 4.0 | 6.1 | 37.4 | 0.0 | 18.7 | 1.6 |
| Malt-O-Meal, Choc | 607.2 | 0.0 | 1.5 | 16.5 | 128.2 | 0.0 | 17.3 | 0.0 | 0.0 | 23.1 | 47.2 |
| Pizza w/Pepperoni | 181.0 | 14.2 | 7.0 | 267.0 | 19.9 | 0.0 | 10.1 | 281.9 | 1.6 | 64.6 | 0.9 |
| Taco |  | 369.4 | 56.4 | 20.6 | 802.0 | 26.7 | 0.0 | 20.7 | 855.0 | 2.2 | 220.6 |
| Hamburger w/Toppings | 275.0 | 42.8 | 10.2 | 563.9 | 32.7 | 0.0 | 13.6 | 126.3 | 2.6 | 51.4 | 2.5 |
| Hotdog, Plain | 242.1 | 44.1 | 14.5 | 670.3 | 18.0 | 0.0 | 10.4 | 0.0 | 0.1 | 23.5 | 2.3 |
| Couscous | 100.8 | 0.0 | 0.1 | 4.5 | 20.9 | 1.3 | 3.4 | 0.0 | 0.0 | 7.2 | 0.3 |
| White Rice |  | 102.7 | 0.0 | 0.2 | 0.8 | 22.3 | 0.3 | 2.1 | 0.0 | 0.0 | 7.9 |
| Macaroni, cooked | 98.7 | 0.0 | 0.5 | 0.7 | 19.8 | 0.9 | 3.3 | 0.0 | 0.0 | 4.9 | 1.0 |
| Peanut Butter | 188.5 | 0.0 | 16.0 | 155.5 | 6.9 | 2.1 | 7.7 | 0.0 | 0.0 | 13.1 | 0.6 |
| Pork | 710.8 | 105.1 | 72.2 | 38.4 | 0.0 | 0.0 | 13.8 | 14.7 | 0.0 | 59.9 | 0.4 |
| Sardines in Oil | 49.9 | 34.1 | 2.7 | 121.2 | 0.0 | 0.0 | 5.9 | 53.8 | 0.0 | 91.7 | 0.7 |
| White Tuna in Water | 115.6 | 35.7 | 2.1 | 333.2 | 0.0 | 0.0 | 22.7 | 68.0 | 0.0 | 3.4 | 0.5 |
| Popcorn, Air-Popped | 108.3 | 0.0 | 1.2 | 1.1 | 22.1 | 4.3 | 3.4 | 55.6 | 0.0 | 2.8 | 0.8 |
| Potato Chips, BBQ | 139.2 | 0.0 | 9.2 | 212.6 | 15.0 | 1.2 | 2.2 | 61.5 | 9.6 | 14.2 | 0.5 |
| Pretzels | 108.0 | 0.0 | 1.0 | 486.2 | 22.5 | 0.9 | 2.6 | 0.0 | 0.0 | 10.2 | 1.2 |
| Tortilla Chips | 142.0 | 0.0 | 7.4 | 149.7 | 17.8 | 1.8 | 2.0 | 55.6 | 0.0 | 43.7 | 0.4 |
| Chicken Noodle Soup | 150.1 | 12.3 | 4.6 | 1862.2 | 18.7 | 1.5 | 7.9 | 1308.7 | 0.0 | 27.1 | 1.5 |
| Splt Pea&Ham Soup | 184.8 | 7.2 | 4.0 | 964.8 | 26.8 | 4.1 | 11.1 | 4872.0 | 7.0 | 33.6 | 2.1 |
| Veggie Beef Soup | 158.1 | 10.0 | 3.8 | 1915.1 | 20.4 | 4.0 | 11.2 | 3785.1 | 4.8 | 32.6 | 2.2 |
| New Eng Clam Chwd | 175.7 | 10.0 | 5.0 | 1864.9 | 21.8 | 1.5 | 10.9 | 20.1 | 4.8 | 82.8 | 2.8 |
| Tomato Soup | 170.7 | 0.0 | 3.8 | 1744.4 | 33.2 | 1.0 | 4.1 | 1393.0 | 133.0 | 27.6 | 3.5 |
| New Eng Clam Chwd, w/Mlk | 163.7 | 22.3 | 6.6 | 992.0 | 16.6 | 1.5 | 9.5 | 163.7 | 3.5 | 186.0 | 1.5 |
| Crm Mshrm Soup, w/Mlk | 203.4 | 19.8 | 13.6 | 1076.3 | 15.0 | 0.5 | 6.1 | 153.8 | 2.2 | 178.6 | 0.6 |
| Bean Bacon Soup, w/Watr | 172.0 | 2.5 | 5.9 | 951.3 | 22.8 | 8.6 | 7.9 | 888.0 | 1.5 | 81.0 | 2.0 |

## Mathematical Formulation

The Diet Problem can be formulated mathematically as a linear programming problem as shown below.

**Sets**

F = set of foods

N = set of nutrients

**Parameters**

aijaij = amount of nutrient jj in food ii, ∀i∈F∀i∈F, ∀j∈N∀j∈N

cici = cost per serving of food ii, ∀i∈F∀i∈F

FminiFmini = minimum number of required servings of food ii, ∀i∈F∀i∈F

FmaxiFmaxi = maximum allowable number of servings of food ii, ∀i∈F∀i∈F

NminjNminj = minimum required level of nutrient jj, ∀j∈N∀j∈N

NmaxjNmaxj = maximum allowable level of nutrient jj, ∀j∈N∀j∈N

**Variables**

xixi = number of servings of food ii to purchase/consume, ∀i∈F∀i∈F

**Objective Function**: Minimize the total cost of the food

Minimize ∑i∈Fcixi∑i∈Fcixi

**Constraint Set 1**: For each nutrient j∈Nj∈N, at least meet the minimum required level.

∑i∈Faijxi≥Nminj,∀j∈N∑i∈Faijxi≥Nminj,∀j∈N

**Constraint Set 2**:For each nutrient j∈Nj∈N, do not exceed the maximum allowable level.

∑i∈Faijxi≤Nmaxj,∀j∈N∑i∈Faijxi≤Nmaxj,∀j∈N

**Constraint Set 3**:For each food i∈Fi∈F, select at least the minimum required number of servings.

xi≥Fmini,∀i∈Fxi≥Fmini,∀i∈F

**Constraint Set 4**:For each food i∈Fi∈F, do not exceed the maximum allowable number of servings.

xi≤Fmaxi,∀i∈Fxi≤Fmaxi,∀i∈F

To solve this linear programming problem, we can use one of the NEOS Server solvers in the Linear Programming category. Each LP solver has one or more input formats that it accepts. As an example, we provide an AMPL model for the simple example described above.

## AMPL Implementation

############# model file #############

set F;

set N;

param a{F,N} >= 0;

param c{F} >= 0;

param Fmin{F} >= 0;

param Fmax{i in F} >= Fmin\[i\];

param Nmin{j in N} >= 0;

param Nmax{j in N} >= Nmax\[j\];

var x{i in F} >= Fmin\[i\], <= Fmax\[i\];

minimize total\_cost: sum {i in F} c\[i\]\*x\[i\];

subject to nutritional\_reqs{j in N}:
Nmin\[j\] <= sum {i in F} amt \[i,j\]\*x\[i\] <= Nmax\[j\];

############# data file #############
data;
set F := corn, milk, bread;
set N := vitA, calories;

param: c Fmin Fmax :=
corn 0.18 0 10
milk 0.23 0 10
bread 0.05 0 10;

param: Nmin Nmax :=
vitA 5000 50000
calories 2000 2250;

param a: vitA calories :=
corn 107 72
milk 500 121
bread 0 65;

############# command file #############
solve;
display x;

## Interpreting the Solution

Every linear program has associated with it another linear programming problem called the dual. One key application of duality theory — the relationships between the primal problem and the dual problem — is sensitivity analysis. Associated with each constraint in the primal problem is a dual variable, which represents in some sense the cost of having the constraint in the model. In the diet problem, there are two types of constraints, bounds on the number of servings for each food type and requirements on the allowable levels for each nutrient. Consider first the bounds on the number of servings for each food type. The table below shows the number of servings in the optimal solution and the associated dual variable value.

|     |     |     |
| --- | --- | --- |
| Food | \# Servings | Dual Value |
| Corn | 1.94 | 0 |
| Milk | 10 | -0.073 |
| Bread | 10 | -0.113 |

The variables for milk and bread are both at their upper bounds and have negative dual variable values, while the variable for corn is between its lower and upper bounds and has a zero dual variable value. A simple interpretation of this information is that the cost of the menu could be decreased if the upper bounds on the number of servings of milk and bread were increased. The cost of the menu would not change in response to an increase in the upper bound on the number of servings of corn. Modifying the AMPL data file to change Fmax\[milk\] to 11 and Fmax\[bread\] to 11 and solving again yields a solution with an objective function value of $2.99 and variable values of x\[corn\] = 0, x\[milk\] = 10.6198, and x\[bread\] = 11.

Consider now the two nutrient constraints on vitamin A and calories. The level of vitamin A (in the original solution) is 5208, which is between its minimum and maximum allowable levels, and therefore the corresponding dual variable values for both bounds are zero. The number of calories (in the original solution) is 2000, however, which is the minimum required. The corresponding dual variable value for the lower bound on the number of calories is 0.0025, which can be interpreted as the amount by which the objective function will decrease per unit of decrease in the bound. Therefore, modifying the AMPL data file to change Nmin\[calories\] to 1999 and solving again yields an optimal solution with an objective function value of $3.1475 and variable values of x\[corn\] = 1.93, x\[milk\] = 10, and x\[bread\] = 10. The objective function value decreased from $3.15 to $3.1475 as expected. Additional sensitivity analysis can be done to investigate the impacts of changing the cost coefficients as well as the aijaij parameter values.

For more information on linear programming, consult one of the many good references available, such as _Introduction to Operations Research, 8th ed_ by Hillier and Lieberman or _Introduction to Linear Optimization_ by Bertsimas and Tsitsiklis.

## Acknowledgments

\\* The nutrition information was obtained from [USDA Ag Data Commons](https://data.nal.usda.gov/dataset/fooddata-central).

\\* The demo and description of this case study were originally created by [Optimization Center at Northwestern University](https://www.mccormick.northwestern.edu/research/optimization-machine-learning-center/).

\\* The history of the diet problem was obtained from George Dantzig’s 1990 article in _Interfaces_: G.B. Dantzig. The Diet Problem, _Interfaces_ 20(4), 1990, 43-47.