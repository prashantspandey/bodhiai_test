import pandas as pd

df = pd.read_csv('square_cube_root.csv')
links = df['QuestionLink']
links2 = []
for i in links:
    links2.append(str(i)+'.png')
df['QuestionLink'] = links2
print(df['QuestionLink'])
df.to_csv('square_cube_roots.csv')
