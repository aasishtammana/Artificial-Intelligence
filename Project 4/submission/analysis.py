# analysis.py
# -----------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


######################
# ANALYSIS QUESTIONS #
######################

# Set the given parameters to obtain the specified policies through
# value iteration.

def question2():
    answerDiscount = 0.9
    answerNoise = 0 #Setting the noise to 0 means there is no chance of random actions which will ensure agent moves in right direction
    return answerDiscount, answerNoise

def question3a():
    answerDiscount = 0.9
    answerNoise = 0.2
    answerLivingReward = -4#Since the living reward is much more damaging than the reward, the agent will immediately chose the closest exit by risking the cliff i.e shortest path
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3b():
    answerDiscount = 0.3
    answerNoise = 0.2
    answerLivingReward = -2# SInce the discount factor is high, and the living reward is negative, agent will choose short term gain and chose the close exit
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3c():
    answerDiscount = 0.9
    answerNoise = 0.2
    answerLivingReward = -1#A small negative living reward will direct the agent to get to the highest reward in shortest distance, which will make it risk the cliff
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3d():
    answerDiscount = 0.9
    answerNoise = 0.2
    answerLivingReward = 0#Since the living reward is 0, the agent will try to find its way to the highest possible reward by avoiding the cliff   
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3e():
    answerDiscount = 0.9
    answerNoise = 0
    answerLivingReward = 100#A very high living reward would indicate the agent to stay clear of both the exit states and continue moving within the grid
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question8():
    answerEpsilon = None
    answerLearningRate = None
    #return answerEpsilon, answerLearningRate
    return 'NOT POSSIBLE' #There is no factors which make it learn only in 50 iterations, the agent will be stuck. Hence it is not possible.
    # If not possible, return 'NOT POSSIBLE'

if __name__ == '__main__':
    print('Answers to analysis questions:')
    import analysis
    for q in [q for q in dir(analysis) if q.startswith('question')]:
        response = getattr(analysis, q)()
        print('  Question %s:\t%s' % (q, str(response)))
