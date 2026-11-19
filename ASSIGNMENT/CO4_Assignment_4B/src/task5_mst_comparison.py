"""
Task 5: Three Greedy Engineers, One Network (Kruskal + Prim + Boruvka MST)
Course: CSA06 Design and Analysis of Algorithms - CO4 Assignment 4B
"""

import heapq
from typing import List, Tuple, Dict, Any

Edge = Tuple[str, str, int]

class DisjointSet:
    def __init__(self, vertices: List[str]):
        self.parent = {v: v for v in vertices}
        self.rank = {v: 0 for v in vertices}

    def find(self, v: str) -> str:
        if self.parent[v] != v:
            self.parent[v] = self.find(self.parent[v])
        return self.parent[v]

    def union(self, u: str, v: str) -> bool:
        ru, rv = self.find(u), self.find(v)
        if ru == rv:
            return False
        if self.rank[ru] < self.rank[rv]:
            self.parent[ru] = rv
        elif self.rank[ru] > self.rank[rv]:
            self.parent[rv] = ru
        else:
            self.parent[rv] = ru
            self.rank[ru] += 1
        return True

def mst_kruskal(vertices: List[str], edges: List[Edge]) -> Dict[str, Any]:
    sorted_edges = sorted(edges, key=lambda e: (e[2], e[0], e[1]))
    dsu, mst, trace, total_cost = DisjointSet(vertices), [], [], 0
    for u, v, w in sorted_edges:
        if dsu.union(u, v):
            mst.append((u, v, w))
            total_cost += w
            trace.append(f"ACCEPT ({u}-{v}, w={w}): Merges components.")
        else:
            trace.append(f"REJECT ({u}-{v}, w={w}): Forms cycle.")
        if len(mst) == len(vertices) - 1:
            break
    return {"algorithm": "Kruskal's", "mst": mst, "cost": total_cost, "trace": trace}

def mst_prim(vertices: List[str], edges: List[Edge], start: str) -> Dict[str, Any]:
    adj = {v: [] for v in vertices}
    for u, v, w in edges:
        adj[u].append((w, v, u))
        adj[v].append((w, u, v))
    visited, pq, mst, trace, total_cost = {start}, list(adj[start]), [], [f"INIT: Root '{start}'"], 0
    heapq.heapify(pq)
    while pq and len(mst) < len(vertices) - 1:
        w, to_v, from_u = heapq.heappop(pq)
        if to_v in visited:
            continue
        visited.add(to_v)
        mst.append((from_u, to_v, w))
        total_cost += w
        trace.append(f"ADD ({from_u}-{to_v}, w={w}): Minimum cut edge to '{to_v}'.")
        for nw, nbr, src in adj[to_v]:
            if nbr not in visited:
                heapq.heappush(pq, (nw, nbr, src))
    return {"algorithm": "Prim's", "mst": mst, "cost": total_cost, "trace": trace}

def mst_boruvka(vertices: List[str], edges: List[Edge]) -> Dict[str, Any]:
    dsu, comps, mst, trace, total_cost, rnd = DisjointSet(vertices), len(vertices), [], [], 0, 1
    while comps > 1:
        cheapest: Dict[str, Edge] = {}
        for u, v, w in edges:
            ru, rv = dsu.find(u), dsu.find(v)
            if ru != rv:
                if ru not in cheapest or (w, u, v) < (cheapest[ru][2], cheapest[ru][0], cheapest[ru][1]):
                    cheapest[ru] = (u, v, w)
                if rv not in cheapest or (w, u, v) < (cheapest[rv][2], cheapest[rv][0], cheapest[rv][1]):
                    cheapest[rv] = (u, v, w)
        added = []
        for u, v, w in cheapest.values():
            if dsu.union(u, v):
                mst.append((u, v, w))
                total_cost += w
                comps -= 1
                added.append(f"({u}-{v}, w={w})")
        trace.append(f"ROUND {rnd}: Added {', '.join(added)}")
        rnd += 1
    return {"algorithm": "Boruvka's", "mst": mst, "cost": total_cost, "trace": trace}

if __name__ == "__main__":
    verts = ["F1", "F2", "F3", "F4", "F5", "F6", "F7"]
    unique_edges = [
        ("F1", "F2", 7), ("F1", "F4", 5), ("F2", "F3", 8), ("F2", "F4", 9),
        ("F2", "F5", 10), ("F3", "F5", 6), ("F4", "F5", 15), ("F4", "F6", 4),
        ("F5", "F6", 11), ("F5", "F7", 12), ("F6", "F7", 13)
    ]

    print("=== TASK 5.1: UNIQUE MST COMPARISON ===")
    for fn in [lambda: mst_kruskal(verts, unique_edges),
               lambda: mst_prim(verts, unique_edges, "F1"),
               lambda: mst_boruvka(verts, unique_edges)]:
        r = fn()
        print(f"--- {r['algorithm']} (Cost = {r['cost']}) ---")
        for t in r["trace"]:
            print("  ", t)
        print("  MST:", r["mst"])

    print("\n=== TASK 5.2: STRESS TEST (MULTIPLE VALID MSTS WITH TIED WEIGHTS) ===")
    tied_edges = [
        ("F1", "F2", 5), ("F1", "F4", 5), ("F2", "F4", 5),
        ("F2", "F3", 6), ("F3", "F5", 6), ("F2", "F5", 6),
        ("F4", "F6", 4), ("F5", "F7", 8), ("F6", "F7", 9)
    ]
    for r in [mst_kruskal(verts, tied_edges), mst_prim(verts, tied_edges, "F4"), mst_boruvka(verts, tied_edges)]:
        print(f"{r['algorithm']:<10} | Cost = {r['cost']} | Edges = {r['mst']}")
