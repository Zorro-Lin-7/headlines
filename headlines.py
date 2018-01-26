from flask import Flask
import feedparser


app = Flask(__name__)

BBC_FEED = 'http://feeds.bbci.co.uk/news/rss.xml'


@app.route("/")
def get_news():
    feed = feedparser.parse(BBC_FEED) # return a dict
    entries = feed['entries']  # return a list
    first_article = entries[0] # return a dict
    return """
    <html>
        <body>
            <h1> BBC Headlines </h1>
            <b>{0}</b> <br />
            <i>{1}</i> <br />
            <p>{2}</p> <br />
        </body>
    </html>""".format(first_article.get('title'),
                      first_article.get('published'),
                      first_article.get('summary'))

if __name__ == '__main__':
    app.run(port=5000, debug=True)