import sys
import fileinput

def read_input(input):
    input = list(map(float, input.split()))

    height = int(input.pop(0))
    width = int(input.pop(0))

    matrix = []
    while input:
        matrix.append(input[:width])
        input = input[width:]

    return matrix

def matmul(A,B):
    matrix = []
    for i in range(len(A)):
        row = []
        for j in range(len(B[0])):
            sum = 0
            for k in range(len(B)):
                sum += A[i][k] * B[k][j]
            row.append(sum)
        matrix.append(row)
    return matrix


input = sys.stdin
A = read_input(input.readline())
B = read_input(input.readline())
pi = read_input(input.readline())

trans = matmul(matmul(pi, A), B)

res = ""
res = res + str(len(trans)) + " " + str(len(trans[0]))

for i in range(len(trans[0])):
    res += " " + str(trans[0][i])

print(res)
