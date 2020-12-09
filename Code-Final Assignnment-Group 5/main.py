# Web scrapping from reviews of movies from Rotten Tomatoes
# Movie: Hillbilly Elegy
# Import libraries
import requests
from bs4 import BeautifulSoup
import re
import pymongo
import ssl

# SA: vadar sentiment analyzer library
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# SA: sentiment analyzer instance
analyser = SentimentIntensityAnalyzer()

# Collect first page of artists’ list (Collecting and Parsing data)
page = requests.get('https://www.rottentomatoes.com/m/you_me_and_dupree/reviews')

# Create a BeautifulSoup object
soup = BeautifulSoup(page.text, 'html.parser')

# Pull all text from the review
dupree = soup.find(class_='review_table')

# Remove tag <span>
for match in dupree.findAll('span'):
    match.unwrap()

# Pull text from all instances of <h6> tag within BodyText div
dupree_review = dupree.find_all(class_='the_review')

# Pull text from all instances of 'cast' tag within BodyText div
dupree_date = dupree.find_all(class_='review-date subtle small')

# Pull text from all instances of 'genre' tag within BodyText div
dupree_critic = dupree.find_all(class_='unstyled bold articleLink')

comments = []
for review in dupree_review:
    rev = review.contents[0]
    rev = re.sub('\r\n', '', rev)
    comments.append(rev)

dates = []
for date in dupree_date:
    dat = date.contents[0]
    dat = re.sub('\r\n', '', dat)
    dates.append(dat)

critics = []
for critic in dupree_critic:
    crit = critic.contents[0]
    crit = re.sub('\r\n', '', crit)
    critics.append(crit)

# Collect first page of artists’ list (Collecting and Parsing data)
page = requests.get('https://www.rottentomatoes.com/m/you_me_and_dupree/reviews?type=&sort=&page=2')

# Create a BeautifulSoup object
soup = BeautifulSoup(page.text, 'html.parser')

# Pull all text from the review
dupree = soup.find(class_='review_table')

# Remove tag <span>
for match in dupree.findAll('span'):
    match.unwrap()

# Pull text from all instances of <h6> tag within BodyText div
dupree_review = dupree.find_all(class_='the_review')

# Pull text from all instances of 'cast' tag within BodyText div
dupree_date = dupree.find_all(class_='review-date subtle small')

# Pull text from all instances of 'genre' tag within BodyText div
dupree_critic = dupree.find_all(class_='unstyled bold articleLink')

for review in dupree_review:
    rev = review.contents[0]
    rev = re.sub('\r\n', '', rev)
    comments.append(rev)

for date in dupree_date:
    dat = date.contents[0]
    dat = re.sub('\r\n', '', dat)
    dates.append(dat)

for critic in dupree_critic:
    crit = critic.contents[0]
    crit = re.sub('\r\n', '', crit)
    critics.append(crit)

# Collect first page of artists’ list (Collecting and Parsing data)
page = requests.get('https://www.rottentomatoes.com/m/you_me_and_dupree/reviews?type=&sort=&page=3')

# Create a BeautifulSoup object
soup = BeautifulSoup(page.text, 'html.parser')

# Pull all text from the review
dupree = soup.find(class_='review_table')

# Remove tag <span>
for match in dupree.findAll('span'):
    match.unwrap()

# Pull text from all instances of <h6> tag within BodyText div
dupree_review = dupree.find_all(class_='the_review')

# Pull text from all instances of 'cast' tag within BodyText div
dupree_date = dupree.find_all(class_='review-date subtle small')

# Pull text from all instances of 'genre' tag within BodyText div
dupree_critic = dupree.find_all(class_='unstyled bold articleLink')

for review in dupree_review:
    rev = review.contents[0]
    rev = re.sub('\r\n', '', rev)
    comments.append(rev)

for date in dupree_date:
    dat = date.contents[0]
    dat = re.sub('\r\n', '', dat)
    dates.append(dat)

for critic in dupree_critic:
    crit = critic.contents[0]
    crit = re.sub('\r\n', '', crit)
    critics.append(crit)

reviews_dupree = []
for i in range(0, 59):
    record = []
    record.append('You, me and Dupree')
    record.append(critics[i])
    record.append(dates[i])
    record.append(comments[i])

    # SA: appending compound scores and categories
    sentiment_rev = analyser.polarity_scores(comments[i])
    record.append(sentiment_rev['compound'])

    # SA: Classificatin of compound score
    if sentiment_rev['compound'] >= 0.05:
        record.append('Positive')
    elif sentiment_rev['compound'] <= - 0.05:
        record.append('Negative')
    else:
        record.append('Neutral')

    reviews_dupree.append(record)

reviews_dupree

for record in reviews_dupree:
    movie_name = record[0]
    critic_name = record[1]
    date = record[2]
    comment = record[3]
    polarity = record[4]
    sentiment = record[5]

    print(movie_name)

    client = pymongo.MongoClient("mongodb+srv://vishal:panchal@cluster0.lwyjh.mongodb.net/reviews?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
    db = client.reviews
    review_table = db["reviews"]

    json = {
        "movie_name": movie_name,
        "critic_name": critic_name,
        "date": date.strip(),
        "comment": comment.strip(),
        "polarity": polarity,
        "sentiment": sentiment
    }
    review_table.insert_one(json)
