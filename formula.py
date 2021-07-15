"""
defining classes of formulas in Propositional Modal Logic

semantic : returns valuations in the worlds (given as argument) to be tested on
"""
from utils import *

class Atom:
    """
    atomic Propositional variables
    """

    def __init__(self, name):
        self.name = name

    def semantic(self, ks, world):
        """
        returns valuation of variable in world
        """
        return world.assignment.get(self.name, False)   # If a variable assignment doesn't exist then it is False

    def __str__(self):
        return str(self.name)


class Box_a:
    """
    Box operator of Modal Logic wrt agent a
    """

    def __init__(self, agent, inner):
        self.agent = agent
        self.inner = inner

    def semantic(self, ks, ThisWorld):
        valuation = True
        relation_a = ks.relations.get(self.agent,{})  #takes care of whether relation_a is empty
        try:
            worlds = relation_a[ThisWorld.name]
        except IndexError:
            return valuation                        #if no world exists then Box will be vacously True
        for world_name in worlds:
            valuation = valuation and self.inner.semantic(ks, ks.worlds[world_name])
        return valuation

    def __eq__(self, other):
        return isinstance(other, Box_a) and self.inner == other.inner and self.agent == other.agent

    def __str__(self):
        if isinstance(self.inner, Atom):
            return u"\u2610" + get_sub(str(self.agent)) + " " + str(self.inner)
        else:
            return u"\u2610" + get_sub(str(self.agent)) + "(" + str(self.inner) + ")"


class Box:
    """
    Box operator of Modal Logic wrt all agents     ----(TODO)-----
    """

    def _init__(self, inner):
        self.inner = inner

    def semantic(self, ks, ThisWorld):
        valuation = True
        for agents in ks.relations:
            for worlds in agents[ThisWorld.name]:
                valuation = valuation and self.inner.semantic(ks, worlds)
            return valuation


class Diamond_a:
    """
    Diamond operator of Modal Logic wrt Agent a
    """

    def __init__(self, agent, inner):
        self.agent = agent
        self.inner = inner

    def semantic(self, ks, ThisWorld):
        valuation = False
        relation_a = ks.relations.get(self.agent,{})  #takes care of whether relation_a is empty
        try:
            worlds = relation_a[ThisWorld.name]
        except IndexError:
            return valuation                        #if no world exists then due to no witness Diamond will be False
        for world_name in worlds:
            valuation = valuation or self.inner.semantic(ks, ks.worlds[world_name])
        return valuation

    def __eq__(self, other):
        return isinstance(other, Diamond_a) and self.inner == other.inner and self.agent == other.agent

    def __str__(self):
        if isinstance(self.inner, Atom):
            return u"\u25C7" + get_sub(str(self.agent)) + " " + str(self.inner)
        else:
            return u"\u25C7" + get_sub(str(self.agent)) + "(" + str(self.inner) + ")"


class Diamond:
    """
    Diamond operator of Modal Logic wrt all agents  ---(TODO)---
    """

    def _init__(self, inner):
        self.inner = inner

    def semantic(self, ks, ThisWorld):
        valuation = False
        for agents in ks.relations:
            for worlds in agents[ThisWorld.name]:
                valuation = valuation or self.inner.semantic(ks, worlds)
            return valuation


class Implies:
    """
    Implication derived from classic propositional logic
    """

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def semantic(self, ks, ThisWorld):
        return not self.left.semantic(ks, ThisWorld) or self.right.semantic(ks, ThisWorld)

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right

    def __str__(self):
        return "(" + self.left.__str__() + " -> " + self.right.__str__() + ")"


class Not:
    """
    Negation derived from classic propositional logic
    """

    def __init__(self, inner):
        self.inner = inner

    def semantic(self, ks, ThisWorld):
        return not self.inner.semantic(ks, ThisWorld)

    def __eq__(self, other):
        return self.inner == other.inner

    def __str__(self):
        return u"\uFFE2" + str(self.inner)


class And:
    """
    And derived from classic propositional logic
    """

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def semantic(self, ks, ThisWorld):
        return self.left.semantic(ks, ThisWorld) and self.right.semantic(ks, ThisWorld)

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right

    def __str__(self):
        return "(" + self.left.__str__() + " " + u"\u2227" + " " + self.right.__str__() + ")"


class Or:
    """
    Or derived from classic propositional logic
    """

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def semantic(self, ks, ThisWorld):
        return self.left.semantic(ks, ThisWorld) or self.right.semantic(ks, ThisWorld)

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right

    def __str__(self):
        return "(" + self.left.__str__() + " " + u"\u2228" + " " + self.right.__str__() + ")"
