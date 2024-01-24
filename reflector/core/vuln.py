import sys
import requests
from urllib.parse import quote
from ..config import PLACEHOLDER
from threading import Thread
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Vuln:
    def __init__(self, urls, headers, proxies):
        self.urls = urls
        self.headers = headers
        self.proxies = proxies

    def generate_payloads(self):
        ctx = {
            'payload': 'reflected'
        }

        return ctx

    def battering_ram(self, url, payloads, headers=None, proxies=None):
        headers = headers if headers else dict()
        proxies = proxies if proxies else dict()
        for payload in payloads.keys():
            reflected = payloads[payload]
            url = url.replace(PLACEHOLDER, quote(payload))
            try:
                r = requests.get(url, headers=headers, proxies=proxies, verify=False)
            except requests.exceptions.RequestException as e:
                return
            if reflected in r.text:
                sys.stdout.write(f"{url}\n")
        
    def attack(self):
        payloads = self.generate_payloads()
        ts = []
        for url in self.urls:
            if "?" in url:
                ts.append(Thread(
                    target=self.battering_ram,
                    args=(url, payloads,),
                    kwargs={'headers': self.headers, 'proxies': self.proxies}
                ))
        for t in ts:
            t.start()
        for t in ts:
            t.join()