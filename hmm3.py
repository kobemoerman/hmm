import sys
import math
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

def backward(A, B, O, pi, c):
    beta = []
    #initialisation step
    beta.extend([[1]*len(A)])

    for t in range(0, len(O)-1):
        state = []
        for s in range(len(A)):
            backward_path = [beta[0][k] * A[s][k] * B[k][O[t+1]] for k in range(len(A))]
            state.append(c[t]*sum(backward_path))
        beta.insert(0, state)

    return beta

def forward(A, B, O, pi):
    c = []
    alpha = []
    alpha_n = []
    # initialisation step
    alpha.append([pi[s]*B[s][O[0]] for s in range(len(A))])
    c.append(1/sum(alpha[0]))
    alpha_n.append([c[0]*alpha[0][i] for i in range len(A)])

    # recursion step
    for t in range(1, len(O)):
        state = []
        for s in range(len(A)):
            forward_path = [alpha_n[t-1][k] * A[k][s] * B[s][O[t]] for k in range(len(A))]
            state.append(sum(forward_path))
        c.append(1/sum(state))
        alpha.append(state)
        alpha_n.append([c[t]*alpha[t][i] for i in range len(A)])

    # termination step
    return alpha_n, c, sum(alpha[len(O)-1])

def estimator(A, B, O, alpha, beta):
    gamma = []  # gamma
    digamma = [] # di-gamma

    for t in range(len(O)-1):
        g = []
        dg = []
        for s in range(len(A)):
            prob = [alpha[t][s]*A[i][k]*B[k][O[t+1]]*beta[t+1][k] for k in range(len(A))]
            g.append(sum(prob))
            dg.append(prob)
        gamma.append(g)
        digamma.append(dg)

    gamma.append(alpha[len(O)-1])

    return gamma, digamma

def maximise_pi(pi_est, n, gamma):
    return [gamma[0][i] for i in range(n)]

def maximise_A(A_est, n, gamma, digamma):
    A = [[]]

    for i in range(len(A)):
        i_trans = 0
        for t in range(n):
            i_trans += gamma[t][i]

        for j in range(len(A)):
            ij_trans = 0
            for t in range(n):
                ij_trans += digamma[t][i]
            A[j].append(ij_trans/i_trans)

    return A

def baum_welch(A, B, O, pi):
    # A = B = []
    log_prob = 1
    convergence = float('-inf')

    while (log_prob > convergence):
        alpha, c, _ = forward(A, B, O, pi)
        beta = backward(A, B, O, pi, c)

        # expectation step
        gamma, digamma = estimator(A, B, O, alpha, beta)

        # maximisation step (recompute A, B and pi)
        pi = maximise_pi(pi, len(A), gamma)
        A  = maximise_A(A, len(O)-1, gamma, digamma)

        log_prob = compute_convergence(c, len(O))

    return A, B

def compute_convergence(c, n):
    prob = 0

    for i in range(0, n):
        prob += math.log(c[i])

    return -prob

# estimates
input  = sys.stdin
A_est  = read_input(input.readline())
B_est  = read_input(input.readline())
pi_est = read_input(input.readline())[0]
O_est  = [int(elem) for elem in input.readline().split()[1:]]

# learn transition and emission probabilities
A, B = baum_welch(A_est, B_est, O_est, pi_est)
