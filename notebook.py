from typing import Dict, List
import requests
import json
import pandas as pd
import time
from typing import TypedDict


class Company(TypedDict):
    company_name: str
    hatebu_count: str
    url: str


df = pd.read_csv("techbloglist.csv", usecols=['company_name', 'url'])
endpoint = 'https://bookmark.hatenaapis.com/count/entry'
values: List[Company] = []
for idx, row in enumerate(df.itertuples()):
    r = requests.get(endpoint, params={'url': row.url})
    hatebu_count = r.text

    company: Company = {
        'company_name': row.company_name,
        'hatebu_count': hatebu_count,
        'url': row.url
    }

    values.append(company)
    # reduce api load
    time.sleep(0.5)

with open('hatebucount.json', 'w') as file:
    json.dump(values, file, indent=4, ensure_ascii=True)