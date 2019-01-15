from django.shortcuts import render
from bs4 import BeautifulSoup
from konlpy.tag import Twitter
from collections import Counter
import requests


# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def result(request):
    text = parse(request.GET['keyword'])
    words = text.split()

    nlpy = Twitter()
    nouns = nlpy.nouns(text)
    count = Counter(nouns)

    tag_count = []
    tags = []

    for n, c in count.most_common(100):
        dics = {'tag': n, 'count': c}
        if len(dics['tag']) >= 2 and len(tags) <= 49:
            tag_count.append(dics)
            tags.append(dics['tag'])

    return render(request, 'result.html', {'keyword': request.GET['keyword'], 'full': text, 'wordCount': len(words), 'tags': tag_count})

def parse(keyword):
    url = 'https://ko.wikipedia.org/wiki/' + keyword
    req = requests.get(url)
    req.encoding=None
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    urlInfo = soup.select(
        'div#mw-content-text'
    )

    for n in urlInfo:
        content = n.text

    return content
