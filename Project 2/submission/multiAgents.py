# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        def foodpositionasList(currentGameState):# Given the current game state compute the food postion and return the list
            foodPos=currentGameState.getFood()
            foodPoslist=foodPos.asList()
            return foodPoslist
        
        if action == 'Stop': # If the action to be taken is stop return a very small value
            return float('-inf')
        length,fooditer,ghostIter = 0,0,0 #initialise variables
        lowest = float('inf')        
        foodPosition=foodpositionasList(currentGameState) # use the previously defined function to compute list of food positions
        ghostPos = [ghostState.getPosition() for ghostState in newGhostStates] #check ghost positions
        while ghostIter < len(newScaredTimes): # avoiding the step if the ghost is close by returning a small value
            if ghostPos[ghostIter] == tuple(newPos) and newScaredTimes[ghostIter]==0:
                return float('-inf')
            ghostIter=ghostIter+1 #incrementing variable
        while fooditer < len(foodPosition):
            length =  (manhattanDistance(foodPosition[fooditer], list(newPos))) # find the manhattan distance 
            if length < lowest: # If the distance is less, change value to this distance to prefer the step
                lowest = length
            fooditer=fooditer+1 #incrementing variable

        return -lowest

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def maxagentscore(depth,agentIndex,gameState): #define max function as per pseudo code
            if gameState.isWin() or gameState.isLose(): #Check if the game is ending and get the score
                return gameState.getScore()
            score=float("-inf")# set initial score to a very small value
            possibleactions=gameState.getLegalActions(agentIndex) # compute the set of all possible actions
            desiredaction=None #initialise next action to none
            for action in possibleactions: #iterate through the actions and compute the score recursively 
                newstate=gameState.generateSuccessor(agentIndex, action)#generate the next state
                childscore=minagentscore(depth,agentIndex+1,newstate) #the max agent calls the minagent funtion for nextagent
                if childscore>score:
                    score=childscore #check the desired action based on the score
                    desiredaction=action
            if depth==0:
                return desiredaction #If the node is leaf node,just return the action
            return score #return final score
                
        def minagentscore(depth,agentIndex,gameState): #define min function as per pseudo code
            if gameState.isWin() or gameState.isLose():#Check if the game is ending and get the score
                return gameState.getScore()        
            totalagents=gameState.getNumAgents() # compute the total number of agents
            nextagent=(agentIndex+1)%totalagents  # Checking for the last agent
            score=float("inf")
            possibleactions=gameState.getLegalActions(agentIndex)   # compute the set of all possible actions          
            for action in possibleactions:#iterate through the actions and compute the score recursively 
                newstate=gameState.generateSuccessor(agentIndex, action)  #generating successor states              
                if nextagent==0: #if last agent, reduce the depth
                    if depth==self.depth - 1:
                        childscore=self.evaluationFunction(newstate) #compute score
                    else:
                        childscore=maxagentscore(depth+1,nextagent,newstate) #recursively call max agent on the next level
                else:
                    childscore=minagentscore(depth,nextagent,newstate) #If not last call min agent on current depth
                if childscore<score:
                    score=childscore
            return score #return final score

        return maxagentscore(0,0,gameState) #calling the main function with depth 0 and agent index 0
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def maxagentscore(depth,agentIndex,gameState,alpha,beta):  #define max function as per pseudo code with alpha and beta
            if gameState.isWin() or gameState.isLose():#Check if the game is ending and get the score
                return gameState.getScore()
            score=float("-inf")# set initial score to a very small value
            possibleactions=gameState.getLegalActions(agentIndex)# compute the set of all possible actions
            desiredaction=None#initialise next action to none
            for action in possibleactions: #iterate through the actions and compute the score recursively 
                newstate=gameState.generateSuccessor(agentIndex, action)#generate the next state
                childscore=minagentscore(depth,agentIndex+1,newstate,alpha,beta)#the max agent calls the minagent funtion for nextagent 
                if(childscore>beta): #Check for pruning
                    return childscore
                if childscore>score: #check the desired action based on the score
                    score=childscore
                    desiredaction=action
                alpha=max(alpha,childscore) #reset alpha values
            if depth==0:
                return desiredaction #If the node is leaf node,just return the action
            
            return score #return final score
                
        def minagentscore(depth,agentIndex,gameState,alpha,beta):  #define min function as per pseudo code with alpha and beta
            if gameState.isWin() or gameState.isLose():#Check if the game is ending and get the score
                return gameState.getScore()        
            totalagents=gameState.getNumAgents() # compute the total number of agents
            nextagent=(agentIndex+1)%totalagents # Checking for the last agent
            score=float("inf")
            possibleactions=gameState.getLegalActions(agentIndex)   # compute the set of all possible actions                   
            for action in possibleactions:#iterate through the actions and compute the score recursively 
                newstate=gameState.generateSuccessor(agentIndex, action)      #generating successor states                  
                if nextagent==0:#if last agent, reduce the depth
                    if depth==self.depth - 1:
                        childscore=self.evaluationFunction(newstate)#compute score
                    else:
                        childscore=maxagentscore(depth+1,nextagent,newstate,alpha,beta)    #recursively call max agent on the next level                 
                else:
                    childscore=minagentscore(depth,nextagent,newstate,alpha,beta)#If not last call min agent on current depth
                if(childscore<alpha):#Check for pruning
                    return childscore
                if childscore<score:
                    score=childscore
                beta=min(beta,childscore)#reset beta values
            return score #return final score
        
        return maxagentscore(0,0,gameState,float("-inf"),float("inf"))#calling the main function with depth 0,agent index 0,alpha and beta -inf and +inf respectively
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def maxagentscore(depth,agentIndex,gameState):  #define max function as per pseudo code
            if gameState.isWin() or gameState.isLose(): #Check if the game is ending and get the score
                return gameState.getScore()
            score=float("-inf")# set initial score to a very small value
            possibleactions=gameState.getLegalActions(agentIndex)# compute the set of all possible actions
            desiredaction=None#initialise next action to none
            for action in possibleactions: #iterate through the actions and compute the score recursively 
                newstate=gameState.generateSuccessor(agentIndex, action)#generate the next state
                childscore=minagentscore(depth,agentIndex+1,newstate)#the max agent calls the minagent funtion for nextagent
                if childscore>score:
                    score=childscore #check the desired action based on the score
                    desiredaction=action
            if depth==0:
                return desiredaction #If the node is leaf node,just return the action
            return score#return final score
                
        def minagentscore(depth,agentIndex,gameState):#define min function as per pseudo code
            if gameState.isWin() or gameState.isLose():#Check if the game is ending and get the score
                return gameState.getScore()        
            totalagents=gameState.getNumAgents() # compute the total number of agents
            nextagent=(agentIndex+1)%totalagents # Checking for the last agent
            score=0 #initialise score to 0 because the action does not matter
            possibleactions=gameState.getLegalActions(agentIndex)     # compute the set of all possible actions       
            for action in possibleactions:#iterate through the actions and compute the score recursively 
                newstate=gameState.generateSuccessor(agentIndex, action)      #generating successor states              
                if nextagent==0:#if last agent, reduce the depth
                    if depth==self.depth - 1:
                        childscore=self.evaluationFunction(newstate)#compute score
                    else:
                        childscore=maxagentscore(depth+1,nextagent,newstate)#recursively call max agent on the next level
                else:
                    childscore=minagentscore(depth,nextagent,newstate)#If not last call min agent on current depth
                score=score+childscore #increment the score with child score to take a weighted sum               
            return score/len(possibleactions) # return average score

        return maxagentscore(0,0,gameState) #calling the main function with depth 0 and agent index 0
        util.raiseNotDefined()

