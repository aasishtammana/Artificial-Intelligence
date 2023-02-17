# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def terminal_state(self,state): # Define a function to check if it a terminal state 
            if self.mdp.isTerminal(state):
                return 1 #return 1 if it is terminal state
            return 0 #return 0 if it is not terminal state

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"  
        def get_action_value(state): #Defining a local function to get all actions and compute their value
            output = []
            for steps in self.mdp.getPossibleActions(state): # Iterate through possible actions
                output+=[self.computeQValueFromValues(state,steps)] #Compute their values and append them
            return output #return value
        
        states=self.mdp.getStates()   #Get all the states
        iterations=self.iterations #Check number of iterations

        for run in range(iterations): #run for loop over the number of iterations
            newval = dict(self.values) #create a copy of the dictionary values
            for pos in states: #Iterate through the states
                if self.terminal_state(pos)==1: #Check if it is terminal state
                    newval[pos] = 0#If terminal stat, return 0
                else:
                    newval[pos] = max(get_action_value(pos)) #Otherwise return the max value from the actions
            self.values = newval

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        output = 0 #Initialise variable to 0
        step = self.mdp.getTransitionStatesAndProbs(state,action)#Get transition states and their probabilities
        for element in step:#Iterate through the transition states
            next_state=element[0]#Assign possible next state
            prob=element[1]#Assign the given probability
            reward=self.mdp.getReward(state,action,next_state)#Compute reward for the given dynamics
            discount=self.discount#Discount factor
            qvalue=prob*(reward+self.values[next_state]*discount)#Compute qvalue using the given formula
            output += qvalue #Add to output through the loops     
        return output #return output

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        direction = 'north'#Set random direction as default to initialise
        maxval = -999999 #Set a very high negative value for the max       
        for step in self.mdp.getPossibleActions(state): #Iterate through the possible actions
            val = self.computeQValueFromValues(state, step) #Compute the qvalue for the iteration
            if maxval<val:#Check that maxval is lesser than the computed val
                direction = step #reassign the correct direction/action
                maxval = val #Change the maxval
        return direction #return the final direction after all loops

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)
    
    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()#Get all states
        for run in range(self.iterations):#Range through the iterations
            pos = states[run%len(states)]#Cyclic iteration to update only one value per cycle
            if self.terminal_state(pos)==0:#Check if terminal state or not by using function defined above
                self.values[pos] = self.getQValue(pos,self.getAction(pos))#reassign the value for the given position


class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
