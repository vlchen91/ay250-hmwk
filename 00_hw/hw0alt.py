from sys import argv
import numpy.random
#import networkx as nx

# sample call in python: run hw0.py $num_years $P_male

#G = nx.Graph()

class Bear(object):
	
	# initialization
	def __init__(self,name,gender='unknown',age=0,dead=False,children=[],parents=[]):
		self.name = name
		self.gender = gender
		self.age = age
		self.max_age = numpy.random.normal(35,5)
		self.abstinence = 0 # default value; it could also be any positive number
		self.dead = dead
		self.children = children
		self.parents = parents
		#G.add_node(self)
		#if not (self.parents == [] or self.parents == [god,god]): # ignore sentinels
			#G.add_edge(self.parents[0],self)
			#G.add_edge(self.parents[1],self)
		# -- OR --
		#G.add_node(name)
		#if not (self.parents == [] or self.parents == [god,god]): # ignore sentinels
			#G.add_edge(self.parents[0].name,name)
			#G.add_edge(self.parents[1].name,name)
			
	def __repr__(self):
		return self.name
	
	def grow_older(self):
		if not self.dead:
			self.age += 1
			self.abstinence += 1
		if self.age > self.max_age:
			self.dead = True
		

class Bear_Population(object):
	
	# initialization
	def __init__(self,bears=[]):
		self.bears = bears
		self.population = len(bears) # assuming no bear is dead initially
	
	# modifier(s)
	def update_population(self):
		for i in range(len(self.bears)-1,-1,-1):
			if self.bears[i].dead:
				del(self.bears[i])
		alive_checker = lambda x: 1 if (not x.dead) else 0
		self.population = sum(map(alive_checker, self.bears))
		
		
	def track_bear(self,bear):
		self.bears.append(bear)
		self.update_population()
	
	def procreate(self,bear, other_bear):
		bear.abstinence = 0
		other_bear.abstinence = 0
		cub = Bear(rand_name.next(),rand_gend.next(),parents=[bear.name,other_bear.name])
		bear.children.append(cub)
		other_bear.children.append(cub)
		self.track_bear(cub)
	
	# function(s)
	
	def possible_mates(self,bear):
		rule1 = filter(lambda x: (not x.dead) and (not bear.dead), self.bears)
		rule2 = filter(lambda x: x.gender != bear.gender,rule1)
		rule3 = filter(lambda x: x.abstinence >= 5 and bear.abstinence >= 5, rule2)
		rule4 = filter(lambda x: x.age >= 5 and bear.age >= 5, rule3)
		rule5 = filter(lambda x: abs(x.age - bear.age) <= 10, rule4)
		rule6 = filter(lambda x: True if (x.parents == [god.name,god.name] or bear.parents == [god.name,god.name]) else x.parents != bear.parents, rule5)
		return rule6


file_name, num_years, P_male = argv
num_years = int(num_years)
P_male = float(P_male)

def name_generator():
	char1 = ['a','b','c','d','e','f','g','h','i','j','k','l','m']
	char2 = ['n','o','p','q','r','s','t','u','v','w','x','y','z']
	char3 = ['A','B','C','D','E','F','G','H','I','J','K','L','M']
	char4 = ['N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
	char5 = ['0','1','2','3','4','5','6','7','8','9']
	char6 = char5

	#used_names = []
	while True:
		random_name = ""
		random_name += char1[numpy.random.randint(0,len(char1))]
		random_name += char2[numpy.random.randint(0,len(char2))]
		random_name += char3[numpy.random.randint(0,len(char3))]
		random_name += char4[numpy.random.randint(0,len(char4))]
		random_name += char5[numpy.random.randint(0,len(char5))]
		random_name += char6[numpy.random.randint(0,len(char6))]
		#if not (random_name in used_names):
		yield random_name
		
		#used_names.append(random_name)

def gender_generator():
	while True:
		if numpy.random.random() <= P_male:
			yield 'm'
		else:
			yield 'f'
			
###### SIMULATION ######


# initial population of bear cubs
my_pop = Bear_Population()
god = Bear('God') # sentinel
adam = Bear('Adam','m',parents=[god.name,god.name])
eve = Bear('Eve','f',parents=[god.name,god.name])
mary = Bear('Mary','f',parents=[god.name,god.name])
my_pop.track_bear(adam)
my_pop.track_bear(eve)
my_pop.track_bear(mary)

# simulate bear population growth
rand_name = name_generator()
rand_gend = gender_generator()
t = 0
while t <= num_years:

	for i in my_pop.bears:
		i.grow_older()
	
	if t % 5 == 0:
		for my_bear in my_pop.bears:
			pos_mates = my_pop.possible_mates(my_bear)
			# Choose one random candidate from a list of possible mates
			if len(pos_mates) != 0:
				lucky_bear = pos_mates[numpy.random.randint(0,len(pos_mates))]
				my_pop.procreate(my_bear,lucky_bear)
	
	my_pop.update_population()
	print "Year {}\nPopulation: {}".format(t,my_pop.population)
	t += 1

print "In a total of {} years:\nTotal births: {}".format(num_years,len(my_pop.bears) - 4)


	
'''	
###### BUG TEST ######
t = 1

def test():

	for i in my_pop.bears:
		i.grow_older()
		
	for my_bear in my_pop.bears:
		pos_mates = my_pop.possible_mates(my_bear)
		# Choose one random candidate from a list of possible mates
		if len(pos_mates) != 0:
			lucky_bear = pos_mates[numpy.random.randint(0,len(pos_mates))]
			my_pop.procreate(my_bear,lucky_bear)
		else:
			my_pop.update_population()
	global t
	t += 1
	print "Year {}\nPopulation: {}".format(t,my_pop.population)
	for bear in my_pop.bears:
		print "\t{} ({}) is {} yrs. Dead? {}. Abstinence: {}. Parents: {} {}".format(bear.name,bear.gender,bear.age,bear.dead,bear.abstinence,bear.parents[0].name,bear.parents[1].name)
	
'''

		
		
		