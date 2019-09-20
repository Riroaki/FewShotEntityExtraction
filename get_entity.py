import json
import requests
import logging
import tagme
from config import TAGME_TOKEN, KG_KEY, PROXIES

logger = logging.getLogger('Entity')
tagme.GCUBE_TOKEN = TAGME_TOKEN
WIKI_URL = 'https://www.wikidata.org/w/api.php?action=wbsearchentities&search={}&language=en&limit=1&format=json'
KG_URL = 'https://kgsearch.googleapis.com/v1/entities:search?query={}&key=' + KG_KEY + '&limit=1'


def get_entities(sentence: str) -> list:
    # Extract entities from a sentence, return information about entities
    res = []
    for ann in tagme.annotate(sentence).annotations:
        entity = {
            'start_pos': ann.begin,
            'end_pos': ann.end,
            'score': ann.score,
            'title': ann.entity_title,
            'tagme_id': ann.entity_id,
            'wiki_id': get_wiki_id(ann.entity_title),
            'kg_id': get_kg_id(ann.entity_title)
        }
        res.append(entity)
    return res


def get_wiki_id(entity_title: str) -> str:
    # Get entity id from wiki data
    try:
        search_res = json.loads(
            requests.get(WIKI_URL.format(entity_title)).text)
        entity_id = search_res['search'][0]['id']
    except Exception as e:
        logger.debug(e)
        entity_id = ''
    return entity_id


def get_kg_id(entity_title: str) -> str:
    # Get id from KG-search
    try:
        search_res = json.loads(requests.get(KG_URL.format(entity_title),
                                             proxies=PROXIES).text)
        entity_id = search_res['itemListElement'][0]['result']['@id']
    except Exception as e:
        logger.debug(e)
        entity_id = ''
    return entity_id


if __name__ == '__main__':
    s = 'hampion cotton rocks ! not only they variety sizes colours , but also good quality . this make excellent gift'
    entities = get_entities(s)
    print(entities)
