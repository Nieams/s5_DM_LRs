
from collections import deque

INF = float("inf")
N = 11

# Исходный граф: (откуда, куда, вес)
edges = [
    (1, 2, 6),
    (1, 6, 4),
    (1, 9, 9),
    (2, 3, 3),
    (2, 7, 2),
    (3, 4, 7),
    (3, 8, 2),
    (4, 5, 2),
    (6, 3, 5),
    (6, 7, 4),
    (6, 10, 3),
    (7, 8, 5),
    (7, 11, 4),
    (8, 5, 5),
    (9, 10, 5),
    (10, 8, 1),
    (10, 11, 2),
    (11, 5, 8),
]

# Меняем знаки весов дуг у источника и стока
modified_edges = [
    (u, v, -w if u == 1 or v == 5 else w)
    for u, v, w in edges
]


def bellman_ford(edges, start):
    dist = [INF] * (N + 1)
    prev = [None] * (N + 1)
    dist[start] = 0

    for _ in range(N - 1):
        new_dist = dist.copy()
        new_prev = prev.copy()

        for u, v, w in edges:
            if dist[u] + w < new_dist[v]:
                new_dist[v] = dist[u] + w
                new_prev[v] = u

        if new_dist == dist:
            break

        dist, prev = new_dist, new_prev

    return dist, prev


def wave_algorithm(edges, start):
    dist = [INF] * (N + 1)
    prev = [None] * (N + 1)
    dist[start] = 0

    queue = deque([start])
    in_queue = {start}

    while queue:
        u = queue.popleft()
        in_queue.remove(u)

        for a, v, w in edges:
            if a == u and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u

                if v not in in_queue:
                    queue.append(v)
                    in_queue.add(v)

    return dist, prev


def dijkstra(edges, start):
    dist = [INF] * (N + 1)
    prev = [None] * (N + 1)
    visited = set()
    dist[start] = 0

    for _ in range(N):
        u = None

        # Выбираем непосещённую вершину
        # с минимальным расстоянием
        for v in range(1, N + 1):
            if v not in visited:
                if u is None or dist[v] < dist[u]:
                    u = v

        if u is None or dist[u] == INF:
            break

        visited.add(u)

        for a, v, w in edges:
            if a == u and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u

    return dist, prev


def get_path(prev, start, finish):
    path = []
    v = finish

    while v is not None:
        path.append(v)

        if v == start:
            return path[::-1]

        v = prev[v]

    return []


def print_result(name, dist, prev, start, finish):
    path = get_path(prev, start, finish)

    print(f"\n{name}")

    if not path:
        print("Путь не существует")
        return

    print("Путь:", " -> ".join(map(str, path)))
    print("Вес:", dist[finish])


# Запуск алгоритмов
start, finish = 1, 5

dist, prev = bellman_ford(edges, start)
print_result("Форд — Беллман (исходный)",
             dist, prev, start, finish)

dist, prev = wave_algorithm(edges, start)
print_result("Волновой алгоритм", dist, prev, start, finish)

dist, prev = dijkstra(edges, start)
print_result("Дейкстра", dist, prev, start, finish)

dist, prev = bellman_ford(modified_edges, start)

print_result("Форд — Беллман (модифицированный)",
             dist, prev, start, finish)

print("\nКратчайшие пути до всех вершин:")
for v in range(1, N + 1):
    path = get_path(prev, start, v)
    print(f"{v}: {path}, вес = {dist[v]}")
