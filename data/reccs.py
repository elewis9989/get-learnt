from pyspark import SparkContext
import MySQLdb
import re


sc = SparkContext("spark://spark-master:7077", "Recommendations")

data = sc.textFile("/tmp/data/output-test.txt", 2)


pairs = data.map(lambda line: line.split("\t"))

#Group data into user id and the items clicked on
groups = pairs.groupByKey()

for key, value in groups.collect():
    print(str(key) + str(list(value)))

#Transform into user_id: (item, item)

def extract_pairs(line):
    # Return a list (user id, coview) pairs
    user_id = line[0]
    item_ids = set(line[1])
    coviews = []
    for item_id1 in item_ids:
        for item_id2 in item_ids:
            if item_id1 < item_id2:
                coview = str([item_id1, item_id2])
                t = [user_id, coview]
                coviews.append(t)
    return coviews


uid_tuple = groups.flatMap(lambda line: extract_pairs(line))

tuple_uid = uid_tuple.map(lambda pair : (pair[1], pair[0]))

t2 = tuple_uid.groupByKey()

t3 = t2.distinct()

t4 = t3.map(lambda pair: (pair[0], len(pair[1])))

t5 = t4.filter(lambda x: x[1] >= 3)

recommendations = []
for key, value in t5.collect():
    k = map(int, re.findall(r'\d+', key))
    recommendations.append(k)
    print(k)

# Connect with db?"""

db = MySQLdb.connect(host="db", port=3306, passwd="$3cureUS", db="cs4501")
cursor = db.cursor()

# Clear the table?
cursor.execute("TRUNCATE marketplace_recommendation")
# for each thing in recommendations
for recommendation in recommendations:
    # check to see if the key is in the table yet
    print(recommendation)
    item_id1 = str(recommendation[0])
    item_id2 = str(recommendation[1])
    print(item_id1)
    print(item_id2)


    cursor.execute("INSERT INTO marketplace_recommendation (item_id, recommended_items) VALUES(%s, %s) ON DUPLICATE KEY UPDATE recommended_items=CONCAT(recommended_items, ',', %s)", (item_id1, item_id2, item_id2))
    cursor.execute("INSERT INTO marketplace_recommendation (item_id, recommended_items) VALUES(%s, %s) ON DUPLICATE KEY UPDATE recommended_items=CONCAT(recommended_items, ',', %s)", (item_id2, item_id1, item_id1))
    db.commit()

db.close()
