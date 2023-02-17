import math
import os
import numpy as np
import pandas as pd
import statistics as st
mps = os.listdir('./modelperformance')
agents = ['TOSarsaAgent','ApproximateQAgent']
Rewards = {}
mapdf={}
for mp in mps:
    df = pd.read_json('./modelperformance/'+mp)
    mapdf[mp]=df
print('loaded all jsons')
layouts = os.listdir('./layouts')
agents = ['TOSarsaAgent','ApproximateQAgent']
# rates=[0.1,0.3,0.5,0.7,0.9]
rates=[0.3]
Rewards['TOSarsaAgent'] = {}
Rewards['ApproximateQAgent'] = {}
for layout in layouts:
    print(layout)
    approxnm='output_ApproximateQAgent_'+layout+'_Alpha_0.0_Instance_0.json'
    qdf=mapdf[approxnm]
    Rewards[agents[1]][layout]=qdf[0:2000]
    Count=0
    Rewards[agents[0]][layout]={}
    for j in rates:
        print(j)
        tosnm='output_TOSarsaAgent_'+layout+'_Alpha_0.2_Epsilon_0.05_Gamma_0.8_Lambda_'+str(j)+'_Instance_'+str(1)+'.json'
        Count+=1
        tosdf=mapdf[tosnm]
        Rewards[agents[0]][layout][str(j)]=tosdf[0:2000]
print('loaded all rewards')
import matplotlib.pyplot as plt
for layout in layouts:
    print(layout)
    x =  Rewards[agents[1]][layout]['TrainingEpisodeNumber']
    y1 = Rewards[agents[1]][layout]['TotalAverageReward']
    # y2 = Rewards[agents[0]][layout][str(rates[0])]['TotalAverageReward']
    y3 = Rewards[agents[0]][layout][str(rates[0])]['TotalAverageReward']
    # y4 = Rewards[agents[0]][layout][str(rates[2])]['TotalAverageReward']
    # y5 = Rewards[agents[0]][layout][str(rates[3])]['TotalAverageReward']
    # y6 = Rewards[agents[0]][layout][str(rates[4])]['TotalAverageReward']

    plt.plot(x,y1,label = 'Approximate Q Agent')
    # plt.plot(x,y2,label = 'True Online Sarsa Agent with lambda = '+str(rates[0]))
    plt.plot(x,y3,label = 'True Online Sarsa Agent with lambda = '+str(rates[0]))
    # plt.plot(x,y4,label = 'True Online Sarsa Agent with lambda = '+str(rates[2]))
    # plt.plot(x,y5,label = 'True Online Sarsa Agent with lambda = '+str(rates[3]))
    # plt.plot(x,y6,label = 'True Online Sarsa Agent with lambda = '+str(rates[4]))
    plt.legend(loc="lower right")
    plt.title(layout,fontweight = 'bold')
    plt.ylabel('Total Avearge Reward',fontweight = 'bold')
    plt.xlabel('Episode',fontweight = 'bold')
    # plt.savefig('graphs\\'+layout+'_graph.png')
    plt.show()
    plt.close()