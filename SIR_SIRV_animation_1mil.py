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
total_simulation_days = 15 #30days without vaccine and 30 days with vaccine = 60days sim
death_rate = 0.02
print("Duration: ",total_simulation_days)
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
print("Current Infected People before vaccine: ", total_infected_case, "/", population*population)  ##Number of infected people without vaccine 
print("Total Death People before vaccine:", total_death, "/", population*population)

ani=sim.animate(ts_plots=['I', 'SIR'], node_size = 4)
ani.save('SIR_1Mil_15days_without_vaccine.mp4', fps=5, extra_args=['-vcodec', 'libx264'])

#How to initialize the size of infection... 

##-----------------------------------When Vaccine is found-------------------------------------------
print("Vaccine is found.. lets give it to everyone")

#Current Infection Population
infected_population = int(math.sqrt(previous_infected_case)/2)
print(infected_population)
G = nx.grid_2d_graph(population,population) 
x = 500-infected_population
y = 500+infected_population
initial_infections = [(u,v) for (u,v) in G if x<u<y and x<v<y]

H = nx.DiGraph()  #the spontaneous transitions
H.add_edge('Sus', 'Vac', rate = 0.01)
H.add_edge('Inf', 'Rec', rate = 1.0)

J = nx.DiGraph()  #the induced transitions
J.add_edge(('Inf', 'Sus'), ('Inf', 'Inf'), rate = 2.0)

IC = defaultdict(lambda:'Sus')
for node in initial_infections:
    IC[node] = 'Inf'

return_statuses = ['Sus', 'Inf', 'Rec', 'Vac']

color_dict = {'Sus': '#009a80','Inf':'#ff2000', 'Rec':'gray','Vac': '#5AB3E6'}
pos = {node:node for node in G}
tex = False
sim_kwargs = {'color_dict':color_dict, 'pos':pos, 'tex':tex}

sim = EoN.Gillespie_simple_contagion(G, H, J, IC, return_statuses, tmax=total_simulation_days, return_full_data=True, sim_kwargs=sim_kwargs)

count = 0
while(count < total_simulation_days):
	t, S, E, I, R = EoN.Gillespie_simple_contagion(G, H, J, IC, return_statuses, tmax=count, sim_kwargs=sim_kwargs)
	new_infected_case = I[-1]
	diff = new_infected_case - previous_infected_case
	previous_infected_case = new_infected_case
	total_infected_case=total_infected_case+diff
	count=count+1

total_death=total_death + int(total_infected_case*0.02)  #percentage of death based on current data.. 
print("Current Infected People after vaccine: ", total_infected_case, "/", population*population)  ##Number of infected people without vaccine 
print("Total Death People after vaccine:", total_death, "/", population*population)


times, D = sim.summary()
#
#times is a numpy array of times.  D is a dict, whose keys are the entries in
#return_statuses.  The values are numpy arrays giving the number in that
#status at the corresponding time.

newD = {'Sus+Vac':D['Sus']+D['Vac'], 'Inf+Rec' : D['Inf'] + D['Rec']}
#
#newD is a new dict giving number not yet infected or the number ever infected
#Let's add this timeseries to the simulation.
#
new_timeseries = (times, newD)
sim.add_timeseries(new_timeseries, label = 'Simulation', color_dict={'Sus+Vac':'#E69A00', 'Inf+Rec':'#CD9AB3'})

# sim.display(1, node_size = 4, ts_plots=[['Inf'], ['Sus+Vac', 'Inf+Rec']])
# plt.savefig('SIRV_display.png')

ani=sim.animate(ts_plots=[['Inf'], ['Sus+Vac', 'Inf+Rec']], node_size = 4)
ani.save('SIRV_1Mil_15days_after_vaccine.mp4', fps=5, extra_args=['-vcodec', 'libx264'])


#Simulation ended
end = datetime.now()
finish_time = end.strftime("%H:%M:%S")
print("Time Finish Simulation =", finish_time)
