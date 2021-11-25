import sys
import fileinput

def argmax(list):
    f = lambda i: list[i]
    return max(range(len(list)), key=f)

def read_input(input):
    input = list(map(float, input.split()))

    height = int(input.pop(0))
    width = int(input.pop(0))

    matrix = []
    while input:
        matrix.append(input[:width])
        input = input[width:]

    return matrix

def best_path(best, list, idx, n):
    if n < 0:
        return

    best_path(best, list, list[n][idx], n-1)

    best.append(idx)

def viterbi(A, B, O, pi):
    v = []
    back_ptr = []

    # initialisation
    v.append([pi[s]*B[s][O[0]] for s in range(len(A))])
    back_ptr.extend([[0]*len(A)])

    # recursive step
    for t in range(1, len(O)):
        state = []
        ptr = []
        for s in range(len(A)):
            path = [v[t-1][k] * A[k][s] * B[s][O[t]] for k in range(len(A))]
            state.append(max(path))
            ptr.append(argmax(path))
        v.append(state)
        back_ptr.append(ptr)

    # termination step
    best_path_prob = []
    best_path_ptr = []

    best_path(best_path_ptr, back_ptr, argmax(back_ptr[len(O)-1]), len(O)-1)

    return best_path_ptr


input = sys.stdin
A = read_input(input.readline())
B = read_input(input.readline())
pi = read_input(input.readline())[0]
O = [int(elem) for elem in input.readline().split()[1:]]

path = viterbi(A, B, O, pi)

print(" ".join(map(str, path)))