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
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()    # list = [NORTH, SOUTH, WEST, EAST, STOP]

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        minGhostDistance = min([manhattanDistance(newPos, state.getPosition()) for state in newGhostStates])

        scoreDiff = childGameState.getScore() - currentGameState.getScore()

        pos = currentGameState.getPacmanPosition()
        nearestFoodDistance = min([manhattanDistance(pos, food) for food in currentGameState.getFood().asList()])
        newFoodsDistances = [manhattanDistance(newPos, food) for food in newFood.asList()]
        newNearestFoodDistance = 0 if not newFoodsDistances else min(newFoodsDistances)
        isFoodNearer = nearestFoodDistance - newNearestFoodDistance

        direction = currentGameState.getPacmanState().getDirection()
        if minGhostDistance <= 1 or action == Directions.STOP:
            return 0
        if scoreDiff > 0:
            return 8
        elif isFoodNearer > 0:
            return 4
        elif action == direction:
            return 2
        else:
            return 1


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
    Your minimax agent (Part 1)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        # Begin your code (Part 1)
        # raise NotImplementedError("To be implemented")
        """ explain part 1 code: minimax
        I add two new functions, get_min and get_max.
        get_min means that it is ghost's turn, while get_max means it's pacman's turn.
        In getAction, go through all legal moves using gameState.getLegalActions.
        The score = get_min, where depth = 0 and agent = 1.
        Update the bets_score and best_action
        and return the best_action (the action that will make the highest score).

        In get_min, which means it's ghost's turn,
        if we have reached the depth or there is no legal moves,
        return the score in current gameState.
        Otherwise, go through all the legal actions to find the min score.
        But there are more than one ghost, so we check the agentIdx.
        If agentIdx == total agent, then we have finished min part.
        We can move to the max part (and depth + 1). score = get_max.
        Otherwise, we stay in min and go to check the next agent (agent + 1).

        In get_max, which means it's pacman's turn.
        It also return the score when it reach the depth or there is no legal moves.
        Otherwise, go through all valid moves to find the max score.
        Notice that there is only one pacman, so in every iteration, score = get_min.
        """
        
        # test all legal moves and update best_action and best_score
        best_action = None
        best_score = -float('inf')
        for action in gameState.getLegalActions(0):
            # start from depth 0, agent 1 (ghost)
            score = self.get_min(gameState.getNextState(0, action), 0, 1)
            if score > best_score:
                best_score = score
                best_action = action
        return best_action

    # it is min's turn (ghost)
    def get_min(self, gameState, depth, agentIdx):
        # reach the end, return the score
        if depth >= self.depth:
            return self.evaluationFunction(gameState)
        # no moves, also return
        """
        error massage:
        If your algorithm is returning a different
        action, make sure you are calling the
        evaluation function on winning states.
        """
        if len(gameState.getLegalActions(agentIdx))==0:
            return self.evaluationFunction(gameState)
        
        # test all legal action
        mn_score = float('inf')
        for action in gameState.getLegalActions(agentIdx):
            cur_score = None
            # it is the last agent, finish min part and go to max part (pacman's turn)
            if agentIdx == gameState.getNumAgents()-1:
                cur_score = self.get_max(gameState.getNextState(agentIdx, action), depth+1, 0)
            # it is not the last agent, keep doing min part to find the min score
            else:
                cur_score = self.get_min(gameState.getNextState(agentIdx, action), depth, agentIdx+1)
            mn_score = min(cur_score, mn_score)
        return mn_score
        
    # it is max's turn (pacman)
    def get_max(self, gameState, depth, agentIdx):
        # reach the end, return the score
        if depth >= self.depth:
            return self.evaluationFunction(gameState)
        # no moves, also return
        if len(gameState.getLegalActions(agentIdx))==0:
            return self.evaluationFunction(gameState)
        
        # test all legal action
        mx_score = -float('inf')
        for action in gameState.getLegalActions(agentIdx):
            cur_score = self.get_min(gameState.getNextState(agentIdx, action), depth, agentIdx+1)
            mx_score = max(mx_score, cur_score)
        return mx_score

        # End your code (Part 1)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (Part 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        # Begin your code (Part 2)
        # raise NotImplementedError("To be implemented")
        """explain part 2 code: alpha beta
        This is similar to minimax, but we add some constrains.
        For each node, we will have alpha < score < beta.
        In min node, we update beta in each iteration (beta = min(mn_score, beta)).
        If we found that the score we compute is smaller than alpha,
        then we can break and don't check the remaining nodes (prune)
        because we already have beta > alpha.
        No matter what's the value of other nodes, they won't change the value of parent node.
        So we can prune it.
        Similarly, in max node, we always find a larger alpha (alpha = max(alpha, mx_score)).
        If we found that the score is larger than beta, then we can prune it
        and don't visit its child node.
        Notice that in getAction, it is actually also a get_max,
        so we also need to update and compare alpha, beta, and our score.
        """
        
        # test all legal moves and update best_action and best_score
        best_action = None
        best_score = -float('inf')
        alpha = -float('inf')
        beta = float('inf')
        for action in gameState.getLegalActions(0):
            # start from depth 0, agent 1 (ghost)
            score = self.get_min(gameState.getNextState(0, action), 0, 1, alpha, beta)
            if score > best_score:
                best_score = score
                best_action = action
            # here is also a get_max, so we also need to update alpha or break due to beta (debug for a long time ......)
            if score > beta:
                break
            alpha = max(alpha, score)
        return best_action

    # it is min's turn (ghost)
    def get_min(self, gameState, depth, agentIdx, alpha, beta):
        # reach the end, return the score
        if depth >= self.depth:
            return self.evaluationFunction(gameState)
        # no moves, also return
        if len(gameState.getLegalActions(agentIdx))==0:
            return self.evaluationFunction(gameState)
        
        # test all legal action
        mn_score = float('inf')
        for action in gameState.getLegalActions(agentIdx):
            cur_score = None
            # it is the last agent, finish min part and go to max part (pacman's turn)
            if agentIdx == gameState.getNumAgents()-1:
                cur_score = self.get_max(gameState.getNextState(agentIdx, action), depth+1, 0, alpha, beta)
            # it is not the last agent, keep doing min part to find the min score
            else:
                cur_score = self.get_min(gameState.getNextState(agentIdx, action), depth, agentIdx+1, alpha, beta)
            mn_score = min(cur_score, mn_score)
            # mn_score is smaller than alpha, prune
            if mn_score < alpha:
                break
            beta = min(mn_score, beta)  # update beta

        return mn_score
        
    # it is max's turn (pacman)
    def get_max(self, gameState, depth, agentIdx, alpha, beta):
        # reach the end, return the score
        if depth >= self.depth:
            return self.evaluationFunction(gameState)
        # no moves, also return
        if len(gameState.getLegalActions(agentIdx))==0:
            return self.evaluationFunction(gameState)
        
        # test all legal action
        mx_score = -float('inf')
        for action in gameState.getLegalActions(agentIdx):
            cur_score = self.get_min(gameState.getNextState(agentIdx, action), depth, agentIdx+1, alpha, beta)
            mx_score = max(mx_score, cur_score)
            # mx_score is larger than beta, prune
            if mx_score > beta:
                break
            alpha = max(alpha, mx_score)    # update alpha
        return mx_score
        # End your code (Part 2)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (Part 3)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        # Begin your code (Part 3)
        # raise NotImplementedError("To be implemented")
        """explain part 3 code: Expectimax search
        This is also similar to minimax, but instead of assuming
        the ghost will always choose the best action like what we did in minimax,
        in expectimax search, we assuem the ghosts may make mistake and therefore
        don't make the optimal move, or we assume the ghosts move randomly.
        So in expectimax search, we do not return the action with the highest score,
        but return the action with the highest "average" score.
        In get_max (max node), we do the same thing as in minimax.
        We iterate through all the legal moves, call get_min, and return the highest score.
        In get_min, it is a chance node, not a min node.
        We sum up all the score and take its average 
        (while in minimax's min node, we return the smallest score).
        In this way, the max node will choose the node with the largest expected utility.
        """

        # test all legal moves and update best_action and best_score
        best_action = None
        best_score = -float('inf')
        for action in gameState.getLegalActions(0):
            # start from depth 0, agent 1 (ghost)
            score = self.get_min(gameState.getNextState(0, action), 0, 1)
            if score > best_score:
                best_score = score
                best_action = action
        return best_action

    # it is min's turn (ghost)
    def get_min(self, gameState, depth, agentIdx):
        # reach the end, return the score
        if depth >= self.depth:
            return self.evaluationFunction(gameState)
        # no moves, also return
        if len(gameState.getLegalActions(agentIdx))==0:
            return self.evaluationFunction(gameState)
        
        # test all legal action
        tot_score = 0
        for action in gameState.getLegalActions(agentIdx):
            # it is the last agent, finish min part and go to max part (pacman's turn)
            if agentIdx == gameState.getNumAgents()-1:
                tot_score += self.get_max(gameState.getNextState(agentIdx, action), depth+1, 0)
            # it is not the last agent, keep doing min part to find the min score
            else:
                tot_score += self.get_min(gameState.getNextState(agentIdx, action), depth, agentIdx+1)
        
        # return the average of all possible action
        return tot_score / len(gameState.getLegalActions(agentIdx))
        
    # it is max's turn (pacman)
    def get_max(self, gameState, depth, agentIdx):
        # reach the end, return the score
        if depth >= self.depth:
            return self.evaluationFunction(gameState)
        # no moves, also return
        if len(gameState.getLegalActions(agentIdx))==0:
            return self.evaluationFunction(gameState)
        
        # test all legal action
        mx_score = -float('inf')
        for action in gameState.getLegalActions(agentIdx):
            cur_score = self.get_min(gameState.getNextState(agentIdx, action), depth, agentIdx+1)
            mx_score = max(mx_score, cur_score)
        return mx_score
        # End your code (Part 3)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (Part 4).
    """
    # Begin your code (Part 4)
    # raise NotImplementedError("To be implemented")
    """explain part 4 code: Evaluation Function
    To evaluate the score of pacman, we consider its distance between food and distance between ghosts.
    For food, we want pacman to be as close as possible.
    score += 10/food distance, so the closer distance with food, the higher score pacman can get.
    For ghosts, if the ghosts are scared, we want to chase them to eat them and get higher score.
    If they are normal ghost, we want to be as far as possible from them.
    If they are scared (ScaredTime > 0), score += 100/ghost distance.
    Here we use 100 not 10 because we want to highlight the advantage of eating ghosts.
    If they are normal ghosts (ScaredTime < 0), score -= 10/ghost distance
    because we don't want to be too close to the ghost.
    If ghost distance <= 0 meaning that pacman is dead,
    then return -float('inf') meaning this is a very bad choice.
    """

    Pos = currentGameState.getPacmanPosition()
    Food = currentGameState.getFood()
    FoodsDistance = [manhattanDistance(Pos, food) for food in Food.asList()]
    minFoodsDistance = min(FoodsDistance) if len(FoodsDistance)>0 else 0    # should check whether it's empty. error msg: min() arg is an empty sequence

    score = currentGameState.getScore()

    # food : want to be as close to food as possible
    if minFoodsDistance>0:
        score += 10 / minFoodsDistance

    # ghost : if it's scared, then go close to it, otherwise, go away
    for ghostState in currentGameState.getGhostStates():
        GhostDistance = manhattanDistance(Pos, ghostState.getPosition())
        ScaredTime = ghostState.scaredTimer
        # go to ghost
        if ScaredTime>0:
            if GhostDistance>0:
                score += 100 / GhostDistance
            # to avoid devide by zero
            else:
                score += 100
        # leave ghost
        else:
            # eaten by the ghost, should avoid
            if GhostDistance<=0:
                score = -float('inf')
                break
            # closer ghost distance, lower score
            else:
                score -= 10 / GhostDistance
    
    return score

    # End your code (Part 4)

# Abbreviation
better = betterEvaluationFunction
