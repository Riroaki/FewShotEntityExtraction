# FewShotEntityExtraction

> Extract entities from sentences in few-shot dataset using `tagme`.

## Requirements

- `python3`
- `tagme==0.1.3`

## Fewshot dataset

Data source: `https://github.com/zxlzr/FewShotNLP/tree/master/data`

Command: `python tag_fewshot.py`

Output: original file named `A.train` -> `A.train.json`

Data format:

```json
[{
  "sentence": "nice looking picture but what dementions thing ? it looks good but it 4 \" 8 \" or 12 \" 8 \" ? sure would nice know size before i buy ............. da trol",
  "class": "1",
  "entities": [
    [0, 4, 0.11888746172189713],  // begin position, end location, score
    [0, 12, 0.12973745167255402],
    [13, 20, 0.017505625262856483],
    [41, 46, 0.02188337966799736],
    [58, 62, 0.0011372914304956794],
    [92, 96, 0.042721934616565704],
    [103, 107, 0.124010369181633],
    [113, 117, 0.013514379970729351],
    [127, 130, 0.03306431695818901],
    [145, 147, 0.11792175471782684],
    [148, 152, 0.10552945733070374]
  ]
}, ...]
```

## Fewrel dataset

Data source: `https://github.com/thunlp/FewRel/tree/master/data`

Command: `python tag_fewrel.py [train/val]`

Output: `train_tagme.json` (you need to copy and rename `train.json`, the script extracts and saves entities in place.)

Data format:

```json
[{
  "tokens": ["It", "is", "the", "main", "alternate", "of", "Jinnah", "International", "Airport", "in", "Karachi", "with", "a", "distance", "of", "about", "350", "\u00a0", "km/220", "miles", ";", "well", "under", "an", "hour", "'s", "flight", "time", "in", "turboprop", "aircraft", "."],
  "h": ["jinnah international airport", "Q61052", [[6, 7, 8]]],
  "t": ["karachi", "Q8660", [[10]]],
  "entities": [
    [3, 4, 0.05648687109351158],
    [4, 5, 0.05953952670097351],
    [6, 9, 0.5],
    [7, 9, 0.24509519338607788],
    [8, 9, 0.18682029843330383],
    [10, 11, 0.4931352138519287],
    [13, 14, 0.18960361182689667],
    [18, 19, 0.2723827362060547],
    [19, 20, 0.2740946114063263],
    [21, 22, 0.0614713579416275],
    [22, 25, 0.013358778320252895],
    [26, 27, 0.05468727648258209],
    [27, 28, 0.0891151949763298],
    [29, 30, 0.4731414318084717],
    [30, 31, 0.24223822355270386]
  ]
},...]
```

