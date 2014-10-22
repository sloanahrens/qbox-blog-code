
# run spark with four cores

# cd ~/spark
# ./bin/pyspark --master local[4]

# read in a text file
textFile = sc.textFile('CHANGES.txt')

# count lines
print('lines in file: %s' % textFile.count())

# add up lenths of each line
chars = textFile.map(lambda s: len(s)).reduce(lambda a, b: a + b)
print('number of non-newline characters in file: %s' % chars)

# run a simple word count of the doc

# map each line to its words
wordCounts = textFile.flatMap(lambda line: line.split())

# emit value:1 for each key:word
wordCounts = wordCounts.map(lambda word: (word, 1))

# add up word counts by key:word
wordCounts = wordCounts.reduceByKey(lambda a, b: a+b)

# sort in descending order by word counts
wordCounts = wordCounts.sortBy(lambda item: -item[1])

# collect the results in an array
results = wordCounts.collect()

# print the first ten elements
print(results[:10])

###############################################


# run spark with elasticsearch-hadoop jar
# cd ~/spark
# ./bin/pyspark --master local[4] --jars jars/elasticsearch-hadoop-2.1.0.Beta2.jar

# read in ES index "titanic/passenger"
es_rdd = sc.newAPIHadoopRDD(
    inputFormatClass="org.elasticsearch.hadoop.mr.EsInputFormat",
    keyClass="org.apache.hadoop.io.NullWritable", 
    valueClass="org.elasticsearch.hadoop.mr.LinkedMapWritable", 
    conf={ "es.resource" : "titanic/passenger" })

print(es_rdd.first())

# extract values for the "sex" field, count occurences of each value
value_counts = es_rdd.map(lambda item: item[1]["sex"])
value_counts = value_counts.map(lambda word: (word, 1))
value_counts = value_counts.reduceByKey(lambda a, b: a+b)

# put the results in the right format for the adapter
value_counts = value_counts.map(lambda item: ('key', { 
    'field': 'sex', 
    'val': item[0], 
    'count': item[1] 
}))

# write the results to "titanic/value_counts"
value_counts.saveAsNewAPIHadoopFile(
    path='-', 
    outputFormatClass="org.elasticsearch.hadoop.mr.EsOutputFormat",
    keyClass="org.apache.hadoop.io.NullWritable", 
    valueClass="org.elasticsearch.hadoop.mr.LinkedMapWritable", 
    conf={ "es.resource" : "titanic/value_counts" })
