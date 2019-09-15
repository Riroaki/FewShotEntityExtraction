import os
import logging
from queue import Queue
import threading
from datetime import datetime
import json
import tagme
from config import TAGME_TOKEN, MAX_WORKERS

tagme.GCUBE_TOKEN = TAGME_TOKEN
logger = logging.getLogger('Entity extraction(fewrel)')
logger.setLevel(logging.DEBUG)
queue = Queue()


def load_queue():
    global queue, data
    for rel, sentence_list in data.items():
        for sentence_meta in sentence_list:
            if 'entities' not in sentence_meta:
                queue.put(sentence_meta)


class Worker(threading.Thread):
    """Add tags for few-rel dataset."""

    def __init__(self, idx: int):
        super(Worker, self).__init__()
        self._index = idx
        self._stop_event = threading.Event()

    def run(self):
        global queue
        while queue.qsize() > 0:
            # Killed
            if self._stop_event.is_set():
                break
            # Extract entities from sentences in queue
            sentence_meta = queue.get()
            try:
                if 'entities' not in sentence_meta:
                    tokens = sentence_meta['tokens']
                    sentence = ' '.join(tokens)
                    sentence_annotations = tagme.annotate(sentence)
                    entities = []
                    for ann in sentence_annotations.annotations:
                        # map entity back to word position
                        start, length = 0, 0
                        while length < ann.begin:
                            length += len(tokens[start]) + 1
                            start += 1
                        end = start
                        while length < ann.end:
                            length += len(tokens[end]) + 1
                            end += 1
                        # add entity information
                        entities.append({'index_begin': start,
                                         'index_end': end,
                                         'entity_id': ann.entity_id,
                                         'score': ann.score})
                    sentence_meta['entities'] = entities
                logger.info(
                    '{}, worker: {}, jobs remain: {}.'.format(datetime.now(),
                                                              self._index,
                                                              queue.qsize()))
            except Exception as e:
                logger.warning(e)
                # Send job back to queue
                queue.put(sentence_meta)
        logger.info('Worker {} exited.'.format(self._index))

    def stop(self):
        self._stop_event.set()


if __name__ == '__main__':
    for dataset in {'train', 'val'}:
        # Load data
        if os.path.exists('data/fewrel/{}_entity.json'.format(dataset)):
            with open('data/fewrel/{}_entity.json'.format(dataset),
                      'r') as f:
                data = json.load(f)
        else:
            with open('data/fewrel/{}.json'.format(dataset), 'r') as f:
                data = json.load(f)
        workers = []
        try:
            # Add sentences to queue
            load_queue()
            if queue.qsize() == 0:
                logger.info('No job left.')
                continue
            # Create workers
            count = int(min(MAX_WORKERS, queue.qsize() // 20))
            for index in range(count):
                w = Worker(index)
                w.start()
                workers.append(w)
            # Wait till jobs finished
            for w in workers:
                w.join()
        except KeyboardInterrupt:
            logger.info('Stopped by user.')
            # Stop workers
            for w in workers:
                w.stop()
            for w in workers:
                w.join()
            logger.info('Jobs left: {}.'.format(queue.qsize()))
        # Save data
        with open('data/fewrel/{}_entity.json'.format(dataset), 'w') as f:
            json.dump(data, f)
        logger.info('Saved data.')
    logger.info('Everything done.')
