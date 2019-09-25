# Few-Shot Entity Extraction

> Utility scripts to extract entities from sentences in few-shot dataset using `tagme`, `wikidata`, `kgsearch` APIs.

## Requirements

- `python3`
- `tagme==0.1.3`
- Tagme's api key: to use `tagme` api, you need to register an account [here](https://sobigdata.d4science.org/group/tagme), and overwrite the token as `TAGME_TOKEN` in  `config.py`.
- Google KG's api key: to use google KG-search api, you need to register an accound [here](https://developers.google.com/knowledge-graph/how-tos/authorizing), and overwrite tokens as `KG_KEY` in `config.py`.
- VPN is required if you are inside the GFW to access Google KG api. If you use proxies, overwrite the `PROXIES` in `config.py`, in the format: `{'https': 'x.x.x.x:xxxx'}` 

## Fewshot dataset

- Data source: `https://github.com/zxlzr/FewShotNLP/tree/master/data`

- Command: `python tag_fewshot.py`

- Output: original file named `A.train(dev/test)` -> `A.train(dev/test).json`

- Data format (after processing):
    - `sentence`: sentence.
    - `class`: type of sentence.
    - `entities`: list of entities' information
        - `start_pos`: begin position of entity in sentence.
        - `end_pos`: end position of entity in sentence.
        - `score`: probability of entity derived from tagme.
        - `title`: title of entity.
        - `tagme_id`: entity id according to tagme.
        - `wiki_id`: entity id according to wiki data.
        - `kg_id`: entity id according to google KG.

- Sample data:
```json
[{"sentence": "it advertised not stock so i unable get it", "class": "-1", "entities": [{"start_pos": 3, "end_pos": 13, "score": 0.1549598127603531, "title": "Advertising", "tagme_id": 2861, "wiki_id": "Q37038", "kg_id": "kg:/m/019rl6"}, {"start_pos": 18, "end_pos": 23, "score": 0.09428920596837997, "title": "Stock and flow", "tagme_id": 888140, "wiki_id": "Q2714114", "kg_id": "kg:/m/01116q1q"}, {"start_pos": 36, "end_pos": 42, "score": 0.08518906682729721, "title": "Get It On (T. Rex song)", "tagme_id": 5590319, "wiki_id": "", "kg_id": "kg:/m/01972m"}]}]
```

## Fewrel dataset

- Data source: `https://github.com/thunlp/FewRel/tree/master/data`

- Command: `python tag_fewrel.py`

- Output: `train(val).json` -> `train(val)_entity.json`

- Data format (after processing):
    - `$relation_type$`: name of each relation type, e.g., 'P931'.
        - `tokens`: words / segments split from sentences.
        - `h`: first item in relation.
        - `t`: second item in relation.
        - `entities`: list of entities' information.
            - `index_begin`: index of starting word in sentence.
            - `index_end`: index of ending word in sentence.
            - `start_pos`: begin position of entity in sentence.
            - `end_pos`: end position of entity in sentence.
            - `score`: probability of entity derived from tagme.
            - `title`: title of entity.
            - `tagme_id`: entity id according to tagme.
            - `wiki_id`: entity id according to wiki data.
            - `kg_id`: entity id according to google KG.

- Sample data:
```json
{"P931": [{"tokens": ["Merpati", "flight", "106", "departed", "Jakarta", "(", "CGK", ")", "on", "a", "domestic", "flight", "to", "Tanjung", "Pandan", "(", "TJQ", ")", "."], "h": ["tjq", "Q1331049", [[16]]], "t": ["tanjung pandan", "Q3056359", [[13, 14]]], "entities": [{"start_pos": 0, "end_pos": 7, "score": 0.2455686628818512, "title": "Merpati Nusantara Airlines", "tagme_id": 1289337, "wiki_id": "Q619118", "kg_id": "", "index_begin": 0, "index_end": 1}, {"start_pos": 8, "end_pos": 14, "score": 0.16067400574684143, "title": "Flight International", "tagme_id": 3080620, "wiki_id": "Q1428742", "kg_id": "", "index_begin": 1, "index_end": 2}, {"start_pos": 19, "end_pos": 27, "score": 0.00844799354672432, "title": "The Departed", "tagme_id": 1349086, "wiki_id": "Q172975", "kg_id": "", "index_begin": 3, "index_end": 4}, {"start_pos": 28, "end_pos": 35, "score": 0.5443639755249023, "title": "Jakarta", "tagme_id": 16275, "wiki_id": "Q3630", "kg_id": "", "index_begin": 4, "index_end": 5}, {"start_pos": 38, "end_pos": 41, "score": 0.35298147797584534, "title": "Soekarno\u2013Hatta International Airport", "tagme_id": 1203751, "wiki_id": "Q749497", "kg_id": "", "index_begin": 6, "index_end": 7}, {"start_pos": 49, "end_pos": 64, "score": 0.3290479779243469, "title": "1982 Garuda Fokker F28 crash", "tagme_id": 15540624, "wiki_id": "Q4580452", "kg_id": "", "index_begin": 10, "index_end": 12}, {"start_pos": 68, "end_pos": 82, "score": 0.5, "title": "Tanjung Pandan", "tagme_id": 20621756, "wiki_id": "Q3056359", "kg_id": "", "index_begin": 13, "index_end": 15}]}]}
```

## Note

- Max workers: specified in `config.py`. Using larger numbers would improve efficiency, but not all the time.
- Termination: The program terminates when all jobs are done. You may stop processing by typing `ctrl+c` whenever you want, but please make sure all workers exited and the program output `Saved data.`, which means the extracted entities has been written into output files. You may restart and the program would process from where you stopped last time.
