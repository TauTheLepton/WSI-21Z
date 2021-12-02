import csv

# returns list of tuples as data with onli the data and header is one tuple with names of elements in tuples
def readFile(file_name):
    with open(file_name, mode='r') as file:
        reader = csv.reader(file, delimiter=';')
        data = [tuple(row) for row in reader]
        header = data[0]
        data.remove(data[0])
    return data, header

def getLearnData(data):
    return data[:int(len(data)*0.6)]

def getTestData(data):
    return data[int(len(data)*0.6):]

def divideLearnTestData(data, coef):
    learn_data = data[:int(len(data)*coef)]
    test_data = data[int(len(data)*coef):]
    return learn_data, test_data

def getDIdx(data):
    return len(data[0])-1

def makeDict(data):
    dictd = {}
    D = getDList(data)
    for d in D:
        dictd[int(d)] = []
    for wine in data:
        *wine_data, d = wine
        dictd[int(d)].append(wine_data)
    return dictd

# creates a list containing every different d once
def getDList(data):
    D = []
    d_idx = getDIdx(data)
    for item in data:
        is_d = False
        for d in D:
            if item[d_idx] == d:
                is_d = True
        if not is_d:
            D.append(item[d_idx])
    return D

# returns probability of other elements with the same d having the same parameter value on given parameter index
def getOneProbab(data, idx, val, d):
    d_idx = getDIdx(data)
    vd_count = 0
    d_count = 0
    for item in data:
        if item[d_idx] == d:
            d_count += 1
            if item[idx] == val:
                vd_count += 1
    if d_count != 0:
        return vd_count/d_count
    else:
        return 0

# returns probability of element in data having the same d as given
def getProbabD(data, d):
    d_idx = getDIdx(data)
    count_d = 0
    for item in data:
        if item[d_idx] == d:
            count_d += 1
    return count_d/len(data)

# returns best d for given individual item, based on given data
def getBestD(data, indiv):
    best_value = 0
    best_d = 0
    D = getDList(data)
    *indiv_data, indiv_d = indiv
    for d in D:
        end_probab = getProbabD(data, d)
        for i in range(len(indiv_data)):
            probab = getOneProbab(data, i, indiv_data[i], d)
            end_probab = end_probab * probab
        if end_probab > best_value:
            best_value = end_probab
            best_d = d
    return best_d

# tests all elements of test data based on learn data
def test(file_name, coef):
    data, header = readFile(file_name)
    # learn_data = getLearnData(data)
    # test_data = getTestData(data)
    learn_data, test_data = divideLearnTestData(data, coef)
    d_idx = getDIdx(data)
    sum_best_d = 0
    count_best_d = 0
    win_rate = 0
    for test_item in test_data:
        best_d = getBestD(learn_data, test_item)
        if best_d == test_item[d_idx]:
            win_rate += 1
        else:
            sum_best_d += abs(int(best_d) - int(test_item[d_idx]))
            count_best_d += 1

    print("Win rate:", win_rate/len(test_data))
    print("Average mistake:", sum_best_d/count_best_d)

def main():
    # idx=4
    # data, header = readFile('winequality-white.csv')
    # learn_data = getLearnData(data)
    # test_data = getTestData(data)
    # dictd = makeDict(learn_data)
    # best_d = getBestD(learn_data, test_data[idx])
    # print(best_d)
    # print(test_data[idx])
    test('winequality-white.csv', 0.6)
    # data, header = readFile('winequality-white-test.csv')
    # probab = getProbabD(data, 5)
    # print(probab)
    # print(getDList(readFile('winequality-white.csv')[0]))
    
    
    # print(len(data))
    # print()
    # print(len(test_data) + len(learn_data))
    # print(learn_data[len(learn_data)-1])
    # print(test_data[0])

    # print(len(dictd[5]))
    # new_item = data[]

    # print(header[length])

if __name__ == '__main__':
    main()
