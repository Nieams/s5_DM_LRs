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
print(f'BFS: {[v+1 for v in BFS(0)]}')

# Исходный список ребер вашего графа в формате: (вес, вершина_1, вершина_2)
# Всего 18 рёбер
graph_edges = [
    (6, 0, 1), (3, 1, 2), (7, 2, 3), (2, 3, 4), (4, 0, 5),
    (5, 5, 2), (2, 1, 6), (2, 2, 7), (4, 5, 6), (5, 6, 7),
    (5, 7, 4), (9, 0, 8), (5, 8, 9), (2, 9, 10), (8, 10, 4),
    (3, 5, 9), (1, 9, 7), (4, 6, 10)
]

num_vertices = 11  # Вершины от 0 до 10

def has_path(u, v, mst_adj, visited):
    """Обычный DFS. Проверяет, есть ли уже путь между u и v в строящемся дереве"""
    if u == v:
        return True
    visited.append(u)
    for neighbor in mst_adj[u]:
        if neighbor not in visited:
            if has_path(neighbor, v, mst_adj, visited):
                return True
    return False

def kruskal(edges, n_vertices):
    # 1. Сортируем все рёбра графа по возрастанию веса
    edges.sort()
    
    # Создаем пустой список смежности для будущего минимального остова (дерева)
    mst_adj = [[] for _ in range(n_vertices)]
    
    mst_edges = []     # Здесь сохраним рёбра, вошедшие в ответ
    total_weight = 0   # Суммарный вес минимального остова
    
    # 2. Перебираем отсортированные рёбра
    for weight, u, v in edges:
        # С помощью DFS проверяем: связаны ли уже вершины u и v?
        if not has_path(u, v, mst_adj, []):
            # Если пути между ними нет — ребро НЕ создаст цикл. Добавляем его!
            mst_adj[u].append(v)
            mst_adj[v].append(u)
            mst_edges.append((u, v, weight))
            total_weight += weight
            
    return mst_edges, total_weight

# Запуск алгоритма
final_mst, total_w = kruskal(graph_edges, num_vertices)

# Вывод результатов
print("Рёбра, вошедшие в минимальное остовное дерево (МСТ):")
for u, v, w in final_mst:
    print(f"Ребро {u} - {v} с весом {w}")

print(f"\nМинимальный суммарный вес дерева: {total_w}")

            
        
        
    

    
        
    
       
       
            
    