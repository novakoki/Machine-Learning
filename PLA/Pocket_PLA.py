from PLA import *
import threading


def count_mistakes(w, x, y, row):
    mistakes = 0
    for i in range(0, row):
        sign = np.sign(np.vdot(w.T, x[i]))
        if (sign != y[i, 0]) and not (sign == 0 and y[i, 0] == -1):
            mistakes += 1
    return mistakes


def pocket_PLA(x, y, row, count):
    rand_list = con_list('random', row)
    w = y[rand_list[0]] * x[rand_list[0]]
    res = w

    current_mistakes = count_mistakes(w, x, y, row)

    for i in range(1, row):
        w = w + y[rand_list[i]] * x[rand_list[i]]
        mistakes = count_mistakes(w, x, y, row)
        if mistakes < current_mistakes:
            res = w
            current_mistakes = mistakes
        count -= 1
        if count == 0:
            break

    return res


def average_error_rate(train, test, count, times):
    total_mistakes = 0
    for i in range(0, times):
        w = pocket_PLA(train[0], train[1], train[2], count)
        total_mistakes += count_mistakes(w, test[0], test[1], test[2])
    return float(total_mistakes)/times/test[2]

total_mistakes = 0


def multi_average_error_rate(train, test, count, times, lock):
    w = pocket_PLA(train[0], train[1], train[2], count)
    global total_mistakes
    local_mistakes = count_mistakes(w, test[0], test[1], test[2])
    lock.acquire()
    total_mistakes += local_mistakes
    lock.release()

if __name__ == '__main__':
    train = loadmat('ntumlone%2Fhw1%2Fhw1_18_train.dat')
    test = loadmat('ntumlone%2Fhw1%2Fhw1_18_test.dat')
    # print average_error_rate(train, test, 100, 2000)
    # multi_average_error_rate(train, test, 100, 100)
    for x in xrange(40):
        record = []
        lock = threading.Lock()
        for i in range(50):
            thread = threading.Thread(
              target=multi_average_error_rate,
              args=(train, test, 50, 100, lock))
            thread.start()
            record.append(thread)

        for thread in record:
            thread.join()

    print total_mistakes
