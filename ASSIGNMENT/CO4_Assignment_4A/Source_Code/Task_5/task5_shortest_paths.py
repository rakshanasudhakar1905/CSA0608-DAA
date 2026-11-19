"""
Task 5: Shortest-Path Algorithms (Dijkstra, Bellman-Ford, Floyd-Warshall)
Course: CSA06 Design and Analysis of Algorithms (CO4 - Assignment 4A)
"""
import heapq

INF = float('inf')

def dijkstra(vertices, edges, source):
    adj = {v: [] for v in vertices}
    for u, v, w in edges:
        adj[u].append((v, w))

    dist = {v: INF for v in vertices}
    pred = {v: None for v in vertices}
    visited = set()
    dist[source] = 0
    pq = [(0, source)]

    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        for v, w in adj[u]:
            if v not in visited and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                pred[v] = u
                heapq.heappush(pq, (dist[v], v))
    return dist, pred


def bellman_ford(vertices, edges, source):
    dist = {v: INF for v in vertices}
    pred = {v: None for v in vertices}
    dist[source] = 0

    for _ in range(len(vertices) - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                pred[v] = u
                updated = True
        if not updated:
            break

    has_negative_cycle = False
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            has_negative_cycle = True
            break

    return dist, pred, has_negative_cycle


def floyd_warshall(vertices, edges):
    n = len(vertices)
    idx = {v: i for i, v in enumerate(vertices)}
    D = [[INF] * n for _ in range(n)]
    for i in range(n):
        D[i][i] = 0
    for u, v, w in edges:
        D[idx[u]][idx[v]] = min(D[idx[u]][idx[v]], w)

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if D[i][k] != INF and D[k][j] != INF:
                    if D[i][k] + D[k][j] < D[i][j]:
                        D[i][j] = D[i][k] + D[k][j]
    return D


if __name__ == "__main__":
    V = ['A', 'B', 'C', 'D', 'E']
    E = [
        ('A', 'B', 4),
        ('A', 'C', 7),
        ('B', 'C', 2),
        ('B', 'D', 6),
        ('C', 'D', 1),
        ('D', 'E', 3),
        ('C', 'E', 8)
    ]

    print("=== 5.1 Dijkstra's Algorithm (Source = A) ===")
    d_dist, d_pred = dijkstra(V, E, 'A')
    for v in V:
        print(f"  A -> {v}: Distance = {d_dist[v]}, Predecessor = {d_pred[v]}")

    print("\n=== 5.2 Bellman-Ford with Negative Edge (B -> C changed to -2) ===")
    E_neg = [
        ('A', 'B', 4),
        ('A', 'C', 7),
        ('B', 'C', -2),
        ('B', 'D', 6),
        ('C', 'D', 1),
        ('D', 'E', 3),
        ('C', 'E', 8)
    ]
    bf_dist, bf_pred, neg_cycle = bellman_ford(V, E_neg, 'A')
    print(f"  Negative Cycle Detected: {neg_cycle}")
    for v in V:
        print(f"  A -> {v}: Distance = {bf_dist[v]}, Predecessor = {bf_pred[v]}")

    print("\n=== 5.3 Floyd-Warshall All-Pairs Shortest Paths ===")
    fw_matrix = floyd_warshall(V, E)
    print("      " + "  ".join(f"{v:>4}" for v in V))
    for i, u in enumerate(V):
        row_str = "  ".join(f"{(val if val != INF else 'INF'):>4}" for val in fw_matrix[i])
        print(f"  {u}:  {row_str}")
