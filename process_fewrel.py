import os
import json
import logging
import threading
from queue import Queue
from datetime import datetime
from config import MAX_WORKERS
from get_entity import get_entities

logger = logging.getLogger('Few-rel')
Q = Queue()


def load_queue():
    for rel, sentence_list in DATA.items():
        for sentence_meta in sentence_list:
            if 'entities' not in sentence_meta:
                Q.put(sentence_meta)


class Worker(threading.Thread):
    """Add tags for few-rel dataset."""

    def __init__(self, idx: int):
        super(Worker, self).__init__()
        self._index = idx
        self._stop_event = threading.Event()

    def run(self):
        global Q
        while Q.qsize() > 0:
            # Killed
            if self._stop_event.is_set():
                break
            # Extract entities from sentences in queue
            sentence_meta = Q.get()
            try:
                if 'entities' not in sentence_meta:
                    tokens = sentence_meta['tokens']
                    sentence = ' '.join(tokens)
                    entities = get_entities(sentence)
                    for entity in entities:
                        # map entity back to word position
                        start, length = 0, 0
                        while length < entity['start_pos']:
                            length += len(tokens[start]) + 1
                            start += 1
                        end = start
                        while length < entity['end_pos']:
                            length += len(tokens[end]) + 1
                            end += 1
                        # add entity information
                        entity['index_begin'] = start
                        entity['index_end'] = end
                    sentence_meta['entities'] = entities
                logger.info(
                    '{}, worker: {}, jobs remain: {}.'.format(datetime.now(),
                                                              self._index,
                                                              Q.qsize()))
            except Exception as e:
                logger.warning(e)
                # Send job back to queue
                Q.put(sentence_meta)
        logger.info('Worker {} exited.'.format(self._index))

    def stop(self):
        self._stop_event.set()


if __name__ == '__main__':
    for dataset in {'train', 'val'}:
        # Load data
        if os.path.exists('data/fewrel/{}_entity.json'.format(dataset)):
            with open('data/fewrel/{}_entity.json'.format(dataset),
                      'r') as f:
                DATA = json.load(f)
        else:
            with open('data/fewrel/{}.json'.format(dataset), 'r') as f:
                DATA = json.load(f)
        workers = []
        try:
            # Add sentences to queue
            load_queue()
            if Q.qsize() == 0:
                logger.info('No job left.')
                continue
            # Create workers
            count = int(min(MAX_WORKERS, Q.qsize() // 10))
            workers = [Worker(index) for index in range(count)]
            _ = [w.start() for w in workers]
            # Wait till jobs finished
            for w in workers:
                w.join()
        except KeyboardInterrupt:
            logger.info('Stopped by user.')
            # Stop workers
            _ = [w.stop() for w in workers]
            for w in workers:
                w.join()
            logger.info('Jobs left: {}.'.format(Q.qsize()))
        # Save data
        with open('data/fewrel/{}_entity.json'.format(dataset), 'w') as f:
            json.dump(DATA, f)
        full_name = 'data/fewrel/{}.json'.format(dataset)
        logger.info('File `{}` processed.'.format(full_name))
