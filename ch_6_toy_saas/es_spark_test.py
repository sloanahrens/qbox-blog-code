import sys
import json

from pyspark import SparkContext, SparkConf

from elasticsearch import Elasticsearch


if __name__ == "__main__":

    task_id = sys.argv[1]
    print(task_id)

    ES_HOST = {
        "host" : "localhost", 
        "port" : 9200
    }
    es = Elasticsearch(hosts = [ES_HOST])

    es.update(index='spark-jobs', doc_type='job', id=task_id, body={
        'doc': { 
            'current': 1,
            'status': 'Spark job started..' 
        }
    })

    result_indices = len(es.indices.get_aliases(index="titanic-results-*"))
    output_resource = "titanic-results-%s/value-counts" % (result_indices + 1)

    conf = SparkConf().setAppName("ESTest")
    sc = SparkContext(conf=conf)
    
    es_rdd = sc.newAPIHadoopRDD(
        inputFormatClass="org.elasticsearch.hadoop.mr.EsInputFormat",
        keyClass="org.apache.hadoop.io.NullWritable", 
        valueClass="org.elasticsearch.hadoop.mr.LinkedMapWritable", 
        conf={ "es.resource" : "titanic/passenger" })

    doc = es_rdd.first()[1]

    num_fields = len(doc)

    for idx, field in enumerate(doc):

        es.update(index='spark-jobs', doc_type='job', id=task_id, body={
            'doc': { 
                'current': (idx+1) * 95 / num_fields,
                'status': 'Spark job underway..' 
            }
        })

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
            conf={ "es.resource" : output_resource })
        

    es.update(index='spark-jobs', doc_type='job', id=task_id, body={
        'doc': { 
            'current': 100,
            'status': 'Spark job finished.',
            'result': output_resource
        }
    })
