import fileinput
import copy
import sys
import itertools
import heapq
import time

class State(object):
    def __init__(self, string=None, containers=[], cost=0, steps=[]):
        self.cost       = cost
        self.heuristicCost = 0
        self.steps      = steps
        self.containers = containers

        if string:
            self.initializeContainer(string)

    def getCost(self):
        return str(int(self.cost)) + "\n"

    def getSteps(self):
        return "; ".join(map(str, self.steps)) + "\n"

    def updateCost(self,action): 
        """
        Calculates g(n)
        """
        self.cost += 0.5 + 0.5 + abs(action[0] - action[1])
    
    def updateFinalCost(self, action, goal): 
        """
        Calcualtes g(n) + h(n)
        """
        goal_location = goal.lookupDic[self.containers[action[0]][-1]]
        self.heuristicCost = self.cost + abs(action[0] - goal_location)

    def applyAction(self, action, goal):
        """
        Applies the action tho the current state
        """
        # Updates the cost
        self.updateFinalCost(action, goal)
        self.updateCost(action)
        
        # Executes the actions
        x = self.containers[action[0]].pop()
        self.containers[action[1]].append(x)
        self.steps.append(action)
        

    def cloneState(self):
        """
        Clones a state
        """
        new_state = State(containers=copy.deepcopy(self.containers),
                    cost=self.cost,
                    steps=copy.deepcopy(self.steps))
        return new_state


    def isValidAction(self, action, height):
        """
        Check if an action is valid based on the 
        """
        return len(self.containers[action[1]]) + 1 <= height and \
            len(self.containers[action[0]]) - 1 >= 0

    def setContainer(self, containers):
        self.containers = containers

    def initializeContainer(self, string):
        """
        Gets a string and parses it into a matrix
        """
        for stack in string.split("; "):
            c = stack.strip("()")
            if len(c):
                c = c.split(", ")
            else:
                c = []
            self.containers.append(c)

    def __str__(self):
        """
        Override of str() method
        """
        return str(self.containers)

    def __hash__(self):
        """
        Override of hashing function when pushing a state to a set
        for visited states
        """
        return hash(str(self.containers))

    def __eq__(self, other):
        """
        Overrides equality function to use '==' operator between states
        """
        return str(self) == other
    
    def __cmp__(self, other):
        """
        Override of compare method, used when 
        pushing to ordered queue to compare between states
        """
        return cmp(self.heuristicCost, other.heuristicCost)


class Goal(object):
    def __init__(self, string=None, containers=[], cost=0, steps=[]):
        self.cost           = cost
        self.steps          = steps
        self.containers     = containers
        self.shouldCheck    = []
        self.lookupDic      = {}

        if string:
            self.initializeContainer(string)
            self.initializeDict()
            
    def initializeDict(self):
        """
        Initialize reverse lookup for stacks
        Keys: letters
        Values: stack index
        """
        for idx, stack in enumerate(self.containers):
            for box in stack:
                self.lookupDic[box] = idx
        
    def initializeContainer(self, string):
        """
        Overrides initializeContainer to handle 'X'
        """
        for stack in string.split("; "):
            c = stack.strip("()")
            shouldCheck = True

            if len(c) and c[0] == "X":
                shouldCheck = False
            elif len(c):
                c = c.split(", ")
            else:
                c = []

            self.shouldCheck.append(shouldCheck)
            self.containers.append(c)

    def __eq__(self, other):
        """
        Override of equality function '==' to be able 
        to compare states
        """
        is_equal = True
        for idx, stack in enumerate(self.containers):
            if self.shouldCheck[idx]:
                is_equal = is_equal and str(stack) == str(other.containers[idx])

        return is_equal


def create_valid_actions(state, height):
    """
    Generates the product of the containers and
    check against the current state if the generated actions
    are valid
    """
    space = tuple(range(len(state.containers)))
    possible_actions = itertools.product(space, repeat=2)
    return [action for action in possible_actions
                if state.isValidAction(action, height)]
                
        
                
if __name__ == "__main__":
    max_height    = -1
    frontier      = []
    explored      = set()
    goal          = None
    solutionFound = False
    input         = []

    # Read each input line
    for line in sys.stdin:
        # sys.stdout.write(line)
        line = line.strip("\n")
        input.append(line)

    for idx, line in enumerate(input):
        # Height
        if idx == 0:
            max_height = int(line)
        # Initial State
        elif idx == 1:
            frontier.append(State(string=line))
        # # Goal
        elif idx == 2:
            goal = Goal(string=line)
          
    # A* cons
    t0 = time.time()
    while(len(frontier)):
        # Add get element with lowest cost
        node = heapq.heappop(frontier)
        # Add to explored
        explored.add(node)
        # Generate valid actions
        valid_actions = create_valid_actions(node, max_height)
        for action in valid_actions:
            new_node = node.cloneState()
            new_node.applyAction(action,goal)
            if new_node not in explored:
                # Print solution
                if goal == new_node:
                    sys.stdout.write(new_node.getCost())
                    sys.stdout.write(new_node.getSteps())
                    frontier = []
                    solutionFound = True
                    break
                else:
                    # Sorted push of new node
                    print(new_node)
                    heapq.heappush(frontier, new_node)
    if not solutionFound:
        sys.stdout.write("No solution found\n")
    #print time.time()