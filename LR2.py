import sys
sys.setrecursionlimit(2000)

def build_matrix(adj_list):
    n = len(adj_list)
    matrix = [[0] * n for _ in range(n)]
    for u in range(n):
        for v in adj_list[u]:
            matrix[u][v] = 1
            matrix[v][u] = 1
    return matrix

def is_connected(matrix):
    n = len(matrix)
    visited = [False] * n
    start_node = -1
    for i in range(n):
        if sum(matrix[i]) > 0:
            start_node = i
            break
    if start_node == -1: return True
    
    stack = [start_node]
    visited[start_node] = True
    count = 0
    while stack:
        u = stack.pop()
        count += 1
        for v in range(n):
            if matrix[u][v] > 0 and not visited[v]:
                visited[v] = True
                stack.append(v)
                
    vertices_with_edges = sum(1 for i in range(n) if sum(matrix[i]) > 0)
    return count == vertices_with_edges

def count_edges(matrix):
    count = 0
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            count += matrix[i][j]
    return count // 2

def fleury(adj_list, graph_name):
    n = len(adj_list)
    matrix = build_matrix(adj_list)
    
    odd_vertices = []
    for i in range(n):
        degree = sum(matrix[i])
        if degree % 2 != 0:
            odd_vertices.append(i)
            
    print(f"\n--- Анализ графа: {graph_name} ---")
    print(f"Вершины с нечетной степенью (0-based): {odd_vertices}")
    
    if len(odd_vertices) == 0:
        task_type = "Эйлеров ЦИКЛ"
        start_node = 0 
        print("Условие: Все вершины четные. Ищем Эйлеров ЦИКЛ.")
    elif len(odd_vertices) == 2:
        task_type = "Эйлеров ПУТЬ"
        start_node = odd_vertices[0]
        print(f"Условие: Две нечетные вершины. Ищем Эйлеров ПУТЬ. Старт: {start_node+1}")
    else:
        print(f"ОШИБКА: Нечетных вершин {len(odd_vertices)}. Эйлеров путь/цикл не существует.")
        return

    if not is_connected(matrix):
        print("ОШИБКА: Граф несвязный.")
        return

    path = []
    curr = start_node
    total_edges = count_edges(matrix)
    
    for _ in range(total_edges):
        path.append(curr)
        neighbors = [v for v in range(n) if matrix[curr][v] > 0]
        
        if not neighbors:
            print("Ошибка: тупик.")
            return
            
        next_node = -1
        
        if len(neighbors) == 1:
            next_node = neighbors[0]
        else:
            for v in neighbors:
                matrix[curr][v] -= 1
                matrix[v][curr] -= 1
                
                if is_connected(matrix):
                    next_node = v
                    matrix[curr][v] += 1
                    matrix[v][curr] += 1
                    break
                else:
                    matrix[curr][v] += 1
                    matrix[v][curr] += 1
            
            if next_node == -1:
                next_node = neighbors[0]

        matrix[curr][next_node] -= 1
        matrix[next_node][curr] -= 1
        curr = next_node

    path.append(curr)
    path_1_based = [x + 1 for x in path]
    print(f"РЕЗУЛЬТАТ ({task_type}): {path_1_based}")

# --- ЗАПУСК ---

# 1. Граф для ЦИКЛА
graph_cycle = [
    [5, 8], [2, 6], [1, 3, 5, 7], [2, 4], [3, 7], 
    [0, 2, 6, 9], [1, 5, 7, 10], [2, 4, 6, 9], [0, 9], 
    [5, 7, 8, 10], [6, 9]
]
fleury(graph_cycle, "Модифицированный (Цикл)")

# 2. Граф для ПУТИ
graph_path = [
    [5, 8], [2, 6], [1, 3, 5, 7], [2, 4], [3, 7, 10], 
    [0, 2, 6, 9], [1, 5, 7, 10], [2, 4, 6, 9], [0, 9], 
    [5, 7, 8, 10], [4, 9, 6]
]
fleury(graph_path, "Модифицированный (Путь)")

# 3. ИСХОДНЫЙ ГРАФ (не Эйлеров)
graph_original = [
    [1, 5, 8], [0, 2, 6], [1, 3, 5, 7], [2, 4], [3, 7, 10], 
    [0, 2, 6, 9], [1, 5, 7, 10], [2, 4, 6, 9], [0, 9], 
    [5, 7, 8, 10], [4, 9, 6]
]
fleury(graph_original, "Исходный (Не Эйлеров)")