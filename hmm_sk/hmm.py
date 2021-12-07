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

def write_output(matrix):
    res = ''

    dx, dy = len(matrix), len(matrix[0])

    res += ' '.join(map(str, [dx, dy]))
    for elem in matrix:
        elem = [round(e, 6) for e in elem]
        res = res + ' ' + ' '.join(map(str, elem))

    print(res)


def backward(A, B, O, pi, c):
    beta = []

    #initialisation step
    beta.extend([[c[len(O)-1]]*len(A)])

    # recursion step
    for t in range(len(O)-2, -1, -1):
        state = []
        for s in range(len(A)):
            backward_path = [beta[0][k] * A[s][k] * B[k][O[t+1]] for k in range(len(A))]
            state.append(c[t]*sum(backward_path))
        beta.insert(0, state)

    # termination step
    return beta

def forward(A, B, O, pi):
    c = []
    alpha = []
    alpha_n = []

    # initialisation step
    alpha.append([pi[s]*B[s][O[0]] for s in range(len(A))])
    c.append(1/sum(alpha[0]))
    alpha_n.append([c[0]*alpha[0][s] for s in range(len(A))])

    # recursion step
    for t in range(1, len(O)):
        state = []
        for s in range(len(A)):
            forward_path = [alpha_n[t-1][k] * A[k][s] * B[s][O[t]] for k in range(len(A))]
            state.append(sum(forward_path))
        c.append(1/sum(state))
        alpha.append(state)
        alpha_n.append([c[t]*alpha[t][i] for i in range(len(A))])

    # termination step
    return alpha_n, c, sum(alpha[len(O)-1])

def estimator(A, B, O, alpha, beta):
    gamma = []  # gamma
    digamma = [] # di-gamma

    for t in range(len(O)-1):
        g = []
        dg = []
        for s in range(len(A)):
            prob = [alpha[t][s]*A[s][k]*B[k][O[t+1]]*beta[t+1][k] for k in range(len(A))]
            g.append(sum(prob))
            dg.append(prob)
        gamma.append(g)
        digamma.append(dg)

    gamma.append(alpha[len(O)-1])

    return gamma, digamma

def maximise_pi(n, gamma):
    return [gamma[0][i] for i in range(n)]

def maximise_A(n_state, n_obs, gamma, digamma):
    A = []

    for i in range(n_state):
        i_trans = sum([gamma[t][i] for t in range(n_obs)])

        A_new = []
        for j in range(n_state):
            ij_trans = sum([digamma[t][i][j] for t in range(n_obs)])
            A_new.append(ij_trans/i_trans)
        A.append(A_new)

    return A

def maximise_B(B_est, O, n_state, n_obs, gamma):
    B = []

    for i in range(n_state):
        i_trans = sum([gamma[t][i] for t in range(n_obs)])

        B_new = []
        for j in range(len(B_est[0])):
            ij_trans = sum([gamma[t][i] for t in range(n_obs) if O[t] == j])
            B_new.append(ij_trans/i_trans)
        B.append(B_new)

    return B

def baum_welch(A, B, O, pi):
    iter = 0
    log_prob = float('-inf')

    while (True):
        # forward and backward probabilities
        alpha, c, _ = forward(A, B, O, pi)
        beta = backward(A, B, O, pi, c)

        new_log_prob = compute_convergence(c, len(O))
        if log_prob >= new_log_prob or iter > 100:
            break

        # expectation step
        gamma, digamma = estimator(A, B, O, alpha, beta)

        # maximisation step (recompute A, B and pi)
        pi = maximise_pi(len(A), gamma)
        A  = maximise_A(len(A), len(O)-1, gamma, digamma)
        B  = maximise_B(B, O, len(A), len(O), gamma)

        iter += 1
        log_prob = new_log_prob


    return A, B, pi

def compute_convergence(c, n):
    log_prob = 0

    for i in range(0, n):
        log_prob += math.log(c[i])

    return -log_prob
