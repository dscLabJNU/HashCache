from sklearn.linear_model import LinearRegression
import numpy as np

def linear_regression(X, y):
    lr = LinearRegression()
    lr.fit(X, y)
    return lr.coef_.tolist()


def main(args):
    X = args.get('X', np.random.rand(5, 5))
    y = args.get('y', np.random.rand(5, 1))
    return {"coef": linear_regression(X, y)}
