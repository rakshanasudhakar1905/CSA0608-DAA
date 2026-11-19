"""
Task 2: Job Sequencing with Deadlines
Course: CSA06 Design and Analysis of Algorithms (CO4 - Assignment 4A)
"""

def schedule_jobs(jobs):
    """
    Schedules unit-time jobs to maximize profit within deadlines.
    jobs: list of tuples (job_id, deadline, profit)
    """
    if not jobs:
        return 0, []

    # Sort jobs in descending order of profit
    sorted_jobs = sorted(jobs, key=lambda x: x[2], reverse=True)
    max_deadline = max(job[1] for job in sorted_jobs)

    # 1-indexed time slots: None indicates free slot
    slots = [None] * (max_deadline + 1)
    total_profit = 0
    trace = []

    for job_id, deadline, profit in sorted_jobs:
        placed = False
        chosen_slot = -1
        # Search backwards from min(deadline, max_deadline) to 1
        for t in range(min(deadline, max_deadline), 0, -1):
            if slots[t] is None:
                slots[t] = (job_id, deadline, profit)
                total_profit += profit
                placed = True
                chosen_slot = t
                break
        trace.append((job_id, deadline, profit, placed, chosen_slot))

    scheduled = [(t, slots[t][0], slots[t][2]) for t in range(1, max_deadline + 1) if slots[t] is not None]
    return total_profit, scheduled, trace


if __name__ == "__main__":
    # Desk-Check Dataset from Assignment
    jobs_base = [
        ("A", 2, 80),
        ("B", 1, 35),
        ("C", 2, 60),
        ("D", 3, 40),
        ("E", 1, 25)
    ]
    profit, sched, trace = schedule_jobs(jobs_base)
    print("=== Test Case 1: Assignment Desk-Check Dataset ===")
    for j_id, dl, pr, ok, sl in trace:
        status = f"Scheduled in Slot {sl}" if ok else "Rejected (No free slot <= deadline)"
        print(f"  Consider Job {j_id} (Deadline={dl}, Profit={pr}) -> {status}")
    print(f"Final Schedule (Slot, Job, Profit): {sched}")
    print(f"Total Profit: {profit}")

    # Task 2.5 Challenge Case: Change Job B profit from 35 to 90
    jobs_modified = [
        ("A", 2, 80),
        ("B", 1, 90),  # Modified from 35 -> 90
        ("C", 2, 60),
        ("D", 3, 40),
        ("E", 1, 25)
    ]
    profit_m, sched_m, trace_m = schedule_jobs(jobs_modified)
    print("\n=== Test Case 2: Modified Instance (Job B Profit = 90) ===")
    for j_id, dl, pr, ok, sl in trace_m:
        status = f"Scheduled in Slot {sl}" if ok else "Rejected (No free slot <= deadline)"
        print(f"  Consider Job {j_id} (Deadline={dl}, Profit={pr}) -> {status}")
    print(f"Final Schedule (Slot, Job, Profit): {sched_m}")
    print(f"Total Profit: {profit_m}")
