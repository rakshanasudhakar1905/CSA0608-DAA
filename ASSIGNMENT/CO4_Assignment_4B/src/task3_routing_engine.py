"""
Task 3: Routing Engine Under Changing Network Conditions
Algorithms: Dijkstra, Bellman-Ford, Floyd-Warshall
Course: CSA06 Design and Analysis of Algorithms - CO4 Assignment 4B
"""

import heapq
from typing import Dict, List, Tuple, Optional, Any

INF = float('inf')

class LogisticsNetwork:
    def __init__(self, vertices: List[str]):
        self.vertices = vertices
        self.edges: List[Tuple[str, str, int]] = []

    def add_edge(self, u: str, v: str, w: int):
        self.edges.append((u, v, w))

    def copy(self) -> 'LogisticsNetwork':
        net = LogisticsNetwork(list(self.vertices))
        net.edges = list(self.edges)
        return net

def reconstruct_path(pred: Dict[str, Optional[str]], target: str) -> List[str]:
    path, curr, seen = [], target, set()
    while curr is not None:
        if curr in seen:
            return ["CYCLE_DETECTED"]
        seen.add(curr)
        path.append(curr)
        curr = pred[curr]
    path.reverse()
    return path

def run_dijkstra(net: LogisticsNetwork, source: str) -> Dict[str, Any]:
    adj = {v: [] for v in net.vertices}
    for u, v, w in net.edges:
        adj[u].append((v, w))
    dist = {v: INF for v in net.vertices}
    pred = {v: None for v in net.vertices}
    dist[source] = 0
    pq, finalised_order, visited = [(0, source)], [], set()

    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        finalised_order.append((u, d))
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                pred[v] = u
                heapq.heappush(pq, (dist[v], v))

    paths = {v: reconstruct_path(pred, v) if dist[v] < INF else [] for v in net.vertices}
    return {"dist": dist, "pred": pred, "finalised_order": finalised_order, "paths": paths}

def run_bellman_ford(net: LogisticsNetwork, source: str) -> Dict[str, Any]:
    dist = {v: INF for v in net.vertices}
    pred = {v: None for v in net.vertices}
    dist[source] = 0
    V = len(net.vertices)

    for _ in range(V - 1):
        updated = False
        for u, v, w in net.edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                pred[v] = u
                updated = True
        if not updated:
            break

    neg_cycle_edges = [(u, v, w) for u, v, w in net.edges if dist[u] != INF and dist[u] + w < dist[v]]
    if neg_cycle_edges:
        return {
            "has_negative_cycle": True,
            "message": f"CRITICAL ALERT: Reachable negative-weight cycle detected via edge(s) {neg_cycle_edges}!"
        }
    paths = {v: reconstruct_path(pred, v) if dist[v] < INF else [] for v in net.vertices}
    return {"has_negative_cycle": False, "dist": dist, "pred": pred, "paths": paths}

def run_floyd_warshall(net: LogisticsNetwork) -> Tuple[List[List[float]], List[List[int]]]:
    n = len(net.vertices)
    idx = {v: i for i, v in enumerate(net.vertices)}
    dist = [[INF] * n for _ in range(n)]
    reach = [[0] * n for _ in range(n)]
    for i in range(n):
        dist[i][i], reach[i][i] = 0, 1
    for u, v, w in net.edges:
        i, j = idx[u], idx[v]
        dist[i][j] = min(dist[i][j], w)
        reach[i][j] = 1
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] != INF and dist[k][j] != INF and dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                if reach[i][k] and reach[k][j]:
                    reach[i][j] = 1
    return dist, reach

if __name__ == "__main__":
    nodes = ["HUB", "N1", "N2", "N3", "N4", "N5", "N6", "DEST"]
    net_a = LogisticsNetwork(nodes)
    edges_a = [
        ("HUB", "N1", 4), ("HUB", "N2", 10), ("N1", "N2", 3), ("N1", "N3", 8),
        ("N2", "N3", 2), ("N2", "N4", 9), ("N3", "N4", 4), ("N3", "N5", 6),
        ("N4", "N5", 1), ("N4", "N6", 7), ("N5", "N6", 3), ("N5", "DEST", 8), ("N6", "DEST", 2)
    ]
    for u, v, w in edges_a:
        net_a.add_edge(u, v, w)

    print("=== STAGE A: NORMAL ROUTING (DIJKSTRA FROM 'HUB') ===")
    res_dijk_a = run_dijkstra(net_a, "HUB")
    print("Finalisation Order:", res_dijk_a["finalised_order"])
    for v in nodes:
        print(f"  {v:<5} | Dist: {res_dijk_a['dist'][v]:<4} | Pred: {str(res_dijk_a['pred'][v]):<5} | Path: {' -> '.join(res_dijk_a['paths'][v])}")

    print("\n=== STAGE B: NEGATIVE EDGE INTRODUCED (N3 -> N2 = -5) ===")
    net_b = net_a.copy()
    net_b.edges = [e for e in net_b.edges if not (e[0] in ("HUB", "N1", "N2") and e[1] in ("N1", "N2", "N3"))]
    net_b.add_edge("HUB", "N2", 5)
    net_b.add_edge("HUB", "N1", 3)
    net_b.add_edge("N1", "N3", 4)
    net_b.add_edge("N3", "N2", -5)
    net_b.add_edge("N2", "N4", 3)

    dijk_b = run_dijkstra(net_b, "HUB")
    bf_b = run_bellman_ford(net_b, "HUB")
    for v in nodes:
        d_val, b_val = dijk_b["dist"][v], bf_b["dist"][v]
        flag = " <-- DIJKSTRA SUBOPTIMAL!" if d_val != b_val else ""
        print(f"  {v:<5} | Dijkstra: {d_val:<4} ({'->'.join(dijk_b['paths'][v])}) | Bellman-Ford: {b_val:<4} ({'->'.join(bf_b['paths'][v])}){flag}")

    print("\n=== STAGE C: PRODUCTION FAILURE (REACHABLE NEGATIVE-WEIGHT CYCLE) ===")
    net_c = net_b.copy()
    net_c.add_edge("N2", "N1", -1)
    print(run_bellman_ford(net_c, "HUB")["message"])

    print("\n=== STAGE D: FLOYD DISTANCE MATRIX & WARSHALL REACHABILITY MATRIX ===")
    dist_mat, reach_mat = run_floyd_warshall(net_a)
    header = "      " + " ".join(f"{v:>5}" for v in nodes)
    print("[Floyd's All-Pairs Shortest Path Matrix]")
    print(header)
    for i, u in enumerate(nodes):
        print(f"{u:<5} " + " ".join(f"{'INF':>5}" if dist_mat[i][j] == INF else f"{int(dist_mat[i][j]):>5}" for j in range(len(nodes))))
    print("[Warshall's Reachability Matrix]")
    print(header)
    for i, u in enumerate(nodes):
        print(f"{u:<5} " + " ".join(f"{reach_mat[i][j]:>5}" for j in range(len(nodes))))
