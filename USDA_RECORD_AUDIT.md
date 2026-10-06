# USDA record audit

Audited: 2026-10-06

Every product diet prices takes its nutrition from a [USDA FoodData Central (FDC)](https://fdc.nal.usda.gov/) record, unless the product's own label supplies a value. This audit checked whether each record describes the food actually sold, and whether its nutrients apply to the weight the product is priced by.

The check listed every FDC record used in `data/skus.yaml` (Kroger), `data/walmart_skus.yaml` (Walmart) and `data/canada_product_map.yaml` (Canadian retailers) beside the products matched to it, and compared each record's description with the products' names and package sizes. Records shared by several products were checked against all of them.

## Records that described a different food

| Products | Old record | New record | Effect of the old record |
|---|---|---|---|
| Orange juice | 169103, Orange peel, raw | 169100, Orange juice, chilled, includes from concentrate | Peel's fiber, calcium and vitamin C were credited to juice, which put juice in 35 of 100 baskets (11 after the fix) |
| Cheddar cheese | 169901, Cheese, american cheddar, imitation | 173414, Cheese, cheddar | Imitation cheese has less protein and calcium |
| Whole wheat sliced bread | 174916, Bread, pita, whole-wheat | 172688, Bread, whole-wheat, commercially prepared | Close, but a different food |
| Canned pinto beans | 170086, Beans, pinto, mature seeds, sprouted, raw | 175201, Beans, pinto, mature seeds, canned, solids and liquids | Sprouted raw beans have a different nutrient profile |
| Dry pinto beans | 175201, Beans, pinto, mature seeds, canned, solids and liquids | 175199, Beans, pinto, mature seeds, raw | Canned beans with their liquid have about a quarter of dry beans' nutrients per gram |
| Canned sliced carrots | 2258587, Carrots, baby, raw | 170395, Carrots, canned, regular pack, solids and liquids | Raw carrots are denser in most nutrients |
| Frozen diced sweet potato | 168016, Sweet Potato puffs, frozen, unprepared | 168482, Sweet potato, raw, unprepared | Puffs are a processed side with added fat and starch; FDC has no plain frozen sweet potato record |
| Light tuna in water | 173708, Fish, tuna, light, canned in oil, drained solids | 171986, Fish, tuna, light, canned in water, without salt, drained solids | Oil-packed tuna has far more fat and calories; FDC's only light tuna in water record is unsalted, so sodium is understated |
| Plain nonfat Greek yogurt | 2647437, Yogurt, plain, nonfat | 170894, Yogurt, Greek, plain, nonfat | Greek yogurt has about twice the protein |
| Canned whole potatoes | 170028, Potatoes, white, flesh and skin, raw | 170444, Potatoes, canned, drained solids | Raw potato, not the canned product |
| Vital wheat gluten | 168944, Wheat flour, whole-grain, soft wheat | 168147, Vital wheat gluten | Gluten is about 75% protein; whole wheat flour is about 10% |

The pinto records were swapped across the two product groups, and the Kroger list was matched the opposite way to the Walmart and Canadian lists, so each pinto product was assigned by its package size: 907 g bags to the raw record, 435 to 540 g cans to the canned record.

## Records kept as approximations

| Products | Record | Why it stays |
|---|---|---|
| Frozen mixed fruit blends (mango, berries) | 171710, Blackberries, frozen, unsweetened | FDC has no mixed frozen fruit record |
| Frozen sliced bananas | 1105073, Bananas, overripe, raw | Close to plain frozen banana; fresh bananas use 1105314, Bananas, ripe and slightly ripe, raw |
| Unsalted roasted pistachios | 169426, Nuts, pistachio nuts, dry roasted, with salt added | Differs only in sodium |
| Nutritional yeast | 167717, Yeast extract spread | FDC has no generic nutritional yeast record; product label values take precedence where retailers supply them |
| Kroger enriched white rice | 2512381, Rice, white, long grain, unenriched, raw | Shared with Canadian white rice, which is not enriched; understates the US product's added thiamin, iron and folic acid |

## Nutrients missing from records

Many newer FDC Foundation records omit choline, vitamin K, folate or other tracked nutrients. `data/nutrient_fallbacks.yaml` fills each gap from the closest SR Legacy record, taking only the nutrients the primary record lacks. The new tuna record lacks vitamins A, D, E and K and choline, which come from white tuna in water rather than tuna in oil, whose oil would add vitamins E and K. Canned potatoes take their gaps from raw potatoes. No close record reports choline for vital wheat gluten, chia seeds, oat milk or raw cashews, or vitamin K for pancake mix; those count as zero.

## Nutrients that applied to the wrong weight

Canned products are priced by net weight, including liquid, but several records describe drained solids. `data/edible_shares.yaml` scales values from those records to the can's net weight: beans 0.6, tuna 0.7, salmon, sardines and mackerel 0.85, clams 0.5, canned potatoes 0.6. Great northern beans' record is denser than whole can contents, so it counts as 74% of can weight.

## Upper limits that counted the wrong form

The folate upper limit applies only to synthetic folic acid, and the vitamin A upper limit only to preformed vitamin A (retinol and retinyl esters). Both had been applied to all forms, which capped legumes and every food with beta-carotene. They are now separate `folic_acid_mcg` and `retinol_mcg` rows in `data/dri.json`, read from FDC's "Folic acid" and "Retinol" values, supplement labels and fortified-product labels. Three multivitamins do not record how much of their vitamin A is preformed, so all of it is counted as preformed.

## Bone, peel and core

Bone-in meats and whole produce are priced by whole weight, but their records describe the edible part. `data/edible_shares.yaml` gives each such record its edible share from the Canadian Nutrient File's refuse data: whole chickens 0.68, leg quarters 0.73, bone-in pork shoulder 0.75, fresh bananas 0.64, navel oranges 0.68, cabbage 0.8, onions and apples 0.9, carrots 0.89. Every product on these records is bought whole; boneless chicken breast uses a separate meat-only record.

## All records in use

Generated from the product files after these fixes. Gap fill is the record that supplies missing nutrients; edible share scales values to the purchased weight.

| FDC ID | USDA description | Gap fill from | Edible share | Products |
|---|---|---|---|---|
| 1999631 | Almond milk, unsweetened, plain, shelf stable | 168751 |  | Canada: Earth's Own Unsweetened Organic Almond Beverage; Kroger: MALK Organic Dairy Free Unsweetened Almond Milk |
| 171688 | Apples, raw, with skin (Includes foods for USDA's Food Distribution Program) |  | 0.9 | Canada: Bag of Apples, Royal Gala; Canada: Farmer's Market Gala Apples |
| 1105073 | Bananas, overripe, raw | 173944 |  | Canada: Life Smart Frozen Banana Slices; Kroger: Kroger® Frozen Sliced Bananas; Walmart: Great Value Sliced Bananas, 16 oz Bag |
| 1105314 | Bananas, ripe and slightly ripe, raw |  | 0.64 | Canada: Banana |
| 170284 | Barley, pearled, raw |  |  | Canada: Cedar Phoenicia Pearl Barley; Kroger: Quaker® Quick Pearled Barley; Walmart: Quaker Quick Pearled Barley, 11 oz, Single Pack, Low Fat, Sodium Free |
| 175188 | Beans, black turtle, mature seeds, canned |  |  | Canada: Life Smart Black Beans; Kroger: Kroger® Black Beans; Walmart: Great Value Black Beans, 15 oz |
| 175186 | Beans, black turtle, mature seeds, raw | 173734 |  | Canada: Cedar Phoenicia Black Turtle Beans; Canada: PC Blue Menu Black Turtle Beans; Kroger: La Preferida® Black Beans Dry; Walmart: Great Value Black Beans, 32 oz |
| 175192 | Beans, great northern, mature seeds, canned |  | 0.74 | Kroger: Kroger® Great Northern Beans; Walmart: Great Value Great Northern Beans, 15.5 oz |
| 174285 | Beans, kidney, red, mature seeds, canned, drained solids | 175243 | 0.6 | Canada: Selection Dark Red Kidney Beans; Kroger: Light Red Kidney Beans; Walmart: Great Value Light Red Kidney Beans, 15.5 oz |
| 173744 | Beans, kidney, red, mature seeds, raw |  |  | Canada: Divya Dry Kidney Beans; Canada: PC Blue Menu Red Kidney Beans; Walmart: Great Value Light Red Kidney Beans, 1 lb |
| 173745 | Beans, navy, mature seeds, raw |  |  | Canada: Life Smart White Navy Beans; Walmart: Great Value Navy Beans, 1 lb |
| 175201 | Beans, pinto, mature seeds, canned, solids and liquids |  |  | Canada: Selection Canned Pinto Beans; Kroger: Pinto Beans; Walmart: Great Value Pinto Beans, 15.5 oz |
| 175199 | Beans, pinto, mature seeds, raw (Includes foods for USDA's Food Distribution Program) |  |  | Canada: Cedar Phoenicia Pinto Beans; Kroger: Kroger® Pinto Beans; Walmart: Great Value Pinto Beans, 32 oz |
| 175204 | Beans, white, mature seeds, canned |  | 0.74 | Canada: Selection White Kidney Beans |
| 2514744 | Beef, ground, 80% lean meat / 20% fat, raw | 174036 |  | Canada: Medium Ground Beef; Kroger: Kroger® 80/20 Ground Beef Roll 1 LB; Walmart: 80% Lean / 20% Fat Ground Beef Chuck, 1 lb Tray, Fresh, All Natural* |
| 171710 | Blackberries, frozen, unsweetened |  |  | Canada: Irrésistible Frozen Summertime Blend Mixed Fruit; Kroger: Wyman's® Mango Berry Frozen Fruit; Walmart: Wyman's Mango Berry, 1 - 48 oz Bag (Frozen) |
| 172688 | Bread, whole-wheat, commercially prepared |  |  | Canada: Selection Whole Wheat Sliced Bread; Kroger: Kroger® 100% Whole Wheat Bread; Walmart: Great Value 100% Whole Wheat Round Top Bread, 20 oz |
| 169968 | Broccoli, frozen, chopped, unprepared |  |  | Canada: Green Giant Frozen Cut Broccoli, Valley Selections; Canada: Green Giant Valley Selections Cut Broccoli; Canada: Life Smart Frozen Broccoli Florets, Organic; Canada: Selection Frozen Broccoli Florets Value Pack; and 2 more |
| 2346407 | Cabbage, green, raw | 169975 | 0.8 | Canada: Green Cabbage; Kroger: Organic Green Cabbage |
| 170395 | Carrots, canned, regular pack, solids and liquids |  |  | Canada: Selection Sliced Carrots; Kroger: Kroger No Salt Added Sliced Carrots - 8.25oz can; Walmart: Great Value Sliced Carrots, 8.25 oz Can |
| 170393 | Carrots, raw |  | 0.89 | Canada: Bag of Carrots; Canada: Farmer's Market Carrots |
| 173884 | Cereals ready-to-eat, GENERAL MILLS, CHEERIOS |  |  | Canada: Cheerios Oats Cereal Value Pack; Canada: General Mills Original Cheerios Family Size; Kroger: General Mills Cheerios Cereal Cup; Walmart: Cheerios, Heart Healthy Gluten Free Breakfast Cereal, 8.9 oz |
| 173414 | Cheese, cheddar (Includes foods for USDA's Food Distribution Program) |  |  | Canada: Selection Old Cheddar Cheese; Kroger: Kroger® Sharp Cheddar Shredded Cheese; Walmart: Great Value Sharp Cheddar Finely Shredded Cheese, 8 oz Bag |
| 172378 | Chicken, broilers or fryers, leg, meat and skin, raw |  | 0.73 | Canada: Back Attached Chicken Leg Quarters; Canada: Halal Chicken Leg Quarters; Kroger: Fresh Chicken Seasoned Leg Quarters; Walmart: Fresh Chicken Leg Quarters, 4.25-6 lb Tray |
| 171447 | Chicken, broilers or fryers, meat and skin, raw |  | 0.68 | Canada: Fresh Whole Chicken; Canada: Maple Lodge Whole Chicken; Kroger: Simple Truth Organic® Fresh Organic Whole Chicken with Giblets; Walmart: Foster Farms Fresh & Natural Cage Free Whole Chicken, 5.0-5.5 lb |
| 171052 | Chicken, broilers or fryers, meat only, raw |  |  | Canada: Boneless and Skinless Chicken Breast; Canada: Boneless and Skinless Chicken Breasts Value Pack; Kroger: Kroger® Boneless Skinless Uncooked Chicken Breast With Rib Meat Thin-Sliced; Walmart: Freshness Guaranteed Boneless, Skinless Chicken Breasts, 4.7-6.1 lb Tray |
| 171060 | Chicken, liver, all classes, raw |  |  | Canada: Chicken Livers; Kroger: Heritage Farm® Chicken Livers; Walmart: Foster Farms Fresh & Natural Cage Free Chicken Livers, 1.0-1.4 lb |
| 2644288 | Chickpeas (garbanzo beans, bengal gram), canned, sodium added, drained and rinsed | 175250 | 0.6 | Canada: Life Smart Chickpeas; Kroger: Simple Truth Organic® Low Sodium Garbanzo Beans; Walmart: S&W Garbanzo Beans - Low Sodium - 15.5 oz. Can |
| 173756 | Chickpeas (garbanzo beans, bengal gram), mature seeds, raw |  |  | Canada: Cedar Phoenicia Chick Peas; Canada: Divya Dry Chickpeas; Canada: PC Blue Menu Chickpeas |
| 169694 | Corn flour, masa, enriched, white |  |  | Canada: Maseca Instant Corn Masa Flour; Walmart: Great Value Corn Masa Flour, 4 lb |
| 170409 | Corn, sweet, yellow, canned, brine pack, regular pack, solids and liquids |  |  | Canada: Selection Whole Kernel Corn; Kroger: Del Monte Golden Sweet Whole Kernel Corn; Walmart: Great Value Golden Sweet Whole Kernel Corn, 15 oz |
| 168867 | Cornmeal, degermed, enriched, yellow |  |  | Walmart: Great Value Enriched Yellow Corn Meal, 4 x 80 oz Bags |
| 169697 | Cornmeal, whole-grain, yellow |  |  | Canada: Grace Corn Meal; Canada: Grace Cornmeal; Canada: Unico Cornmeal; Kroger: Quaker® Yellow Corn Meal For Baking |
| 169698 | Cornstarch |  |  | Canada: Selection Corn Starch; Kroger: Kroger® Pure Corn Starch; Walmart: Argo 100% Pure Corn Starch, 16 Oz |
| 168410 | Edamame, frozen, unprepared |  |  | Canada: Cedar Phoenicia Frozen Shelled Soybeans; Kroger: Kroger® Edamame; Walmart: Great Value Frozen Edamame, 12 oz |
| 171287 | Egg, whole, raw, fresh |  |  | Canada: Selection Large Eggs; Kroger: KROGER GRADE A 12CT LARGE EGGS Rack |
| 175121 | Fish, mackerel, jack, canned, drained solids |  | 0.85 | Canada: Grace Mackerel in Tomato Sauce; Kroger: Grace® Classic Mackerel with Tomato Sauce |
| 175175 | Fish, salmon, pink, canned, drained solids |  | 0.85 | Canada: Clover Leaf Wild Red Pacific Sockeye Salmon; Kroger: Kroger® Alaskan Red Sockeye Salmon; Walmart: Deming's Red Sockeye Wild Caught Alaskan Canned Salmon, 14.75 Oz |
| 175139 | Fish, sardine, Atlantic, canned in oil, drained solids with bone |  | 0.85 | Canada: Clover Leaf Boneless Sardine Fillets in Olive Oil; Canada: Sabor Do Mar Sardines in Vegetable Olive Oil; Kroger: Chicken of the Sea Wild Caught Sardines in Olive Oil; Walmart: Chicken of the Sea Wild Caught Sardines in Olive Oil 3.75 oz |
| 171986 | Fish, tuna, light, canned in water, without salt, drained solids | 175158 | 0.7 | Canada: Selection Flaked Light Tuna in Water; Kroger: Kroger® Wild Caught Chunk Light Tuna in Water; Walmart: StarKist Chunk Light Tuna in Water, Wild Caught, 16g Protein, 12 oz Can |
| 171401 | Lard |  |  | Canada: Tenderflake Pure Lard; Kroger: John Morrell® Snow Cap Edible Lard; Walmart: Morrell Snow Cap® Lard 16 oz. Box |
| 2644283 | Lentils, dry | 172420 |  | Canada: Cedar Phoenicia Large Green Lentils; Canada: PC Blue Menu Green Lentils; Kroger: Simple Truth Organic® Dry Green Lentils; Walmart: GOYA Lentils 16 oz Bag |
| 171276 | Milk, canned, evaporated, with added vitamin D and without added vitamin A |  |  | Canada: Selection Evaporated Milk; Kroger: Kroger® Regular Evaporated Milk; Walmart: Great Value Evaporated Milk, 12 fl oz US |
| 170877 | Milk, dry, nonfat, regular, without added vitamin A and vitamin D |  |  | Canada: Life Smart Instant Skim Milk Powder; Kroger: Kroger® Instant Non-Fat Dry Milk Pouches; Walmart: Nestle Carnation Instant Non-Fat Dry Milk, Vitamin D Added, Cooking Milk, Shelf Milk 9.625 oz |
| 170872 | Milk, lowfat, fluid, 1% milkfat, with added vitamin A and vitamin D |  |  | Canada: Beatrice 1% Milk; Canada: Lactantia 1% Milk PūrFiltre; Kroger: Kroger® 1% Lowfat Milk Half Gallon; Walmart: Great Value Milk 1% Low-fat, Half Gallon, 64 fl oz |
| 168820 | Molasses |  |  | Canada: Grandma Fancy Molasses; Kroger: Grandma's® Original Molasses 12 Fluid Ounce Bottle; Walmart: Grandma's Original Molasses, Unsulphured, 12 fl oz Jar |
| 171976 | Mollusks, clam, mixed species, canned, drained solids |  | 0.5 | Canada: Clover Leaf Whole Yellow Baby Clams in Water; Kroger: Snow's® MSC Chopped Clams; Walmart: Snow's Wild Caught Chopped Clams in Clam Juice, 5g Protein per Serving, Shelf Stable Can, 6.5 oz |
| 170567 | Nuts, almonds |  |  | Canada: Irrésistible Whole Natural Almonds Value Pack; Kroger: Simple Truth® Raw Almonds; Walmart: Great Value Natural Whole Almonds, 25 oz |
| 170162 | Nuts, cashew nuts, raw |  |  | Canada: Johnvince Raw Cashews; Canada: Selection Whole Raw Cashew Nuts; Kroger: Simple Truth® Raw Cashews; Walmart: Great Value Organic Raw Whole Cashews, 14 oz |
| 170583 | Nuts, hazelnuts or filberts, dry roasted, without salt added | 170581 |  | Kroger: Kroger® Roasted Chopped Hazelnuts; Walmart: Now Foods Dry Roasted & Unsalted Hazelnuts 16 oz Bag |
| 168598 | Nuts, macadamia nuts, dry roasted, with salt added |  |  | Kroger: Simple Truth® Sea Salt Dry Roasted Macadamia Nuts; Walmart: bettergoods Dry Roasted and Salted Macadamias, 10 oz |
| 170182 | Nuts, pecans |  |  | Canada: Selection Pecan Halves; Canada: Selection Pecan Pieces; Kroger: Kroger® Pecan Halves; Walmart: Great Value Pecan Halves, 32 oz |
| 170591 | Nuts, pine nuts, dried |  |  | Canada: Irrésistible Pine Nuts; Canada: Selection Pine Nuts; Kroger: Fresh Gourmet Raw Whole Pine Nuts; Walmart: Great Value Pine Nuts, 4 oz |
| 169426 | Nuts, pistachio nuts, dry roasted, with salt added |  |  | Canada: Irrésistible Unsalted Roasted Pistachios; Kroger: Simple Truth® Shelled Roasted & Salted Pistachios; Walmart: Great Value Roasted & Salted, No Shell Pistachios, 12 oz Resealable Bag |
| 170187 | Nuts, walnuts, english |  |  | Canada: Irrésistible Walnut Halves and Pieces Value Pack; Kroger: Kroger® Gluten Free Vegan Halves and Pieces Walnuts; Walmart: Great Value Walnuts Halves & Pieces, 16 oz |
| 2705412 | Oat milk |  |  | Canada: Earth's Own Original Oat Beverage; Canada: Earth's Own Original Oat Milk Alternative; Kroger: Simple Truth® Plant Based Non Dairy Original Oat Milk; Walmart: Planet Oat, Original Oatmilk, Dairy Free, 52 oz, Refrigerated Cardboard Carton |
| 2257046 | Oat milk, unsweetened, plain, refrigerated | 2705412 |  | Canada: Earth's Own Oat Zero Sugar Original; Canada: Earth's Own Zero Sugar Original Oat Milk Alternative |
| 2346396 | Oats, whole grain, rolled, old fashioned | 173904 |  | Canada: Dan-D-Pak Rolled Oats; Canada: Quaker Large Oats; Kroger: Simple Truth Organic® 100% Whole Grain Rolled 1 Minute Oats |
| 748278 | Oil, canola | 172336 |  | Canada: Selection Canola Oil Value Pack; Kroger: Kroger® 100% Pure Canola Oil; Walmart: Crisco Pure Canola Oil, Cooking Oil, 40 fl oz |
| 748323 | Oil, corn | 171029 |  | Canada: Saporito Corn Oil; Walmart: Great Value Corn Oil, 1 Gallon Bottle |
| 171413 | Oil, olive, salad or cooking |  |  | Canada: Selection Extra Virgin Olive Oil; Kroger: Kroger® Extra Virgin Olive Oil; Walmart: Great Value Extra Virgin Olive Oil, 17 fl oz; Walmart: Great Value Vegetable Oil, 1 Gallon Bottle |
| 172370 | Oil, vegetable, soybean, refined |  |  | Canada: No Name 100% Pure Vegetable Oil; Canada: Selection Vegetable Oil Value Pack; Kroger: Kroger® 100% Pure Vegetable Oil |
| 169094 | Olives, ripe, canned (small-extra large) |  |  | Canada: Selection Pitted Black Olives; Kroger: Kroger® Large Pitted Ripe Black Olives; Walmart: Great Value Large Pitted Black Olives, 6 oz |
| 170000 | Onions, raw |  | 0.9 | Canada: Farmer's Market Yellow Onions; Canada: Yellow Onions |
| 169100 | Orange juice, chilled, includes from concentrate |  |  | Canada: Oasis Orange Pure Breakfast Juice; Canada: Oasis Pure Breakfast Orange Juice; Kroger: Kroger® Premium Homestyle Orange Juice with Pulp; Walmart: Tropicana Pure Premium No Pulp Original Orange Juice 89 Oz |
| 169917 | Oranges, raw, navels (Includes foods for USDA's Food Distribution Program) |  | 0.68 | Canada: Farmer's Market Oranges; Canada: Navel Oranges |
| 172772 | Pancakes, plain, dry mix, complete (includes buttermilk) | 175006 |  | Canada: Selection Buttermilk Pancake and Waffle Mix; Walmart: Great Value Complete Buttermilk Pancake and Waffle Mix, 32 oz |
| 169736 | Pasta, dry, enriched |  |  | Canada: Selection Fettuccine Pasta; Kroger: Kroger 12 Oz Tri Color Rotini Pasta; Walmart: Barilla Classic Non-GMO, Kosher Certified Tri-Color Rotini Pasta, 12 oz |
| 174266 | Peanut butter, smooth style, with salt (Includes foods for USDA's Food Distribution Program) |  |  | Canada: No Name Smooth Peanut Butter; Canada: Selection Smooth Peanut Butter; Kroger: Kroger® Creamy Peanut Butter |
| 172470 | Peanut butter, smooth style, without salt |  |  | Canada: Kraft Natural Smooth Peanut Butter Only Peanuts; Walmart: Great Value No Stir Creamy Natural Peanut Butter Spread, 40 oz |
| 173806 | Peanuts, all types, dry-roasted, without salt |  |  | Kroger: Kroger® Dry Roasted Unsalted Peanuts; Walmart: PLANTERS Unsalted Dry Roasted Peanuts, Snacks, Plant Based Protein, 16oz Plastic Jar |
| 172428 | Peas, green, split, mature seeds, raw |  |  | Canada: Cedar Phoenicia Split Green Peas; Canada: Life Smart Dried Yellow Split Peas; Canada: PC Blue Menu Green Split Peas; Kroger: Goya® Green Split Peas; and 1 more |
| 167843 | Pork, fresh, shoulder, whole, separable lean and fat, raw |  | 0.75 | Canada: Pork Shoulder Picnic Roast Value Pack; Kroger: Kroger® Fresh Natural Pork Shoulder Butt Bone In; Walmart: Farmer John, Pork Shoulder Butt Roast, 4.9-8.5lb (Fresh), 20 Grams of Protein per 4 oz Serving |
| 170444 | Potatoes, canned, drained solids | 170026 | 0.6 | Canada: Selection Whole White Potatoes; Kroger: Kroger Whole White Potatoes - 15oz can; Walmart: Great Value Whole New Potatoes, 15 oz |
| 170026 | Potatoes, flesh and skin, raw |  |  | Canada: President's Choice Russet Potatoes; Canada: Russet Potatoes |
| 168166 | Raisins, seeded | 168165 |  | Canada: Sun-Maid Natural California Raisins; Kroger: Kroger® Seedless Raisins; Walmart: Great Value Sun-Dried Raisins Carton, 12 oz (340g) |
| 2512380 | Rice, brown, long grain, unenriched, raw | 169703 |  | Canada: Ben's Original Wholegrain Brown Rice; Kroger: Kroger® Long Grain Brown Rice; Walmart: Great Value Brown Rice, Whole Grain, 16 oz |
| 2512381 | Rice, white, long grain, unenriched, raw | 169756 |  | Canada: Selection Long Grain White Rice; Kroger: Kroger® Enriched Long Grain White Rice |
| 168877 | Rice, white, long-grain, regular, raw, enriched |  |  | Walmart: Carolina Enriched Extra Long Grain White Rice, 20 lb Bag |
| 170554 | Seeds, chia seeds, dried |  |  | Canada: Life Smart Whole Black Chia Seeds; Kroger: Happy Tot Organics Super Morning Stage 4 Organic Bananas, Dragon Fruit, Coconut milk, Oats & Chia; Walmart: Happy Tot Organics Super Morning Stage 4, Bananas Blueberries Yogurt & Oats, Organic Tot Food, 4 oz Pouch |
| 169414 | Seeds, flaxseed |  |  | Canada: Bob's Red Mill Whole Ground Flaxseed Meal; Kroger: Simple Truth Organic® Whole Ground Flaxseed Meal; Walmart: Great Value Organic Ground Cold Milled Flax Seed, 16 oz |
| 167959 | Snacks, popcorn, air-popped |  |  | Canada: Selection Popcorn Kernels; Walmart: Great Value Yellow Popping Corn, 32 oz |
| 173768 | Soymilk, original and vanilla, light, unsweetened, with added calcium, vitamins A and D | 173766 |  | Canada: Silk Organic Fortified Soy Beverage; Kroger: Silk Original Dairy Free Vegan Soy Milk Half Gallon; Walmart: Silk Dairy Free, Gluten Free, Original Soy Milk, Plant Based Milk, 64 fl oz Half Gallon |
| 169287 | Spinach, frozen, chopped or leaf, unprepared (Includes foods for USDA's Food Distribution Program) |  |  | Canada: President's Choice Chopped Spinach; Canada: Selection Frozen Chopped Spinach; Kroger: Kroger® Frozen Spinach Chopped; Walmart: Great Value Chopped Spinach, 12 oz (Frozen) |
| 746784 | Sugars, granulated | 169655 |  | Canada: Redpath Special Fine Granulated Sugar; Walmart: Great Value Pure Granulated Sugar, 25 lb |
| 168482 | Sweet potato, raw, unprepared (Includes foods for USDA's Food Distribution Program) |  |  | Kroger: Simple Truth Organic® Diced Frozen Sweet Potato; Walmart: Great Value Diced Sweet Potatoes, 10 oz (Frozen) |
| 172475 | Tofu, raw, firm, prepared with calcium sulfate | 172448 |  | Canada: Life Smart Extra Firm Plain Tofu; Canada: Sunrise Soya Foods Firm Tofu; Kroger: Simple Truth Organic® Extra Firm Tofu; Walmart: Nasoya Refrigerated Soy Extra Firm Organic Tofu, 14 oz |
| 170138 | Tomatoes, red, ripe, canned, packed in tomato juice, no salt added |  |  | Canada: Selection Diced Tomatoes; Kroger: Kroger® Italian Style Diced Tomatoes; Walmart: Great Value Italian-Style Petite Diced Tomatoes with Basil, Garlic and Oregano, 14.5 oz |
| 168147 | Vital wheat gluten |  |  | Kroger: Bob's Red Mill Vital Wheat Gluten Flour; Walmart: Bob's Red Mill Vital Wheat Gluten Flour, 20 oz |
| 168894 | Wheat flour, white, all-purpose, enriched, bleached |  |  | Canada: Selection All-Purpose Flour; Kroger: Kroger® All Purpose Bleached Enriched Flour; Walmart: Great Value All-Purpose Enriched Bleached Wheat Flour, 25 lb Bag |
| 168895 | Wheat flour, white, all-purpose, self-rising, enriched |  |  | Canada: Brodie Self-Raising Cake and Pastry Flour; Walmart: Great Value Self-Rising Enriched Bleached Flour, 5 lb Bag |
| 168892 | Wheat germ, crude | 173896 |  | Canada: Kretschmer Toasted Wheat Germ; Kroger: Kretschmer® Original Toasted Wheat Germ; Walmart: Kretschmer Original Toasted Wheat Germ, 4g Plant Protein per Serving, 12 oz Jar |
| 167717 | Yeast extract spread |  |  | Kroger: Simple Truth® Non-Dairy Nutritional Yeast; Walmart: Bragg Nutritional Yeast Seasoning, “Cheesy” Flavor, Dairy-Free, Gluten Free, Active Dry Yeast, 4.5 oz |
| 170894 | Yogurt, Greek, plain, nonfat (Includes foods for USDA's Food Distribution Program) |  |  | Canada: Irrésistible 0% Plain Greek Yogurt; Kroger: Kroger® Plain Nonfat Greek Yogurt Cup; Walmart: Great Value Plain Nonfat Greek Yogurt, 32 oz Tub |
