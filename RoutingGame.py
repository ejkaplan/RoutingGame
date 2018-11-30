from random import *
from string import ascii_uppercase


class Router(object):

    def __init__(self, name):
        self.name = name
        self.connections = {}

    def connect(self, other):
        # w = randint(1,10)
        w = sorted((round(gauss(5, 2)), 10, 1))[1]  # Clamp to range [1,10]
        self.connections[other] = w
        other.connections[self] = w

    def disconnect(self, other):
        if other in self.connections:
            self.connections.pop(other)
            other.connections.pop(self)

    def __str__(self):
        conn = sorted(list(self.connections.keys()), key = lambda x:x.name)
        return f"{self.name}: " + ", ".join([f"{r.name}={self.connections[r]}" for r in conn])


def make_cut(routers):
    for _ in range(pow(len(routers),2)):
        opts = [r for r in routers if len(r.connections) == 3]
        if len(opts) == 0: return False
        c0 = choice(opts)
        opts = [r for r in c0.connections if len(r.connections) == 3]
        if len(opts) == 0: continue
        c1 = choice(opts)
        if is_connected(routers, (c0,c1)):
            c0.disconnect(c1)
            print(f"The connection between {c0.name} and {c1.name} has been cut.")
            return True
    return False


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


def randomize_routers(n, rand_seed):
    seed(rand_seed)
    while True:
        routers = []
        bad = False
        for i in range(n):
            routers.append(Router(ascii_uppercase[i]))
        for r in routers:
            available = [x for x in routers if x is not r and x not in r.connections and len(x.connections) < 3]
            if len(available) < 2-len(r.connections):
                bad = True
                break
            shuffle(available)
            available.sort(key=lambda x: len(x.connections))
            while len(r.connections) < 3 and len(available) > 0:
                r.connect(available.pop())
        if not bad and is_connected(routers):
            return routers

def shortest_path(routers, source, target):
    q = set(routers)
    dist = {r: float('inf') for r in routers}
    dist[source] = 0
    prev = {source: None}
    dist[source] = 0
    while len(q) > 0:
        u = min(q, key=lambda x: dist[x])
        if u is target:
            s = []
            while u is not None:
                s.insert(0,u)
                u = prev[u]
            return s
        q.remove(u)
        for v in u.connections:
            alt = dist[u] + u.connections[v]
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u


def print_path(s):
    out = s[0].name
    path_length = 0
    for i in range(1,len(s)):
        out += f" --{s[i-1].connections[s[i]]}--> {s[i].name}"
        path_length += s[i-1].connections[s[i]]
    out += f" ({path_length})"
    print(out)


def make_file(n, rand_seed):
    routers = randomize_routers(n, rand_seed)
    with open(f"{n}_routers.txt","w") as f:
        for r in routers:
            f.write(f"You are router {r.name}.\n")
            for neighbor in sorted(r.connections.keys(), key=lambda x: x.name):
                f.write(f"You are connected to router {neighbor.name} with path weight {r.connections[neighbor]}.\n")
            f.write("\n\n\n")


def routing_tables(routers):
    tables = {}
    for r in routers:
        tables[r] = {x:(None, float('inf')) for x in routers}
        tables[r][r] = (None, 0)
        for n in r.connections:
            tables[r][n] = (n, r.connections[n])
    changed = True
    while changed:
        changed = False
        for r in routers:
            for n in r.connections:
                wt = r.connections[n]
                for dest in tables[n]:
                    poss_wt = wt + tables[n][dest][1]
                    if poss_wt < tables[r][dest][1]:
                        tables[r][dest] = (n, poss_wt)
                        changed = True
    return tables


def display_table(tables, r):
    table = tables[r]
    out = f"{r.name}'s Routing Table:\n"
    for x in routers:
        if r == x: continue
        out += f"   Packets for {x.name} should be forwarded to {table[x][0].name}, path weight = {table[x][1]}\n"
    print(out)

if __name__ == "__main__":
    rand_seed = 1
    # rand_seed = 2
    # for n in range(15,21):
    n = 15
    make_file(n, rand_seed)
    routers = randomize_routers(n, rand_seed)
    tables = routing_tables(routers)
    display_table(tables, routers[5])
    # for i in range(len(routers)):
    #     print(f"{i:2}) {routers[i]}")
    # print("---")
    print_path(shortest_path(routers, routers[13], routers[1]))
    print(routing_tables(routers))

