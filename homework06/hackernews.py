from bayes import NaiveBayesClassifier
from bottle import redirect, request, route, run, template
from db import News, session
from scraputils import get_news

try:
    bayes = NaiveBayesClassifier.load("data/model.bin")
except FileNotFoundError:
    bayes = NaiveBayesClassifier(alpha=0.05)


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template("news_template", rows=rows)


@route("/add_label/")
def add_label():

    label = request.query.label
    nid = request.query.id
    s = session()
    news = s.query(News).filter(News.id == nid).first()
    news.label = label
    s.commit()

    redirect("/news")


@route("/update")
def update_news():

    s = session()
    news = get_news("https://news.ycombinator.com/newest", 1)
    for i in news:
        if not s.query(News).filter(News.title == i["title"]).first():
            s.add(
                News(
                    title=i["title"],
                    author=i["author"],
                    url=i["url"],
                    comments=i["comments"],
                    points=i["points"],
                )
            )
    s.commit()

    redirect("/news")


@route("/recommendations")
def recommendations():

    s = session()
    news = s.query(News).filter(News.label == None).all()
    X = [i.title for i in news]
    y = bayes.predict(X)
    for i in range(len(news)):
        news[i].label = y[i]
    s.commit()
    return template("news_template", rows=news)


if __name__ == "__main__":
    run(host="localhost", port=1111, debug=False)
    bayes.save("data/model.bin")
