# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import matplotlib, style, math, random, matplotlib.pyplot as plt

population = 20
mutation_chance = 2
max_generation = 31
tournament_size = 3
tour = 1
elitism = True

def function(x, y):
    return ((-5) * math.sin(x) * math.sin(y)) - (math.sin(5 * x) * math.sin(5 * y))

def generate():
    x = random.uniform(0, math.pi)
    y = random.uniform(0, math.pi)
    return [x, y]

def tournament(results):
	selections = [results[random.randint(0, population - 1)] for i in range(tournament_size)]
	res_index = results.index(min(selections))
	return res_index

def roulette(results):
	res_for_roul = [1 / (((results[i] + 8.0) / (sum(results) + 8.0 * len(results)))) for i in range(population)]
	sing_prob = [((res_for_roul[i]) / sum(res_for_roul)) for i in range(population)]
	prob = []
	prob_value = 0
	for i in range(0, population):
		prob_value = prob_value + sing_prob[i]
		prob.append(prob_value)
	r = random.random()
	for i in range(0, population):
		if prob[i] > r:
			return i

def elite(elitism, coord, generation):
	if elitism == True:
		generation[-1] = coord

def crossover(first_index, second_index, generation):
	r = random.random()
	x = r * generation[first_index][0] + (1 - r) * generation[second_index][0]
	r = random.random()
	y = r * generation[first_index][1] + (1 - r) * generation[second_index][1]
	return [x, y]
    
def mutation(mut_index, generation):
	r = random.randint(0, 1)
	generation[mut_index][r] = generate()[r]
	return True
		
def evaluate():
	### first generation ###
	generation = [generate() for i in range(population)]
	mins = []
	avgs = []
	maxs = []
	xs = [i for i in range(max_generation)]

	for i in range(0, max_generation):

		### evaluation ###
		results = [function(generation[i][0], generation[i][1]) for i in range(population)]
		coord = generation[results.index(min(results))]

		### crossover ###
		if tour == 1 :
			sel_res = [tournament(results) for i in range(2 * population)]
		elif tour == 0 :
			sel_res = [roulette(results) for i in range(2 * population)]
		generation = [crossover(sel_res[i], sel_res[i + 1], generation) for i in range(0, 2 * population, 2)]

		### mutation ###
		for i in range(population):
			if random.uniform(0, 100) < mutation_chance :
				mutation(i, generation)

		elite(elitism, coord, generation)

		mins.append(min(results))
		avgs.append(sum(results) / float(population))

	return(mins, avgs, xs)

probes = 1000

all_mins = []
all_avgs = []
for i in range(0, probes):
	eva = evaluate()
	mins, avgs, xs = eva[0], eva[1], eva[2]
	all_mins.append(mins)
	all_avgs.append(avgs)

res_mins = []
res_avgs = []
res_std_avgs = []
res_std_mins = []
for i in range(0, max_generation):
	sing_mins = [all_mins[k][i] for k in range(probes)]
	sing_avgs = [all_avgs[k][i] for k in range(probes)]
	res_mins.append(sum(sing_mins) / float(probes))
	res_avgs.append(sum(sing_avgs) / float(probes))
	std_avgs = [(all_avgs[k][i] - res_avgs[i])**2 for k in range(probes)]
	res_std_avgs.append(math.sqrt(sum(std_avgs) / float(probes)))
	std_mins = [(all_mins[k][i] - res_mins[i])**2 for k in range(probes)]
	res_std_mins.append(math.sqrt(sum(std_mins) / float(probes)))

res_avgs_low = [res_avgs[i] - res_std_avgs[i] for i in range(max_generation)]
res_avgs_high = [res_avgs[i] + res_std_avgs[i] for i in range(max_generation)]

res_mins_low = [res_mins[i] - res_std_mins[i] for i in range(max_generation)]
res_mins_high = [res_mins[i] + res_std_mins[i] for i in range(max_generation)]

style.style(matplotlib)
fig = plt.figure()
ax = fig.add_subplot(111)
plt.ylim(-6.5, -3.5)
plt.xlim(0, 20)
plt.plot(xs, res_mins, label = "minimum", c = "black")
plt.plot(xs, res_avgs, label = "średnia", c = "black", ls = "dashed")
plt.xlabel("Generacja")
plt.ylabel("Wartość funkcji")
plt.legend(loc = "best")
ax.set_xticks([0,4,8,12,16,20])
plt.grid()
#plt.fill_between(xs, res_avgs_high, res_avgs_low, facecolor='black', alpha=0.3)
plt.fill_between(xs, res_mins_high, res_mins_low, facecolor='black', alpha=0.3)
#plt.show()  

#plt.savefig('rys/ga_r_ne.png', format='png', dpi=300, bbox_inches='tight')

print res_mins[-1]
print res_std_mins[-1]
