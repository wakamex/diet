# Source: Enhancing Decision Space Diversity in Multi-Objective Evolutionary Optimization for the Diet Problem

- URL: https://arxiv.org/html/2508.07077
- Slug: 12_arxiv_2025_decision_space_diversity

---

# Enhancing Decision Space Diversity in Multi-Objective Evolutionary Optimization for the Diet Problem

Report issue for preceding element

Gustavo V. Nascimento1, Ivan R. Meneghini1, Valéria Santos1,

Eduardo Luz1 and Gladston Moreira1

1Computing Department, Universidade Federal de Ouro Preto, Ouro
Preto, 35402-136, Minas Gerais, Brazil.

gladston@ufop.edu.br

Report issue for preceding element

###### Abstract

Report issue for preceding element

Multi-objective evolutionary algorithms (MOEAs) are essential for solving complex optimization problems, such as the diet problem, where balancing conflicting objectives, like cost and nutritional content, is crucial.
However, most MOEAs focus on optimizing solutions in the objective space, often neglecting the diversity of solutions in the decision space, which is critical for providing decision-makers with a wide range of choices.
This paper introduces an approach that directly integrates a Hamming distance-based measure of uniformity into the selection mechanism of a MOEA to enhance decision space diversity.
Experiments on a multi-objective formulation of the diet problem demonstrate that our approach significantly improves decision space diversity compared to NSGA-II, while maintaining comparable objective space performance.
The proposed method offers a generalizable strategy for integrating decision space awareness into MOEAs.

Report issue for preceding element

_K_ eywords Multi-objective optimization  ⋅\\cdot
Evolutionary algorithms  ⋅\\cdot
Decision space diversity  ⋅\\cdot
Hamming distance  ⋅\\cdot
Diet problem.

Report issue for preceding element

## 1 Introduction

Report issue for preceding element

The growing emphasis on healthy lifestyles has increased the importance of optimizing food selection to meet nutritional needs while minimizing cost and maximizing variety \[ [1](https://arxiv.org/html/2508.07077v1#bib.bib1 ""), [2](https://arxiv.org/html/2508.07077v1#bib.bib2 ""), [3](https://arxiv.org/html/2508.07077v1#bib.bib3 "")\].
The diet problem, initially proposed by \[ [4](https://arxiv.org/html/2508.07077v1#bib.bib4 "")\], captures the core challenge of finding a cost-effective food combination that satisfies nutritional requirements.
In real-world scenarios, the diet problem extends beyond cost minimization to include multiple conflicting objectives, such as maximizing nutritional diversity and specific nutrient intake, posing a significant multi-objective optimization challenge \[ [5](https://arxiv.org/html/2508.07077v1#bib.bib5 ""), [6](https://arxiv.org/html/2508.07077v1#bib.bib6 ""), [7](https://arxiv.org/html/2508.07077v1#bib.bib7 "")\].
The high dimensionality and combinatorial nature of the problem make finding a set of Pareto-optimal solutions computationally intensive, necessitating efficient multi-objective evolutionary algorithms (MOEAs) \[ [8](https://arxiv.org/html/2508.07077v1#bib.bib8 "")\].

Report issue for preceding element

While MOEAs excel at exploring the objective space to approximate the Pareto front, they often overlook the importance of diversity in the decision space \[ [9](https://arxiv.org/html/2508.07077v1#bib.bib9 "")\].
Offering a wide range of food combinations is crucial for effective diet planning, enabling decision-makers (e.g., nutritionists or individuals) to select solutions that best suit their personal preferences and constraints.

Report issue for preceding element

This paper addresses this gap by introducing the Dominance-Weight Hamming Distance (DWH) heuristic, a heuristic that explicitly promotes decision space diversity, using a Hamming distance-based uniformity measure. The DWH heuristic extends the Dominance-Weighted Uniformity (DWU) approach in \[ [9](https://arxiv.org/html/2508.07077v1#bib.bib9 "")\] for discrete multi-objective optimization problems.
We evaluate our approach on a multi-objective formulation of the diet problem, comparing it against the well-established NSGA-II \[ [10](https://arxiv.org/html/2508.07077v1#bib.bib10 "")\].
Our results demonstrate a significant improvement in decision space diversity, as measured by the minimum and average Hamming distances, with comparable Hypervolume in the objective space.
This suggests that our method effectively explores a wider range of dietary options without compromising the quality of the solutions in terms of cost, protein content, and variety.
Our key contributions are:

Report issue for preceding element

- •


Integration of a Hamming distance-based uniformity measure into the selection process of a MOEA to enhance decision space diversity;

Report issue for preceding element

- •


A demonstration of the effectiveness of this approach in the context of the multi-objective diet problem, a challenging real-world optimization problem;

Report issue for preceding element

- •


A quantitative comparison with NSGA-II, highlighting the trade-off between decision space diversity and objective space performance.

Report issue for preceding element


Future work will explore the application of this approach to other multi-objective optimization problems and investigate alternative measures of decision space diversity.

Report issue for preceding element

## 2 Related Work

Report issue for preceding element

The multi-objective diet problem has been addressed using various MOEAs and modeling techniques. In \[ [11](https://arxiv.org/html/2508.07077v1#bib.bib11 "")\], the authors use NSGA-II to generate personalized diets based on user characteristics, focusing on objective space optimization. A multi-objective model that minimizes cost, unhealthy fats, and sugar, while maximizing fiber intake, is proposed in \[ [5](https://arxiv.org/html/2508.07077v1#bib.bib5 "")\]. Still, their approach uses scalarization methods, which are known to sometimes struggle with Pareto front diversity.

Report issue for preceding element

The work in \[ [6](https://arxiv.org/html/2508.07077v1#bib.bib6 "")\] presents an approach to the menu planning problem, specifically for school canteens. The approach aims to minimize the cost of the menus and the repetition of courses and food groups. To solve this, the authors proposed a multi-objective memetic algorithm based on the MOEA/D framework.

Report issue for preceding element

In \[ [12](https://arxiv.org/html/2508.07077v1#bib.bib12 "")\], the authors compared different MOEAs for school lunch planning, showing the effectiveness of NSGA-II and SPEA2 under different conditions. However, their analysis centers on objective space metrics, such as Hypervolume. A bi-level recommender system for food diets, utilizing NSGA-II at the higher level to determine the optimal combination of foods, is presented in \[ [7](https://arxiv.org/html/2508.07077v1#bib.bib7 "")\]. The authors in \[ [13](https://arxiv.org/html/2508.07077v1#bib.bib13 "")\] incorporated fuzzy inference to represent user preferences in the objective function, showing the importance of personalized models.

Report issue for preceding element

The authors in \[ [9](https://arxiv.org/html/2508.07077v1#bib.bib9 "")\] introduced a uniformity measure weighted by dominance for decision space diversity. However, its formulation aims to solve continuous multi-objective optimization problems.

Report issue for preceding element

This paper introduces the DWH heuristic, a heuristic based on the Hamming distance, which is more suitable for the discrete nature of the diet problem’s decision variables (i.e., food choices).

Report issue for preceding element

## 3 Background

Report issue for preceding element

### 3.1 Problem Setting

Report issue for preceding element

The diet problem, in its basic form, aims to minimize the cost of a diet while satisfying nutritional requirements \[ [4](https://arxiv.org/html/2508.07077v1#bib.bib4 "")\].
Let A={1,2,…,n}A=\\{1,2,...,n\\} be the set of nn available food items, and N={1,2,…,m}N=\\{1,2,...,m\\} be the set of mm essential nutrients.
The classical formulation, using linear programming, is:

Report issue for preceding element

|     |     |     |     |
| --- | --- | --- | --- |
|  | minimizef1​(x)=∑i=1nci​xi\\text{minimize}\\quad f\_{1}(x)=\\sum\_{i=1}^{n}c\_{i}x\_{i} |  | (1) |

subject to:

Report issue for preceding element

|     |     |     |     |
| --- | --- | --- | --- |
|  | ∑i=1nai​j​xi≥Rj,∀j∈N\\sum\_{i=1}^{n}a\_{ij}x\_{i}\\geq R\_{j},\\quad\\forall j\\in N |  | (2) |

|     |     |     |     |
| --- | --- | --- | --- |
|  | xi≥0,∀i∈Ax\_{i}\\geq 0,\\quad\\forall i\\in A |  | (3) |

where cic\_{i} is the cost per serving of food item ii, xix\_{i} is the number of servings of food item ii, ai​ja\_{ij} is the amount of nutrient jj in food item ii, and RjR\_{j} is the minimum required amount of nutrient jj.

Report issue for preceding element

In this work, we extend this classical formulation to a multi-objective optimization problem over a 7-day period, considering the following objectives:

Report issue for preceding element

1. 1.


Minimize Cost:f1f\_{1} as defined in Equation [1](https://arxiv.org/html/2508.07077v1#S3.E1 "Equation 1 ‣ 3.1 Problem Setting ‣ 3 Background ‣ Enhancing Decision Space Diversity in Multi-Objective Evolutionary Optimization for the Diet Problem"), extended over 7 days:

Report issue for preceding element

|     |     |     |     |
| --- | --- | --- | --- |
|  | f1​(x)=∑d=17∑i=1nci​xi​df\_{1}(x)=\\sum\_{d=1}^{7}\\sum\_{i=1}^{n}c\_{i}x\_{id} |  | (4) |



where xi​dx\_{id} is the number of servings of food item ii on day dd.

Report issue for preceding element

2. 2.


Minimize Repetitiveness: Following \[ [12](https://arxiv.org/html/2508.07077v1#bib.bib12 "")\], we minimize the repetitiveness of food categories across days.
Let G={1,2,…,p}G=\\{1,2,...,p\\} be the set of pp food categories.
The repetitiveness penalty for day dd is:

Report issue for preceding element

|     |     |     |     |
| --- | --- | --- | --- |
|  | vd=∑k=1d−1(∑g=1pyg​k​pg+zk​pp+k)v\_{d}=\\sum\_{k=1}^{d-1}\\left(\\sum\_{g=1}^{p}y\_{gk}p\_{g}+z\_{k}p\_{p+k}\\right) |  | (5) |



where yg​k=1y\_{gk}=1 if category gg is repeated on day d−kd-k and 0 otherwise, zk=1z\_{k}=1 if any category is repeated kk days before, and pgp\_{g} and pp+kp\_{p+k} are the repetition penalties (see Table [1](https://arxiv.org/html/2508.07077v1#S3.T1 "Table 1 ‣ 3.1 Problem Setting ‣ 3 Background ‣ Enhancing Decision Space Diversity in Multi-Objective Evolutionary Optimization for the Diet Problem")).
The overall repetitiveness objective is:

Report issue for preceding element

|     |     |     |     |
| --- | --- | --- | --- |
|  | f2​(x)=∑d=17vdf\_{2}(x)=\\sum\_{d=1}^{7}v\_{d} |  | (6) |

3. 3.


Maximize Protein: We maximize the total protein content of the diet:

Report issue for preceding element

|     |     |     |     |
| --- | --- | --- | --- |
|  | f3​(x)=∑d=17∑i=1nui​xi​df\_{3}(x)=\\sum\_{d=1}^{7}\\sum\_{i=1}^{n}u\_{i}x\_{id} |  | (7) |



where uiu\_{i} is the protein content per serving of food item ii.

Report issue for preceding element


The multi-objective problem is then:

Report issue for preceding element

|     |     |     |     |
| --- | --- | --- | --- |
|  | minimizeF​(x)=(f1​(x),f2​(x),−f3​(x))\\text{minimize}\\quad F(x)=(f\_{1}(x),f\_{2}(x),-f\_{3}(x)) |  | (8) |

subject to:

Report issue for preceding element

|     |     |     |     |
| --- | --- | --- | --- |
|  | ∑i=1nai​j​xi​d≥Rj,∀j∈N,∀d∈{1,2,…,7}\\sum\_{i=1}^{n}a\_{ij}x\_{id}\\geq R\_{j},\\quad\\forall j\\in N,\\forall d\\in\\{1,2,...,7\\} |  | (9) |

|     |     |     |     |
| --- | --- | --- | --- |
|  | xi​d≥0,∀i∈A,∀d∈{1,2,…,7}x\_{id}\\geq 0,\\quad\\forall i\\in A,\\forall d\\in\\{1,2,...,7\\} |  | (10) |

This formulation presents a challenging multi-objective optimization problem with a large, complex search space. Our approach focuses on effectively exploring this space while maintaining diversity in the set of solutions.

Report issue for preceding element

Table 1: Repetition penalties considered to minimize the repetitiveness of food categories across days.

| Penalty | Description | Value |
| --- | --- | --- |
| p1p\_{1} | Repeat “Other” category | 0.1 |
| p2p\_{2} | Repeat “Meats” category | 3 |
| p3p\_{3} | Repeat “Cereals” category | 0.3 |
| p4p\_{4} | Repeat “Fruits” category | 0.1 |
| p5p\_{5} | Repeat “Dairy” category | 0.3 |
| p6p\_{6} | Repeat “Legumes” category | 0.3 |
| p7p\_{7} | Repeat “Seafood” category | 0.5 |
| p8p\_{8} | Repeat “Vegetables” category | 0.1 |
| p9p\_{9} | Repeat category 1 day before | 3 |
| p10p\_{10} | Repeat category 2 days before | 2.5 |
| p11p\_{11} | Repeat category 3 days before | 1.8 |
| p12p\_{12} | Repeat category 4 days before | 1 |
| p13p\_{13} | Repeat category 5 days before | 0.2 |
| p14p\_{14} | Repeat category 6 days before | 0.1 |

Report issue for preceding element

### 3.2 Dataset

Report issue for preceding element

We used the TACO dataset - (Brazilian Food Composition Table)\[ [14](https://arxiv.org/html/2508.07077v1#bib.bib14 "")\], which provides nutritional information for 597 food items across 15 categories (see Table [2](https://arxiv.org/html/2508.07077v1#S3.T2 "Table 2 ‣ 3.2 Dataset ‣ 3 Background ‣ Enhancing Decision Space Diversity in Multi-Objective Evolutionary Optimization for the Diet Problem")).
Since the TACO dataset lacks cost information, we assigned random costs between $1.00 and $10.00 to each food item.
The nutritional requirements (RjR\_{j} in Equation ( [9](https://arxiv.org/html/2508.07077v1#S3.E9 "Equation 9 ‣ 3.1 Problem Setting ‣ 3 Background ‣ Enhancing Decision Space Diversity in Multi-Objective Evolutionary Optimization for the Diet Problem"))) were based on the Brazilian Recommended Daily Intake values provided by ANVISA - (National Health Surveillance Agency in Brazil)\[ [15](https://arxiv.org/html/2508.07077v1#bib.bib15 "")\].

Report issue for preceding element

Table 2: TACO dataset \[ [14](https://arxiv.org/html/2508.07077v1#bib.bib14 "")\] composed of 15 Food Categories with 597 food items.

| Category | Number of Items |
| --- | --- |
| Cereals and derivatives | 63 |
| Vegetables, greens, and derivatives | 99 |
| Fruits and derivatives | 96 |
| Fats and oils | 14 |
| fish and Seafood | 50 |
| Meats and meat products | 123 |
| Milk and dairy products | 24 |
| Alcoholic and non-alcoholic beverages | 14 |
| Eggs and derivatives | 7 |
| Sugary products | 20 |
| Miscellaneous | 9 |
| Other processed foods | 5 |
| Prepared food | 32 |
| Legumes and derivatives | 30 |
| Nuts and seeds | 11 |

Report issue for preceding element

## 4 Method

Report issue for preceding element

Our approach integrates a Hamming distance-based uniformity measure into the selection process of a multi-objective evolutionary algorithm.
The aim is to generate a set of Pareto-optimal solutions that are well-distributed in the objective space and diverse in the decision space.

Report issue for preceding element

### 4.1 Uniformity Measure based on Hamming Distance

Report issue for preceding element

We define a uniformity measure, wd​Hw\_{dH}, that quantifies the dissimilarity between two diets based on their Hamming distance.
Given two diets 𝒟\\mathcal{D} and 𝒟′\\mathcal{D}^{\\prime}, represented by binary vectors xx and x′x^{\\prime} of length nn (the number of food items), wd​Hw\_{dH} is calculated as:

Report issue for preceding element

|     |     |     |     |
| --- | --- | --- | --- |
|  | wd​H​(x,x′)=dH​(x,x′)\|r​(x)−r​(x′)\|+1w\_{dH}(x,x^{\\prime})=\\frac{d\_{H}(x,x^{\\prime})}{\|r(x)-r(x^{\\prime})\|+1} |  | (11) |

where dH​(x,x′)d\_{H}(x,x^{\\prime}) is the Hamming distance between the binary vectors representing the diets, defined by equation ( [13](https://arxiv.org/html/2508.07077v1#S5.E13 "Equation 13 ‣ 5.1 Hamming Distance ‣ 5 Experimental Setup ‣ Enhancing Decision Space Diversity in Multi-Objective Evolutionary Optimization for the Diet Problem")), and r​(x)r(x) is the SPEA-2 raw fitness of solution xx, as described in \[ [16](https://arxiv.org/html/2508.07077v1#bib.bib16 "")\].
The denominator normalizes the Hamming distance by the difference in fitness values, giving more weight to solutions that are dissimilar in the decision space and have similar fitness.
This measure is then incorporated into a MinMax heuristic, shown in Algorithm [1](https://arxiv.org/html/2508.07077v1#alg1 "Algorithm 1 ‣ 4.2 Multi-Objective Evolutionary Algorithm with Hamming Diversity (MOEA-HD) ‣ 4 Method ‣ Enhancing Decision Space Diversity in Multi-Objective Evolutionary Optimization for the Diet Problem"), to guide the selection process in the evolutionary algorithm.

Report issue for preceding element

### 4.2 Multi-Objective Evolutionary Algorithm with Hamming Diversity (MOEA-HD)

Report issue for preceding element

Our MOEA-HD algorithm follows a standard evolutionary algorithm framework with modifications to the selection process to incorporate the wd​Hw\_{dH} measure.
A solution is represented as a matrix of size n×7n\\times 7, where nn is the number of food items, and each element (i,d)(i,d) represents the number of servings of food item ii on day dd.
The algorithm proceeds as follows:

Report issue for preceding element

1. 1.


Initialization: Generate an initial population P0P\_{0} of kk individuals (diets) randomly. Apply a repair operator to ensure all individuals satisfy the nutritional constraints (Equation [9](https://arxiv.org/html/2508.07077v1#S3.E9 "Equation 9 ‣ 3.1 Problem Setting ‣ 3 Background ‣ Enhancing Decision Space Diversity in Multi-Objective Evolutionary Optimization for the Diet Problem")).

Report issue for preceding element

2. 2.


Iteration: For t=0t=0 to m​a​x​\_​g​e​nmax\\\_gen:

Report issue for preceding element

1. (a)


      Fitness Assignment: Calculate the fitness of each individual in PtP\_{t} using Non-dominated Sorting as in NSGA-II \[ [10](https://arxiv.org/html/2508.07077v1#bib.bib10 "")\].

      Report issue for preceding element

2. (b)


      Selection: Perform kk binary tournaments. The winner of each tournament is determined by:

      Report issue for preceding element

      - •


        If one solution is feasible and the other is not, the feasible solution wins.

        Report issue for preceding element

      - •


        If both are infeasible, the solution with the lower constraint violation penalty (Equation [12](https://arxiv.org/html/2508.07077v1#S4.E12 "Equation 12 ‣ 4.3 Constraint Handling ‣ 4 Method ‣ Enhancing Decision Space Diversity in Multi-Objective Evolutionary Optimization for the Diet Problem")) wins.

        Report issue for preceding element

      - •


        If both are feasible, the solution that maximizes wd​Hw\_{dH} with respect to other selected solutions wins (using Algorithm [1](https://arxiv.org/html/2508.07077v1#alg1 "Algorithm 1 ‣ 4.2 Multi-Objective Evolutionary Algorithm with Hamming Diversity (MOEA-HD) ‣ 4 Method ‣ Enhancing Decision Space Diversity in Multi-Objective Evolutionary Optimization for the Diet Problem")).

        Report issue for preceding element


3. (c)


      Crossover: Apply multi-point crossover (20 points) on selected pairs to generate offspring.

      Report issue for preceding element

4. (d)


      Mutation: Apply bit-flip mutation to the offspring.

      Report issue for preceding element

5. (e)


      Population Update: Combine PtP\_{t} and the offspring, and use Algorithm [1](https://arxiv.org/html/2508.07077v1#alg1 "Algorithm 1 ‣ 4.2 Multi-Objective Evolutionary Algorithm with Hamming Diversity (MOEA-HD) ‣ 4 Method ‣ Enhancing Decision Space Diversity in Multi-Objective Evolutionary Optimization for the Diet Problem") to select the kk individuals for Pt+1P\_{t+1}.

      Report issue for preceding element


3. 3.


Final Repair: Apply the repair operator to the individuals in the final population Pm​a​x​\_​g​e​nP\_{max\\\_gen}.

Report issue for preceding element

4. 4.


Output: Return the non-dominated solutions from Pm​a​x​\_​g​e​nP\_{max\\\_gen}.

Report issue for preceding element


Algorithm 1 DWH Heuristic for Diversity Selection

0: Population PP, scalar kk

0: Set of diverse solutions RR

1:NP←N\_{P}\\leftarrow Non-dominated solutions of PP

2:R←arg⁡maxx,x′∈NP⁡wd​H​(x,x′)R\\leftarrow\\arg\\max\_{x,x^{\\prime}\\in N\_{P}}w\_{dH}(x,x^{\\prime})

3:while\|R\|<k\|R\|<kdo

4:x′←arg⁡maxx∈P∖R⁡minr∈R⁡wd​H​(x,r)x^{\\prime}\\leftarrow\\arg\\max\_{x\\in P\\setminus R}\\min\_{r\\in R}w\_{dH}(x,r)

5:R←R∪{x′}R\\leftarrow R\\cup\\{x^{\\prime}\\}

6:returnRR

Report issue for preceding element

### 4.3 Constraint Handling

Report issue for preceding element

Solutions that violate the nutritional constraints (Equation [9](https://arxiv.org/html/2508.07077v1#S3.E9 "Equation 9 ‣ 3.1 Problem Setting ‣ 3 Background ‣ Enhancing Decision Space Diversity in Multi-Objective Evolutionary Optimization for the Diet Problem")) are penalized.
The penalty is calculated as the sum of the deficits for each nutrient and day:

Report issue for preceding element

|     |     |     |     |
| --- | --- | --- | --- |
|  | penalty=∑d=17∑j=1mmax⁡(0,Rj−ai​j​xi​d)\\text{penalty}=\\sum\_{d=1}^{7}\\sum\_{j=1}^{m}\\max(0,R\_{j}-a\_{ij}x\_{id}) |  | (12) |

This penalty is used in the selection process to favor feasible solutions and to differentiate between infeasible solutions.

Report issue for preceding element

## 5 Experimental Setup

Report issue for preceding element

To evaluate the effectiveness of our MOEA-HD, we compared its performance with that of NSGA-II \[ [10](https://arxiv.org/html/2508.07077v1#bib.bib10 "")\], a widely used and effective multi-objective evolutionary algorithm.
Both algorithms were implemented in Python, and experiments were conducted on a machine equipped with a Ryzen 5 2600 processor and 16GB of RAM.

Report issue for preceding element

### 5.1 Hamming Distance

Report issue for preceding element

The Hamming distance \[ [17](https://arxiv.org/html/2508.07077v1#bib.bib17 "")\] is a metric used to measure the difference between two binary strings.
Given two strings of equal length, the Hamming distance is the number of positions at which the corresponding symbols differ.
Formally, given two binary strings a=a1​a2​…​ana=a\_{1}a\_{2}\\ldots a\_{n} and b=b1​b2​…​bnb=b\_{1}b\_{2}\\ldots b\_{n}, with ai,bj∈{0,1},i,j=1,2,…​na\_{i},b\_{j}\\in\\{0,1\\},~i,j=1,2,\\ldots n, the Hamming distance dHd\_{H} between aa and bb is:

Report issue for preceding element

|     |     |     |     |
| --- | --- | --- | --- |
|  | dH​(a,b)=∑i=1n\|ai−bi\|d\_{H}(a,b)=\\sum\_{i=1}^{n}\|a\_{i}-b\_{i}\| |  | (13) |

In this work we will represent the string x=x1​x2,…​xnx=x\_{1}x\_{2},\\ldots x\_{n} as a binary vector x=(x1,x2,…,xn),xi∈{0,1},i=1,2,…​nx=(x\_{1},x\_{2},\\ldots,x\_{n}),~x\_{i}\\in\\{0,1\\},~i=1,2,\\ldots n. Furthermore, we represent each diet as a binary vector where each element indicates the presence or absence of a particular food item. The Hamming distance then measures how different two diets are in terms of their food composition.

Report issue for preceding element

### 5.2 Performance Metrics

Report issue for preceding element

To evaluate the performance of our algorithm, we use two sets of metrics:

Report issue for preceding element

#### 5.2.1 Objective Space Metric

Report issue for preceding element

- •


Hypervolume: This metric measures the region’s volume in the objective space dominated by the non-dominated solutions and bounded by a reference point \[ [18](https://arxiv.org/html/2508.07077v1#bib.bib18 "")\]. A higher hypervolume generally indicates a better approximation of the Pareto front.

Report issue for preceding element


#### 5.2.2 Decision Space Metrics

Report issue for preceding element

- •


𝐝𝐇𝐦𝐢𝐧\\mathbf{d\_{Hmin}}: The minimum Hamming distance between any two solutions in the non-dominated set. This metric reflects the closeness of the most similar solutions; a higher value indicates better diversity.

Report issue for preceding element

|     |     |     |     |
| --- | --- | --- | --- |
|  | dH​m​i​n=m​i​n​(dH​(x,x′))d\_{Hmin}=min(d\_{H}(x,x^{\\prime})) |  | (14) |

- •


𝐝𝐇𝐦𝐞𝐝\\mathbf{d\_{Hmed}}: The average Hamming distance between all pairs of solutions in the non-dominated set. This provides an overall measure of diversity in the decision space; a higher value is desirable.

Report issue for preceding element

|     |     |     |     |
| --- | --- | --- | --- |
|  | dH​m​e​d=∑x′∈𝒟∑x∈𝒟dH​(x,x′)\|𝒟\|2d\_{Hmed}=\\frac{\\sum\_{x^{\\prime}\\in\\mathcal{D}}\\sum\_{x\\in\\mathcal{D}}d\_{H}(x,x^{\\prime})}{\|\\mathcal{D}\|^{2}} |  | (15) |


### 5.3 Parameters

Report issue for preceding element

The parameters for both algorithms were:

Report issue for preceding element

- •


Population size: 30

Report issue for preceding element

- •


Initialization: Food quantities were randomly initialized with a weighted distribution (94% chance of 0, 4% of 1, 1% of 2 servings).

Report issue for preceding element

- •


Maximum generations: 30, 100, 300

Report issue for preceding element

- •


Crossover: 20-point multi-point crossover

Report issue for preceding element

- •


Mutation: Bit-flip with 5% probability for 1-to-0 and 0.16% for 0-to-1 flips.

Report issue for preceding element


For each algorithm, we run it 30 times for each generation setting, and the average results were recorded.
Hypervolume was calculated using a reference point based on the worst-case objective values, and the objective values were normalized prior to hypervolume calculation.

Report issue for preceding element

## 6 Results and Discussion

Report issue for preceding element

### 6.1 Performance metrics

Report issue for preceding element

Table [3](https://arxiv.org/html/2508.07077v1#S6.T3 "Table 3 ‣ 6.1 Performance metrics ‣ 6 Results and Discussion ‣ Enhancing Decision Space Diversity in Multi-Objective Evolutionary Optimization for the Diet Problem") presents the comparative results of MOEA-HD and NSGA-II. The key observation is that MOEA-HD consistently outperforms NSGA-II in decision space diversity metrics [5.2.2](https://arxiv.org/html/2508.07077v1#S5.SS2.SSS2 "5.2.2 Decision Space Metrics ‣ 5.2 Performance Metrics ‣ 5 Experimental Setup ‣ Enhancing Decision Space Diversity in Multi-Objective Evolutionary Optimization for the Diet Problem").
This confirms our hypothesis that incorporating Hamming distance into the selection process effectively promotes the generation of more diverse dietary solutions.

Report issue for preceding element

Table 3: Hypervolume, minimum and average Hamming distances of the solutions obtained by the MOEA-HD and NSGA-II algorithms.

| Generations | MOEA-HD | NSGA-II |
| --- | --- | --- |
| Hv | 𝐝𝐇𝐦𝐢𝐧\\mathbf{d\_{Hmin}} | 𝐝𝐇𝐦𝐞𝐝\\mathbf{d\_{Hmed}} | Hv | 𝐝𝐇𝐦𝐢𝐧\\mathbf{d\_{Hmin}} | 𝐝𝐇𝐦𝐞𝐝\\mathbf{d\_{Hmed}} |
| --- | --- | --- | --- | --- | --- |
| 30 | 0.379 | 95.03 | 184.77 | 0.446 | 43.30 | 157.90 |
| 100 | 0.387 | 87.90 | 159.91 | 0.412 | 32.86 | 121.30 |
| 300 | 0.389 | 90.46 | 154.39 | 0.381 | 26.56 | 108.82 |

Report issue for preceding element

Specifically, at 30 generations, the minimum Hamming distance dH​m​i​nd\_{Hmin} for MOEA-HD is 95.03, compared to 43.30 for NSGA-II.
This indicates that even the most similar solutions generated by MOEA-HD are significantly more different than those generated by NSGA-II.
The average Hamming distance dH​m​e​dd\_{Hmed} also exhibits a similar trend, with MOEA-HD achieving higher values, which confirms greater overall diversity.
Importantly, this enhanced diversity in the decision space is achieved without a significant compromise in objective space performance, as the hypervolume values are comparable between the two algorithms.

Report issue for preceding element

### 6.2 Objective space

Report issue for preceding element

Figure [1](https://arxiv.org/html/2508.07077v1#S6.F1 "Figure 1 ‣ 6.2 Objective space ‣ 6 Results and Discussion ‣ Enhancing Decision Space Diversity in Multi-Objective Evolutionary Optimization for the Diet Problem") visually compares the Pareto front approximations obtained by both algorithms after 100 generations.
While both algorithms cover a similar region in the objective space, the solutions generated by MOEA-HD appear to be more evenly distributed, as reflected in the quantitative diversity measures.

Report issue for preceding element

![Refer to caption](https://arxiv.org/html/2508.07077v1/x1.png)(a) MOEA-HD algorithm.Report issue for preceding element

![Refer to caption](https://arxiv.org/html/2508.07077v1/x2.png)(b) NSGA-II algorithm.Report issue for preceding element

Figure 1: Pareto front approximations for Maximum generations =300=300 for: (a) MOEA-HD algorithm; (b) NSGA-II algorithm.Report issue for preceding element

### 6.3 Decision space

Report issue for preceding element

Figures [2](https://arxiv.org/html/2508.07077v1#S6.F2 "Figure 2 ‣ 6.3 Decision space ‣ 6 Results and Discussion ‣ Enhancing Decision Space Diversity in Multi-Objective Evolutionary Optimization for the Diet Problem") and [3](https://arxiv.org/html/2508.07077v1#S6.F3 "Figure 3 ‣ 6.3 Decision space ‣ 6 Results and Discussion ‣ Enhancing Decision Space Diversity in Multi-Objective Evolutionary Optimization for the Diet Problem") illustrate the diets proposed by the algorithms. In each figure, the points in the decision space of one execution of each algorithm are grouped according to the categories presented in Table [2](https://arxiv.org/html/2508.07077v1#S3.T2 "Table 2 ‣ 3.2 Dataset ‣ 3 Background ‣ Enhancing Decision Space Diversity in Multi-Objective Evolutionary Optimization for the Diet Problem"). Figure [2](https://arxiv.org/html/2508.07077v1#S6.F2 "Figure 2 ‣ 6.3 Decision space ‣ 6 Results and Discussion ‣ Enhancing Decision Space Diversity in Multi-Objective Evolutionary Optimization for the Diet Problem") illustrates the weekly consumption of the items, while Figure [3](https://arxiv.org/html/2508.07077v1#S6.F3 "Figure 3 ‣ 6.3 Decision space ‣ 6 Results and Discussion ‣ Enhancing Decision Space Diversity in Multi-Objective Evolutionary Optimization for the Diet Problem") presents the diets proposed for each day of the week.

Report issue for preceding element

The comparison of Figures [2(a)](https://arxiv.org/html/2508.07077v1#S6.F2.sf1 "Figure 2(a) ‣ Figure 2 ‣ 6.3 Decision space ‣ 6 Results and Discussion ‣ Enhancing Decision Space Diversity in Multi-Objective Evolutionary Optimization for the Diet Problem") and [2(b)](https://arxiv.org/html/2508.07077v1#S6.F2.sf2 "Figure 2(b) ‣ Figure 2 ‣ 6.3 Decision space ‣ 6 Results and Discussion ‣ Enhancing Decision Space Diversity in Multi-Objective Evolutionary Optimization for the Diet Problem") shows that the MOEA-HD algorithm reduced the consumption of the item meat and meat products and increased the consumption of fish and seafood. An increase in demand for the item fruits and derivatives and the item vegetables, greens and derivatives is also observed in the response presented by the MOEA-HD algorithm. There was also a slight reduction in sugary products, milk and dairy products, and prepared foods.
The demand for processed food was eliminated. No significant variation in the quantity of the items fats and oils, eggs and derivatives, and vegetables and derivatives was observed. The observed variations can facilitate the purchasing process by presenting a more diversified shopping list, thereby reducing the impact of potential supply restrictions on specific items.

Report issue for preceding element

![Refer to caption](https://arxiv.org/html/2508.07077v1/x3.png)(a) Items demanded by the MOEA-HD algorithm.Report issue for preceding element

![Refer to caption](https://arxiv.org/html/2508.07077v1/x4.png)(b) Items demanded by the NSGA-II algorithm.Report issue for preceding element

Figure 2: Weekly consumption of the items proposed by the algorithms.Report issue for preceding element

In addition, a more diversified demand allows the decision maker to purchase items that are more abundant at certain times of the year, resulting in cost savings.

Report issue for preceding element

![Refer to caption](https://arxiv.org/html/2508.07077v1/x5.png)(a) Items on the days of the week obtained by the MOEA-HD algorithm.Report issue for preceding element

![Refer to caption](https://arxiv.org/html/2508.07077v1/x6.png)(b) Items on the days of the week obtained by the NSGA-II algorithm.Report issue for preceding element

Figure 3: Diets proposed for each day of the week.Report issue for preceding element

The use of items on the days of the week, shown in Figures [3(a)](https://arxiv.org/html/2508.07077v1#S6.F3.sf1 "Figure 3(a) ‣ Figure 3 ‣ 6.3 Decision space ‣ 6 Results and Discussion ‣ Enhancing Decision Space Diversity in Multi-Objective Evolutionary Optimization for the Diet Problem") and [3(b)](https://arxiv.org/html/2508.07077v1#S6.F3.sf2 "Figure 3(b) ‣ Figure 3 ‣ 6.3 Decision space ‣ 6 Results and Discussion ‣ Enhancing Decision Space Diversity in Multi-Objective Evolutionary Optimization for the Diet Problem"), also reveals important details. Initially, a more even distribution of item consumption is observed during a week, as indicated by the greater regularity in the height of the bars in each graph. There is an offer of animal protein (meat or fish) on all days of the week in the diets proposed by the MOEA-HD algorithm, while this item is absent on Wednesdays in all diets proposed by the NSGA-II algorithm. Another important aspect is the increase in dietary diversity proposed by the MOEA-HD algorithm, particularly on weekends, such as Saturdays and Sundays.

Report issue for preceding element

In general, figures [2](https://arxiv.org/html/2508.07077v1#S6.F2 "Figure 2 ‣ 6.3 Decision space ‣ 6 Results and Discussion ‣ Enhancing Decision Space Diversity in Multi-Objective Evolutionary Optimization for the Diet Problem") and [3](https://arxiv.org/html/2508.07077v1#S6.F3 "Figure 3 ‣ 6.3 Decision space ‣ 6 Results and Discussion ‣ Enhancing Decision Space Diversity in Multi-Objective Evolutionary Optimization for the Diet Problem") show that the diversification of solutions in the decision space increased the quality of the proposed solutions, both from a financial and nutritional point of view.

Report issue for preceding element

### 6.4 Statistical validation

Report issue for preceding element

We performed a Monte Carlo simulation to further validate our results’ statistical significance.
For each performance metric (Hypervolume, dH​m​i​nd\_{Hmin}, and dH​m​e​dd\_{Hmed}) and each generation setting, we generated 5000 random permutations of the combined results from both algorithms. We calculated the difference in means for each permutation.
This allowed us to construct a distribution of mean differences under the null hypothesis that no significant difference exists between the algorithms.
We then compared the observed mean difference to this distribution to assess its statistical significance.

Report issue for preceding element

![Refer to caption](https://arxiv.org/html/2508.07077v1/x7.png)Figure 4: Monte Carlo simulation for dH​m​e​dd\_{Hmed} after 300 generations. The observed differences are highly statistically significant.Report issue for preceding element

The results of the Monte Carlo simulations are shown in Figures [4](https://arxiv.org/html/2508.07077v1#S6.F4 "Figure 4 ‣ 6.4 Statistical validation ‣ 6 Results and Discussion ‣ Enhancing Decision Space Diversity in Multi-Objective Evolutionary Optimization for the Diet Problem"), [5](https://arxiv.org/html/2508.07077v1#S6.F5 "Figure 5 ‣ 6.4 Statistical validation ‣ 6 Results and Discussion ‣ Enhancing Decision Space Diversity in Multi-Objective Evolutionary Optimization for the Diet Problem"), and [6](https://arxiv.org/html/2508.07077v1#S6.F6 "Figure 6 ‣ 6.4 Statistical validation ‣ 6 Results and Discussion ‣ Enhancing Decision Space Diversity in Multi-Objective Evolutionary Optimization for the Diet Problem").
For Hypervolume (Figure [5](https://arxiv.org/html/2508.07077v1#S6.F5 "Figure 5 ‣ 6.4 Statistical validation ‣ 6 Results and Discussion ‣ Enhancing Decision Space Diversity in Multi-Objective Evolutionary Optimization for the Diet Problem")), the observed mean differences are not statistically significant, indicating that both algorithms achieve comparable objective space performance.
However, for dH​m​i​nd\_{Hmin} (Figure [6](https://arxiv.org/html/2508.07077v1#S6.F6 "Figure 6 ‣ 6.4 Statistical validation ‣ 6 Results and Discussion ‣ Enhancing Decision Space Diversity in Multi-Objective Evolutionary Optimization for the Diet Problem")) and dH​m​e​dd\_{Hmed} (Figure [4](https://arxiv.org/html/2508.07077v1#S6.F4 "Figure 4 ‣ 6.4 Statistical validation ‣ 6 Results and Discussion ‣ Enhancing Decision Space Diversity in Multi-Objective Evolutionary Optimization for the Diet Problem")), the observed differences are highly significant (p<0.01p<0.01) across all generation settings, strongly supporting the superiority of MOEA-HD in terms of decision space diversity.

Report issue for preceding element

![Refer to caption](https://arxiv.org/html/2508.07077v1/x8.png)Figure 5: Monte Carlo simulation for Hypervolume after 300 generations. The observed mean differences are not statistically significant.Report issue for preceding element![Refer to caption](https://arxiv.org/html/2508.07077v1/x9.png)Figure 6: Monte Carlo simulation for dH​m​i​nd\_{Hmin} after 300 generations. The observed differences are highly statistically significant.Report issue for preceding element

These results highlight a crucial trade-off in multi-objective optimization.
While NSGA-II excels at converging to a well-performing Pareto front in the objective space, it may sacrifice diversity in the solutions.
In contrast, MOEA-HD prioritizes exploring a wider range of solutions, providing decision-makers with more options, which can be particularly valuable in real-world applications, such as personalized diet planning.

Report issue for preceding element

### 6.5 Limitations

Report issue for preceding element

The limitations of our study include the use of randomly generated costs for food items, which may not accurately reflect actual price variations in the real world.
Future work should incorporate more realistic cost data and explore the impact of different diversity measures and selection strategies.

Report issue for preceding element

## 7 Conclusion

Report issue for preceding element

This paper presented MOEA-HD, a novel multi-objective evolutionary algorithm that enhances decision space diversity by integrating a Hamming distance-based uniformity measure into its selection mechanism.
Experiments on a multi-objective formulation of the diet problem demonstrated that MOEA-HD significantly outperforms NSGA-II in terms of decision space diversity, while maintaining comparable objective space performance. Additionally, demonstrate that the diversification of solutions in the decision space enhances the quality of the proposed solutions, both from a financial and nutritional perspective.
This suggests that MOEA-HD is a valuable tool for applications where providing diverse solutions is crucial for decision-making.
Future work will extend this approach to other multi-objective optimization problems and explore alternative diversity measures.

Report issue for preceding element

## Acknowledgments

Report issue for preceding element

This work was supported by the Conselho Nacional de Desenvolvimento Científico e Tecnológico (CNPq, grants 307151/2022-0, 308400/2022-4, 152613/2024-2), Fundação de Amparo à Pesquisa do Estado de Minas Gerais (FAPEMIG, grant APQ-01647-22). We also thank the Universidade Federal de Ouro Preto (UFOP) for their invaluable support.

Report issue for preceding element

## References

Report issue for preceding element

- \[1\]
International Food Information Council Foundation, [2023 food & health survey](https://foodinsight.org/2023-food-and-health-survey/ "") (2023).



URL [https://foodinsight.org/2023-food-and-health-survey/](https://foodinsight.org/2023-food-and-health-survey/ "")
- \[2\]
GlobalData, [Consumer attitudes towards health and wellness](https://www.globaldata.com/store/report/consumer-attitudes-health-wellness-trend-analysis/ "") (2020).



URL [https://www.globaldata.com/store/report/consumer-attitudes-health-wellness-trend-analysis/](https://www.globaldata.com/store/report/consumer-attitudes-health-wellness-trend-analysis/ "")
- \[3\]
P. Duarte, M. Teixeira, S. Silva, Healthy eating as a trend: Consumers’ perceptions towards products with nutrition and health claims, Review of Business Management 23 (2021) 405–421.

[doi:10.7819/rbgn.v23i3.4113](http://dx.doi.org/10.7819/rbgn.v23i3.4113 "").

- \[4\]
G. J. Stigler, [The cost of subsistence](http://www.jstor.org/stable/1231810 ""), Journal of Farm Economics 27 (2) (1945) 303–314.



URL [http://www.jstor.org/stable/1231810](http://www.jstor.org/stable/1231810 "")
- \[5\]
S. H. Amin, S. Mulligan-Gow, G. Zhang, [Selection of food items for diet problem using a multi-objective approach under uncertainty](https://doi.org/10.5772/intechopen.88691 ""), in: F. P. G. Márquez (Ed.), Application of Decision Science in Business and Management, IntechOpen, Rijeka, 2019, Ch. 11.

[doi:10.5772/intechopen.88691](http://dx.doi.org/10.5772/intechopen.88691 "").



URL [https://doi.org/10.5772/intechopen.88691](https://doi.org/10.5772/intechopen.88691 "")
- \[6\]
A. Marrero, E. Segredo, C. Leon, C. Segura, A memetic decomposition-based multi-objective evolutionary algorithm applied to a constrained menu planning problem, Mathematics 8 (2020) 1960.

[doi:10.3390/math8111960](http://dx.doi.org/10.3390/math8111960 "").

- \[7\]
V. O. Pochmann, F. J. Von Zuben, Multi-objective bilevel recommender system for food diets, in: 2022 IEEE Congress on Evolutionary Computation (CEC), 2022, pp. 1–8.

[doi:10.1109/CEC55065.2022.9870408](http://dx.doi.org/10.1109/CEC55065.2022.9870408 "").

- \[8\]
J. H. Holland, Adaptation in Natural and Artificial Systems, University of Michigan Press, Ann Arbor, MI, 1975.

- \[9\]
G. Moreira, L. Paquete, Guiding under uniformity measure in the decision space, in: 2019 IEEE Latin American Conference on Computational Intelligence (LA-CCI), 2019, pp. 1–6.

[doi:10.1109/LA-CCI47412.2019.9037034](http://dx.doi.org/10.1109/LA-CCI47412.2019.9037034 "").

- \[10\]
K. Deb, A. Pratap, S. Agarwal, T. Meyarivan, A fast and elitist multiobjective genetic algorithm: Nsga-ii, IEEE Transactions on Evolutionary Computation 6 (2) (2002) 182–197.

[doi:10.1109/4235.996017](http://dx.doi.org/10.1109/4235.996017 "").

- \[11\]
E. Kaldirim, Z. Kose, Application of a multi-objective genetic algorithm to the modified diet problem, in: Genetic and Evolutionary Computation Conference (GECCO), Vol. 6, 2006.

- \[12\]
J.-M. Ramos-Pérez, G. Miranda, E. Segredo, C. León, C. Rodríguez-León, [Application of multi-objective evolutionary algorithms for planning healthy and balanced school lunches](https://www.mdpi.com/2227-7390/9/1/80 ""), Mathematics 9 (1).

[doi:10.3390/math9010080](http://dx.doi.org/10.3390/math9010080 "").



URL [https://www.mdpi.com/2227-7390/9/1/80](https://www.mdpi.com/2227-7390/9/1/80 "")
- \[13\]
C. Türkmenoglu, A. Şima Uyar, B. Kiraz, [Fuzzy inference based a posterior decision-making for multi-objective diet optimization problem](https://api.semanticscholar.org/CorpusID:255116355 ""), European Journal of Science and Technology.



URL [https://api.semanticscholar.org/CorpusID:255116355](https://api.semanticscholar.org/CorpusID:255116355 "")
- \[14\]
Universidade Estadual de Campinas, NEPA-UNICAMP, Campinas, Brasil, Tabela Brasileira de Composição de Alimentos (TACO), versão 4.0 (2011).

- \[15\]
Agência Nacional de Vigilância Sanitária (ANVISA), Instrução Normativa nº 75, de 8 de outubro de 2020, Diário Oficial da União, dispõe sobre os procedimentos para regularização de produtos (out 2020).

- \[16\]
E. Zitzler, M. Laumanns, L. Thiele, SPEA2: Improving the strength pareto evolutionary algorithm, in: Evolutionary Methods for Design, Optimisation and Control with Applications to Industrial Problems (EUROGEN 2001), International Center for Numerical Methods in Engineering (CIMNE), Athens, Greece, 2001, pp. 95–100.

- \[17\]
R. W. Hamming, Error detecting and error correcting codes, Bell System Technical Journal 29 (2) (1950) 147–160.

[doi:10.1002/j.1538-7305.1950.tb00463.x](http://dx.doi.org/10.1002/j.1538-7305.1950.tb00463.x "").

- \[18\]
E. Zitzler, L. Thiele, Multiobjective evolutionary algorithms: a comparative case study and the strength pareto approach, IEEE Transactions on Evolutionary Computation 3 (4) (1999) 257–271.

[doi:10.1109/4235.797969](http://dx.doi.org/10.1109/4235.797969 "").


Report IssueReport Issue for Selection