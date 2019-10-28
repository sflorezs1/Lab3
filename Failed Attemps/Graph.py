from collections import deque


class Vertex(object):
    def __init__(self, data):
        self.data = data
        self.neighbors = []
        self.is_visited = False

    def add_edge(self, v):
        if v not in self.neighbors:
            self.neighbors.append(v)

    def set_visited(self, val):
        self.is_visited = val

    def __eq__(self, other):
        if not isinstance(other, Vertex):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.data == other.data

    def __str__(self):
        return str(self.data)

    def __hash__(self):
        return hash(str(self.data))


class Graph(object):
    def __init__(self):
        self.n_vertex = 0
        self.n_edges = 0
        self.V = []

    def add_vertex(self, v):
        self.V.append(v)
        self.n_vertex += 1

    def add_edge(self, start, end):
        self.V[self.search(start)].add_edge(self.V[self.search(end)])
        self.V[self.search(end)].add_edge(self.V[self.search(start)])
        self.n_edges += 1

    def get_vertex(self, data) -> Vertex:
        return self.V[self.search(Vertex(data))]

    def new_BFS(self, initial: Vertex, target: Vertex):
        q = deque()
        distance = 0
        q.append(initial)
        distance_delay = 0
        distance_delay2 = 1
        if initial == target:
            return distance
        while len(q) != 0:
            v = q.popleft()
            if distance_delay == 0:
                distance += 1
                distance_delay = distance_delay2
                distance_delay2 = 0
            if v == target:
                return distance - 1
            for x in v.neighbors:
                if not x.is_visited:
                    distance_delay2 = distance_delay2 + 1
                    x.set_visited(True)
                    q.append(x)
            distance_delay = distance_delay - 1
        return -1

    def search(self, some_vertex):
        index = 0
        for i in self.V:
            if i == some_vertex:
                return index
            index += 1
        return -1

    def search_data(self, some_data):
        index = 0
        for i in self.V:
            if i.data == some_data:
                return index
            index += 1
        return -1

    def print_edges(self):
        for v in self.V:
            for e in v.neighbors:
                print(v.data, "->", e.data, end=", ")
            print()

    def unvisit_all(self):
        for n in self.V:
            n.set_visited(False)
