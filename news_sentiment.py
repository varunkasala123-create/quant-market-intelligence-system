from newsapi import NewsApiClient
import numpy as np

newsapi = NewsApiClient(api_key="news api paste here")

def get_sentiment(symbol):

    try:

        articles = newsapi.get_everything(
            q=symbol,
            language="en",
            page_size=10
        )

        score = []

        for a in articles["articles"]:

            title = a["title"]

            if "beats" in title.lower():
                score.append(1)

            elif "miss" in title.lower():
                score.append(-1)

            else:
                score.append(0)

        if len(score)==0:
            return 0

        return np.mean(score)

    except:

        return 0