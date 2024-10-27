import joblib
import numpy as np
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
# import tensorflow as tf

class Recommend:
    def __init__(self):
        with open('rf_model.joblib', 'rb') as file:
            self.model = joblib.load(file)
        self.difficulties = []
        self.correct_answers = []
        self.X = None

    def prepare_sequence(self, X):
        difficulty = []
        for i,j in enumerate(X):
            difficulty.append(X[i][0])
            self.correct_answers.append(X[i][1])
        self.difficulties = np.array(difficulty) / 10.0
        self.X = np.column_stack((self.difficulties, self.correct_answers))
        self.X = self.X.reshape((1, 5, 2))

    def predict_next_difficulty(self, X):
        length = len(X)
        if length in (0, 1, 2):
            return 5
        elif length == 3:
            X.insert(0, (5, 0))
            X.insert(0, (5, 1))
        elif length == 4:
            avg_diff = 0
            avg_correctness = 0
            for i,j in enumerate(X):
                avg_diff += X[i][0]
                avg_correctness += X[i][1]
            X.insert(0, (round(avg_diff/length), round(avg_correctness/length)))
        elif length > 5:
            while len(X) > 5:
                del X[0]
        print(X)
        self.prepare_sequence(X)
        prediction = self.model.predict(self.X, verbose=0)[0][0]
        return round(prediction * 10)
    
# r = Recommend()
# X = [(4, 1), (5, 1), (6, 1), (6, 1), (6, 1), (7, 1), (8, 1), (10, 1), (10, 1)]
# print(r.predict_next_difficulty(X))
