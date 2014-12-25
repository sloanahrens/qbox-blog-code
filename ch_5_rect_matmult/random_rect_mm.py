from os import system
from math import sqrt, log, ceil
from time import time
from random import seed, randrange, randint
from elasticsearch import Elasticsearch

# ES_HOST = { 
#     "host" : "23ca3ca1db3fc430000.qbox.io", 
#     "port" : 80 
# }

ES_HOST = { 
    "host" : "localhost", 
    "port" : 9200
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

def createRandomSparseMatrix(es_client, index_name, M, N, elem_range, shards, D):

    createMatrixIndex(es_client, index_name, shards)

    bulk_data = [] 

    num_of_elements = int(round(D * M*N))

    for elem_num in xrange(num_of_elements):
        
        # generate random row and column indices, and element value
        i = randint(1, M)
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

    start_time = time()

    shards = 5

    seed(time())

    es_client = Elasticsearch(hosts = [ES_HOST])

    D = 1 #log(N, 2)**4 / N**2

    M = 15
    N = 5
    P = 10

    print('\nD* = %s\nM = %s\nN = %s\nP = %s' % (D, M, N, P))

    createMatrixIndex(es_client, 'matrix-c', shards)

    createRandomSparseMatrix(es_client, 'matrix-a', M, N, 10, shards, D)

    createRandomSparseMatrix(es_client, 'matrix-b', N, P, 10, shards, D)

    matA_count = es_client.count(index='matrix-a', doc_type='elem')['count']
    matB_count = es_client.count(index='matrix-b', doc_type='elem')['count']

    D = (matA_count + matB_count) / float(M*N + M*P)

    print('\nD = %s\n' % D)
    print('M = %s' % M)
    print('N = %s' % N)
    print('P = %s\n' % P)
    print('M*N = %s' % (M*N))
    print('D * M*N = %s\n' % int(round(D * M*N)))
    print('N*P = %s' % (N*P))
    print('D * N*P = %s\n' % int(round(D * N*P)))

    elapsed = round(time() - start_time, 2)
    print("--- %s seconds ---" % elapsed)

    # master_path = 'spark://ec2-54-149-165-224.us-west-2.compute.amazonaws.com:7077'
    master_path = 'local[4]'
    jar_path = '~/spark/jars/elasticsearch-hadoop-2.1.0.Beta2.jar'
    code_path = '~/qbox-blog-code/ch_5_rect_matmult/es_spark_rect_mm.py'

    system("~/spark/bin/spark-submit --master %s --jars %s %s %s %s %s" % 
        (master_path, jar_path, code_path, M, N, P))


