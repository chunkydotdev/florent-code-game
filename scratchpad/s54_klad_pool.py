"""Frozen study pool for the kladde v173 replay study (s54, 2026-08-22).

POOL A  archived kladde-v173 games present in replay_archive at the 07:16:25Z
        freeze, attributed via corpus/meta_join.tsv (21 matches / 105 games).
POOL B  11 crack-side matches (opponents that BEAT kladde v173) pulled by hand
        07:17Z, attributed via corpus/league_matches.tsv (55 games).

Every row carries: file, match, kladde side index (0/1) DERIVED FROM
teamAName (platform metadata, not from any winner-derived field — corpus-howto
TRAP 7), opponent name, opponent version, rated flag.
"""
from __future__ import annotations
import csv, json, os

K = 'kladde chatte tville (och oss)'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

POOL_B_MATCHES = [
    '7e0a295c-5854-4604-9b94-aa7f0496a046', 'ba678875-2a9b-4852-9fef-6935e9a1fb14',
    'e3ab1b8b-f811-4454-93d1-65a31bf606a5', '377d2b7f-3642-4948-b8e5-3df12ef69f06',
    '5829e6b5-56ee-4b8e-995f-3cec7e71cd97', 'a642abd7-47c7-46fd-846c-edbf8e92f640',
    'd95d65e4-89f9-413a-8193-1cc0ccee9180', '34b29cfe-7e6a-468a-b849-72455c36d28a',
    'db0e11f7-7c8b-4e8b-bb03-75a9ab42fabe', '6dc970d9-f4f6-42c7-964d-ce0b3e6d675f',
    '8b5feeca-8420-4e92-b9d8-ee1a7a86af62',
]


def _p(*a):
    return os.path.join(ROOT, *a)


def pool(version='173'):
    rows = []
    seen = set()
    frozen = json.load(open(_p('scratchpad', 's54_klad_pool_frozen.json')))
    for r in frozen:
        kv = r['teamAVersion'] if r['teamAName'] == K else r['teamBVersion']
        if kv != version:
            continue
        ks = 0 if r['teamAName'] == K else 1
        rows.append(dict(file=r['file'], match=r['match'], game=int(r['game']),
                         ks=ks,
                         opp=r['teamBName'] if ks == 0 else r['teamAName'],
                         oppver=r['teamBVersion'] if ks == 0 else r['teamAVersion'],
                         rated=(r['triggeredBy'] == 'ladder'),
                         pool='A', when=r['completedAt']))
        seen.add(r['file'])
    LM = {r['id']: r for r in csv.DictReader(open(_p('corpus', 'league_matches.tsv')),
                                             delimiter='\t')}
    for mid in POOL_B_MATCHES:
        r = LM[mid]
        ks = 0 if r['teamAName'] == K else 1
        kv = r['teamAVersion'] if ks == 0 else r['teamBVersion']
        assert kv == version, (mid, kv)
        for gnum in range(1, 6):
            f = f'{mid}_game_{gnum}.replay26'
            if f in seen or not os.path.exists(_p('replay_archive', f)):
                continue
            rows.append(dict(file=f, match=mid, game=gnum, ks=ks,
                             opp=r['teamBName'] if ks == 0 else r['teamAName'],
                             oppver=r['teamBVersion'] if ks == 0 else r['teamAVersion'],
                             rated=True, pool='B', when=r['createdAt']))
    return rows
