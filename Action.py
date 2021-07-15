import numpy as np
import copy

class Event:
    """
    class defining Nodes (each event) of the Action model
    precondition must be a modal formula
    """

    def __init__(self, name, pre, post):
        self.name = name
        self.precondition = pre
        self.postcondition = post

    def __eq__(self, other):
        return self.name == other.name and self.precondition == other.precondition and self.postcondition == other.postcondition

    def __str__(self):
        return "(" + self.name + ',' + str(self.precondition) + ',' + str(self.postcondition) + ')'\



class Action:
    """
    Action model with it's events and relations

    events : array of event class
    agents : array of agents
    """

    # 'relations' is in set format, change it to adjacency list format for ease of computation
    def __init__(self, events, relations, point):
        '''
        Includes prepocessings before and after initating Kripke Structure
        '''
        self.events = [None for i in range(len(events))]
        for event in events:
            self.events[event.name] = event
        self.agents = relations.keys()
        self.point = point
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
