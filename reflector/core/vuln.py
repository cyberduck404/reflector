import sys
import requests
from urllib.parse import quote
from ..config import PLACEHOLDER
from threading import Thread, BoundedSemaphore
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Vuln:
    def __init__(self, urls, headers, proxies, max_threads=None):
        self.urls = urls
        self.headers = headers
        self.proxies = proxies
        self.max_threads = max_threads
        self.sema = BoundedSemaphore(value=self.max_threads)

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
            _url = url.replace(PLACEHOLDER, quote(payload))
            try:
                self.sema.acquire()
                r = requests.get(_url, headers=headers, proxies=proxies, verify=False)
                self.sema.release()
            except requests.exceptions.RequestException as e:
                self.sema.release()
                return
            if reflected in r.text:
                sys.stdout.write(f"[+] [B] {payload} {_url}\n")
            if reflected in str(r.headers):
                sys.stdout.write(f"[+] [H] {payload} {_url}\n")
        
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