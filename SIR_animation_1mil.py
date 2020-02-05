import networkx as nx
import EoN
import math
import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict

#Run time begin
now = datetime.now()
start_time = now.strftime("%H:%M:%S")
print("Time Start Simulation =", start_time)

## Population 
population = 1000
print("Run Simulation with Population of: ", population*population)
G = nx.grid_2d_graph(population,population) #each node is (u,v) where 0<=u,v<=99
#we'll initially infect those near the middle
initial_infections = [(u,v) for (u,v) in G if 545<u<555 and 545<v<555]  #Cluster of population usually at middle

##-----------------------------------Without Vaccine---------------------------------------------------
#Transmission and Death rate is from here https://www.worldometers.info/coronavirus/
trans_rate = 4.0
recovery_rate = 0.3
total_simulation_days = 30 #180 #6 month
death_rate = 0.02
print("Duration: 60 days")
print("Module SIR: TransRate: ", trans_rate,", DeathRate: ", death_rate, "%, RecoveryRate: ", recovery_rate, "%")

pos = {node:node for node in G}
sim_kwargs = {'pos': pos}
sim = EoN.fast_SIR(G, trans_rate, recovery_rate, initial_infecteds = initial_infections,
               tmax = total_simulation_days, return_full_data=True, sim_kwargs = sim_kwargs)

count = 1
total_death = 0
total_infected_case = 0
previous_infected_case = 0
new_infected_case = 0

while(count < total_simulation_days):
	t, S, I, R= EoN.fast_SIR(G, trans_rate, recovery_rate, initial_infecteds = initial_infections,
	               tmax = count, sim_kwargs = sim_kwargs)
	new_infected_case = I[-1]
	diff = new_infected_case - previous_infected_case
	previous_infected_case = new_infected_case
	total_infected_case=total_infected_case+diff
	count=count+1

total_death=int(total_infected_case*death_rate)  #percentage of death based on current data.. 
print("Total Infected Case: ", total_infected_case, "/", population*population)  ##Number of infected people without vaccine 
print("Total Death People before vaccine:", total_death, "/", population*population)
print("")

ani=sim.animate(ts_plots=['I', 'SIR'], node_size = 4)
ani.save('SIR_1Mil_30days.mp4', fps=5, extra_args=['-vcodec', 'libx264'])


#Simulation ended
end = datetime.now()
finish_time = end.strftime("%H:%M:%S")
print("Time Finish Simulation =", finish_time)