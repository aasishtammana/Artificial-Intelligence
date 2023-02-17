import math
import os
import numpy as np
import pandas as pd
import statistics as st
layouts = os.listdir('./layouts')
layouts = [i[:-4] for i in layouts]
agents = ['TOSarsaAgent','ApproximateQAgent']
Rewards = {}
for agent in agents:
    Rewards[agent] = {}
    for i in layouts:
        Rewards[agent][i] = {}
        Rewards[agent][i]['AVGRewards'] = []
        if agent == agents[1]:
            Rewards[agent][i]['files'] = [file for file in os.listdir('./modelperformance') if (agent in file and i in file)]
        else:
            Rewards[agent][i] = {}
            Rewards[agent][i]['AVGRewards'] = []
            Rewards[agent][i]['files'] = [file for file in os.listdir('./modelperformance') if (agent in file and i in file and '0.3' in file)]
for agent in agents:
    for lay in layouts:
        for file in Rewards[agent][lay]['files']:
            df = pd.read_json('./modelperformance/'+file)
            Rewards[agent][lay]['AVGRewards'].extend([i for i in list(df['TotalAverageReward'])])

TTest = {}
print('layout                               p-value')
for layout in layouts:
    lt = Rewards[agents[0]][layout]['AVGRewards']
    a = [lt[i] for i in range(100,2000,100)]
    lt = Rewards[agents[1]][layout]['AVGRewards']
    b = [lt[i] for i in range(100,2000,100)]
    import scipy.stats as sts

    x = sts.ttest_rel(b,a)
    print(f'{layout}             {x[1] / 2.0}')