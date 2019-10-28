from Graph import *
import graphviz as gv
import os

os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'


class LockSolver(object):

    def __init__(self, initial: [int], forbidden: [[int]], target: [int]):
        self.graph = Graph()
        self.digraph = gv.Digraph(comment="Yolo")
        self.initial: [int] = initial
        self.graph.add_vertex(Vertex(self.initial))
        self.forbidden: [[int]] = forbidden
        self.target: [int] = target
        self.difference: [int] = []

    def solve(self):
        if self.make_graph() is None:
            try:
                initial = self.graph.V[self.graph.search_data(self.initial)]
                target = self.graph.V[self.graph.search_data(self.target)]
            except IndexError:
                return
            self.graph.unvisit_all()
            dist_dict = self.graph.new_BFS(initial, target)
            return dist_dict
        else:
            return -1

    def make_graph(self):
        if self.solvable() == -1 or self.target in self.forbidden:
            return False
        if self.initial == self.target:
            return
        current_vertex: Vertex = self.graph.get_vertex(self.initial)
        while self.graph.search_data(self.target) == -1:
            minor_difference: ([int], [int], Vertex) = ([9, 9, 9, 9], [-1, -1, -1, -1], current_vertex)
            self.generate_adjacent(current_vertex)
            for vertex in current_vertex.neighbors:
                if not vertex.is_visited:
                    forbidden_difference = [[0, 0, 0, 0]]
                    for i in self.near_forbidden(vertex):
                        forbidden_difference.append([abs(i[j] - vertex.data[j]) for j in range(4)])
                    difference = [abs(self.target[i] - vertex.data[i]) for i in range(4)]  # Calculate diff to target
                    max_forbidden_dif = [0, 0, 0, 0]
                    for forbidden in forbidden_difference:
                        for i in range(4):
                            max_forbidden_dif[i] += forbidden[i]
                    max_forbidden_dif = [i / len(forbidden_difference) for i in max_forbidden_dif]
                    if abs(sum(difference) - sum(max_forbidden_dif)) <\
                            abs(sum(minor_difference[0]) - sum(minor_difference[1])):
                        minor_difference = (difference, max_forbidden_dif, vertex)
                    vertex.is_visited = True
            if current_vertex == minor_difference[2]:
                return False
            current_vertex = minor_difference[2]

    def near_forbidden(self, data):
        forbidden: [int] = []
        for combination in self.forbidden:
            for i in range(4):
                tolerance_range = 8
                for tolerance in range(1, tolerance_range):
                    copy_pos: [int] = combination.copy()
                    copy_neg: [int] = combination.copy()
                    copy_pos[i] = combination[i] - tolerance
                    normalize(copy_pos)
                    copy_neg[i] = combination[i] + tolerance
                    normalize(copy_neg)
                    if data == copy_neg or copy_pos == data:
                        forbidden.append(combination)
        return forbidden

    def solvable(self) -> int:
        solvable = []
        for i in range(len(self.initial)):
            copy = self.initial.copy()
            copy[i] += 1
            normalize(copy)
            if copy in self.forbidden:
                solvable.append(False)
            copy[i] -= 2
            normalize(copy)
            if copy in self.forbidden:
                solvable.append(False)
        if len(solvable) == 8:
            return False
        else:
            return True

    def solve_analytically(self, times: int = 0) -> int:
        if self.solvable() == -1:
            return -1
        if self.target == self.initial:
            return 0
        if self.target in self.forbidden:
            return -1
        while self.initial != self.target:
            self.difference = [self.target[i] - self.initial[i] for i in range(4)]
            consider = []
            for i in range(4):
                self.difference = [self.target[i] - self.initial[i] for i in range(4)]
                some = self.initial.copy()
                if self.difference[i] != 0:
                    if (self.difference[i] < 0 or self.difference[i] >= 5) and self.difference[i] > -5:
                        some[i] -= 1
                        normalize(some)
                        if some in self.forbidden:
                            some[i] += 2
                            normalize(some)
                            if some in self.forbidden:
                                continue
                            else:
                                consider.append(some)
                        else:
                            consider.append(some)
                    elif 0 <= self.difference[i] < 5 or self.difference[i] <= -5:
                        some[i] += 1
                        normalize(some)
                        if some in self.forbidden:
                            some[i] -= 2
                            normalize(some)
                            if some in self.forbidden:
                                continue
                            else:
                                consider.append(some)
                        else:
                            consider.append(some)
            far = (consider[0], -1)
            for combination in consider:
                for j in self.near_forbidden(combination):
                    num = sum([abs(combination[i] - j[i]) for i in range(4)])
                    if num >= far[1]:
                        far = (combination, num)
            self. initial = far[0]
            times += 1
        self.graph.unvisit_all()
        return times

    def generate_adjacent(self, vertex: Vertex):
        for k in range(4):
            positive: [int] = vertex.data.copy()
            negative: [int] = vertex.data.copy()
            positive[k] += 1
            negative[k] -= 1
            normalize(positive)
            normalize(negative)
            if positive not in self.forbidden and self.graph.search_data(positive) == -1:
                new_one_pos: Vertex = Vertex(positive.copy())
                self.graph.add_vertex(new_one_pos)
                self.graph.add_edge(vertex, new_one_pos)
            if negative not in self.forbidden and self.graph.search_data(negative) == -1:
                new_one_neg: Vertex = Vertex(negative.copy())
                self.graph.add_vertex(new_one_neg)
                self.graph.add_edge(vertex, new_one_neg)


def normalize(some_combination: [int]):
    for i in range(len(some_combination)):
        if some_combination[i] < 0:
            some_combination[i] += 10
            continue
        elif some_combination[i] > 9:
            some_combination[i] -= 10
            continue


def main():
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
        format(case.initial, case.target, case.forbidden)
        print(case.solve_analytically())


def format(initial, target, forbidden):
    print(format_list(initial))
    print(format_list(target))
    print(len(forbidden))
    for thing in forbidden:
        print(format_list(thing))
    print()


def format_list(some_list):
    s = ""
    for i in range(len(some_list)):
        s += str(some_list[i]) + (" " if i <= len(some_list) else "")
    return s


if __name__ == '__main__':
    main()
