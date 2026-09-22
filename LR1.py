def DFS(visited, vertex):
    neor_graph = [[1, 5, 8], [0, 2, 6], [1, 3, 5, 7], [2, 4], [3, 7, 10], [0, 2, 6, 9], [1, 5, 7, 10], [2, 4, 6, 9], [0, 9], [5, 7, 8, 10], [4, 9, 6]]
    for v in neor_graph[vertex]:
        if v not in visited:
            print(f"   Идём вглубь: из точки {vertex + 1} переходим в новую точку {v + 1}")
            visited.append(v)
            DFS(visited, v)
            # Этот лог срабатывает при возврате назад по рекурсии (бэктрекинге)
            print(f"   [Возврат назад]: впереди тупик, откатываемся обратно в точку {vertex + 1}")
    return visited
  
def BFS(v0):
    neor_graph = [[1, 5, 8], [0, 2, 6], [1, 3, 5, 7], [2, 4], [3, 7, 10], [0, 2, 6, 9], [1, 5, 7, 10], [2, 4, 6, 9], [0, 9], [5, 7, 8, 10], [4, 9, 6]]
    visited = [v0]
    queue = [v0]
    step = 1
    
    while len(queue) > 0:
        print(f"   Шаг {step}: Состояние очереди на обработку: {[q + 1 for q in queue]}")
        current = queue.pop(0)
        print(f"   -> Извлекаем из начала очереди точку {current + 1} и проверяем её соседей...")
        
        added_neighbors = []
        for neighbor in neor_graph[current]:
            if neighbor not in visited:
                visited.append(neighbor)
                queue.append(neighbor)
                added_neighbors.append(neighbor + 1)
                
        if added_neighbors:
            print(f"      Обнаружены новые доступные точки: {added_neighbors}. Добавляем их в конец очереди.")
        else:
            print(f"      Все соседи точки {current + 1} уже были посещены ранее.")
        step += 1
        
    return visited

# Исходный список ребер (вес, вершина_1, вершина_2)
graph_edges = [
    (6, 0, 1), (3, 1, 2), (7, 2, 3), (2, 3, 4), (4, 0, 5),
    (5, 5, 2), (2, 1, 6), (2, 2, 7), (4, 5, 6), (5, 6, 7),
    (5, 7, 4), (9, 0, 8), (5, 8, 9), (2, 9, 10), (8, 10, 4),
    (3, 5, 9), (1, 9, 7), (4, 6, 10)
]

num_vertices = 11

def has_path(u, v, mst_adj, visited):
    if u == v:
        return True
    visited.append(u)
    for neighbor in mst_adj[u]:
        if neighbor not in visited:
            if has_path(neighbor, v, mst_adj, visited):
                return True
    return False

def kruskal(edges, n_vertices):
    edges.sort()
    mst_adj = [[] for _ in range(n_vertices)]
    mst_edges = []
    total_weight = 0
    
    for weight, u, v in edges:
        if not has_path(u, v, mst_adj, []):
            mst_adj[u].append(v)
            mst_adj[v].append(u)
            mst_edges.append((u, v, weight))
            total_weight += weight
            
    return mst_edges, total_weight

#ВЫВОД РЕЗУЛЬТАТОВ 

print("=" * 80)
print("             ПОДРОБНЫЙ ПОШАГОВЫЙ ПРОТОКОЛ ОБХОДА И СИНТЕЗА ГРАФА")
print("=" * 80)

# 1. Вывод для DFS
print("1. ХРОНОЛОГИЯ ПОИСКА «В ГЛУБИНУ» (DFS):")
print("   Стартуем из начальной точки 1")
dfs_route = [v + 1 for v in DFS([0], 0)]
# Соединяем вершины стрелочками: '1 -> 2 -> 3...'
dfs_formatted = " -> ".join(map(str, dfs_route))
print(f"\n   [ИТОГОВЫЙ ПОРЯДОК ОБНАРУЖЕНИЯ ТОЧЕК ДЛЯ DFS]:")
print(f"   {dfs_formatted}")
print("-" * 80)

# 2. Вывод для BFS
print("2. ХРОНОЛОГИЯ ПОИСКА «В ШИРИНУ» (BFS):")
print("   Стартуем из начальной точки 1")
bfs_route = [v + 1 for v in BFS(0)]
bfs_formatted = " -> ".join(map(str, bfs_route))
print(f"\n   [ИТОГОВЫЙ ПОРЯДОК ОБНАРУЖЕНИЯ ТОЧЕК ДЛЯ BFS]:")
print(f"   {bfs_formatted}")
print("-" * 80)

# 3. Вывод для Алгоритма Краскала
final_mst, total_w = kruskal(graph_edges, num_vertices)
print("3. Минимальное остовное дерево:")
print("   Выбранные линии связи между точками:")

for u, v, w in final_mst:
    # Делаем красивую строчку с выравниванием, прибавляя 1 к вершинам
    print(f"   • Соединяем точку {u+1:<2} и точку {v+1:<2} (стоимость/вес линии: {w})")

print(f"\n   -> Общая минимальная стоимость всей получившейся сети: {total_w}")
print("=" * 80)
