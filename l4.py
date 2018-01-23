from bs4 import BeautifulSoup as BS
import requests
import threading
import time
from queue import Queue
from l3 import findAllNews

def threadFunction(newsQueue):
    seenNewsTitles = set({})

    while True:
        allNews = findAllNews()
        newNews = []
        for n in allNews:
            if n["title"] not in seenNewsTitles:
                newNews.append(n)
        seenNewsTitles = seenNewsTitles | set([x["title"] for x in newNews])
        if len(newNews) == 0:
            print("Нет новых новостей")
        for n in newNews:
            newsQueue.put(n)
        time.sleep(10)

idx = 0
newsQueue = Queue()
thread = threading.Thread(target=threadFunction, args=(newsQueue,))
thread.start()

while True:
    newsItem = newsQueue.get()
    print("#{}\n Тематика: {}\n Заголовок: {}\n Автор: {}\n Содержание: {}\n".format(idx + 1,
                                                                                     newsItem["theme"],
                                                                                     newsItem["title"],
                                                                                     newsItem["author"],
                                                                                     newsItem["content"]))
    idx += 1



