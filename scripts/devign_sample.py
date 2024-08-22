import json
import pandas as pd

RANDOM_SEED = 42

df = pd.read_json('./original_datasets/Devign/function.json')

df_vuln = df[df['target'] == 1]
df_vuln = df_vuln.sample(n=100, random_state=RANDOM_SEED)

df_vuln.to_csv('./raw_samples/devign_sample.csv')

df_secure = df[df['target'] == 0]
df_secure = df_secure.sample(n=30, random_state=RANDOM_SEED)

df_secure.to_csv('./raw_samples/devign_secure_sample.csv')