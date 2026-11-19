"""
Task 4: Word Break Problem (Faulty vs. Repaired Dynamic Programming)
Course: CSA06 Design and Analysis of Algorithms (CO4 - Assignment 4A)
"""

def word_break_faulty(text, dictionary):
    """Original faulty implementation missing DP[j] check."""
    n = len(text)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        dp[i] = False
        for j in range(i):
            if text[j:i] in dictionary:
                dp[i] = True
                break
    return dp[n], dp


def word_break_repaired(text, dictionary):
    """Repaired implementation enforcing valid prefix segmentation (DP[j] == True)."""
    n = len(text)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        dp[i] = False
        for j in range(i):
            if dp[j] and (text[j:i] in dictionary):
                dp[i] = True
                break
    return dp[n], dp


if __name__ == "__main__":
    # Counterexample exposing the defect (Task 4.2)
    fail_text = "catsand"
    fail_dict = {"cat", "and"}
    res_f, dp_f = word_break_faulty(fail_text, fail_dict)
    res_r, dp_r = word_break_repaired(fail_text, fail_dict)

    print("=== Test Case 1: Failing Counterexample ('catsand', Dict={'cat', 'and'}) ===")
    print(f"  Faulty Output   : {res_f} | DP Table: {dp_f}")
    print(f"  Repaired Output : {res_r} | DP Table: {dp_r}")

    # Regression Case (Task 4.4)
    pass_text = "leetcode"
    pass_dict = {"leet", "code"}
    res_f2, dp_f2 = word_break_faulty(pass_text, pass_dict)
    res_r2, dp_r2 = word_break_repaired(pass_text, pass_dict)

    print("\n=== Test Case 2: Regression Check ('leetcode', Dict={'leet', 'code'}) ===")
    print(f"  Faulty Output   : {res_f2} | DP Table: {dp_f2}")
    print(f"  Repaired Output : {res_r2} | DP Table: {dp_r2}")

    # Multi-word valid segmentation
    pass_text3 = "applepenapple"
    pass_dict3 = {"apple", "pen"}
    res_r3, dp_r3 = word_break_repaired(pass_text3, pass_dict3)
    print("\n=== Test Case 3: Repeated Dictionary Words ('applepenapple') ===")
    print(f"  Repaired Output : {res_r3} | DP Table: {dp_r3}")
