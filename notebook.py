import requests
import json
import pandas as pd
import time

df = pd.read_csv("techbloglist.csv", usecols=['company_name', 'url'])
endpoint = 'https://bookmark.hatenaapis.com/count/entry'
values = []
for row in df.itertuples():
    r = requests.get(endpoint, params={'url': row.url})
    hatebu_count = int(r.text)
    values.append([row.company_name, hatebu_count, row.url])
    # reduce api load
    time.sleep(0.5)

with open('hatebucount.json', 'w') as file:
    json.dump(values, file)
