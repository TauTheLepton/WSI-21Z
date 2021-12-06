import csv
import math
import numpy as np

# returns list of tuples as data with onli the data and header is one tuple with names of elements in tuples
def readFile(file_name):
    with open(file_name, mode='r') as file:
        reader = csv.reader(file, delimiter=';')
        data = [list(row) for row in reader]
        header = data[0]
        data.remove(data[0])
    return data, header

# was supposed to convert every element of data from string to float, but it doesn't matter
def convertDataToFloat(data):
    for i in range(len(data)):
        for j in range(len(data[i])):
            data[i][j] = float(data[i][j])
    return data

# divides data into learn data and test data with given coefficient
def divideLearnTestData(data, coef):
    learn_data = data[:int(len(data)*coef)]
    test_data = data[int(len(data)*coef):]
    return learn_data, test_data

# divides data into given amount (k) of sets
def divideDataIntoSets(data, k):
    sets = []
    set_length = math.trunc(len(data) / k)
    for i in range(k):
        sets.append(data[i*set_length:(i+1)*set_length])
    return sets

# merges all sets form list 'sets' without set 'exclude_set' into one set
def mergeSets(sets, exclude_set):
    merged = []
    for set in sets:
        if set != exclude_set:
            for item in set:
                merged.append(item)
    return merged

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
            if item[d_idx] == d:
                is_d = True
        if not is_d:
            D.append(item[d_idx])
    return D

# calculates one model params for given idx (column / data type) and filters only for given d
def calculateOneModel(data, idx, d):
    d_idx = getDIdx(data)
    d_data = []
    for item in data:
        if item[d_idx] == d:
            d_data.append(item[idx])

    # WRITE TO FILE TO CHECK WITH LIBRE OFFICE CALC IF STANDARD DEVIATION AND MEAN VALUES ARE CORRECT
    # YES THEY ARE
    # print()
    # for item in d_data: print(item)
    # print()
    # with open('test_write_one_column.csv', mode='w') as file:
    #     writer = csv.writer(file, delimiter='\n')
    #     for item in d_data:
    #         writer.writerow([item])

    # if d_data != []:
    mean = np.mean(d_data)
    std = np.std(d_data)
    # else:
    #     mean = 0
    #     std = 0
    return mean, std

# calculates models od every idx for every d, so all models
def calculateModels(data, D):
    models = {}
    for d in D:
        models_param = {}
        for idx in range(len(data[0])-1):
            mean, std = calculateOneModel(data, idx, d)
            model = dict([('mean', mean), ('std', std)])
            models_param[idx] = model
        models[d] = models_param
    return models

# calculates model value - probability that given individual is in class d
def calculateModelValue(models, d, indiv):
    end_probab = 1
    end_probab1 = 0
    *indiv_data, indiv_d = indiv
    for i in range(len(indiv_data)):
        # MY OLD CALCULATIONS, BUT RESULTS ARE PRETTY MUCH THE SAME
        # if True:
        # if models[d][i]['std'] ** 2 != 0:
        #     index = -(((indiv_data[i] - models[d][i]['mean']) ** 2) / (2 * (models[d][i]['std'] ** 2)))
        #     probab = (1 / (math.sqrt(2 * math.pi) * abs(models[d][i]['std']))) * math.exp(index)
        # else:
        #     probab = 0

        # EQUATION STRAIGHT FROM https://towardsdatascience.com/how-to-impliment-a-gaussian-naive-bayes-classifier-in-python-from-scratch-11e0b80faf5a
        # STANDARD DEVIATION STILL SOMETIMES 0
        if models[d][i]['std'] ** 2 != 0:
            exponent = math.exp(-((indiv_data[i] - models[d][i]['mean']) ** 2 / (2 * models[d][i]['std'] ** 2)))
            probab = (1 / (math.sqrt(1 * math.pi) * models[d][i]['std'])) * exponent
        else:
            probab = 0
        # if models[d][i]['std'] ** 2 == 0:
        #     print(index, probab)
        end_probab *= probab
        if probab != 0:
            end_probab1 += math.log(probab, math.e)
    end_probab1 = math.exp(end_probab1)
    return end_probab1

# calculates best d for given item
def calcBestD(D, models, test_item):
    best_probab = 0
    best_d = None
    for d in D:
        probab = calculateModelValue(models, d, test_item)
        if probab > best_probab:
            best_probab = probab
            best_d = d
    return best_d

# does everything, divides data, learns on one part (coef) and tests on the other part
def test(file_name, coef):
    data, header = readFile(file_name)
    data = convertDataToFloat(data)
    D = getDList(data)
    d_idx = getDIdx(data)
    learn_data, test_data = divideLearnTestData(data, coef)
    models = calculateModels(learn_data, D)
    sum_best_d = 0
    count_best_d = 0
    win_rate = 0
    for test_item in test_data:
        best_d = calcBestD(D, models, test_item)
        if best_d == test_item[d_idx]:
            win_rate += 1
        else:
            sum_best_d += abs(best_d - test_item[d_idx])
            count_best_d += 1
    print("Win rate:", win_rate/len(test_data))
    print("Average mistake:", sum_best_d/count_best_d)

# tests whole implementation with cross validation with given amount of sets (k)
def testCrossValidation(file_name, k):
    data, header = readFile(file_name)
    data = convertDataToFloat(data)
    D = getDList(data)
    d_idx = getDIdx(data)
    dataSets = divideDataIntoSets(data, k)
    accuracy = []
    mistake = []
    for dataSet in dataSets:
        learn_data = mergeSets(dataSets, dataSet)
        test_data = dataSet
        models = calculateModels(learn_data, D)
        sum_best_d = 0
        count_best_d = 0
        win_rate = 0
        for test_item in test_data:
            best_d = calcBestD(D, models, test_item)
            if best_d == test_item[d_idx]:
                win_rate += 1
            else:
                sum_best_d += abs(best_d - test_item[d_idx])
                count_best_d += 1
        accuracy.append(win_rate/len(test_data))
        mistake.append(sum_best_d/count_best_d)
    end_accuracy = sum(accuracy)/len(accuracy)
    end_mistake = sum(mistake)/len(mistake)
    print("Win rate:", end_accuracy)
    print("Average mistake:", end_mistake)

def main():
    red = 'winequality-red.csv'
    white = 'winequality-white.csv'
    white_test = 'winequality-white-test.csv'
    my_set = white
    print("60/40")
    test(my_set, 0.6)
    print("Cross validation")
    testCrossValidation(my_set, 5)

    # data, header = readFile(white)
    # data = convertDataToFloat(data)
    # mean, std = calculateOneModel(data, 1, 6)
    # print('mean', mean)
    # print('std', std)

if __name__ == '__main__':
    main()
