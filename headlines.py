from flask import Flask
from flask import render_template
import feedparser
from flask import request    # for Flask's request context


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
    #first_article = entries[0] # return a dict
    return render_template('home.html',articles=entries)

if __name__ == '__main__':
    app.run(port=5000, debug=True)