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

def forward(A, B, O, pi):
    alpha = []
    # initialisation step
    for s in range(len(A)):
        alpha.append(pi[s] * B[s][O[0]])

    # recursion step
    for t in range(1, len(O)):
        state = []
        for s in range(len(A)):
            # prob[s'][t-1] * A[s'][s] * B[s][O[t]]
            forward_path = [alpha[k] * A[k][s] * B[s][O[t]] for k in range(0, len(A))]
            state.append(sum(forward_path))
        alpha = state

    return sum(alpha)

input = sys.stdin
A = read_input(input.readline())
B = read_input(input.readline())
pi = read_input(input.readline())[0]
O = [int(elem) for elem in input.readline().split()[1:]]

print(forward(A, B, O, pi))
