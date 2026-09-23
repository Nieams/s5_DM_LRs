def DFS(visited, vertex):
    neor_graph = [[1, 5, 8], [0, 2, 6], [1, 3, 5, 7], [2, 4], [3, 7, 10], [0, 2, 6, 9], [1, 5, 7, 10], [2, 4, 6, 9], [0, 9], [5, 7, 8, 10], [4, 9, 6]]
    for v in neor_graph[vertex]:
        if v not in visited:
            visited.append(v)
            # visited = DFS(visited, v)
            DFS(visited, v)
    return visited


print(f"Путь, полученный алгоритмом BFS: {[v+1 for v in DFS([0], 0)]}")        
            
    