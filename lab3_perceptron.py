import numpy as np


class Perceptron:
    def __init__(self, inputs, outputs, init_weights=None):
        self.inputs = inputs
        self.outputs = outputs
        if init_weights is not None:
            self.weights = init_weights
        else:
            self.weights = np.random.rand(len(self.inputs[0]))
        self.bias = np.random.rand()

    @staticmethod
    def threshold_func(x):
        return 0 if x < 0 else 1

    def train(self, learning_rate=0.05):
        trained = False
        str_fl = '{:^7.2f}'
        str_int = '{:^7}'
        pattern_names = str_int * 10 + '{:^10}' + str_int * 3 + '{:^6}'
        pattern_values = str_fl * 4 + str_int * 3 + str_fl + str_int * 2 + '{:^10.2f}{:^7.2f}{:^7.2f}{:^7.2f}{:^6.2f}'
        print(pattern_names.format('w1', 'w2', 'w3', 'θ', 'x1', 'x2', 'x3', 'a', 'Y', 'T', 'η(T-Y)',
                                   'δw1', 'δw2', 'δw3', 'δθ'))
        while not trained:
            trained = True
            error = 0
            for X, y_expected in zip(self.inputs, self.outputs):
                a = np.dot(X, self.weights) + self.bias
                y = self.threshold_func(a)
                delta = y_expected - y
                if delta != 0:
                    self.weights = np.array([weight + learning_rate * delta * x for weight, x in zip(self.weights, X)])
                    self.bias += learning_rate * delta
                    trained = False
                w1, w2, w3 = self.weights
                print(pattern_values.format(w1, w2, w3, self.bias, X[0], X[1], X[2], a, y, y_expected,
                                            learning_rate * delta, delta * w1, delta * w2, delta * w3,
                                            delta * self.bias))
                error += abs(delta)
            print('Error: ', error)


def test_perceptron():
    # Generating truth table
    inputs = [[1 if num & (1 << (2 - i)) else 0 for i in range(3)] for num in range(8)]
    # Generating outputs for logical function
    outputs = [1 if (not x1 or x2) and x3 else 0 for [x1, x2, x3] in inputs]

    p = Perceptron(inputs, outputs, [.02, .05, .4])
    p.train()


test_perceptron()
