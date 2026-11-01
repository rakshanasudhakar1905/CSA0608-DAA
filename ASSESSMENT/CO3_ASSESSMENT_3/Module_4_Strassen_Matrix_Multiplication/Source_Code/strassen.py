def add(X, Y):
    n = len(X)
    return [[X[i][j] + Y[i][j] for j in range(n)] for i in range(n)]
def sub(X, Y):
    n = len(X)
    return [[X[i][j] - Y[i][j] for j in range(n)] for i in range(n)]
def conventional(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            for j in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C
def split(M):
    n = len(M)
    h = n // 2
    return ([row[:h] for row in M[:h]],
            [row[h:] for row in M[:h]],
            [row[:h] for row in M[h:]],
            [row[h:] for row in M[h:]])
def join(C11, C12, C21, C22):
    top = [C11[i] + C12[i] for i in range(len(C11))]
    bottom = [C21[i] + C22[i] for i in range(len(C21))]
    return top + bottom
def strassen(A, B, cutoff=2):
    n = len(A)
    if n <= cutoff:
        return conventional(A, B)
    A11, A12, A21, A22 = split(A)
    B11, B12, B21, B22 = split(B)
    M1 = strassen(add(A11, A22), add(B11, B22), cutoff)
    M2 = strassen(add(A21, A22), B11, cutoff)
    M3 = strassen(A11, sub(B12, B22), cutoff)
    M4 = strassen(A22, sub(B21, B11), cutoff)
    M5 = strassen(add(A11, A12), B22, cutoff)
    M6 = strassen(sub(A21, A11), add(B11, B12), cutoff)
    M7 = strassen(sub(A12, A22), add(B21, B22), cutoff)
    C11 = add(sub(add(M1, M4), M5), M7)
    C12 = add(M3, M5)
    C21 = add(M2, M4)
    C22 = add(add(sub(M1, M2), M3), M6)
    return join(C11, C12, C21, C22)
def pad_matrix(M, size):
    return [row + [0] * (size - len(row)) for row in M] + \
           [[0] * size for _ in range(size - len(M))]
def multiply(A, B, cutoff=64):
    if not A or not B or len(A[0]) != len(B):
        raise ValueError("Incompatible matrix dimensions")
    if len(A) != len(A[0]) or len(B) != len(B[0]) or len(A) != len(B):
        raise ValueError("This demonstration expects square matrices of equal size")
    n = len(A)
    size = 1
    while size < n:
        size *= 2
    Ap, Bp = pad_matrix(A, size), pad_matrix(B, size)
    Cp = strassen(Ap, Bp, cutoff)
    return [row[:n] for row in Cp[:n]]
if __name__ == "__main__":
    A = [[1, 7], [3, 5]]
    B = [[1, 3], [7, 5]]
    print("A =", A)
    print("B =", B)
    print("Strassen result =", multiply(A, B, cutoff=1))
    print("Conventional result =", conventional(A, B))
    print("Expected result = [[50, 38], [38, 34]]")