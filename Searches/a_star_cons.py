"""
    Daryl Mayumi Luque - A00512316
    Daniel Adalaid Carranza - A01270898
"""
import fileinput
import copy

class State:
    state = []
    actions = []
    parent = []
    heuristic_cost = 0
    goal_cost = 0
    def __init__(self, state, parent, goal_cost)
        self.state = state
        self.parent = parent
        self.goal_cost = goal_cost

if __name__ == "__main__":

    # Arreglo de arreglos donde se guardaran el initial state
    # Y el goal state
    initial_state = []
    goal_state = []

    # Recibir los parametros de entrada
    height = int(input())
    initial_input = input()
    goal_input = input()

    # Eliminamos parentesis, espacios y comas
    # y guardamos en los arreglos
    # De initial state y goal state
    while True:
        temp = initial_input[:initial_input.find(";")]
        temp2 = goal_input[:goal_input.find(";")]
        temp = temp.replace("(", "")
        temp2 = temp2.replace("(", "")
        temp = temp.replace(")", "")
        temp2 = temp2.replace(")", "")
        temp = temp.replace(",", "")
        temp2 = temp2.replace(",", "")
        temp = temp.replace(" ", "")
        temp2 = temp2.replace(" ", "")
        initial_input = initial_input[initial_input.find(";") + 1:]
        goal_input = goal_input[goal_input.find(";") + 1:]
        initial_state.append(list(temp))
        goal_state.append(list(temp2))
        if initial_input.find(";") < 0:
            temp = initial_input
            temp = temp.replace("(", "")
            temp = temp.replace(")", "")
            temp = temp.replace(",", "")
            temp = temp.replace(" ", "")
            initial_state.append(list(temp))
        if goal_input.find(";") < 0:
            temp2 = goal_input
            temp2 = temp2.replace("(", "")
            temp2 = temp2.replace(")", "")
            temp2 = temp2.replace(",", "")
            temp2 = temp2.replace(" ", "")
            goal_state.append(list(temp2))
            break
    
    root = State(initial_state, None, 0)