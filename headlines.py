import datetime
import feedparser
from flask import Flask
from flask import make_response
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
            'city': 'London,UK',
            'currency_from': 'GBP',
            'currency_to': 'USD'
            }

WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=26f21a04122e72113ff3977ee7cf7977'# 加API Key
CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id=9593551754524eba911fca081a9e6628"

@app.route("/")
def home():
    # get customised headlines, based on user input or default
    publication = get_value_with_fallback("publication")
    articles = get_news(publication)
    
    # get customised weather based on user input or default
    city = get_value_with_fallback('city')
    weather = get_weather(city)
    
    # get customised currency based on user input or default
    currency_from = get_value_with_fallback('currency_from')
    currency_to = get_value_with_fallback('currency_to')
    rate, currencies = get_rate(currency_from, currency_to)
    
    # save cookies and return template
    response = make_response(render_template('home.html',
                           articles=articles,
                           weather=weather,
                           currency_from=currency_from,
                           currency_to=currency_to,
                           rate=rate,
                           currencies=sorted(currencies)))
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie("publication", publication, expires=expires)
    response.set_cookie("city", city, expires=expires)
    response.set_cookie("currency_from", currency_from, expires=expires)
    response.set_cookie("currency_to", currency_to, expires=expires)
    return response


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
    query = urllib.parse.quote(query)  # 处理url中的特殊符号，使符合url编码，如空格转换为"%20"
    url = WEATHER_URL.format(query)
    data = urllib.request.urlopen(url).read() # return JSON string
    parsed = json.loads(data) # load string to convert into a Dict
    weather = None  # 技巧，设一个空变量
    if parsed.get("weather"):
        weather = {"description": parsed['weather'][0]['description'],  # 生成一个字典并返回
                    "temperature": parsed['main']['temp'],
                    'city': parsed['name'],
                    'country': parsed['sys']['country']
                    }
    return weather
    

def get_rate(frm, to):
    all_currency = urllib.request.urlopen(CURRENCY_URL).read()
    parsed = json.loads(all_currency).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return (to_rate/frm_rate, parsed.keys())


def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS[key]


if __name__ == '__main__':
    app.run(port=5000, debug=True)