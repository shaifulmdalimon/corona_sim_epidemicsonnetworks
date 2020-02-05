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

total_simulation_days = 30 #1 month

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
# t, S, E, I, R = EoN.Gillespie_simple_contagion(G, H, J, IC, return_statuses2, tmax=total_simulation_days, sim_kwargs=sim_kwargs)

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

ani=sim.animate(ts_plots=[['Inf'], ['Sus+Vac', 'Inf+Rec']], node_size = 4)
ani.save('SIRV_1Mil_180days.mp4', fps=5, extra_args=['-vcodec', 'libx264'])
##-----

#Simulation ended
end = datetime.now()
finish_time = end.strftime("%H:%M:%S")
print("Time Finish Simulation =", finish_time)