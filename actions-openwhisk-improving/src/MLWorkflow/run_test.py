import numpy as np
from main import linear_regression, rule_match, decision_tree, feature_transform


def generate_test_cases():
    test_cases = []

    # 线性回归测试用例
    for i in range(100):
        test_cases.append(generate_linear_regression_test_case())

    # 规则匹配测试用例
    for i in range(100):
        test_cases.append(generate_rule_match_test_case())

    # 决策树测试用例
    for i in range(100):
        test_cases.append(generate_decision_tree_test_case())

    # 特征转换测试用例
    for i in range(100):
        test_cases.append(generate_feature_transform_test_case())

    return test_cases


def generate_linear_regression_test_case():
    # 生成具有10个特征和50个样本的随机数据集
    X = np.random.rand(5, 5)
    y = np.random.rand(5, 1)
    return (linear_regression, (X, y), None)


def generate_rule_match_test_case():
    # 生成包含噪声的文本数据
    keywords = ['apple', 'banana', 'cherry', 'date', 'elderberry']
    texts = ['This is a text about apple', 'The banana is ripe', 'Cherry pie is my favorite',
             'Dates are high in sugar']
    keyword = np.random.choice(keywords)
    text = np.random.choice(texts) + " ".join(np.random.choice(keywords, 1))
    return (rule_match, (text, keyword), None)


def generate_decision_tree_test_case():
    # 生成具有高维特征的数据集
    X = np.random.rand(5, 10)
    y = np.random.rand(5, 1)
    return (decision_tree, (X, y), None)


def generate_feature_transform_test_case():
    # 生成具有非线性结构的数据集
    X = np.random.rand(5, 2)
    y = np.sin(X[:, 0] + X[:, 1])
    return (feature_transform, (X, y), None)


def run_tests(test_cases):
    for i, (func, args, expected) in enumerate(test_cases):
        result = func(*args)
        if expected is not None:
            assert result == expected, f"Test case {i} failed: expected {expected}, but got {result}."
        else:
            print(f"Test case {i} succeeded.")


test_cases = generate_test_cases()
run_tests(test_cases)
