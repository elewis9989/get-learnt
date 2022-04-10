from kafka import KafkaConsumer

import time
import json
print("HEEEEEELLLO")
consumer = None
while consumer == None:

    try:
        consumer = KafkaConsumer('record-click-topic', group_id='click-indexer', bootstrap_servers=['kafka:9092'])
    except:
        continue

    for message in consumer:
        new_click = json.loads((message.value).decode('utf-8'))
        with open("./data/output-test.txt","a") as output:
            output.write(new_click['user_id'] + "\t" + new_click['item_id'] + "\n")
