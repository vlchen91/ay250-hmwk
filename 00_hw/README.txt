README

Description:

Simulates a bear population over number of years and with a pre-determined gender ratio (default is 50-50 male/female).

I made two versions: hw0.py and hw0alt.py
hw0alt.py is much faster b/c:
	It calls the procreate function only every 5 years
	It deletes dead bears

However, hw0alt.py doesn't not use NetworkX and doesn't keep track of names

How to run:

ipython
run hw01.py num_years Prob(male)
e.g.	run hw01.py 100 0.50
	run hw01.py 90 0.33

Improvements:
1. Parallelize for multi-core CPUs
2. Implementing Bears as generators with a limited lifespan to save memory. Currently, they'll take up memory even though they're "dead."
3. Having a clearer OOP implementation of the Bear & Population class


Questions:
a.
On average, how many Bears are born in the first 100 years?

Trial	Total Births
1	2746
2	2476
3	2496
4	2014
5	2138
-------------
avg	2374

How many Bears are alive at the end of 150 years?

Trial	Population
1	9994
2	26629
3	32500
-------------
avg	23041

b. What must be the minimum value of P(male) such that the population does not die out in 150 years?

There were instances (albeit very few) when I made P(male) as low as 0.05. Around once per 10 trials. If we're asking about having the bear race to exist after 150 years consistently over all trials, I found P(male) to be around 0.3 and 0.4, guessing 0.38.

c. Build and use a plotting routine to show the genealogy tree of a given Bear. Show all Bears at the same generation and earlier who are directly related.

Incomplete. See hw0.py for NetworkX partial implementation
