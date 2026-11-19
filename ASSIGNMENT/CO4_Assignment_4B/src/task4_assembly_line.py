"""
Task 4: Smart Manufacturing Optimisation (Assembly Line Scheduling DP)
Course: CSA06 Design and Analysis of Algorithms - CO4 Assignment 4B
"""

from typing import List, Dict, Any

def solve_assembly_line(
    a1: List[int], a2: List[int], t1_to_2: List[int], t2_to_1: List[int],
    e1: int, e2: int, x1: int, x2: int
) -> Dict[str, Any]:
    n = len(a1)
    f1, f2, l1, l2 = [0] * n, [0] * n, [0] * n, [0] * n
    decisions = []

    f1[0], f2[0] = e1 + a1[0], e2 + a2[0]
    decisions.append({"station": 1, "l1_stay": f1[0], "l1_trans": None, "l1_sel": "Entry 1",
                      "l2_stay": f2[0], "l2_trans": None, "l2_sel": "Entry 2"})

    for j in range(1, n):
        stay1 = f1[j - 1] + a1[j]
        trans1 = f2[j - 1] + t2_to_1[j - 1] + a1[j]
        if stay1 <= trans1:
            f1[j], l1[j], sel1 = stay1, 1, "Stay (L1)"
        else:
            f1[j], l1[j], sel1 = trans1, 2, "Transfer (L2->L1)"

        stay2 = f2[j - 1] + a2[j]
        trans2 = f1[j - 1] + t1_to_2[j - 1] + a2[j]
        if stay2 <= trans2:
            f2[j], l2[j], sel2 = stay2, 2, "Stay (L2)"
        else:
            f2[j], l2[j], sel2 = trans2, 1, "Transfer (L1->L2)"

        decisions.append({"station": j + 1, "l1_stay": stay1, "l1_trans": trans1, "l1_sel": sel1,
                          "l2_stay": stay2, "l2_trans": trans2, "l2_sel": sel2})

    if f1[n - 1] + x1 <= f2[n - 1] + x2:
        min_time, last_line = f1[n - 1] + x1, 1
    else:
        min_time, last_line = f2[n - 1] + x2, 2

    route = [0] * n
    route[n - 1] = last_line
    curr = last_line
    for j in range(n - 1, 0, -1):
        curr = l1[j] if curr == 1 else l2[j]
        route[j - 1] = curr

    transfers = [f"Station {j} (Line {route[j-1]}) -> Station {j+1} (Line {route[j]})"
                 for j in range(1, n) if route[j] != route[j - 1]]
    return {"min_time": min_time, "route": route, "transfers": transfers, "decisions": decisions, "exit_line": last_line}

def print_assembly_report(res: Dict[str, Any]):
    print(f"Minimum Production Time = {res['min_time']}")
    print(f"Route Sequence: {' -> '.join(f'L{l}(S{i+1})' for i, l in enumerate(res['route']))} -> Exit(L{res['exit_line']})")
    print("Transfer Points:", res["transfers"])
    print(f"{'Stn':<4} | {'L1 Stay':<8} | {'L1 Trans':<9} | {'L1 Selected':<18} | {'L2 Stay':<8} | {'L2 Trans':<9} | {'L2 Selected'}")
    print("-" * 82)
    for d in res["decisions"]:
        t1 = str(d['l1_trans']) if d['l1_trans'] is not None else "-"
        t2 = str(d['l2_trans']) if d['l2_trans'] is not None else "-"
        print(f"{d['station']:<4} | {d['l1_stay']:<8} | {t1:<9} | {d['l1_sel']:<18} | {d['l2_stay']:<8} | {t2:<9} | {d['l2_sel']}")

if __name__ == "__main__":
    a1, a2 = [7, 9, 3, 4, 8, 4], [8, 5, 6, 4, 5, 7]
    t12, t21 = [2, 3, 1, 3, 4], [2, 1, 2, 2, 1]
    e1, e2, x1, x2 = 2, 4, 3, 2

    print("=== TASK 4.1 & 4.2: BASELINE ASSEMBLY LINE OPTIMISATION ===")
    print_assembly_report(solve_assembly_line(a1, a2, t12, t21, e1, e2, x1, x2))

    print("\n=== TASK 4.3: INCREASE TRANSFER TIME t1_to_2[2] (Station 3->4) FROM 1 TO 10 ===")
    t12_mod = list(t12)
    t12_mod[2] = 10
    print_assembly_report(solve_assembly_line(a1, a2, t12_mod, t21, e1, e2, x1, x2))

    print("\n=== TASK 4.4: MACHINE SLOWDOWN AT LINE 1 STATION 3 (a1[2]: 3 -> 14) ===")
    a1_mod = list(a1)
    a1_mod[2] = 14
    print_assembly_report(solve_assembly_line(a1_mod, a2, t12, t21, e1, e2, x1, x2))
