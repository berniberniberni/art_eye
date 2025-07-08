import pandas as pd
import os
import requests

# Load MET dataset directly from GitHub
df = pd.read_csv("https://media.githubusercontent.com/media/metmuseum/openaccess/master/MetObjects.csv")

# Filter by public domain and object type
filtered = df[
    (df['Is Public Domain']) &
    (df['Image URL'].notnull()) &
    (df['Object Name'].str.contains("textile|painting|print", case=False, na=False))
].head(10)

os.makedirs("images/raw", exist_ok=True)

for i, row in filtered.iterrows():
    url = row['Image URL']
    title = str(row['Title']).replace(" ", "_").replace("/", "_")[:50]
    filename = f"images/raw/{title}_{i}.jpg"
    try:
        r = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(r.content)
        print(f"Downloaded: {filename}")
    except:
        print(f"Failed: {url}")