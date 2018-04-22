# -*- coding: utf-8 -*-
import re
import requests


re_coords = re.compile(r'(?P<longitude>-?\d+\.\d+) (?P<latitude>-?\d+\.\d+)')
url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'


def coords(point):
    match = re.search(re_coords, point)
    if match:
        return float(match.group('longitude')), float(match.group('latitude'))


def request(query):
    return requests.get(url, params={'query': query, 'format': 'json'}).json()


def test_coords():
    assert (-73.94, 40.67) == coords('Point(-73.94 40.67)')