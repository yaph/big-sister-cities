#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import networkx as nx
import wdutil

from pathlib import Path


cities = {}
sisters = set()
query = Path('~/repos/pub/queries/wikidata/big-sister-cities.sparql').expanduser().read_text()
prefixes = ['city', 'sister']


def add_city(record, cid, prefix):
    if cid in cities:
        cities[cid]['degree'] += 1
    else:
        lon, lat = wdutil.coords(record[f'{prefix}_coordinate_location']['value'])
        cities[cid] = {
            'degree': 1,
            'label': record[f'{prefix}Label']['value'],
            'lon': lon,
            'lat': lat,
            'pop': int(record[f'{prefix}_population']['value'])
        }


resp = wdutil.request(query)
for record in resp['results']['bindings']:
    city_id = record['city']['value'].split('/')[-1]
    sister_id = record['sister']['value'].split('/')[-1]

    relation_id = tuple(sorted([city_id, sister_id]))
    sisters.add(relation_id)

    add_city(record, city_id, prefix='city')
    add_city(record, sister_id, prefix='sister')

with open('big-sister-cities.json', 'w') as f:
    json.dump({'cities': cities, 'sisters': list(sisters)}, f)


G = nx.Graph()
for id, attr in cities.items():
    G.add_node(id, **attr)
for sister in sisters:
    G.add_edge(sister[0], sister[1])
nx.write_gexf(G, 'big-sister-cities.gexf')