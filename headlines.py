import feedparser
from flask import Flask
from flask import render_template
from flask import request    # for Flask's request context
import json
import urllib
import urllib2

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
            'cnn': 'http://rss.cnn.com/rss/edition.rss',
            'fox': 'http://feeds.foxnews.com/foxnews/latest',
            'iol': 'http://www.iol.co.za/cmlink/1.640'}


@app.route("/")
def get_news():
    query = request.args.get('publication')
    if not query or query.lower() not in RSS_FEEDS:
        publication = 'bbc'
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication]) # return a dict
    entries = feed['entries']  # return a list
    weather = get_weather("London,UK")
    #first_article = entries[0] # return a dict
    return render_template('home.html',
                            articles=entries,
                            weather=weather)


def get_weather(query):
    api_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid='# 加API Key
    query = urllib.quote(query)
    url = api_url.format(query)
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {"description": parsed['weather'][0]['description'],  # 生成一个字典并返回
                    "temperature": parsed['main']['temp'],
                    'city': parsed['name']}
    return weather
    
if __name__ == '__main__':
    app.run(port=5000, debug=True)