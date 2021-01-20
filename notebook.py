import requests
import pandas as pd
import time

df = pd.read_csv("techbloglist.csv")
urls = df.URL.values

hb_count = 'https://bookmark.hatenaapis.com/count/entry'
for idx, url in enumerate(urls):
    r = requests.get(hb_count, params={'url': url})
    # reduce api load
    time.sleep(0.5)

    print(r.text + "..." + r.url)

    # stop for test
    if idx <= 10:
        continue
    else:
        break