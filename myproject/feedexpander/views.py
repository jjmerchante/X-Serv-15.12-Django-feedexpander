from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
import feedparser
from BeautifulSoup import BeautifulSoup
import urllib2
from urlparse import urlparse


# Change the path of the src
def change_src(img_src, url):
    src = ""
    if img_src.startswith('http'):
        src = img_src
    elif img_src.startswith('/'):
        urlParsed = urlparse(url)
        src = urlParsed[0] + "://" + urlParsed[1] + img_src
    else:
        if url.endswith("/"):
            src = url + img_src
        else:
            src = url + "/" + img_src
    return src


# Returns the first p and the images of the url
def getContent(url):
    try:
        f = urllib2.urlopen(url)
        url = f.geturl()
        html = f.read()
        soup = BeautifulSoup(html)
        firstP = soup.p
        imagesList = soup.findAll('img')
        imgsHtml = ""
        for img in imagesList:
            img['src'] = change_src(img['src'], url)
            imgsHtml += "<img src ='" + img['src'] + "'>" + "<br/>\n"
        return str(firstP) + "<br/>\n" + imgsHtml
    except:
        print "Url error: " + url
        return "Content not found"


# Returns httplinks in a list
def getHttpLinks(tuits):
    httpLinks = []
    list = tuits.split()
    for str in list:
        if str.startswith("http://") or str.startswith("https://"):
            url = str.split('&')[0]
            httpLinks.append(url)
    return httpLinks


def tweets(request, user):
    url = "http://twitrss.me/twitter_user_to_rss/?user=" + user
    dict = feedparser.parse(url)
    tuits = "<ul>\n"
    for i in range(5):
        try:
            tuit = dict.entries[i].summary
            httpLinksList = getHttpLinks(tuit)
            httpContentLinks = ""
            for link in httpLinksList:
                print "URL: <" + link + ">"
                contentLink = getContent(link)
                httpContentLinks += "<li>" + link + "</li>\n<ul>\n" + \
                    contentLink + "</ul>\n"
            tuits += "<li>" + tuit + "</li>\n<ul>\n" + \
                httpContentLinks + "</ul>\n"
        except IndexError:
            break
    tuits += "</ul>\n"
    return HttpResponse(tuits)


def notFound(request):
    return HttpResponseNotFound("Page not found")
