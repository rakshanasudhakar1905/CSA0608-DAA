def standard_multiply(x, y, counter):
    counter[0] += len(str(x)) * len(str(y))
    return x * y
def karatsuba(x, y, counter, threshold=10):
    if x < threshold or y < threshold:
        counter[0] += 1
        return x * y
    n = max(len(str(x)), len(str(y)))
    half = n // 2
    power = 10 ** half
    a, b = divmod(x, power)
    c, d = divmod(y, power)
    ac = karatsuba(a, c, counter, threshold)
    bd = karatsuba(b, d, counter, threshold)
    ab_cd = karatsuba(a + b, c + d, counter, threshold)
    ad_plus_bc = ab_cd - ac - bd
    return ac * (10 ** (2 * half)) + ad_plus_bc * power + bd
def main():
    print("Q3: STANDARD AND KARATSUBA MULTIPLICATION")
    for digits in (4, 8, 16, 32, 64):
        x = int("9" * digits)
        y = int("8" * digits)
        c1 = [0]; c2 = [0]
        answer1 = standard_multiply(x, y, c1)
        answer2 = karatsuba(x, y, c2)
        assert answer1 == answer2
        print(f"digits={digits:2}: standard digit multiplications={c1[0]}, "
              f"Karatsuba digit multiplications={c2[0]}, correct={answer1 == answer2}")
    print("Note: Python integers are highly optimised; use repeated timings for a fair runtime crossover.")
if __name__ == "__main__":
    main()
