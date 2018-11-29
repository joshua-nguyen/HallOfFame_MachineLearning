import math
import numpy as np

# Constants

    #confusion matrix
    # prediction -> p
    # actual -> a
    # p/a  F    T
    # F   0,0  0,1
    # T   1,0  1,1

    # TN = 0,0
    # TP = 1,1
    # FN = 0,1
    # FP = 1,0

TN = (0,0)
FN = (0,1)
FP = (1,0)
TP = (1,1)

def folds(data_set, start_column, end_column, target_column, num_folds, model):
    for fold in range(num_folds):
        chunk = math.floor(len(data_set)/num_folds)
        start = fold*chunk
        end = start+chunk

        data = np.copy(data_set[:,start_column:end_column])
        data = data.astype(float)
        target = np.copy(data_set[:,target_column])
        train_data = np.delete(data, np.s_[start:end], axis = 0)
        test_data = data[start:end]
        train_target = np.delete(target, np.s_[start:end], axis = 0)
        test_target = target[start:end]
        model.fit(train_data, train_target)

        subtotal = 0

        confusion = np.zeros([2, 2], dtype = int)
        for i in range(end-start):
            prediction = int(model.predict([test_data[i]])[0])
            actual = int(test_target[i])
            # print(prediction, actual)
            if prediction == 0 and actual == 0:
                confusion[0,0] += 1
            elif prediction == 1 and actual == 0:
                confusion[1,0] += 1
            elif prediction == 0 and actual == 1:
                confusion[0,1] += 1
            elif prediction == 1 and actual == 1:
                confusion[1,1] += 1
        
    return confusion

def precision(confusion):
    return confusion[TP] / (confusion[TP] + confusion[FP])

def recall(confusion):
    return confusion[TP] / (confusion[TP] + confusion[FN])

def accuracy(confusion):
    return (confusion[TP] + confusion[TN]) / (confusion[TP] + confusion[FP] + confusion[FN] + confusion[TN])

def f1_score(confusion):
    p = precision(confusion)
    r = recall(confusion)
    return 2 * (p * r) / (p + r)

def output_vector(confusion):
    return [
        confusion[TN],
        confusion[FN],
        confusion[FP],
        confusion[TP],
        accuracy(confusion),
        precision(confusion),
        recall(confusion),
        f1_score(confusion)
    ]
