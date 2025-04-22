import os
import random
import pandas as pd
import numpy as np

from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from transformers import AutoTokenizer

from collections import Counter

from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score

from tqdm import tqdm  # Import tqdm for progress bars

import json

fixed_seed = 42

os.environ['PYTHONHASHSEED'] = str(fixed_seed)
np.random.seed(fixed_seed)
random.seed(fixed_seed)

os.environ["TOKENIZERS_PARALLELISM"] = "false"

my_tokenizer = AutoTokenizer.from_pretrained("microsoft/unixcoder-base-nine")

data = []
with open('./original_datasets/DiverseVul/diversevul_20230702.json', 'r') as file:
    for line in file:
        data.append(json.loads(line))

data = pd.DataFrame(data)

train_index, test_index = train_test_split(range(len(data)), test_size=0.5, random_state=fixed_seed)

m1 = data.iloc[train_index]
m2 = data.iloc[test_index]

def encodeDataframe(df, tokenizer):
    vocabulary = tokenizer.get_vocab()
    max_vocab_index = max(vocabulary.values())
    word_counts = []
    labels = df.target.tolist()
    
    # Use tqdm to show progress for the main loop
    for sentence in tqdm(df.func.tolist(), desc="Encoding sentences"):
        tokens = tokenizer.tokenize(sentence)
        token_ids = tokenizer.convert_tokens_to_ids(tokens)
        count = Counter(token_ids)
        count_vector = [0] * (max_vocab_index + 1)
        for idx, cnt in count.items():
            if idx <= max_vocab_index:
                count_vector[idx] = cnt
        word_counts.append(count_vector)

    return word_counts, labels

print("started encoding")

X_train, y_train = encodeDataframe(m1, my_tokenizer)
X_test, y_test = encodeDataframe(m2, my_tokenizer)

print("finished encoding")

clf = HistGradientBoostingClassifier(learning_rate=0.3, max_depth=10, max_iter=200, min_samples_leaf=20)

print("initiated model")

clf.fit(X_train, y_train)

print("fitted model")

y_test_pred = clf.predict(X_test)

print("predicted")

test_accuracy = f1_score(y_test, y_test_pred)
print("Test F1:", test_accuracy)