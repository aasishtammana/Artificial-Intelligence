# qlearningAgents.py
# ------------------
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

import os
import json
from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
        self.Qval=util.Counter()

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        return self.Qval[(state,action)]


    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        actions=self.getLegalActions(state)
        if len(actions)==0:
          return 0.0
        maxval=-9999999999999
        for a in actions:
          v=self.getQValue(state,a)
          if maxval<v:
            maxval=v
        return maxval

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        actions=self.getLegalActions(state)
        if len(actions)==0:
          return None
        maxval=-9999999999999
        maxaction=None
        for a in actions:
          v=self.getQValue(state,a)
          if maxval<v:
            maxval=v
            maxaction=a
        return maxaction
        # util.raiseNotDefined()

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
       
        "*** YOUR CODE HERE ***"
        actions=self.getLegalActions(state)
        action = None
        if len(actions)==0:
          return action
        action=self.computeActionFromQValues(state)
        if util.flipCoin(self.epsilon):
          action=random.choice(actions)
        return action

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        actions=self.getLegalActions(nextState)
        maxval=-99999999999
        for a in actions:
          Q=self.getQValue(nextState,a)
          if maxval<Q:
            maxval=Q
        if len(actions)==0:
          maxval=0
        self.Qval[(state,action)]=(1-self.alpha)*self.getQValue(state,action)+ self.alpha*(reward+(self.discount*maxval))
        
        
    
    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        self.Sarsabool = False
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', inst=0, **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()
        self.NTE = []
        self.TotalAverageReward=[]
        self.ER=[]
        self.Instancerun=inst

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        return self.featExtractor.getFeatures(state,action)*self.weights

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        fv=self.featExtractor.getFeatures(state,action)
        d=reward+self.discount*self.computeValueFromQValues(nextState) -self.getQValue(state,action)
        for i in fv:
          self.weights[i]= self.weights[i]+self.alpha*d*fv[i]

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)
        if self.episodesSoFar <= self.numTraining:
            self.NTE.append(self.episodesSoFar)
            tar=self.accumTrainRewards / (1.0 * self.episodesSoFar)
            self.TotalAverageReward.append(tar)
            self.ER.append(self.episodeRewards)

        if self.episodesSoFar == self.numTraining:
            "*** YOUR CODE HERE ***"
            pass

    def storemodelperformance(self, fname='output.json'):
      fname=	fname[:len(fname)-5]
      fname= fname+'_Alpha_'+str(self.alpha)+'_Instance_'+str(self.Instancerun)+'.json'
      data=[]
      for i in range(0,len(self.NTE)):
        datarow={}
        datarow['TrainingEpisodeNumber']=self.NTE[i]
        datarow['TotalAverageReward']=self.TotalAverageReward[i]
        datarow['RewardforEpisode']=self.ER[i]
        data.append(datarow)
      with open("modelperformance\\"+fname, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

class TOSarsaAgent(ApproximateQAgent):

    def __init__(self, extractor='IdentityExtractor', tDRate=0.0, inst=0, **args):        
        ApproximateQAgent.__init__(self, extractor, **args)
        self.Sarsabool = True         
        self.NTE = []
        self.TotalAverageReward=[]
        self.ER=[]
        self.Alpha=self.alpha
        self.Epsilon=self.epsilon
        self.Gamma=self.discount
        self.Lambda=tDRate
        self.Instancerun=inst
        self.tDRate = float(tDRate)
             
    def getQValue(self, state, action):
        initalval=0.0
        if state.data._lose:
          return initalval
        if state.data._win :
          return initalval
        
        return ApproximateQAgent.getQValue(self, state, action)

    def observationFunction(self, state, action):
        if not self.lastState is None:
            reward = state.getScore() - self.lastState.getScore()
            self.observeTransition(self.lastState, self.lastAction, state, action, reward)
        return state

    def observeTransition(self, state,action,nextState,nextAction,deltaReward):
        self.episodeRewards += deltaReward
        self.update(state,action,nextState,nextAction,deltaReward)
        
    def startEpisode(self):
        ApproximateQAgent.startEpisode(self)
        self.oldQ = 0.0
        self.z = util.Counter() 
        

    def update(self, state, action, nextState, nextAction, reward):
        x = self.featExtractor.getFeatures(state, action)
        q = self.getQValue(state, action)
        q1 = self.getQValue(nextState, nextAction)
        d = reward + self.discount*q1 - q

        dot_product =0 
        for xi in x:
          dot_product+=x[xi]*self.z[xi]
        
        for xi in x:
          self.z[xi] = (self.discount * self.tDRate * self.z[xi]) + (1 - self.alpha*self.discount*self.tDRate*dot_product)*x[xi]
          self.weights[xi] += (self.alpha * (d + q - self.oldQ) * self.z[xi]) - (self.alpha * (q - self.oldQ) * x[xi])
        
        self.oldQ = q1

    def getAction(self, state):
        action = QLearningAgent.getAction(self,state)
        return action
    
    def final(self, state):
        deltaReward = state.getScore() - self.lastState.getScore()
        self.observeTransition(self.lastState, self.lastAction, state, None, deltaReward)
        self.stopEpisode()

        # Make sure we have this var
        if not 'episodeStartTime' in self.__dict__:
            self.episodeStartTime = time.time()
        if not 'lastWindowAccumRewards' in self.__dict__:
            self.lastWindowAccumRewards = 0.0
        self.lastWindowAccumRewards += state.getScore()

        NUM_EPS_UPDATE = 100
        if self.episodesSoFar % NUM_EPS_UPDATE == 0:
            print('Reinforcement Learning Status:')
            windowAvg = self.lastWindowAccumRewards / float(NUM_EPS_UPDATE)
            if self.episodesSoFar <= self.numTraining:
                trainAvg = self.accumTrainRewards / float(self.episodesSoFar)
                print('\tCompleted %d out of %d training episodes' % (
                       self.episodesSoFar,self.numTraining))
                print('\tAverage Rewards over all training: %.2f' % (
                        trainAvg))
            else:
                testAvg = float(self.accumTestRewards) / (self.episodesSoFar - self.numTraining)
                print('\tCompleted %d test episodes' % (self.episodesSoFar - self.numTraining))
                print('\tAverage Rewards over testing: %.2f' % testAvg)
            print('\tAverage Rewards for last %d episodes: %.2f'  % (
                    NUM_EPS_UPDATE,windowAvg))
            print('\tEpisode took %.2f seconds' % (time.time() - self.episodeStartTime))
            self.lastWindowAccumRewards = 0.0
            self.episodeStartTime = time.time()

        if self.episodesSoFar == self.numTraining:
            msg = 'Training Done (turning off epsilon and alpha)'
            print('%s\n%s' % (msg,'-' * len(msg)))

      
        if self.episodesSoFar <= self.numTraining:
            self.NTE.append(self.episodesSoFar) 
            tar=self.accumTrainRewards / (1.0 * self.episodesSoFar)
            self.TotalAverageReward.append(tar)
            self.ER.append(self.episodeRewards)

    def storemodelperformance(self, fname='output.json'):	
      fname=	fname[:len(fname)-5]
      fname= fname+'_Alpha_'+str(self.Alpha)+'_Epsilon_'+str(self.Epsilon)+'_Gamma_'+str(self.Gamma)+'_Lambda_'+str(self.Lambda)+'_Instance_'+str(self.Instancerun)+'.json'
      data=[]
      for i in range(0,len(self.NTE)):
        datarow={}
        datarow['TrainingEpisodeNumber']=self.NTE[i]
        datarow['TotalAverageReward']=self.TotalAverageReward[i]
        datarow['RewardforEpisode']=self.ER[i]
        data.append(datarow)
      with open("modelperformance\\"+fname, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)