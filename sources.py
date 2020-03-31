df = pd.read_excel("hashtags_raw.xlsx")

df.reset_index(inplace=True)
df['Sources'][0]
Updated_source = []
for i in range(len(df)):
    Updated_source.append(str(df['Sources'][i]).partition('>')[-1].rpartition('<')[0])

df['Updated_source'] = Updated_source    


df.to_excel("hashtags_raw_source.xlsx")