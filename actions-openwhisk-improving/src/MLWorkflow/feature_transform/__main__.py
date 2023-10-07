from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import numpy as np


def feature_transform(X, y):
    poly = PolynomialFeatures(degree=2)
    X_poly = poly.fit_transform(X)
    lr = LinearRegression()
    lr.fit(X_poly, y)
    return lr.coef_.tolist()

def main(args):
    X = args.get('X', np.random.rand(5, 2))
    if isinstance(X, list):
        X = np.array(X)
    y = args.get('y', np.sin(X[:, 0] + X[:, 1]))
    return {"coef": feature_transform(X, y)}

if __name__=="__main__":
    X = np.random.rand(5, 2)
    y = np.sin(X[:, 0] + X[:, 1])
    params = {
        "X": X.tolist(),
        "y": y.tolist()
    }
    print(main(params))