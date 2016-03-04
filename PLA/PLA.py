import numpy as np
import random

'''Perceptron Learning Algorithm
    mode = random or naive
    Learning to Answer Yes/No'''


def loadmat(filename):
    '''Read data from file and reshape it to a matrix'''

    raw = open(filename, 'r')
    col = len(raw.readline().split())
    raw.seek(0)
    row = len(raw.readlines())
    data = np.zeros((row, col))
    raw.seek(0)

    for i in range(0, row):
        data[i] = np.mat(raw.readline())

    raw.close()

    y = data[:, col-1:col]
    x = np.ones((row, col))
    x[:, 1:] = data[:, :col-1]

    return x, y, row


def con_list(mode, row):
    rand_list = range(0, row)
    if mode == 'random':
        random.seed()
        random.shuffle(rand_list)
    # Produce a random list

    return rand_list


def PLA(x, y, mode, row):
    w = np.mat('0 0 0 0 0')
    rand_list = con_list(mode, row)
    halt = False
    count = 0
    while not halt:
        halt = True
        for i in rand_list:
            sign = np.sign(np.vdot(w.T, x[i]))
            if (sign != y[i, 0]) and not (sign == 0 and y[i, 0] == -1):
                halt = False
                w = w + y[i]*x[i]
                # Modify the mistake
                count += 1

    return w, count

# test code
if __name__ == '__main__':
    data = loadmat('ntumlone%2Fhw1%2Fhw1_15_train.dat')
    print PLA(data[0], data[1], 'naive', data[2])
    print PLA(data[0], data[1], 'random', data[2])
