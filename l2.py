import re
import requests

domain = "siblogistics.ru"

def getAllEmails(links):
    allEmails = set({})
    regex = "[a-zA-Z0-9_.]+@[a-zA-Z0-9_.]+\.[a-zA-Z0-9_.]+"
    for l in links:
        allEmails = allEmails | set(re.findall(regex, requests.get(l).text))
    return allEmails

def getAllInnerLinks(linksToSeekThrough, parsedLinks):
    newLinks = set({})
    for l in linksToSeekThrough:
        hrefs = re.findall('href="/.*?"', requests.get(l).text)
        links = {
                "http://" + domain + "/" + h[7:len(h) - 1] + "/"
                for h in hrefs
                if h[6] == "/"
                }
        newLinks = newLinks | links
        print(l, ": ", links)
    nextLinks = [x for x in newLinks if x not in parsedLinks]
    parsedLinks = parsedLinks + nextLinks
    if len(nextLinks) > 0:
        getAllInnerLinks(nextLinks, parsedLinks)
    return parsedLinks

allLinks = getAllInnerLinks(linksToSeekThrough=["http://" + domain + "/"], parsedLinks=["http://" + domain + "/"])
allLinksFile = open("allLinks.txt", "w")
print("all links: ", allLinks)
allLinksFile.write("\n".join(allLinks))
allLinksFile.close()
allEmails = getAllEmails(allLinks)
print("all emails: ", allEmails)
allEmailsFile = open("allEmails.txt", "w")
allEmailsFile.write("\n".join(allEmails))
allEmailsFile.close()
