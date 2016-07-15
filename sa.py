# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import matplotlib, style, math, random, matplotlib.pyplot as plt

#tstart = 900
#tend = 0.005
tstart = 1
tend = 0.01

def function(x, y):
    return (((-5) * math.sin(x) * math.sin(y)) - (math.sin(5 * x) * math.sin(5 * y)))

def generate():
    x = random.uniform(0, math.pi)
    y = random.uniform(0, math.pi)
    return [x, y]

def neighbour(x, y):
	x_new = x + random.uniform(-math.pi / 6.0, math.pi / 6.0)
	y_new = y + random.uniform(-math.pi / 6.0, math.pi / 6.0)
	return [x_new, y_new]
	

def evaluate(x, y):
	"""mins = []
	avgs = []
	maxs = []
	xs = [i for i in range(max_generation)]"""
	point = [x, y]
	result = function(x, y)
	npoint = neighbour(x, y)
	nresult = function(npoint[0], npoint[1])
	prob = 1 / (1 + math.e ** ((nresult - result) / t))
	if nresult < result:
		point = npoint
		result = nresult
	elif random.random() < prob:
		point = npoint
		result = nresult
	else:
		point = point
		result = result

	"""mins.append(min(results))
	avgs.append(sum(results) / float(population))"""

	return([result, point[0], point[1]])

def run():
	global t, iteration
	t = tstart
	iteration = 0
	ys = []
	point = generate()
	while t > tend:
		res = (evaluate(point[0], point[1]))
		ys.append(res[0])
		point = (res[1], res[2])
		t = 0.9886 * t
		iteration += 1
		#print point

	xs = [i for i in range(len(ys))]

	return ys

probes = 1000

all_mins = []
for i in range(0, probes):
	eva = run()
	mins = eva
	all_mins.append(mins)

res_mins = []
res_std_mins = []

for i in range(0, len(mins)):
	sing_mins = [all_mins[k][i] for k in range(probes)]
	res_mins.append(sum(sing_mins) / float(probes))
	std_mins = [(all_mins[k][i] - res_mins[i])**2 for k in range(probes)]
	res_std_mins.append(math.sqrt(sum(std_mins) / float(probes)))

res_mins_low = [res_mins[i] - res_std_mins[i] for i in range(len(mins))]
res_mins_high = [res_mins[i] + res_std_mins[i] for i in range(len(mins))]

xs = [i for i in range(len(mins))]

style.style(matplotlib)
fig = plt.figure()
ax = fig.add_subplot(111)
plt.ylim(-6.5, -3.5)
plt.xlim(0, 400)
plt.plot(xs, res_mins, c = "black")#, label = "minimum")
plt.xlabel("Iteracja")
plt.ylabel("Wartość funkcji")
#plt.legend(loc = "best")
plt.grid()
plt.fill_between(xs, res_mins_high, res_mins_low, facecolor='black', alpha=0.3)
#plt.show()  

#print min(mins)
#print iteration
#plt.savefig('rys/sa.png', format='png', dpi=300, bbox_inches='tight')

print res_mins[-1]
print res_std_mins[-1]
