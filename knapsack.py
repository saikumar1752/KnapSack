import random
import tqdm
import sys

class Individual:
	def __init__(self, individual=None):
		self.size=p_w.size
		if individual==None:
			self.individual=[random.choice([0, 1]) for x in range(self.size)]
		else:
			self.individual=individual
		self.profit=sum(p_w.profits[x] for x in range(self.size) if self.individual[x]==1)
		self.weight=sum(p_w.weights[x] for x in range(self.size) if self.individual[x]==1)

	def valid(self):
		if self.weight<p_w.weight:
			return True
		else:
			return False

	def __lt__(self, ob):
		if self.profit<ob.profit:
			return True
		else:
			return False

	def __gt__(self, ob):
		if self.profit>ob.profit:
			return True
		else:
			return False

	def __str__(self):
		return " ".join(str(x) for x in self.individual)+"==>"+str(self.profit)

class p_w:
	size=None
	weights=None
	profits=None
	weight=None
	def __init__(self, weights, profits, weight):
		p_w.size=len(weights)
		p_w.weights=weights
		p_w.profits=profits
		p_w.weight=weight


class KnapSack:
	def __init__(self):
		self.population=[]
		self.best_known=None
		self.best_value_known=0

	def create_population(self):
		count=0
		while count<100:
			x=Individual()
			if x.valid():
				count+=1
				self.population.append(x)
		self.best(self.population)

	def solve(self, times):
		pbar=tqdm.tqdm(total=times, ncols=100)
		mt=self.population
		for _ in range(times):
			mt=self.crossover(mt)
			self.mutate(mt)
			mt_valid=self.valid(mt)
			mt_select=self.select(mt_valid)
			self.best(mt_select)
			mt=mt_select
			pbar.update()

	def crossover(self, population):
		store=[]
		for x in range(len(population)):
			for y in range(x+1, len(population)):
				r=random.randint(0, p_w.size-1)
				store.append(Individual(population[x].individual[:r]+population[y].individual[r:]))
		store.extend(population)
		return store

	def mutate(self, mt_mutate):
		for x in range(len(mt_mutate)):

			r=random.randint(0, p_w.size-1)
			if mt_mutate[x].individual[r]==0:
				mt_mutate[x].individual[r]=1
			else:
				mt_mutate[x].individual[r]=0
	
	def valid(self, mt_valid):
		return [x for x in mt_valid if x.valid()]

	def select(self, mt_select):
		"""
			The number 0.03 indicates the percentage of the population used for crossing.
		"""
		x=sorted(mt_select, reverse=True)
		return x[:int(len(x)*0.03)]

	def best(self, mt_select):
		for x in mt_select:
			if x.profit>self.best_value_known:
				self.best_value_known=x.profit
				self.best_known=Individual(x.individual)
			

if __name__=='__main__':
	weights=[]
	profits=[]
	weight_W=0
	if(len(sys.argv)>1 and sys.argv[1]=="F"):
		with open("profits.txt", "r") as f:
			weights=list(int(x) for x in f.readlines())
		with open("weights.txt", "r") as f:
			profits=(list(int(x) for x in f.readlines()))
		weight_W=6404180
	else:
		print("Enter the number of items")
		n=int(input())
		print("Enter the weights")
		weights=[int(x) for x in input().split()]
		print("Enter the profits")
		profits=[int(x) for x in input().split()]
		print("Enter the capacity of the knapsack")
		weight_W=int(input())
	pw=p_w(weights, profits, weight_W)
	ks=KnapSack()
	ks.create_population()
	ks.solve(100)#Here 10000 include the number of times to crossover.
	print()
	print("#"*30)
	print(ks.best_known)
	print(ks.best_known.profit, ks.best_known.weight)

