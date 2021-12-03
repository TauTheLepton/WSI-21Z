import csv
import math

# returns list of tuples as data with onli the data and header is one tuple with names of elements in tuples
def readFile(file_name):
    with open(file_name, mode='r') as file:
        reader = csv.reader(file, delimiter=';')
        data = [list(row) for row in reader]
        header = data[0]
        data.remove(data[0])
    # data = convertDataToFloat(data)
    return data, header

# was supposed to convert every element of data from string to float, but it doesn't matter
def convertDataToFloat(data):
    # print(type(data))
    for i in range(len(data)):
        for j in range(len(data[i])):
            data[i][j] = float(data[i][j])
    return data

# devides data into learn data and test data with given coefficient
def divideLearnTestData(data, coef):
    learn_data = data[:int(len(data)*coef)]
    test_data = data[int(len(data)*coef):]
    return learn_data, test_data

# returns index of element d, so in this case the last one
def getDIdx(data):
    return len(data[0])-1

# creates a list containing every different d once
def getDList(data):
    D = []
    d_idx = getDIdx(data)
    for item in data:
        is_d = False
        for d in D:
            if float(item[d_idx]) == d:
                is_d = True
        if not is_d:
            D.append(float(item[d_idx]))
    return D

def calculateOneModel(data, idx, d):
    d_idx = getDIdx(data)
    sum_value = 0
    count_d = 0
    for item in data:
        if item[d_idx] == d:
            count_d += 1
            sum_value += item[idx]
    mean = sum_value/count_d
    sum_value = 0
    count_d = 0
    for item in data:
        if item[d_idx] == d:
            count_d += 1
            sum_value = (item[idx] - mean) ** 2
    variance = sum_value/count_d
    return mean, variance

def calculateModels(data):
    D = getDList(data)
    models = {}
    for d in D:
        models_param = {}
        for idx in range(len(data[0])-1):
            mean, variance = calculateOneModel(data, idx, d)
            model = dict([('mean', mean), ('variance', variance)])
            models_param[idx] = model
            # models.append((d, idx, mean, variance))
        models[d] = models_param
    return models

def calculateModelValue(models, d, indiv):
    end_probab = 1
    *indiv_data, indiv_d = indiv
    for i in range(len(indiv_data)):
        # COS W TYM ROWNANIU JEST ZLE ALE NWM CO
        tmp = ((indiv_data[i] - models[d][i]['mean']) ** 2) / (models[d][i]['variance'] ** 2)
        probab = 1 / math.sqrt(2 * math.pi * models[d][i]['variance'] ** 2) * math.exp(-1/2 * tmp)
        end_probab *= probab
    return end_probab

def calcBestD(data, models, test_item):
    D = getDList(data)
    best_probab = 0
    best_d = None
    for d in D:
        probab = calculateModelValue(models, d, test_item)
        if probab > best_probab:
            best_probab = probab
            best_d = d
    return best_d

def test(file_name, coef):
    data, header = readFile(file_name)
    data = convertDataToFloat(data)
    d_idx = getDIdx(data)
    learn_data, test_data = divideLearnTestData(data, coef)
    models = calculateModels(learn_data)
    sum_best_d = 0
    count_best_d = 0
    win_rate = 0
    for test_item in test_data:
        best_d = calcBestD(data, models, test_item)
        if best_d == test_item[d_idx]:
            win_rate += 1
        else:
            sum_best_d += abs(best_d - test_item[d_idx])
            count_best_d += 1
    print("Win rate:", win_rate/len(test_data))
    print("Average mistake:", sum_best_d/count_best_d)

def main():
    test('winequality-white.csv', 0.6)

if __name__ == '__main__':
    main()
