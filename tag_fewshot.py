import os
import logging
import json
import tagme
import threading
from datetime import datetime
from queue import Queue

tagme.GCUBE_TOKEN = 'acb3808f-76fe-444e-832b-aaef47db2f61-843339462'

logger = logging.getLogger('Tagme-fewshot')
logger.setLevel(logging.DEBUG)
queue = Queue()
num_workers = 64


class Worker(threading.Thread):
    """Add tags for few-shot dataset."""

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
                    sentence_annotations = tagme.annotate(
                        sentence_meta['sentence'])
                    entities = [(ann.begin, ann.end, ann.score) for ann in
                                sentence_annotations.annotations]
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


def add_tag(fname: str):
    json_file = fname + '.json'
    logger.info('Start to add tags for sentences in `{}`.'.format(fname))
    with open(fname, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    global queue, num_workers
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
                queue.put(sentence_meta)
        # All work finished
        if queue.qsize() == 0:
            logger.info('File `{}`: entities already added.'.format(fname))
            return
        # Create workers
        for index in range(num_workers):
            w = Worker(index)
            w.start()
            workers.append(w)
        for w in workers:
            w.join()
        with open(json_file, 'w') as f:
            json.dump(dataset, f)
        logger.info('File `{}`: done.'.format(fname))
    except KeyboardInterrupt:
        logger.info('Stopped by user.')
        # Stop workers
        for w in workers:
            w.stop()
        for w in workers:
            w.join()
        logger.info('Jobs left: {} for file: `{}`.'.format(queue.qsize(),
                                                           fname))


if __name__ == '__main__':
    data_dir = 'data/fewshot'
    threads = []
    for filename in filter(
            lambda file: file.endswith('.dev') or file.endswith(
                '.train') or file.endswith('.test'),
            os.listdir(data_dir)):
        full_name = os.path.join(data_dir, filename)
        add_tag(full_name)
