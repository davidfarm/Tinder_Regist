import requests
from requests.exceptions import ProxyError
from core.logger import log_dispatcher

url = 'http://checker.soax.com/api/ipinfo'


def check_proxy(full_url):
    try:
        response = str(requests.get(url, proxies={'http': full_url, 'https': full_url}))
    except ProxyError:
        response = '<Response [400]>'
        log_dispatcher.info(to_write='invalid proxy')

    if response == '<Response [200]>':
        log_dispatcher.info(to_write='proxy is valid')
        return True
    else:
        return False
