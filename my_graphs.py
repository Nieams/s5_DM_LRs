or_graph = [[2, 6, 9], [3, 7], [4, 8], [5], [], [3, 7, 10], [8, 11], [5], [10], [8, 11], [5]]
neor_graph = [[2, 6, 9], [1, 3, 7], [2, 4, 6, 8], [3, 5], [4, 8, 11], [1, 3, 7, 10], [2, 6, 8, 11], [3, 5, 7, 10], [1, 10], [6, 8, 9, 11], [5, 10, 7]]

def correction(graph):
    for i in range(len(graph)):
        graph[i] = [v-1 for v in graph[i]]
    return graph

print('orgrph', correction(or_graph)) 
print('neorgrph', correction(neor_graph))
    
