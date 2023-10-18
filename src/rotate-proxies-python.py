import src.variables    as var
import pandas           as pd
import time
import requests
import urllib.request
import socket
import urllib.error

from bs4 import BeautifulSoup
from requests_html import HTMLSession

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# variables

# start time of function
start_time = time.time()

# project directory
path = var.project_dir

proxies_list = open(path + r"\data\raw\rotating_proxies_list.txt", "r").read().strip().split("\n")
print(proxies_list)

df = pd.read_csv(path + r"\data\raw\rotating_proxies_list.csv", sep=',')

df = df[['ip', 'port']]
df['proxy'] = df.apply(lambda x: x['ip'] + ":" + str(x['port']), axis=1)

proxies_list = df['proxy'].to_list()
print(proxies_list)

unchecked = set(proxies_list[0:20]) # limited to 10 to avoid too many requests
# unchecked = set(proxies_list)
working = set()
not_working = set()

VALID_STATUSES = [200, 301, 302, 307, 404]

def reset_proxy(proxy):
    unchecked.add(proxy)
    working.discard(proxy)
    not_working.discard(proxy)


def set_working(proxy):
    unchecked.discard(proxy)
    working.add(proxy)
    not_working.discard(proxy)


def set_not_working(proxy):
    unchecked.discard(proxy)
    working.discard(proxy)
    not_working.add(proxy)

def get(url, proxy):
    print(proxy)
    try:
        response = requests.get(url, proxies={'http': f"http://{proxy}"}, timeout=30)
        urllib.urlopen(url, proxies={'http': f"http://{proxy}"}, timeout=30)
        if response.status_code in VALID_STATUSES:
            set_working(proxy)
        else:
            set_not_working(proxy)
    except Exception as e:
        print("Exception: ", e)
        set_not_working(proxy)

        VALID_STATUSES = [200, 301, 302, 307, 404]

def check_proxies():
	proxies = proxies_list[0:20] # limited to 10 to avoid too many requests
	for proxy in list(unchecked):
		get("http://onet.pl/", proxy)

check_proxies()

print("unchecked ->", unchecked) # unchecked -> set()
print("working ->", working) # working -> {"152.0.209.175:8080", ...}
print("not_working ->", not_working) # not_working -> {"167.71.5.83:3128", ...}
