from bs4 import BeautifulSoup as BS
import requests

htmlText = requests.get("https://www.washingtonpost.com").text
soup = BS(htmlText, "html.parser")
def findAllNews():
    upperNews = soup.find_all("div", ["pb-f-homepage-story"])
    lowerNewsBlocks = soup.find_all("div", ["moat-trackable pb-f-theme-normal pb-f-dehydrate-false pb-f-async-false pb-feature pb-layout-item pb-f-homepage-card col-lg-3 col-sm-6 col-xs-12 col-md-4", "moat-trackable pb-f-theme-normal pb-f-dehydrate-false pb-f-async-false pb-feature pb-layout-item pb-f-homepage-card col-lg-3 col-sm-6 col-xs-12 col-md-4 first-in-chain-row"])

    allPosts = []

    for item in upperNews:
        themeItem = item.find("div", [" label label-normal label-small label-primary", " label label-normal label-primary"])
        if themeItem:
            theme = themeItem.text
        else:
            theme = "ОТСУТСТВУЕТ"

        contentItem = item.find("div", {"data-pb-field":"summary"})
        if contentItem:
            content = contentItem.text
        else:
            content = "ОТСУТСТВУЕТ"

        authorItem = item.find("li", ["byline"])
        if authorItem:
            author = authorItem.text
        else:
            author = "ОТСУТСТВУЕТ"

        titleItem = item.find("a", {"data-pb-field": "web_headline"})
        if titleItem:
            title = titleItem.text
            allPosts.append({"theme": theme, "content": content, "author": author, "title": title})


    for block in lowerNewsBlocks:
        lowerNews = block.find_all("li")
        for item in lowerNews:
            themeItem = item.find("div", ["section-label"])
            blockTheme = block.find("div", [" label label-normal label-small label-primary", " label label-normal label-primary"])
            theme = (blockTheme.text if blockTheme else "") + (": " + themeItem.text if themeItem else "")

            contentItem = item.find("div", {"data-pb-field": "summary"})
            if contentItem:
                content = contentItem.text
            else:
                content = "ОТСУТСТВУЕТ"

            authorItem = item.find("li", ["byline"])
            if authorItem:
                author = authorItem.text
            else:
                author = "ОТСУТСТВУЕТ"

            title = item.find("a", {"data-pb-field":"web_headline"}).text
            allPosts.append({"theme": theme, "content": content, "author": author, "title": title})

    return(allPosts)

allNews = findAllNews()
print("Всего новостей найдено: ", len(allNews), "\n")
for i in range(len(allNews)):
    print(" #{}\n Тематика: {}\n Заголовок: {}\n Автор: {}\n Содержание: {}\n".format(i + 1, allNews[i]["theme"], allNews[i]["title"], allNews[i]["author"], allNews[i]["content"]))


