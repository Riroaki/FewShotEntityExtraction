import logging

# Set log level
logging.basicConfig(level=logging.INFO)
# Token for using tagme api
TAGME_TOKEN = 'acb3808f-76fe-444e-832b-aaef47db2f61-843339462'
# API key for google KG search
KG_KEY = 'AIzaSyBTVtO0EKStF2ARbtVYuevcGclxKVJOpnE'
# Proxy: cross the GFW
PROXIES = {'https': 'https://127.0.0.1:1087'}
# Number of threads in entity extraction
MAX_WORKERS = 64
