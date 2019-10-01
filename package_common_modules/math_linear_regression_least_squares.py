'''
'''
import numpy as np
import matplotlib.pylab as plt

def math_linear_regression_least_squares(x, y):

    m = (len(x) * np.sum(x*y) - np.sum(x) * np.sum(y)) / (len(x)*np.sum(x*x) - np.sum(x) * np.sum(x))
    b = (np.sum(y) - m *np.sum(x)) / len(x)
    return m * x + b, m, b


if __name__ == '__main__':

    x = np.array([1,2,3,4,5,6,7,8])
    y = np.array([15,32,66,45,90,153,170,200])
    predict, weight, bias = math_linear_regression_least_squares(x, y)

    plt.scatter(x, y)
    plt.plot(x, predict)
    plt.show()
