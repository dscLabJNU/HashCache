import numpy as np


def rule_match(text, keyword):
    if keyword in text:
        return True
    else:
        return False


def main(args):
    keywords = ['apple', 'banana', 'cherry', 'date', 'elderberry']
    texts = ['This is a text about apple', 'The banana is ripe', 'Cherry pie is my favorite',
             'Dates are high in sugar']

    keyword = args.get('keyword', np.random.choice(keywords))
    text = args.get('text', np.random.choice(texts) +
                    " ".join(np.random.choice(keywords, 1)))
    return {"match": rule_match(text, keyword)}
