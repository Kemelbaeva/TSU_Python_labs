import re
import requests

regex = "[a-zA-Z0-9_.]+@[a-zA-Z0-9_.]+\.[a-zA-Z0-9_.]+"

addresses = set(re.findall(regex, requests.get("http://www.mosigra.ru/").text))

print(addresses)
