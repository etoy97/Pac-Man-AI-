# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from util import Stack
from util import Queue
from util import PriorityQueue
from util import PriorityQueueWithFunction
from game import Directions
import time
import copy

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    """
    #"*** YOUR CODE HERE ***"
    st = Stack()

    #Create states that have been seen before, add the start state
    seen = set()
    seen.add(problem.getStartState())


    #Get the successor states and the directions to get to them
    first_successors = problem.getSuccessors(problem.getStartState())

    #Push them onto a stack, initialize that it came from a start state with no moves
    for (a,b,c) in first_successors:
        st.push((a, [], b))


    #While I still have states to explore
    while(st.isEmpty() == False):

        #Get the most recent successor aka the cur_state, add to seen
        #   path_to are the steps taken so far
        (cur_state, path_to, action) = st.pop()
        seen.add(cur_state)
        
        #Add the direction we took to get there
        path_to.append(action)
        
        #If the successor is a goal state, return the directions to get there
        if (problem.isGoalState(cur_state)):
            return path_to

        #Get successors from cur_state
        successors = problem.getSuccessors(cur_state)

        
        #Add the new successors
        for (new_state, new_action, cost) in successors:
            #Check that it's not a repeated state
            if (new_state not in seen):
                st.push((new_state, copy.deepcopy(path_to), new_action)) 

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    #"*** YOUR CODE HERE ***"
    #Create a queue to keep track of states
    q = Queue()
  

    #Create states that have been seen before, add the start state
    seen = set()
    #print (problem.getStartState())
    seen.add(problem.getStartState())

    #Get the successor states and the directions to get to them
    first_successors = problem.getSuccessors(problem.getStartState())

    #Push them onto a stack, initialize that it came from a start state with no moves
    for (a,b,c) in first_successors:
        q.push((a,[], b))
        seen.add(a)

    
    #While I still have states to explore
    while(q.isEmpty() == False):
        #Get the most recent successor aka the cur_state, add to seen
        #   path_to are the steps taken so far
        (cur_state, path_to, action) = q.pop()
        #seen.add(cur_state)
  
        #Add the direction we took to get there
        path_to.append(action)


        #If the successor is a goal state, return the directions to get there
        if (problem.isGoalState(cur_state)):       
            return path_to

        #Get successors from cur_state
        successors = problem.getSuccessors(cur_state)

        
        #Add the new successors
        for (new_state, new_action, cost) in successors:
            #Check that it's not a repeated state
            if (new_state not in seen):
                #Add to seen
                seen.add(new_state)
        
                q.push((new_state, copy.deepcopy(path_to), new_action)) 
    

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    #"*** YOUR CODE HERE ***"
    #Create a Priority Queue to store the new states based on the kind of moves     
    pq = PriorityQueue()
 
    #Create states that have been seen before, add the start state
    visited =set()

    first_node = problem.getStartState()

    nodes = set()
    nodes.add(first_node)
    pq.push((first_node, [], nodes), problem.getCostOfActions([]))
   
    while (pq.isEmpty() == False):  
    
        (cur_state, action_path, nodes) = pq.pop()

        #If it's in visited, ignore this path as we already found the minimum path to this node
        if (cur_state in visited):
            continue
        visited.add(cur_state)


        if (problem.isGoalState(cur_state)):
            return action_path

        successors = problem.getSuccessors(cur_state)

        for (new_state, new_action, c) in successors:
            #If this node is not on the path to the current node, then add it
            if (new_state not in nodes):
                newNodes = copy.deepcopy(nodes)
                #Add that this node is on the path
                newNodes.add(new_state)
                new_path = copy.deepcopy(action_path)
                #Add the action to get to this new_state
                new_path.append(new_action)
                cost = problem.getCostOfActions(new_path)
                pq.push((new_state, new_path, newNodes), cost)                


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    #Create a Priority Queue to store the new states based on the kind of moves     
    pq = PriorityQueue()
 
    first_node = problem.getStartState()
    #Create states that have been seen before, add the start state
    visited =set()

    nodes = set()
    nodes.add(first_node)
    pq.push((first_node, [], nodes), problem.getCostOfActions([]) + heuristic(first_node, problem))
   
    while (pq.isEmpty() == False):  
    
        (cur_state, action_path, nodes) = pq.pop()
        if (cur_state in visited):
            continue
        visited.add(cur_state)
 

        if (problem.isGoalState(cur_state)):
            return action_path

        successors = problem.getSuccessors(cur_state)

        for (new_state, new_action, c) in successors:
            if (new_state not in nodes):
                newNodes = copy.deepcopy(nodes)
                newNodes.add(new_state)
                new_path = copy.deepcopy(action_path)
                new_path.append(new_action)
                cost = problem.getCostOfActions(new_path) + heuristic(new_state, problem)
                pq.push((new_state, new_path, newNodes), cost)                


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
