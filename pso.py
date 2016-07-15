# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import matplotlib, style, math, random, matplotlib.pyplot as plt

pcoeff = 2
gcoeff = 2
population = 20
max_generation = 30
global gbest, gbest_value, gbest_pos
gbest_value = 6
gbest_pos = [0, 0]
gbest = 0

def function(x, y):
    return ((-5) * math.sin(x) * math.sin(y)) - (math.sin(5 * x) * math.sin(5 * y))

def generate():
    x = random.uniform(0, math.pi)
    y = random.uniform(0, math.pi)
    return [x, y]

def best(particles, results, best_value, best_pos):
	if min(results) <= best_value:
		best_value = min(results)	
		return [particles[results.index(min(results))].data(), best_value]
	else:
		return [best_pos, best_value]

class Particle():

	def __init__(self, coord):
		self.position = coord
		self.pbest_value = 6
		self.pbest_pos = coord
		self.vel_x = 0
		self.vel_y = 0

	def pbest(self, value):
		if value < self.pbest_value:
			self.pbest_value = value
			self.pbest_position = self.position
			return [self.pbest_position, self.pbest_value]

	def velocity(self, gbest_pos):
		r = random.random()
		self.vel_x = (pcoeff * r * (self.pbest_pos[0] - self.position[0])) + (gcoeff * r * (gbest_pos[0] - self.position[0]))

		self.vel_y = (pcoeff * r * (self.pbest_pos[1] - self.position[1])) + (gcoeff * r * (gbest_pos[1] - self.position[1]))
		return [self.vel_x, self.vel_y]
	
	def update(self):
		self.position[0] = self.position[0] + self.vel_x
		self.position[1] = self.position[1] + self.vel_y

	def data(self):
		return self.position

def evaluate():
	global gbest, gbest_value, gbest_pos
	particles = [Particle(generate()) for i in range(population)]

	mins = []
	avgs = []
	xs = [i for i in range(max_generation)]

	for k in range(max_generation):
		results = [function(particles[i].data()[0], particles[i].data()[1]) for i in range(population)]	
		gbest = best(particles, results, gbest_value, gbest_pos)
		gbest_value = gbest[1]
		gbest_pos = gbest[0]

		for i in range(population):
			particles[i].pbest(results[i])
			particles[i].velocity(gbest_pos)
			particles[i].update()

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

plt.savefig('rys/pso.png', format='png', dpi=300, bbox_inches='tight')

print res_mins[-1]
print res_std_mins[-1]
