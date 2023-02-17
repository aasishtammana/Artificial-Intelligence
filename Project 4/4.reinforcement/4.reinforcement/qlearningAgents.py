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
        self.values=util.Counter() #initialise values

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        return self.values[state,action]#return qvalue

    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        def get_action_value(state): #defina a local function just like in value iteration to get all actions and compute their value 
            output = []
            for step in self.getLegalActions(state): # Iterate through possible actions
                output+=[self.getQValue(state, step)] #Compute their values and append them
            return output #return value

        output=get_action_value(state) #get the actions and store them in output
        if len(output) != 0: #make sure actions are present
            return max(output) #if they are present return max value
        else:
            return 0 #if no actions return 0

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        direction = 'north' #Set random direction as default to initialise
        maxval = -999999  #Set a very high negative value for the max     
        for step in self.getLegalActions(state): #Iterate through the possible actions
            val = self.getQValue(state, step) #Compute the qvalue for the iteration
            if maxval<val:#Check that maxval is lesser than the computed val
                direction = step #reassign the correct direction/action
                maxval = val #Change the maxval
        return direction #return the final direction after all loops

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
        legalActions = self.getLegalActions(state)
        action = None #No action implies terminal state and we return None
        "*** YOUR CODE HERE ***"
        if util.flipCoin(self.epsilon)==True: #use flipcoin and check if it results in true
            action=random.choice(legalActions) #choose random action if it is true
        else:
            action=self.computeActionFromQValues(state) #Otherwise compute the q value
        return action #return action
        

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        val = self.getQValue(state,action) #Get q values
        fixed=(self.alpha*reward)+(1-self.alpha)*val #Fixed if next state is present or not
        if nextState:#Check if there is a next state
          self.values[state,action] = fixed+(self.alpha*self.discount*self.computeValueFromQValues(nextState)) #Fixed part plus value of next state
        else:
          self.values[state,action] = fixed#only fixed part

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
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def features(self,state,action):#Define a function get features to get features using featureExtractors.py
        return self.featExtractor.getFeatures(state,action)
    
    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        step=self.features(state,action) #Use the function defined to get features
        output = 0 #initialise variable for output to 0
        for val in step:#iterate through the features
            output += step[val]*self.weights[val]#output the product of 
        return output #return output


    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        step=self.features(state,action) #Use the function defined to get features
        difference = (reward + self.discount * self.getValue(nextState)) - self.getQValue(state, action)#compute difference
        for val in step:#iterate through features
            self.weights[val] = self.weights[val] + self.alpha * difference * step[val] #update weights

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
