# FewShotEntityExtraction

> Utility scripts to extract entities from sentences in few-shot dataset using `tagme`.

## Requirements

- `python3`
- `tagme==0.1.3`

To use tagme api, you need to register an account [here](https://sobigdata.d4science.org/group/tagme), and write the token as `TAGME_TOKEN` in  `config.py`.

## Fewshot dataset

- Data source: `https://github.com/zxlzr/FewShotNLP/tree/master/data`

- Command: `python tag_fewshot.py`

- Output: original file named `A.train` -> `A.train.json`

- Data format:

```json
[{
  "sentence": "lasts only 2 weeks ! try them if you don't believe me",
  "class": "-1",
  "entities": [
    {
      "pos_begin": 13,  // index of starting character in sentence
      "pos_end": 18,  // index of ending character in sentence
      "entity_id": 27493154,
      "score": 0.0007660030387341976
    }, {
      "pos_begin": 21,
      "pos_end": 24,
      "entity_id": 3276812,
      "score": 0.009006991051137447
    }, {
      "pos_begin": 30,
      "pos_end": 32,
      "entity_id": 1685851,
      "score": 0.07183314114809036
    }, {
      "pos_begin": 33,
      "pos_end": 36,
      "entity_id": 14148802,
      "score": 0.19438420236110687
    }, {
      "pos_begin": 37,
      "pos_end": 40,
      "entity_id": 294015,
      "score": 0.010517369955778122
    }, {
      "pos_begin": 37,
      "pos_end": 50,
      "entity_id": 27690196,
      "score": 0.005518087185919285
    }, {
      "pos_begin": 43,
      "pos_end": 53,
      "entity_id": 38740213,
      "score": 0.0672566369175911
    }
  ]
}, ...]
```

## Fewrel dataset

- Data source: `https://github.com/thunlp/FewRel/tree/master/data`

- Command: `python tag_fewrel.py`

- Output: `train_tagme.json` (you need to copy and rename `train.json`, the script extracts and saves entities in place.)

- ÏData format:

```json
[{
  "tokens": ["In", "June", "1987", ",", "the", "Missouri", "Highway", "and", "Transportation", "Department", "approved", "design", "location", "of", "a", "new", "four", "-", "lane", "Mississippi", "River", "bridge", "to", "replace", "the", "deteriorating", "Cape", "Girardeau", "Bridge", "."],
  "h": ["cape girardeau bridge", "Q5034838", [[26, 27, 28]]],
  "t": ["mississippi river", "Q1497", [[19, 20]]],
  "entities": [
    {
      "index_begin": 5,  // index of starting word in token list
      "index_end": 6,  // index of ending word in token list
      "entity_id": 19591,
      "score": 0.35695624351501465
    }, {
      "index_begin": 6,
      "index_end": 7,
      "entity_id": 48519,
      "score": 0.22454741597175598
    }, {
      "index_begin": 8,
      "index_end": 10,
      "entity_id": 58235,
      "score": 0.015105740167200565
    }, {
      "index_begin": 11,
      "index_end": 12,
      "entity_id": 631159,
      "score": 0.08602561801671982
    }, {
      "index_begin": 12,
      "index_end": 13,
      "entity_id": 2272383,
      "score": 0.09302778542041779
    }, {
      "index_begin": 18,
      "index_end": 19,
      "entity_id": 95699,
      "score": 0.0887017548084259
    }, {
      "index_begin": 19,
      "index_end": 21,
      "entity_id": 19579,
      "score": 0.6045866012573242
    }, {
      "index_begin": 26,
      "index_end": 29,
      "entity_id": 4910093,
      "score": 0.5
    }
  ]
}, ...]
```

## Note

- Number of threads: specify in `config.py`. Using larger numbers would improve efficiency, but not all the time. 64 is the default value here.
- Termination: The program terminates when all jobs are done. You may stop processing by `ctrl+c` whenever you want, but please make sure all workers exited and the program output `Saved data.`, which means the extracted entities has been written into output files. You may restart and the program would process from where you stopped last time.

