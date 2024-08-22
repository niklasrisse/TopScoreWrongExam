import os
import random
import pandas as pd
import numpy as np

from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from transformers import AutoTokenizer

from collections import Counter

from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

fixed_seed = 42

os.environ['PYTHONHASHSEED'] = str(fixed_seed)
np.random.seed(fixed_seed)
random.seed(fixed_seed)

my_tokenizer = AutoTokenizer.from_pretrained("microsoft/unixcoder-base-nine")

devign_data = pd.read_json('./original_datasets/Devign/function.json')

train_index, test_index = train_test_split(range(len(devign_data)), test_size=0.2, random_state=fixed_seed)

m1 = devign_data.iloc[train_index]
m2 = devign_data.iloc[test_index]

def encodeDataframe(df, tokenizer):
    vocabulary = tokenizer.get_vocab()
    max_vocab_index = max(vocabulary.values())
    word_counts = []
    labels = df.target.tolist()
    
    for sentence in df.func.tolist():
        tokens = tokenizer.tokenize(sentence)
        token_ids = tokenizer.convert_tokens_to_ids(tokens)
        count = Counter(token_ids)
        count_vector = [0] * (max_vocab_index + 1)
        for idx, cnt in count.items():
            if idx <= max_vocab_index:
                count_vector[idx] = cnt
        word_counts.append(count_vector)

    return word_counts, labels


X_train, y_train = encodeDataframe(m1, my_tokenizer)
X_test, y_test = encodeDataframe(m2, my_tokenizer)

clf = HistGradientBoostingClassifier(learning_rate=0.3, max_depth=10, max_iter=200, min_samples_leaf=20)

clf.fit(X_train, y_train)

y_test_pred = clf.predict(X_test)

test_accuracy = accuracy_score(y_test, y_test_pred)
print("Test Accuracy:", test_accuracy)