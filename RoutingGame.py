from random import *

class Router(object):

    def __init__(self, name):
        self.name = name
        self.connections = {}

    def connect(self, other):
        # w = randint(1,10)
        w = sorted((round(gauss(5,2)),10,1))[1]  #Clamp to range [1,10]
        self.connections[other] = w
        other.connections[self] = w

    def disconnect(self, other):
        if other in self.connections:
            self.connections.pop(other)
            other.connections.pop(self)

    def __str__(self):
        return f"{self.name}: " + ", ".join([f"{r.name}={self.connections[r]}" for r in self.connections])

def make_cut(routers):
    while True:
        c0 = choice(routers)
        c1 = choice(list(c0.connections.keys()))
        if is_connected(routers, (c0,c1)):
            c0.disconnect(c1)
            print(f"The connection between {c0.name} and {c1.name} has been cut.")
            return

def is_connected(routers, cut=None):
    visited = set()
    frontier = [routers[0]]
    while len(frontier) > 0:
        curr = frontier.pop()
        if curr in visited: continue
        visited.add(curr)
        for r in curr.connections:
            if cut is not None and r in cut and curr in cut:
                continue
            frontier.append(r)
    return len(visited) == len(routers)

def randomize_routers():
    while True:
        routers = []
        bad = False
        for i in range(8):
            routers.append(Router("ABCDEFGH"[i]))
        for r in routers:
            available = [x for x in routers if x is not r and len(x.connections) < 3]
            if len(available) < 3-len(r.connections):
                bad = True
                break
            shuffle(available)
            while len(r.connections) < 3:
                r.connect(available.pop())
        if not bad and is_connected(routers):
            return routers

seed(2)
routers = randomize_routers()
for r in routers:
    print(r)
print("---")
make_cut(routers)
make_cut(routers)
for r in routers:
    print(r)