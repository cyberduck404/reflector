#!/usr/bin/python3
import os, sys
import argparse
from urllib.parse import urlparse, parse_qs, urlencode
from .core.xss import XSS
from .core.ssti import SSTI
from .config import HARDCODED_EXTENSIONS


p = argparse.ArgumentParser()
p.add_argument('-a', '--all', action='store_true', help='Enable all attacks')
p.add_argument('--xss', action='store_true', help='Enable XSS attack')
p.add_argument('--ssti', action='store_true', help='Enable SSTI attack')
p.add_argument('-x', '--proxy', help='Specify your proxy, like http://127.0.0.1:8080')
p.add_argument('-t', '--threads', type=int, default=64, help='Max Concurrency')
args = p.parse_args()

x_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
x_proxies = {
    'http': args.proxy,
    'https': args.proxy
}

def has_extension(url, extensions):
    parsed_url = urlparse(url)
    path = parsed_url.path
    extension = os.path.splitext(path)[1].lower()

    return extension in extensions

def clean_url(url):
    parsed = urlparse(url)

    if (parsed.port == 80 and parsed.scheme == "http") or (parsed.port == 443 and parsed.scheme == "https"):
        parsed = parsed._replace(netloc=parsed.netloc.rsplit(":", 1)[0])

    return parsed.geturl()

def main():
    if sys.stdin.isatty():
        sys.exit(0)
    extensions = HARDCODED_EXTENSIONS
    urls = []
    for line in sys.stdin.readlines():
        url = line.strip('\n')
        if '?' not in url:
            continue
        urls.append(url)

    cleaned_urls = set()
    for url in urls:
        cleaned_url = clean_url(url)
        if not has_extension(cleaned_url, extensions):
            parsed_url = urlparse(cleaned_url)
            query_params = parse_qs(parsed_url.query)
            cleaned_params = {key: args.keyword for key in query_params}
            cleaned_query = urlencode(cleaned_params, doseq=True)
            cleaned_url = parsed_url._replace(query=cleaned_query).geturl()
            cleaned_urls.add(cleaned_url)
    cleaned_urls = list(cleaned_urls)

    if args.all or args.xss:
        i = XSS(cleaned_urls, x_headers, x_proxies)
        i.attack()
    if args.all or args.ssti:
        i = SSTI(cleaned_urls, x_headers, x_proxies)
        i.attack()


if __name__ == '__main__':
    main()