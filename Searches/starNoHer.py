import fileinput
import copy
import sys
import itertools
import heapq

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

    def updateCost(self,action): #g(n)
        self.cost += 0.5 + 0.5 + abs(action[0] - action[1])
    
    def updateFinalCost(self, action, goal): #H(n)
        goal_location = goal.lookupDic[self.containers[action[0]][-1]]
        self.heuristicCost = self.cost + abs(action[0] - goal_location[0]) + abs(action[0] - goal_location[1])

    def applyAction(self, action, goal):
        self.updateFinalCost(action, goal)
        self.updateCost(action)
        
        x = self.containers[action[0]].pop()
        self.containers[action[1]].append(x)
        self.steps.append(action)
        

    def stateFromAction(self, action):
        new_state = State(containers=copy.deepcopy(self.containers),
                    cost=self.cost,
                    steps=copy.deepcopy(self.steps))
        return new_state


    def isValidAction(self, action, height):
        return len(self.containers[action[1]]) + 1 <= height and \
            len(self.containers[action[0]]) - 1 >= 0

    def setContainer(self, containers):
        self.containers = containers

    def initializeContainer(self, string):
        for stack in string.split("; "):
            c = stack.strip("()")
            if len(c):
                c = c.split(", ")
            else:
                c = []
            self.containers.append(c)

    def __str__(self):
        return str(self.containers)

    def __hash__(self):
        return hash(str(self.containers))

    def __eq__(self, other):
        return str(self) == other
    
    def __cmp__(self, other):
        # return self
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
            self.initializeDic()
            
    def initializeDic(self):
        for idx, stack in enumerate(self.containers):
            for idy, box in enumerate(stack):
                self.lookupDic[box] = [idx,idy]
        
    def initializeContainer(self, string):
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
        is_equal = True
        for idx, stack in enumerate(self.containers):
            if self.shouldCheck[idx]:
                is_equal = is_equal and str(stack) == str(other.containers[idx])

        return is_equal


def create_valid_actions(state, height):
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
    while(len(frontier)):
        node = heapq.heappop(frontier)
        explored.add(node)
        valid_actions = create_valid_actions(node, max_height)
        for action in valid_actions:
            new_node = node.stateFromAction(action)
            new_node.applyAction(action,goal)
            if new_node not in explored:
                if goal == new_node:
                    sys.stdout.write(new_node.getCost())
                    sys.stdout.write(new_node.getSteps())
                    frontier = []
                    solutionFound = True
                    break
                else:
                    heapq.heappush(frontier, State(new_node))
    if not solutionFound:
        sys.stdout.write("No solution found\n")