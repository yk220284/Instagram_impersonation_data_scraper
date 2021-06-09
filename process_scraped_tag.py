import pandas as pd

df = pd.read_csv("fake_account_posts.csv")
print(df.size)
print(df['code'].unique().size)
