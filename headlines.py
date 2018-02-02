import feedparser
from flask import Flask
from flask import render_template
from flask import request    # for Flask's request context
import json
import urllib

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
            'cnn': 'http://rss.cnn.com/rss/edition.rss',
            'fox': 'http://feeds.foxnews.com/foxnews/latest',
            'iol': 'http://www.iol.co.za/cmlink/1.640'}

DEFAULTS = {'publication': 'bbc',
            'city': 'London,UK'}

@app.route("/")
def home():
    publication = request.args.get('publication')
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)
    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)
    return render_template('home.html', articles=articles, weather=weather)


def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS["publication"]
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication]) # return a dict
    entries = feed['entries']  # return a list
    #first_article = entries[0] # return a dict
    return entries


def get_weather(query):  # query 指定查询某一城市（的天气）
    api_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=26f21a04122e72113ff3977ee7cf7977'# 加API Key
    query = urllib.parse.quote(query)  # 处理url中的特殊符号，使符合url编码，如空格转换为"%20"
    url = api_url.format(query)
    data = urllib.request.urlopen(url).read() # return JSON string
    parsed = json.loads(data) # load string to convert into a Dict
    weather = None  # 技巧，设一个空变量
    if parsed.get("weather"):
        weather = {"description": parsed['weather'][0]['description'],  # 生成一个字典并返回
                    "temperature": parsed['main']['temp'],
                    'city': parsed['name']}
    return weather
    
if __name__ == '__main__':
    app.run(port=5000, debug=True)