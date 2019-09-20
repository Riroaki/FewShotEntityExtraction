import os
import logging
import json
import threading
from datetime import datetime
from queue import Queue
from config import MAX_WORKERS
from get_entity import get_entities

logger = logging.getLogger('Few-shot')
Q = Queue()


class Worker(threading.Thread):
    """Add tags for few-shot dataset."""

    def __init__(self, idx: int):
        super(Worker, self).__init__()
        self._index = idx
        self._stop_event = threading.Event()

    def run(self):
        while Q.qsize() > 0:
            # Killed
            if self._stop_event.is_set():
                break
            # Extract entities from sentences in queue
            sentence_meta = Q.get()
            try:
                if 'entities' not in sentence_meta:
                    entities = get_entities(sentence_meta['sentence'])
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


def add_tag(fname: str):
    json_file = fname + '.json'
    logger.info('Start to add tags for sentences in `{}`.'.format(fname))
    with open(fname, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    workers = []
    try:
        # Put data in queue
        dataset = []
        if os.path.exists(json_file):
            with open(json_file, 'r') as f:
                dataset = json.load(f)
        else:
            for line in lines:
                sentence, _, cls = line.partition('\t')
                dataset.append({'sentence': sentence, 'class': cls})
        for sentence_meta in dataset:
            if 'entities' not in sentence_meta:
                Q.put(sentence_meta)
        # All work finished
        if Q.qsize() == 0:
            logger.info('File `{}`: entities already added.'.format(fname))
            return
        # Create workers
        count = int(min(MAX_WORKERS, Q.qsize() // 20))
        workers = [Worker(index) for index in range(count)]
        _ = [w.start() for w in workers]
        # Wait till every worker finishes
        for w in workers:
            w.join()
        with open(json_file, 'w') as f:
            json.dump(dataset, f)
        logger.info('File `{}`: done.'.format(fname))
    except KeyboardInterrupt:
        logger.info('Stopped by user.')
        # Stop workers
        _ = [w.stop() for w in workers]
        for w in workers:
            w.join()
        logger.info('Jobs left: {} for file: `{}`.'.format(Q.qsize(), fname))


if __name__ == '__main__':
    data_dir = 'data/fewshot'
    threads = []
    for filename in filter(
            lambda file: file.endswith('.dev') or file.endswith(
                '.train') or file.endswith('.test'),
            os.listdir(data_dir)):
        full_name = os.path.join(data_dir, filename)
        add_tag(full_name)
        logger.info('File `{}` processed.'.format(full_name))
