import json
import pandas as pd

RANDOM_SEED = 42

data = []
with open('./original_datasets/DiverseVul/diversevul_20230702.json', 'r') as file:
    for line in file:
        data.append(json.loads(line))

df = pd.DataFrame(data)
df_vuln = df[df['target'] == 1]
df_vuln = df_vuln.sample(n=100, random_state=RANDOM_SEED)

df_vuln.to_csv('./raw_samples/diversevul_sample.csv')

df_secure = df[df['target'] == 0]
df_secure = df_secure.sample(n=30, random_state=RANDOM_SEED)

df_secure.to_csv('./raw_samples/diversevul_secure_sample.csv')