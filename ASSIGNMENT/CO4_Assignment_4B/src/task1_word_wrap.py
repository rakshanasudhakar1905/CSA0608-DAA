"""
Task 1: Word Wrap as a Document-Layout Engine (Dynamic Programming)
Course: CSA06 Design and Analysis of Algorithms - CO4 Assignment 4B
"""

from typing import List, Dict, Any

def solve_word_wrap(words: List[str], max_width: int) -> Dict[str, Any]:
    if max_width <= 0:
        raise ValueError(f"Invalid line width: {max_width}. Must be positive.")
    if not words:
        return {"min_penalty": 0, "lines": [], "dp": [], "choice": [], "words": [], "max_width": max_width}

    n = len(words)
    for w in words:
        if len(w) > max_width:
            raise ValueError(f"Word '{w}' (length {len(w)}) exceeds maximum line width {max_width}.")

    INF = float('inf')
    cost = [[INF] * n for _ in range(n)]
    unused_spaces = [[0] * n for _ in range(n)]

    for i in range(n):
        curr_len = 0
        for j in range(i, n):
            curr_len = len(words[j]) if j == i else curr_len + 1 + len(words[j])
            if curr_len <= max_width:
                spaces = max_width - curr_len
                unused_spaces[i][j] = spaces
                cost[i][j] = 0 if j == n - 1 else spaces ** 2
            else:
                break

    dp = [INF] * (n + 1)
    dp[n] = 0
    choice = [-1] * n

    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            if cost[i][j] == INF:
                break
            if cost[i][j] + dp[j + 1] < dp[i]:
                dp[i] = cost[i][j] + dp[j + 1]
                choice[i] = j

    lines = []
    idx = 0
    while idx < n:
        end_idx = choice[idx]
        lines.append({
            "line_no": len(lines) + 1,
            "text": " ".join(words[idx:end_idx + 1]),
            "unused_spaces": unused_spaces[idx][end_idx],
            "penalty": cost[idx][end_idx],
            "is_final": (end_idx == n - 1)
        })
        idx = end_idx + 1

    return {"min_penalty": dp[0], "lines": lines, "dp": dp, "choice": choice, "words": words, "max_width": max_width}

def format_report(res: Dict[str, Any], show_dp: bool = True) -> str:
    out = [
        f"Max Line Width (W) = {res['max_width']} | Total Words = {len(res['words'])}",
        f"Minimum Total Penalty = {res['min_penalty']}",
        "-" * 65,
        f"{'Line':<5} | {'Content':<{res['max_width']}} | {'Unused':<6} | {'Penalty'}",
        "-" * 65
    ]
    for ln in res["lines"]:
        pen_str = f"{ln['penalty']} (Final)" if ln["is_final"] else str(ln["penalty"])
        out.append(f"{ln['line_no']:<5} | {ln['text']:<{res['max_width']}} | {ln['unused_spaces']:<6} | {pen_str}")
    out.append("-" * 65)
    if show_dp:
        out.append("[Intermediate DP States: dp[i] = min penalty for words[i..n-1]]")
        for i in range(len(res["words"])):
            j = res["choice"][i]
            out.append(f"  dp[{i:2d}] ('{res['words'][i]}'): cost = {str(res['dp'][i]):>4} -> breaks after word[{j}] ('{res['words'][j]}')")
        out.append(f"  dp[{len(res['words']):2d}] (Base Case): cost = 0")
    return "\n".join(out)

if __name__ == "__main__":
    sample_text = "Dynamic programming solves complex optimization problems by breaking them into overlapping subproblems"
    words = sample_text.split()

    print("=== TASK 1.1 & 1.2: BASELINE EXECUTION (W = 24) ===")
    print(format_report(solve_word_wrap(words, 24), show_dp=True))

    print("\n=== TASK 1.3: REQUIREMENT CHANGE (MODIFIED WIDTHS W = 20, 28, 32) ===")
    for w in [20, 28, 32]:
        print(f"--- Modified Width W = {w} ---")
        print(format_report(solve_word_wrap(words, w), show_dp=False))

    print("\n=== TASK 1.4: BOUNDARY TEST CASES ===")
    print("[Boundary Test A: Exact Tight Fit W = 10]")
    print(format_report(solve_word_wrap(["alpha", "beta", "gamma", "delta"], 10), show_dp=False))
    print("[Boundary Test B: Word Exceeding Line Width W = 8]")
    try:
        solve_word_wrap(["short", "extraordinary", "text"], 8)
    except ValueError as e:
        print(f"Caught Expected Exception: {e}")
