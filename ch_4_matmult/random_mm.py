from os import system
from math import sqrt, log, ceil
from time import time
from random import seed, randrange, randint
from elasticsearch import Elasticsearch

ES_HOST = { 
    "host" : "23ca3ca1db3fc430000.qbox.io", 
    "port" : 80 
}

def createMatrixIndex(es_client, index_name, shards):
    if es_client.indices.exists(index_name):
        print("deleting '%s' index..." % (index_name))
        print(es_client.indices.delete(index = index_name, ignore=[400, 404]))

    request_body = {
        "settings" : {
            "number_of_shards": shards,
            "number_of_replicas": 1
        }
    }

    print("creating '%s' index..." % (index_name))
    print(es_client.indices.create(index = index_name, body = request_body))

def createRandomSparseMatrix(es_client, index_name, N, elem_range, shards, D):

    createMatrixIndex(es_client, index_name, shards)

    bulk_data = [] 

    num_of_elements = int(round(D * N**2))

    for elem_num in xrange(num_of_elements):
        
        # generate random row and column indices, and element value
        i = randint(1, N)
        j = randint(1, N)
        cell_val = randrange(-elem_range, elem_range, 1)

        # only store non-zero values
        if cell_val == 0:
            continue

        # use the ES bulk API
        bulk_data.append({
            "index": {
                "_index": index_name, 
                "_type": 'elem', 
                "_id": '%s-%s' % (i,j)
            }
        })
        bulk_data.append({
            'row': i,
            'col': j,
            'val': cell_val
        })

        if len(bulk_data) > 10000:
            res = es_client.bulk(index=index_name,body=bulk_data,refresh=True)
            bulk_data = []
        
    if len(bulk_data) > 0:
        res = es_client.bulk(index=index_name,body=bulk_data,refresh=True)



if __name__ == '__main__':

    shards = 10

    seed(time())

    es_client = Elasticsearch(hosts = [ES_HOST])

    n_vals = sorted( [10**(p+2) for p in xrange(7)] + [3*10**(p+2) for p in xrange(7)] )

    for N in [1000]:

        start_time = time()

        D = log(N, 2)**4 / N**2

        print('\nN = %s\nD* = %s' % (N, D))

        createMatrixIndex(es_client, 'matrix-c', shards)

        createRandomSparseMatrix(es_client, 'matrix-a', N, 10, shards, D)

        createRandomSparseMatrix(es_client, 'matrix-b', N, 10, shards, D)

        matA_count = es_client.count(index='matrix-a', doc_type='elem')['count']
        matB_count = es_client.count(index='matrix-b', doc_type='elem')['count']

        D = (matA_count + matB_count) / float(2 * N**2)

        print('N = %s' % N)
        print('N^2 = %s' % N**2)
        print('D = %s' % D)
        print('D * N^2 = %s' % int(round(D * N**2)))

        elapsed = round(time() - start_time, 2)
        print("--- %s seconds ---" % elapsed)

        # master_path = 'spark://ec2-54-149-159-89.us-west-2.compute.amazonaws.com:7077'
        master_path = 'local[4]'
        jar_path = '~/spark/jars/elasticsearch-hadoop-2.1.0.Beta2.jar'
        code_path = '~/qbox-blog-code/ch_4_matmult/es_spark_mm.py'

        system("~/spark/bin/spark-submit --master %s --jars %s %s %s" % (master_path, jar_path, code_path, N))


