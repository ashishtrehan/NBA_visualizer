import requests
import redis
import os
from lxml.html import fromstring
from itertools import cycle
import logging
import traceback

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def redis_conn():
    try:
        rs = redis.StrictRedis(host=os.environ.get('REDIS_HOST', 'redis'),
                               port=os.environ.get('REDIS_PORT', 6379), charset="utf-8", decode_responses=True)
        rs.ping()
        log.info('Connected')
        return rs
    except Exception as ex:
        log.info('Error: {0}'.format(ex))

rs = redis_conn()


def redis_set(ip,status):
    rs.set(ip,status)

def check_redis(ip):
    try:
        result = rs.__getitem__(ip)
        return result
    except KeyError:
        return []

url = 'https://httpbin.org/ip'

def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr'):
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            # Grabbing IP and corresponding PORT
            url_str = './/td[{0}]/text()'
            proxy = ":".join([i.xpath(url_str.format(1))[0], i.xpath(url_str.format(2))[0]])
            proxies.add(proxy)
    return proxies


def proxy_cycling(url):
    proxies = get_proxies()
    proxy_pool = cycle(proxies)
    proxies_list = []
    for i in range(1,len(proxies)):
        proxy = next(proxy_pool)
        print("Request {0}".format(i))
        try:
            response = requests.get(url, proxies={"http": proxy, "https": proxy})
            r = response.json()
            proxies_list.add(r)
            # redis_set()
            print(r)
        except:
            # Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work.
            # We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url
            print("Skipping. Connnection error")
    return proxies_list



print (proxy_cycling(url))