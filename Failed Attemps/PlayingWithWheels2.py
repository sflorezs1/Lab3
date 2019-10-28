from collections import deque

from Graph import Graph, Vertex


class LockSolver(object):
    def __init__(self, start: [int], banned: [[int]], end: [int]):
        self.initial = start
        self.forbidden = banned
        self.target = end
        self.graph = Graph()
        self.graph.add_vertex(Vertex(self.initial))

    def make_graph(self):
        def normalize(some_combination: [int]):
            for i in range(len(some_combination)):
                if some_combination[i] < 0:
                    some_combination[i] += 10
                    continue
                elif some_combination[i] > 9:
                    some_combination[i] -= 10
                    continue

        def solvable():
            if self.target == self.initial:
                return True
            if self.target in self.forbidden:
                return False
            return True

        def make_helper():
            if solvable():
                queue = deque()
                queue.append(self.graph.V[0])
                while self.graph.search_data(self.target) == -1:
                    if self.graph.n_vertex >= 9**4:
                        break
                    vertex: Vertex = queue.popleft()
                    for index in range(4):  # Generate all adjacent, and add the closest to the target to the queue
                        neg: [int] = vertex.data.copy()
                        pos: [int] = vertex.data.copy()
                        neg[index] -= 1
                        normalize(neg)
                        pos[index] += 1
                        normalize(pos)
                        to_add: [[int]] = [neg, pos]
                        for neighbor in to_add:
                            if neighbor not in self.forbidden:
                                existent = self.graph.search_data(neighbor)
                                if existent == -1:
                                    addition_ver = Vertex(neighbor.copy())
                                    self.graph.add_vertex(addition_ver)
                                    self.graph.add_edge(vertex, addition_ver)
                                    if self.graph.search_data(self.target) != -1:
                                        return
                                    queue.append(addition_ver)
                                else:
                                    existent = self.graph.V[existent]
                                    self.graph.add_edge(vertex, existent)
        make_helper()


if __name__ == '__main__':
    filename: str = input("Filename: ")
    with open(filename) as file:
        lock_solvers = []
        test_cases: int = int(file.readline().strip())
        # print("Test cases: ", test_cases)
        for i in range(test_cases):
            line = file.readline()
            initial: [int] = [int(i) for i in (file.readline() if line == "\n" else line).strip().split(" ")]
            # print("Start: ", initial)
            target: [int] = [int(i) for i in file.readline().strip().split(" ")]
            # print("Target: ", target)
            forbidden_ones = int(file.readline().strip())
            forbidden_list = []
            for j in range(forbidden_ones):
                forbidden: [int] = [int(i) for i in file.readline().strip().split(" ")]
                forbidden_list.append(forbidden)
            # print("Forbidden: ", forbidden_list)
            lock_solver: LockSolver = LockSolver(initial, forbidden_list, target)
            lock_solvers.append(lock_solver)

    for case in lock_solvers:
        case.make_graph()
        initial = case.graph.V[case.graph.search_data(case.initial)]
        target = case.graph.V[case.graph.search_data(case.target)]
        print(case.graph.new_BFS(initial, target))
