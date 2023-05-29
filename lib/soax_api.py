import requests, configparser

config = configparser.ConfigParser()
config.read('config.ini')
proxy_country = config.get('Settings', 'proxy_country')
proxy_region = config.get('Settings', 'proxy_region')

package_id = '76853'
package_login = 'rUfgRb6QMNgjiLYv'

url = 'http://checker.soax.com/api/ipinfo'

def stick(name_id):
    proxy_url = "@proxy.soax.com:5000"
    if proxy_region == "none":
        proxy_path_url = f'package-{package_id}-country-{proxy_country}-sessionid-{name_id}-sessionlength-1600'
    elif proxy_region == "":
        proxy_path_url = f'package-{package_id}-country-{proxy_country}-sessionid-{name_id}-sessionlength-1600'
    else:
        proxy_path_url = f'package-{package_id}-country-{proxy_country}-region-{proxy_region}-sessionid-{name_id}-sessionlength-1600'
    full_url = f"http://{proxy_path_url}:{package_login}{proxy_url}"
    requests.get(url, proxies={'http': full_url, 'https': full_url})

    return proxy_path_url

def proxy(proxy_path_url):
    proxy_host = "proxy.soax.com"
    proxy_type = "SOCKS"
    proxy_username = proxy_path_url
    proxy_password = "rUfgRb6QMNgjiLYv"
    ports = "5000"

    return proxy_host, proxy_type, proxy_username