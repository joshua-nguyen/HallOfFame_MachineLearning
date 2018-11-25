import math
import numpy as np

def folds(data_set, num_folds, start_column, end_column, target_column, model):
    fold_classification_total = 0
    for fold in range(num_folds):
        chunk = math.floor(len(table)/num_folds)
        start = fold*chunk
        end = start+chunk

        data = np.copy(data_set[:,start_column:end_column])
        target = np.copy(data_set[:,target_column])
        train_data = np_delete(data, np.s_[start:end], axis = 0)
        test_data = data[start:end]
        train_target = np_delete(target, np.s_[start:end], axis = 0)
        test_target = target[start:end]
        model.fit(train_data, train_target)

        subtotal = 0
        for i in range(end-start):
            if model.predict([test_data[i]]) == test_target[i]:
                subtotal += 1
        fold_mean = subtotal / chunk
        fold_classification_total += fold_mean
    return fold_classification_total / num_folds

