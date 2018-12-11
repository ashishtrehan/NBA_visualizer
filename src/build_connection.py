import requests
from lxml.html import fromstring
from itertools import cycle
import traceback


url = 'https://httpbin.org/ip'

proxies = {
    "http":"159.65.105.57:3128"
}

response = requests.get(url, proxies = proxies)

def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            # Grabbing IP and corresponding PORT
            url_str = './/td[{0}]/text()'
            proxy = ":".join([i.xpath(url_str.format(1))[0], i.xpath(url_str.format(2))[0]])
            proxies.add(proxy)
    return proxies


def proxy_cycling(url):
    proxies = get_proxies()
    proxy_pool = cycle(proxies)
    for i in range(1,len(proxies)):
        proxy = next(proxy_pool)
        print("Request {0}".format(i))
        try:
            response = requests.get(url, proxies={"http": proxy, "https": proxy})
            print(response.json())
        except:
            # Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work.
            # We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url
            print("Skipping. Connnection error")
    return

print (proxy_cycling(url))