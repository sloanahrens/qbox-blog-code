from pyspark import SparkContext, SparkConf

if __name__ == "__main__":

    conf = SparkConf().setAppName("ESTest")
    sc = SparkContext(conf=conf)

    es_read_conf = {
        "es.nodes" : "localhost",
        "es.port" : "9200",
        "es.resource" : "titanic/passenger"
    } 

    es_write_conf = {
        "es.nodes" : "localhost",
        "es.port" : "9200",
        "es.resource" : "titanic/value_counts"
    } 
    
    es_rdd = sc.newAPIHadoopRDD(
        inputFormatClass="org.elasticsearch.hadoop.mr.EsInputFormat",
        keyClass="org.apache.hadoop.io.NullWritable", 
        valueClass="org.elasticsearch.hadoop.mr.LinkedMapWritable", 
        conf=es_read_conf)

    doc = es_rdd.first()[1]

    for field in doc:

        value_counts = es_rdd.map(lambda item: item[1][field])
        value_counts = value_counts.map(lambda word: (word, 1))
        value_counts = value_counts.reduceByKey(lambda a, b: a+b)
        value_counts = value_counts.filter(lambda item: item[1] > 1)
        value_counts = value_counts.map(lambda item: ('key', { 
            'field': field, 
            'val': item[0], 
            'count': item[1] 
        }))

        value_counts.saveAsNewAPIHadoopFile(
            path='-', 
            outputFormatClass="org.elasticsearch.hadoop.mr.EsOutputFormat",
            keyClass="org.apache.hadoop.io.NullWritable", 
            valueClass="org.elasticsearch.hadoop.mr.LinkedMapWritable", 
            conf=es_write_conf)
