import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import numpy as np

def decision_tree(X, y):
    # 将 y 转换为分类变量
    y = pd.cut(y.squeeze(), bins=2, labels=[0, 1])

    dt = DecisionTreeClassifier()
    dt.fit(X, y)
    return dt.predict(X).tolist()


def main(args):
    X = args.get('X', np.random.rand(50, 10))
    y = args.get('y', np.random.rand(50, 1))
    if isinstance(X, list):
        X = np.array(X)
    if isinstance(y, list):
        y = np.array(y)
    return {"prediction": decision_tree(X, y)}

if __name__=="__main__":
    params = {
            "X": np.random.rand(10, 10).tolist(),
            "y": np.random.rand(10, 1).tolist()
    }
    print(main(params))