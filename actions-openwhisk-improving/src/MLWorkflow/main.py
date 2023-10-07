import numpy as np
import hashlib
import csv
import time
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import PolynomialFeatures

with open('log.csv', mode='w') as log_file:
    log_writer = csv.writer(log_file, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    log_writer.writerow(['func_name', 'hash_input', 'hash_output', 'duration'])


def log_csv(func):
    def wrapper(*args, **kwargs):
        input_str = str(args) + str(kwargs)
        input_hash = hashlib.md5(input_str.encode()).hexdigest()

        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start

        output_str = str(result)
        output_hash = hashlib.md5(output_str.encode()).hexdigest()

        with open('log.csv', mode='a') as log_file:
            log_writer = csv.writer(
                log_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            log_writer.writerow(
                [func.__name__, input_hash, output_hash, duration])

        return result

    return wrapper


# 简单的线性回归
@log_csv
def linear_regression(X, y):
    lr = LinearRegression()
    lr.fit(X, y)
    return lr.coef_

# 规则匹配
@log_csv
def rule_match(text, keyword):
    if keyword in text:
        return True
    else:
        return False

# 决策树
@log_csv
def decision_tree(X, y):
    # 将 y 转换为分类变量
    y = pd.cut(y.squeeze(), bins=2, labels=[0, 1])

    dt = DecisionTreeClassifier()
    dt.fit(X, y)
    return dt.predict(X)

# 特征转换
@log_csv
def feature_transform(X, y):
    poly = PolynomialFeatures(degree=2)
    X_poly = poly.fit_transform(X)
    lr = LinearRegression()
    lr.fit(X_poly, y)
    return lr.coef_
