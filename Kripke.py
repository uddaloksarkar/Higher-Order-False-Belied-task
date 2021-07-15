import numpy as np
import copy
from utils import *
from formula import *
from Action import *

class World:
    """
    class defining Nodes (each world) of the Kripke Structure

    name : int (start naming from 0)
    """

    def __init__(self, name, assignment):
        self.name = name    # works as node id
        assignment['top'] = True
        assignment['bottom'] = False
        self.assignment = assignment    # dictionary of truth assignments

    def __eq__(self, other):
        return self.name == other.name and self.assignment == other.assignment

    def __str__(self):
        return "(" + self.name + ',' + str(self.assignment) + ')'\



class Kripke:
    """
    Kripke Frame with it's possible worlds and relation

    worlds : array of Worlds
    agents : array of agents
    """

    # 'relations' is in set format, change it to adjacency list format for ease of computation
    def __init__(self, worlds, relations, point):
        '''
        Includes prepocessings before and after initating Kripke Structure
        '''
        self.worlds = [None for i in range(len(worlds))]
        for world in worlds:
            self.worlds[world.name] = world
        self.agents = relations.keys()
        self.point = point      # world_name of the point in pointed Kripke Structure
        self.relations = self.adjList(relations)


    def adjList(self, relations):
        """
        modifies binary relation to adjacency list
        """
        adj = {}
        for agent in self.agents:
            adj[agent] = {}
        for agent in self.agents:
            for relation in relations[agent]:
                if relation[0] not in adj[agent].keys():
                    adj[agent][relation[0]] = []
                adj[agent][relation[0]].append(relation[1])
        return adj


    def product_update(self, action):
        """
        This routine multiplies the Kripke model with a Action model.
        for epistemic change it only uses preconditions from Action model and
        for factual change it use postcondition from Action model
        """

        # if not isinstance(action, Action):
        #     raise TypeError

        worlds = []; to_remove = [] # to_remove will be used to remove edges from tensor product
        name = 0
        for world in self.worlds:
            for event in action.events:
                assignment = copy.deepcopy(world.assignment)
                if event.precondition.semantic(self, world):
                    if not event.postcondition == None:
                        for i in event.postcondition.keys():
                            assignment[i] = event.postcondition[i]
                    world = World(name, assignment)
                    worlds.append(world)
                    if self.point == world.name and action.point == event.name:
                        self.point = name       # point in modified Kripke model
                    name += 1
                else:
                    to_remove.append((world.name, event.name))
        self.worlds = worlds

        for agent in self.agents:
            event_adj = list2mat(action.relations[agent]) # adj corresponds to adjacency matrix
            world_adj = list2mat(self.relations[agent])
            updated_adj = np.kron(world_adj, event_adj)   # updated Kripke relations
            for w_e in to_remove:
                i = w_e[0]*len(action.events) + w_e[1]  # index of corresponding (world, event) pair in kronecker matrix
                for j in range(updated_adj.shape[0]):
                    updated_adj[i][j] = updated_adj[j][i] = 0   # deleting edges to the removed nodes / worlds
            self.relations[agent] = mat2list(updated_adj)

        return


    def check(self, formula):
        """
        checks whether a formula is true in the real world
        """
        return formula.semantic(self, self.worlds[point])


if __name__ == '__main__':
    # relations = {'a' : [(0,0),(0,1),(1,0),(1,1)], 'b' : [(0,0),(0,1),(1,0),(1,1)]}
    # w0 = World(0, {})
    # w1 = World(1, {'p': True})
    # point = 1
    # ks = Kripke([w0, w1], relations, point)
    # ks.check(Atom('p'))
    # e0 = Event(0, Atom('top'), 'top')
    # e1 = Event(1, Atom('top'), 'q')
    # events = [e0, e1]
    # relations = {'a' : [(0,0),(1,1)], 'b' : [(0,0),(1,0)]}
    # point = 1
    # am = Action(events, relations, point)
    # ks.product_update(am)

    w0 = World(0, {'p' :True})
    e0 = Event(0, Atom('top'), {'p': False})
    e1 = Event(1, Atom('top'), {'p': True})
    events = [e0, e1]
    relations = {'a' : [(0,0),(1,1),(0,1),(1,0)], 'b' : [(0,0),(1,1)]}
    point =1
    am = Action(events, relations, point)
    relations_w = {'a' : [(0,0)], 'b' : [(0,0)]}
    ks = Kripke([w0], relations_w, point)
    ks.product_update(am)
