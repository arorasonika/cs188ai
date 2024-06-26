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
        def getPositionTupleFromState(a):
            return (a.getPosition()[0], a.getPosition()[1])

        ghostPositions = [getPositionTupleFromState(ghostState) for ghostState in newGhostStates]

        if newPos in ghostPositions and not min(newScaredTimes) > 0:  # if not scared and pacman close to ghost position
            return float("-Inf")

        if newPos in currentGameState.getFood().asList():
            return float("Inf")

        nextNearestFood = min([manhattanDistance(f, newPos) for f in newFood.asList()])
        nextNearestGhost = min([manhattanDistance(g, newPos) for g in ghostPositions])

        if not min(newScaredTimes) > 0:  # not scared
            return 100.0*(1.0/nextNearestFood) - 100.0*(1.0/nextNearestGhost)
        else:  # if ghost is scared
            return 100.0*(1.0/nextNearestFood) + 50*(1.0/nextNearestGhost)

        #return successorGameState.getScore()


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

        def isGameOver(state, depth):
            return depth == self.depth or state.isWin() or state.isLose()

        def minimizer(state, depth, agentIndex=1):
            if isGameOver(state, depth):
                return self.evaluationFunction(state)
            retVal = float("Inf")
            for action in state.getLegalActions(agentIndex):
                if agentIndex != (gameState.getNumAgents() - 1):  # consider ghosts
                    retVal = min(retVal, minimizer(state.generateSuccessor(agentIndex, action), depth, agentIndex + 1))
                else:  # consider pacman agent
                    retVal = min(retVal, maximizer(state.generateSuccessor(agentIndex, action), depth + 1, 0))
            return retVal

        def maximizer(state, depth, agentIndex=0):
            if isGameOver(state, depth):
                return self.evaluationFunction(state)
            retVal = float("-Inf")
            for action in state.getLegalActions(agentIndex):  # agentindex always 0 here
                retVal = max(retVal, minimizer(state.generateSuccessor(agentIndex, action), depth))
            return retVal

        d = dict()
        for action in gameState.getLegalActions(0):
            d[action] = minimizer(gameState.generateSuccessor(0, action), 0, 1)
        return sorted(d, key=lambda x: d[x], reverse=True)[0]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def isGameOver(state, depth):
            return depth == self.depth or state.isWin() or state.isLose()

        def minimizer(state, A, B, depth, agentIndex=1):
            if isGameOver(state, depth):
                return self.evaluationFunction(state)
            retVal = float("Inf")
            for action in state.getLegalActions(agentIndex):
                if agentIndex != (gameState.getNumAgents() - 1):  # consider ghosts
                    retVal = min(retVal, minimizer(state.generateSuccessor(agentIndex, action), A, B, depth, agentIndex + 1))
                else:  # consider pacman agent
                    retVal = min(retVal, maximizer(state.generateSuccessor(agentIndex, action), A, B, depth + 1, 0))
                if retVal < A:
                    return retVal
                B = min(B, retVal)
            return retVal

        def maximizer(state, A, B, depth, agentIndex=0):
            if isGameOver(state, depth):
                return self.evaluationFunction(state)
            retVal = float("-Inf")
            for action in state.getLegalActions(agentIndex):  # agentindex always 0 here
                retVal = max(retVal, minimizer(state.generateSuccessor(agentIndex, action), A, B, depth))
                if retVal > B:
                    return retVal
                A = max(A, retVal)
            return retVal

        maxVal = float("-Inf")
        alpha = float("-Inf")
        beta = float("Inf")
        returned_action = None

        for action in gameState.getLegalActions(0):
            value = minimizer(gameState.generateSuccessor(0, action), alpha, beta, 0, 1)
            maxVal = max(maxVal, value)

            if alpha == float("-Inf") or maxVal > alpha:
                returned_action = action
                alpha = maxVal

        return returned_action


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

        def isGameOver(state, depth):
            return depth == self.depth or state.isWin() or state.isLose()

        def expectation(state, depth, agentIndex=1):
            if isGameOver(state, depth):
                return self.evaluationFunction(state)
            retVal = 0
            for action in state.getLegalActions(agentIndex):
                prob = 1 / len(state.getLegalActions(agentIndex))
                if agentIndex != (gameState.getNumAgents() - 1):  # consider ghosts
                    retVal += (prob * expectation(state.generateSuccessor(agentIndex, action), depth, agentIndex + 1))
                else:  # consider pacman agent
                    retVal += (prob * maximizer(state.generateSuccessor(agentIndex, action), depth + 1, 0))
            return retVal

        def maximizer(state, depth, agentIndex=0):
            if isGameOver(state, depth):
                return self.evaluationFunction(state)
            retVal = float("-Inf")
            for action in state.getLegalActions(agentIndex):  # agentindex always 0 here
                retVal = max(retVal, expectation(state.generateSuccessor(agentIndex, action), depth))
            return retVal

        d = dict()
        for action in gameState.getLegalActions(0):
            d[action] = expectation(gameState.generateSuccessor(0, action), 0, 1)
        return sorted(d, key=lambda x: d[x], reverse=True)[0]


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION:
    I calculated the initial score with the given scoreEvaluationFunction above and found the pacman position,
    food positions, ghost positions, scaredtimes and capsule positions from the current GameState.
    If the game is over, then we can instantly assign a value of +Infinity or -Infinity if the gamestate is a winning state
    or losing state respectively.
    Then I found some quantities:
    1. min distance to food: I used the reciprocal of this in the score value with a factor of 2 because we want the
    pacman to eat the food closer to it and we want gains from eating to be proportional to how far it is
    2. numCapsules: I used this with a factor of -15 because the pacman should eat capsules he encounters
    3. min distance to active ghosts: active ghosts being close to the pacman are bad so I used the reciprocal of
    minDistanceToActiveGhost with a factor of -5. Higher distance from the active ghost means less problem.
    4. min distance to scared ghosts: eating scared ghosts gives more points. So closer the scared ghosts are,
    more the pacman should consider eating it. So I used the reciprocal of minDistanceToScaredGhost with a factor of 4.
    5. numFood: This is the amount of food remaining. It is bad to have food remaining. I used it with a factor of -20
    so lesser the food remains, more better the evaluation score gets.
    """
    "*** YOUR CODE HERE ***"
    score = scoreEvaluationFunction(currentGameState)
    pacmanPosition = currentGameState.getPacmanPosition()
    foodPositions = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    capsulePositions = currentGameState.getCapsules()

    def getPositionTupleFromState(a):
        return (a.getPosition()[0], a.getPosition()[1])

    if currentGameState.isLose():
        return float('-Inf')

    if currentGameState.isWin():
        return float('Inf')

    minDistanceToFood = min([manhattanDistance(val, pacmanPosition) for val in foodPositions])

    numCapsules = len(capsulePositions)

    activeGhosts = [ghostStates[i] for i in range(len(scaredTimes)) if scaredTimes[i] == 0]
    scaredGhosts = [ghostStates[i] for i in range(len(scaredTimes)) if scaredTimes[i] != 0]

    minDistanceToActiveGhost = float('Inf')
    minDistanceToScaredGhost = float('Inf')

    if activeGhosts:
        minDistanceToActiveGhost = min([manhattanDistance(getPositionTupleFromState(val), pacmanPosition) for val in activeGhosts])
    elif scaredGhosts:
        minDistanceToScaredGhost = min([manhattanDistance(getPositionTupleFromState(val), pacmanPosition) for val in scaredGhosts])

    numFood = len(foodPositions)

    score += ((1/minDistanceToFood) * 2 +
              numCapsules * -15 +
              (1/minDistanceToActiveGhost) * -5 +
              (1/minDistanceToScaredGhost) * 4 +
              numFood * -20
              )
    return score

# Abbreviation
better = betterEvaluationFunction
