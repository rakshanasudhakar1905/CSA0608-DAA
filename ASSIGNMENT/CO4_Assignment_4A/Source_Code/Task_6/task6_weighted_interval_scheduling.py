"""
Task 6: Design Challenge - Energy-Aware Job Scheduling (Weighted Interval Scheduling)
Course: CSA06 Design and Analysis of Algorithms (CO4 - Assignment 4A)
"""
from bisect import bisect_right

def weighted_interval_scheduling(jobs):
    """
    Finds non-overlapping subset of jobs maximizing total energy-saving value.
    jobs: list of tuples (job_id, start, finish, value)
    """
    if not jobs:
        return 0, [], []

    # Sort jobs by finish time ascending
    sorted_jobs = sorted(jobs, key=lambda x: x[2])
    n = len(sorted_jobs)
    finish_times = [job[2] for job in sorted_jobs]

    # Compute p[j]: 1-based index of latest compatible job finishing <= start[j]
    p = [0] * (n + 1)
    for j in range(1, n + 1):
        start_j = sorted_jobs[j - 1][1]
        # bisect_right returns count of elements <= start_j
        p[j] = bisect_right(finish_times, start_j)

    # Bottom-up Dynamic Programming
    dp = [0] * (n + 1)
    for j in range(1, n + 1):
        val_j = sorted_jobs[j - 1][3]
        include_val = val_j + dp[p[j]]
        exclude_val = dp[j - 1]
        dp[j] = max(include_val, exclude_val)

    # Reconstruct optimal set of jobs
    selected = []
    j = n
    while j > 0:
        val_j = sorted_jobs[j - 1][3]
        if val_j + dp[p[j]] >= dp[j - 1]:
            selected.append(sorted_jobs[j - 1])
            j = p[j]
        else:
            j -= 1

    selected.reverse()
    return dp[n], selected, list(zip(range(1, n + 1), sorted_jobs, p[1:], dp[1:]))


if __name__ == "__main__":
    # Assignment 8-Job Dataset
    jobs_8 = [
        ("J1", 1, 3, 20),
        ("J2", 2, 5, 50),
        ("J3", 4, 6, 30),
        ("J4", 6, 8, 40),
        ("J5", 5, 9, 60),
        ("J6", 8, 10, 30),
        ("J7", 9, 11, 50),
        ("J8", 11, 13, 40)
    ]
    max_energy, chosen_jobs, trace_rows = weighted_interval_scheduling(jobs_8)
    print("=== Stage 5: Assignment 8-Job Dataset ===")
    print("Idx | Job (Start, Finish, Val) | p[j] | DP[j]")
    print("-" * 48)
    for idx, job, pj, dpj in trace_rows:
        print(f"{idx:>3} | {job[0]} ({job[1]:>2}, {job[2]:>2}, {job[3]:>2})           | {pj:>4} | {dpj:>5}")
    print(f"\nSelected Jobs: {[j[0] for j in chosen_jobs]} -> {chosen_jobs}")
    print(f"Maximum Energy-Saving Value: {max_energy}")

    # Stage 6: Adversarial 5-Job Dataset (Greedy Traps)
    adversarial_jobs = [
        ("A1", 1, 4, 40),   # Earliest finish trap
        ("A2", 3, 7, 45),   # Medium overlap
        ("A3", 2, 10, 95),  # Highest single value trap
        ("A4", 4, 8, 40),   # Bridges A1 and A5
        ("A5", 8, 11, 45)   # Completes chain A1 + A4 + A5 = 125
    ]
    max_adv, chosen_adv, trace_adv = weighted_interval_scheduling(adversarial_jobs)
    print("\n=== Stage 6: Adversarial 5-Job Dataset ===")
    for idx, job, pj, dpj in trace_adv:
        print(f"  Idx {idx}: {job} | p[{idx}]={pj} | DP[{idx}]={dpj}")
    print(f"Selected Jobs: {[j[0] for j in chosen_adv]} -> {chosen_adv}")
    print(f"Maximum Energy-Saving Value: {max_adv}")
