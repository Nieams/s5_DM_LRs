def DFS(visited, vertex):
    neor_graph = [[1, 5, 8], [0, 2, 6], [1, 3, 5, 7], [2, 4], [3, 7, 10], [0, 2, 6, 9], [1, 5, 7, 10], [2, 4, 6, 9], [0, 9], [5, 7, 8, 10], [4, 9, 6]]
    for v in neor_graph[vertex]:
        if v not in visited:
            visited.append(v)
            # visited = DFS(visited, v)
            DFS(visited, v)
    return visited

print(f"Путь, полученный алгоритмом DFS: {[v+1 for v in DFS([0], 0)]}")
  
def BFS(v0):
    neor_graph = [[1, 5, 8], [0, 2, 6], [1, 3, 5, 7], [2, 4], [3, 7, 10], [0, 2, 6, 9], [1, 5, 7, 10], [2, 4, 6, 9], [0, 9], [5, 7, 8, 10], [4, 9, 6]]
    
    visited = [v0]  # Сюда записываем вершины в порядке их посещения
    queue = [v0]    # Наша очередь (обычный список)
    
    # Пока в очереди есть хотя бы одна вершина
    while len(queue) > 0:
        # Извлекаем САМЫЙ ПЕРВЫЙ элемент из списка (индекс 0)
        current = queue.pop(0)
        
        # Проверяем всех соседей текущей вершины
        for neighbor in neor_graph[current]:
            if neighbor not in visited:
                visited.append(neighbor)  # Посещаем соседа
                queue.append(neighbor)    # Добавляем в конец очереди
                
    return visited

# Запуск
print(f'BFS: {[v+1 for v in BFS(0)] }')
            
        
        
    

    
        
    
       
       
            
    