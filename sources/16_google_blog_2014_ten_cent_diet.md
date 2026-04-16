# Source: 
            
            Sudoku, Linear Optimization, and the Ten Cent Diet
            
            
            - Google Developers Blog
            
        

- URL: https://developers.googleblog.com/2014/09/sudoku-linear-optimization-and-ten-cent.html
- Slug: 16_google_blog_2014_ten_cent_diet

---

# Sudoku, Linear Optimization, and the Ten Cent Diet

SEPT. 30, 2014

Share

- [Facebook](https://www.facebook.com/sharer/sharer.php?u=https://developers.googleblog.com/sudoku-linear-optimization-and-the-ten-cent-diet/ "Share on Facebook")
- [Twitter](https://twitter.com/intent/tweet?text=https://developers.googleblog.com/sudoku-linear-optimization-and-the-ten-cent-diet/ "Share on Twitter")
- [LinkedIn](https://www.linkedin.com/shareArticle?url=https://developers.googleblog.com/sudoku-linear-optimization-and-the-ten-cent-diet/&mini=true "Share on LinkedIn")
- [Mail](mailto:name@example.com?subject=Check%20out%20this%20site&body=Check%20out%20https://developers.googleblog.com/sudoku-linear-optimization-and-the-ten-cent-diet/ "Send via Email")
- [Get shareable link](https://developers.googleblog.com/sudoku-linear-optimization-and-the-ten-cent-diet/# "Get shareable link")

_Originally posted on the [Google Research blog](http://googleresearch.blogspot.com/). Cross posted on_
_the [Google Apps Developers\_\
_blog](http://googleappsdeveloper.blogspot.com/)_

In 1945, future Nobel laureate [George Stigler](http://en.wikipedia.org/wiki/George_Stigler) wrote an essay
in the Journal of Farm Economics titled _The Cost of Subsistence_ about a
seemingly simple problem: how could a soldier be fed for as little money as possible?

The “Stigler Diet” became a classic problem in the then-new field of [linear optimization](http://en.wikipedia.org/wiki/Linear_programming), which
is used today in many areas of science and engineering. Any time you have a set of linear
constraints such as “at least 50 square meters of solar panels” or “the amount of paint should
equal the amount of primer” along with a linear goal (e.g., “minimize cost” or “maximize
customers served”), that’s a linear optimization problem.

At Google, our engineers work on plenty of optimization problems. One example is our [YouTube\\
video stabilization system](http://googleresearch.blogspot.com/2012/05/video-stabilization-on-youtube.html), which uses linear optimization to eliminate the
shakiness of handheld cameras. A more lighthearted example is in the [Google Docs\\
Sudoku add-on](https://chrome.google.com/webstore/detail/sudoku-sheets/eagolleeideiojopioiiaadjkneafmen?hl=en), which instantaneously generates and solves Sudoku puzzles inside a
Google Sheet, using the [SCIP](http://scip.zib.de/) mixed integer
programming solver to compute the solution.


![](https://storage.googleapis.com/gweb-developer-goog-blog-assets/images_archive/original_images/image02_cHCjQ9X.png)

Today we’re proud to announce two new ways for everyone to solve linear optimization problems.
First, you can now solve linear optimization problems in Google Sheets with the [Linear\\
Optimization add-on](https://chrome.google.com/webstore/detail/linear-optimization/goadmgmjlkioggkbpbjlakbjjmlhdpen?utm_source=permalink) written by Google Software Engineer Mihai Amarandei-Stavila. The
add-on uses Google Apps Script to send optimization problems to Google servers. The solutions
are displayed inside the spreadsheet. For developers who want to create their own applications
on top of Google Apps, we also provide an [API](https://developers.google.com/apps-script/reference/optimization/) to
let you call our linear solver directly.


![](https://storage.googleapis.com/gweb-developer-goog-blog-assets/images_archive/original_images/image00_TGejrHH.png)

Second, we’re open-sourcing the linear solver underlying the add-on: Glop (the Google Linear
Optimization Package), created by [Bruno\\
de Backer](https://plus.google.com/u/0/112941999316165083444/posts?e=-RedirectToSandbox) with other members of the Google Optimization team. It’s available as part
of the [or-tools suite](http://code.google.com/p/or-tools/) and we
provide a [few\\
examples](http://developers.google.com/optimization/docs/lp) to get you started. On that page, you’ll find the Glop solution to the
Stigler diet problem. (A Google Sheets file that uses Glop and the Linear Optimization add-on
to solve the Stigler diet problem is available [here](https://docs.google.com/spreadsheets/d/1XWJLkAwch5GXAt_7zOFDcg8Wm8Xv29_8PWuuW15qmAE/edit?usp=sharing).
You’ll need to [install\\
the add-on first](https://chrome.google.com/webstore/detail/linear-optimization/goadmgmjlkioggkbpbjlakbjjmlhdpen?utm_source=permalink).)

Stigler posed his problem as follows: given nine nutrients (calories, protein, Vitamin C, and
so on) and 77 candidate foods, find the foods that could sustain soldiers at minimum
cost.

The [Simplex algorithm](http://en.wikipedia.org/wiki/Simplex_algorithm)
for linear optimization was two years away from being invented, so Stigler had to do his best,
arriving at a diet that cost $39.93 per year (in 1939 dollars), or just over ten cents per
day. Even that wasn’t the cheapest diet. In 1947, Jack Laderman used Simplex, nine
calculator-wielding clerks, and 120 person-days to arrive at the optimal solution.

Glop’s Simplex implementation solves the problem in 300 milliseconds. Unfortunately, Stigler
didn’t include taste as a constraint, and so the poor hypothetical soldiers will eat nothing
but the following, ever:


- Enriched wheat flour
- Liver
- Cabbage
- Spinach
- Navy beans

Is it possible to create an appealing dish out of these five ingredients? Google Chef Anthony
Marco took it as a challenge, and we’re calling the result _Foie Linéaire à la_
_Stigler_:


![](https://storage.googleapis.com/gweb-developer-goog-blog-assets/images_archive/original_images/image01_dzner0w.jpg)

This optimal meal consists of seared calf liver dredged in flour, atop a navy bean purée with
marinated cabbage and a spinach pesto.

Chef Marco reported that the most difficult constraint was making the dish tasty without
butter or cream. That said, I had the opportunity to taste our linear optimization solution,
and it was delicious.


Posted by Jon Orwant, Engineering Manager

posted in:


[Previous](https://developers.googleblog.com/tell-us-about-your-experience-building-on-google-and-raise-money-for-educational-organizations/) Previous

Next [Next](https://developers.googleblog.com/promises-in-the-google-apis-javascript-client-library/)