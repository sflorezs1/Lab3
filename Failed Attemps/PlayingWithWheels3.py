from Graph import Graph, Vertex
import threading


class LockSolver(object):
    def __init__(self, initial: str, forbidden: [str], target: str):
        self.initial = initial
        self.forbidden = forbidden
        self.target = target
        self.graph = Graph()
        self.graph.add_vertex(Vertex(self.initial))

    def make_graph(self):

        def int_to_list(number: int):
            number = [int(i) for i in str(number)]
            diff = 4 - len(number)
            for j in range(diff):
                number.insert(0, 0)
            return number

        def normalize(some_combination: [int]):
            for i in range(len(some_combination)):
                if some_combination[i] < 0:
                    some_combination[i] += 10
                    continue
                elif some_combination[i] > 9:
                    some_combination[i] -= 10
                    continue

        for i in range(10000):
            disc = int_to_list(i)
            print(disc)
            neighbors = [disc for x in range(8)]
            if disc[0] == 9:
                neighbors[0][3] -= 9
            else:
                neighbors[0][3] += 1
            if disc[1] == 9:
                neighbors[1][2] -= 9
            else:
                neighbors[1][2] += 1
            if disc[2] == 9:
                neighbors[2][1] -= 9
            else:
                neighbors[2][1] += 1
            if disc[3] == 9:
                neighbors[3][0] -= 9
            else:
                neighbors[3][0] += 1
            if disc[0] == 0:
                neighbors[4][3] += 9
            else:
                neighbors[4][3] -= 1
            if disc[1] == 0:
                neighbors[5][2] += 9
            else:
                neighbors[5][2] -= 1
            if disc[2] == 0:
                neighbors[6][1] += 9
            else:
                neighbors[6][1] -= 1
            if disc[3] == 0:
                neighbors[7][0] += 9
            else:
                neighbors[7][0] -= 1

            for neighbor in neighbors:
                normalize(neighbor)

            center = Vertex(disc)
            self.graph.add_vertex(center)
            for j in range(8):
                if j not in self.forbidden:
                    existent = self.graph.search_data(neighbors[j])
                    if existent == -1:
                        vert = Vertex(int_to_list(j))
                        self.graph.add_vertex(vert)
                    else:
                        ex_vert = self.graph.V[existent]
                        self.graph.add_edge(ex_vert, center)

    def solve(self):
        t1 = threading.Thread(target=self.make_graph)
        t2 = threading.Thread(target=self.make_graph)
        t3 = threading.Thread(target=self.make_graph)
        t4 = threading.Thread(target=self.make_graph)
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        return self.graph.new_BFS(self.graph.V[(self.graph.search_data(self.initial))],
                                  self.graph.V[self.graph.search_data(self.target)])


if __name__ == '__main__':
    filename: str = input("Filename: ")
    with open(filename) as file:
        lock_solvers = []
        test_cases: int = int(file.readline().strip())
        # print("Test cases: ", test_cases)
        for i in range(test_cases):
            line = file.readline()
            initial: [int] = "".join([i for i in (file.readline() if line == "\n" else line).strip().split(" ")])
            # print("Start: ", initial)
            target: [int] = "".join([i for i in file.readline().strip().split(" ")])
            # print("Target: ", target)
            forbidden_ones = int(file.readline().strip())
            forbidden_list = []
            for j in range(forbidden_ones):
                forbidden: [int] = "".join([i for i in file.readline().strip().split(" ")])
                forbidden_list.append(forbidden)
            # print("Forbidden: ", forbidden_list)
            lock_solver: LockSolver = LockSolver(initial, forbidden_list, target)
            lock_solvers.append(lock_solver)

    for case in lock_solvers:
        print(case.solve())
