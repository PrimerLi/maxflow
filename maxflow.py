import os
import random

class Graph:
    def __init__(self, edge_file_name):
        assert(os.path.exists(edge_file_name))
        self.nodes = []
        self.capacity = dict()
        self.source = "s"
        self.sink = "t"
        self.children = dict()
        self.flow = dict()

        reader = open(edge_file_name, "r")
        for (index, string) in enumerate(reader):
            a = string.strip("\n").split(";")
            left, right, weight = a
            if left in self.children:
                self.children[left].append(right)
            else:
                self.children[left] = [right]
            self.capacity[(left, right)] = int(weight)
        reader.close()

        edges = self.capacity.keys()
        for edge in edges:
            self.flow[edge] = 0

    def read_flow_from_file(self, input_file_name):
        self.flow = dict()
        assert(os.path.exists(input_file_name))
        reader = open(input_file_name, "r")
        for (index, string) in enumerate(reader):
            a = string.strip("\n").split(";")
            left, right, flow = a
            self.flow[(left, right)] = int(flow)
        reader.close()

        if False:
            edges = self.capacity.keys()
            for i in range(len(edges)):
                print edges[i], self.capacity[edges[i]], self.flow[edges[i]]

    def get_residual_graph(self):
        assert(len(self.capacity) >= len(self.flow))
        edges = self.capacity.keys()
        self.residual_capacity = dict()
        for edge in edges:
            u, v = edge
            residual_capacity = self.capacity[edge] - self.flow.get(edge, 0)
            if residual_capacity > 0:
                self.residual_capacity[edge] = residual_capacity
            assert((v, u) not in self.capacity)
            if edge in self.flow and self.flow[edge] > 0:
                self.residual_capacity[(v, u)] = self.flow[(u, v)]

        self.residual_graph = dict()
        keys = self.residual_capacity.keys()
        for key in keys:
            left, right = key
            if left in self.residual_graph:
                self.residual_graph[left].append(right)
            else:
                self.residual_graph[left] = [right]

    def print_residual_graph(self):
        if len(self.residual_capacity) > 0:
            print "Residual graph: "
            keys = self.residual_capacity.keys()
            for key in keys:
                print key, self.residual_capacity[key]
        else:
            print "Residual graph is empty. "

    def get_augmenting_paths(self):
        if len(self.residual_capacity) == 0:
            self.get_residual()

        paths = []
        visited = set()
        def get_paths(start, target, path):
            if start == target:
                result = [start] + path
                paths.append(list(reversed(result)))
                return True
            visited.add(start)
            neighbors = self.residual_graph.get(start, [])
            for neighbor in neighbors:
                if neighbor not in visited:
                    if get_paths(neighbor, target, [start] + path):
                        continue
                    else:
                        visited.remove(neighbor)
            return False

        get_paths(self.source, self.sink, [])

        for path in paths:
            print "Augmenting path = ", path, ", path residual capacity = ", self.get_path_residual_capacity(path)

        return paths

    def get_path_residual_capacity(self, path):
        result = float("inf")
        for i in range(len(path) - 1):
            residual_capacity = self.residual_capacity[(path[i], path[i+1])]
            result = min(result, residual_capacity)
        return result

    def augment_with_path(self, path):
        path_residual_capacity = self.get_path_residual_capacity(path)
        for i in range(len(path)-1):
            edge = (path[i], path[i+1])
            if edge in self.flow:
                self.flow[edge] += path_residual_capacity
            else:
                reversed_edge = (edge[1], edge[0])
                assert(reversed_edge in self.flow)
                self.flow[reversed_edge] -= path_residual_capacity
                if self.flow[reversed_edge] == 0:
                    self.flow.pop(reversed_edge)

        if False:
            keys = self.capacity.keys()
            for key in keys:
                print key, self.capacity[key], self.flow.get(key, 0)

def find_max_flow(G):
    update_times = 0
    while True:
        G.get_residual_graph()
        G.print_residual_graph()
        paths = G.get_augmenting_paths()
        if len(paths) == 0:
            print "Final result: "
            edges = sorted(G.flow.keys())
            for edge in edges:
                if G.flow[edge] > 0:
                    print edge, G.flow[edge]
            break
        else:
            print "Number of candidate augmenting paths = " + str(len(paths))
        '''
        max_path_index = None
        max_path_residual_capacity = -float("inf")
        for i in range(len(paths)):
            path_residual_capacity = G.get_path_residual_capacity(paths[i])
            if path_residual_capacity > max_path_residual_capacity:
                max_path_index = i
                max_path_residual_capacity = path_residual_capacity
        print "Augment graph with this path: " + str(paths[max_path_index])
        G.augment_with_path(paths[max_path_index])
        '''
        random_index = random.randint(0, len(paths)-1)
        print "Augmenting graph with this path: " + str(paths[random_index])
        G.augment_with_path(paths[random_index])
        update_times += 1
        print "update times = " + str(update_times)
        print "\n\n"

def main():
    import sys
    G = Graph("graph.csv")
    #G.read_flow_from_file("flow.csv")
    find_max_flow(G)
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
