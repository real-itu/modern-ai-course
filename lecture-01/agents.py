# pacmanAgents.py
# ---------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from pacman import Directions
from game import Agent
import copy
import random
import game
import util

class BaseAgent(game.Agent):
    class State:
        def __init__(self):
            self.actions = ['GoRight','GoLeft','GoForward','GoBack']

    def registerInitialState(self, state):
        """AgentState is stored in state"""
        self._dir = 0
        self._dirsMap = {(1,0):'East',(0,-1):'South',(-1,0):'West',(0,1):'North'}
        self._dirs = [(1,0),(0,-1),(-1,0),(0,1)]
        self._percept = ('clear', None)
        self._actions = ['GoRight','GoLeft','GoForward','GoBack']
        self._state = self.State()
        
    def getAction(self, state):
        """Get the next action. Note that the state passed here is used only
        to identify legal actions."""
        self._state = self.update_state_with_percept(self._percept, self._state)
        action = self.choose_action(copy.deepcopy(self._state))
        self._state = self.update_state_with_action(action, self._state)

        # Map the action
        do = self.mapAction(action)
        # If bump
        if do not in state.getLegalPacmanActions() and do != "Nothing":
            self._percept = ('clear','bump')
        else:
            self._percept = ('clear',None)
        
        return do
        
    def mapAction(self, action):
        """Map vacuum action to pacman action"""
        if action == "GoRight": self._dir += 1
        elif action == "GoLeft": self._dir -= 1
        elif action == "GoBack": self._dir += 2
        elif action == "GoForward": pass
        elif action == "Stop": return 'Stop'
        else: return "Nothing"
        self._dir %= 4
        
        return self._dirsMap[self._dirs[self._dir]]

    def update_state_with_percept(self, percept, state):
        """Update the agents state based on a percept"""
        return state

    def choose_action(self, state): 
        """Choose an action: GoLeft, GoRight, GoForward, GoBack, Stop"""
        return random.choice(self._actions)

    def update_state_with_action(self, action, state):
        """Update 'state' based on previous action"""
        return state

    def bfs(self, state):
        print("*** Start search ***")
        explored = []
        frontier = [state]
        while frontier != []:
            # Get next node
            node = frontier.pop(0)
            
            # Timeout
            if len(explored) % 100 == 0:
                print("Expanded: " + str(len(explored)))
                print("Frontier: " + str(len(frontier)))
                print()

            if len(explored) > 10000:
                print("Out of memory: No solution found")
                return ["Stop"]

            # Graph search
            duplicate = False
            for old in explored:
                if old.is_equivalent(node): duplicate = True
            if duplicate: continue

            # Goal test
            if node.contains_food() == False:
                solution = node.get_actions()
                if solution == None: solution = []
                solution += ["Stop"]
                print("Solution found:")
                print("Solution:", solution)
                print("Expanded:", len(explored))
                print("Frontier:", len(frontier))
                return solution

            # Generate successors
            r = node.move_right()
            if r != None: frontier += [r]
            f = node.move_forward()
            if f != None: frontier += [f]
            l = node.move_left()
            if l != None: frontier += [l]
            b = node.move_back()
            if b != None: frontier += [b]

            # Explored
            explored += [node]

        print("No solution found, aborting search...")
        return ["Stop"]


#from pacman import *
#args = readCommand(["--pacman","BaseAgent",#"PacmanWithState",
#                    "--layout","mediumEmpty"])
#runGames(**args)
