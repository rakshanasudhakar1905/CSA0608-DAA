import random
import time
def add(A, B):
    n = len(A)
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]
def sub(A, B):
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]
def conventional(A, B, counter):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            for j in range(n):
                counter[0] += 1
                C[i][j] += A[i][k] * B[k][j]
    return C
def strassen(A, B, counter, cutoff=2):
    n = len(A)
    if n <= cutoff:
        return conventional(A, B, counter)
    h = n // 2
    A11 = [row[:h] for row in A[:h]]
    A12 = [row[h:] for row in A[:h]]
    A21 = [row[:h] for row in A[h:]]
    A22 = [row[h:] for row in A[h:]]
    B11 = [row[:h] for row in B[:h]]
    B12 = [row[h:] for row in B[:h]]
    B21 = [row[:h] for row in B[h:]]
    B22 = [row[h:] for row in B[h:]]
    M1 = strassen(add(A11, A22), add(B11, B22), counter, cutoff)
    M2 = strassen(add(A21, A22), B11, counter, cutoff)
    M3 = strassen(A11, sub(B12, B22), counter, cutoff)
    M4 = strassen(A22, sub(B21, B11), counter, cutoff)
    M5 = strassen(add(A11, A12), B22, counter, cutoff)
    M6 = strassen(sub(A21, A11), add(B11, B12), counter, cutoff)
    M7 = strassen(sub(A12, A22), add(B21, B22), counter, cutoff)
    C11 = add(sub(add(M1, M4), M5), M7)
    C12 = add(M3, M5)
    C21 = add(M2, M4)
    C22 = add(add(sub(M1, M2), M3), M6)
    top = [C11[i] + C12[i] for i in range(h)]
    bottom = [C21[i] + C22[i] for i in range(h)]
    return top + bottom
def pad_matrix(A, size):
    return [row + [0] * (size - len(row)) for row in A] + \
           [[0] * size for _ in range(size - len(A))]
def multiply_strassen(A, B, counter, cutoff=2):
    n = len(A)
    size = 1
    while size < n:
        size *= 2
    Ap, Bp = pad_matrix(A, size), pad_matrix(B, size)
    Cp = strassen(Ap, Bp, counter, cutoff)
    return [row[:n] for row in Cp[:n]]
def main():
    print("Q4: CONVENTIONAL AND STRASSEN MATRIX MULTIPLICATION")
    for n in (2, 4, 8, 16):
        random.seed(n)
        A = [[random.randint(0, 9) for _ in range(n)] for _ in range(n)]
        B = [[random.randint(0, 9) for _ in range(n)] for _ in range(n)]
        c1 = [0]; c2 = [0]
        t1 = time.perf_counter(); X = conventional(A, B, c1); t1 = time.perf_counter() - t1
        t2 = time.perf_counter(); Y = multiply_strassen(A, B, c2); t2 = time.perf_counter() - t2
        print(f"n={n:2}: correct={X == Y}, conventional scalar multiplications={c1[0]}, "
              f"Strassen scalar multiplications={c2[0]}, times={t1:.6f}s/{t2:.6f}s")
    print("For non-power-of-two sizes, zero-padding is used and extra work may be introduced.")
if __name__ == "__main__":
    main()
