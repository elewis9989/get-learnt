from elasticsearch import Elasticsearch
from kafka import KafkaConsumer
import time

import time
import json

consumer = None
connection_established = False
while consumer == None:

    try:
        consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])

    except:
        continue

    time.sleep(60)
    while not connection_established:
        try:
            base_listings = [json.dumps({"object":{"header": "Listing1", "price": "10.1", "description": "this is the first listing", "user":"10", "skill":"8", "id":"8"}}),
            json.dumps({"object":{"header": "Listing2", "price": "11.11", "description": "this is the second listing", "user":"11", "skill":"9", "id":"9"}}),
            json.dumps({"object":{"header": "Cooking101", "price": "123.12", "description": "Basics of cooking", "user":"11", "skill":"10", "id":"10"}}),
            json.dumps({"object":{"header": "Learn to Love", "price": "0.0", "description": "learn how to love for the first time", "user":"10", "skill":"11", "id":"11"}}),
            json.dumps({"object":{"header": "How to get an A in CS4501: ISA", "price": "12.13", "description": "learn how to get an A by someone who knows Django pretty well", "user":"10", "skill":"12", "id":"12"}})]
            es = Elasticsearch(['es'])


            for listing in base_listings:
                listing = json.loads(listing)
                es.index(index='listing_index', doc_type='listing', id=listing['object']['id'], body=listing)
                es.indices.refresh(index="listing_index")
                connection_established = True
        except:
                connection_established = False

    for message in consumer:
        new_listing = json.loads((message.value).decode('utf-8'))
        print(new_listing)
        es = Elasticsearch(['es'])
        es.index(index='listing_index', doc_type='listing', id=new_listing['id'], body=new_listing)
        es.indices.refresh(index="listing_index")
