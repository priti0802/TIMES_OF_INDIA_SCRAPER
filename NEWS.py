from bs4 import BeautifulSoup
from requests import get
import pandas as pd
from tqdm import tqdm
from dateutil import parser
import string

# Checking for the total no. of pages

url = 'https://timesofindia.indiatimes.com/topic/Sanitizer/news/'
soup = BeautifulSoup(get(url).text, 'lxml')

##Because the website displays ages only till 20
max_urls = [url + str(i) for i in range(1, 21)]

# Creating empty lists to save all the features
headlines, dates, news, urls = [], [], [], []

print("[INFO] Extracting links...")
# Extracting all the Headlines, dates and the urls of the articles
for index in max_urls:

    try:
        soup = BeautifulSoup(get(index).text, 'lxml')

        # Extracts the Headlines
        try:
            headline = [soup.select('span.title')[i].text.strip() for i in range(len(soup.select('span.title')))]
            print(headline)
            headlines.extend(headline)
        except:
            headlines.extend(None)

        # Extracts the published dates
        try:
            pub_date = [str(parser.parse(soup.select('span.meta')[0].text)).split()[0] for i in
                        range(len(soup.select('span.meta')))]
            dates.extend(pub_date)
        except:
            dates.extend(None)

        # Extracts the urls
        try:
            source = ['https://timesofindia.indiatimes.com' + soup.select('.content')[i].a['href'] for i in
                      range(len(soup.select('span.meta')))]
            urls.extend(source)
        except:
            urls.extend(None)

    except:
        break

print("[INFO] Links Extracted.")

print("The total no. of pages is=", len(urls))
# print(set(dates))
print("No. articles=", len(dates))
print("Last article goes back till: ", min(dates))

print("[INFO] Extracting articles...")
c = 0
for index in tqdm(urls):
    try:
        # Parse the url to NewsPlease
        soup = BeautifulSoup(get(index).text, 'lxml')

        # Extracts the news articles
        try:
            news_article = ''.join(
                i for i in ' '.join(soup.select_one('._3WlLe').text.split()) if i in string.printable)
            c += 1
            print(c)
            news.append(news_article)
        except:
            news.append(None)

    except:
        news.append(None)

print("[INFO] Articles Extracted.")

df = pd.DataFrame({'Headlines': headlines,
                   'Article': news,
                   'Published_Dates': dates,
                   'Source_URLs': urls
                   })
# Checking for any missing values in the Dataframe
# print(df.isna().sum())


# Now also dropping all the other rows with empty values
# df=df.dropna(axis = 0)
print("Length: ", df.shape)

df.to_csv("export.csv")