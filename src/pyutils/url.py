import re

import tldextract

from pyutils.text import regex_lib

# TODO: get url without params
# TODO: get params from url


DOMAIN_CORRECTIONS = {
    'youtu': 'youtube'
}


def get_urls(text):
    regex = re.compile(regex_lib.url())

    return regex.findall(text)


def get_domain(url):
    extract_result = tldextract.extract(url)

    domain = ''
    if extract_result.subdomain not in ['', 'www']:
        domain += f'{extract_result.subdomain}.'

    domain += extract_result.domain

    return DOMAIN_CORRECTIONS.get(domain, domain)


def get_unique_domains(urls):
    domains = [get_domain(url) for url in urls]
    return list(set(domains))


def get_links_from_domains(domains, urls):
    return [url for url in urls if get_domain(url) in domains]
