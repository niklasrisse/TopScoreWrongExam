import json
import pandas as pd

RANDOM_SEED = 42

df = pd.read_csv('./original_datasets/BigVul/MSR_data_cleaned.csv')
print(df.columns)

df_vuln = df[df['vul'] == 1]
df_vuln = df_vuln.sample(n=100, random_state=RANDOM_SEED)

df_vuln.to_csv('./raw_samples/bigvul_sample.csv')

df_secure = df[df['vul'] == 0]
df_secure = df_secure.sample(n=30, random_state=RANDOM_SEED)

df_secure.to_csv('./raw_samples/bigvul_secure_sample.csv')