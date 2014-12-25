from pyspark import SparkContext, SparkConf
# import json
from math import log, ceil, sqrt
from time import time

from elasticsearch import Elasticsearch

import sys

ES_HOST = { 
    "host" : "localhost", 
    "port" : 9200 
}

# ES_HOST = { 
#     "host" : "23ca3ca1db3fc430000.qbox.io", 
#     "port" : 80 
# }

# this will get set during execution
# needed by grouping mapper functions
GRP_SIZE = 1

# maps an element in matrix A to the appropriate groups
def group_mapper_A(item):
    row = item[1]['row']
    col = item[1]['col']
    val = item[1]['val']

    i_grp = int(ceil(row / float(GRP_SIZE)))

    # the factor of 2 turns out to reduce communication costs
    j_grp = int(ceil(2 * col / float(GRP_SIZE)))

    return [( (i_grp, j_grp, k + 1), ('A', row, col, val) ) for k in xrange(G + 1)]

# maps an element in matrix B to the appropriate groups
def group_mapper_B(item):
    row = item[1]['row']
    col = item[1]['col']
    val = item[1]['val']

    # the factor of 2 turns out to reduce communication costs
    j_grp = int(ceil(2 * row / float(GRP_SIZE)))

    k_grp = int(ceil(col / float(GRP_SIZE)))

    return [( (i + 1, j_grp, k_grp), ('B', row, col, val) ) for i in xrange(G + 1)]

# computes the partial sums corresponding to the elements of C
# that can be calculated from the elements in the given group
# only emits non-zero elements
def partialSums(item):
    partials = {}

    for elem in item[1]:
        if elem[0] == 'B': 
            continue

        A_row = elem[1]
        A_col = elem[2]
        A_val = elem[3]

        for elem in item[1]:
            if elem[0] == 'A':
                continue

            B_row = elem[1]
            B_col = elem[2]
            B_val = elem[3]

            if A_col == B_row:
                group = partials.setdefault((A_row, B_col), [])
                group.append(A_val * B_val)

    partial_sums = [(key, sum(partials[key])) for key in partials.keys()]
    
    return [item for item in partial_sums if item[1] != 0]


if __name__ == "__main__":

    start_time = time()

    if len(sys.argv) < 4:
        print >> sys.stderr, "*** missing matrix size parameter; aborting"
        exit(-1)

    M = int(sys.argv[1])
    N = int(sys.argv[2])
    P = int(sys.argv[3])

    # create Spark context
    sc = SparkContext(appName="ESSparkMM")

    # es client for input parameters, and output stats
    es_client = Elasticsearch(hosts = [ES_HOST])


    # settings for connecting ES to Spark RDD
    es_conf = {
        # "es.net.proxy.http.host" : ES_HOST['host'],
        # "es.net.proxy.http.port": str(ES_HOST['port']),
        # "es.nodes.discovery": "false",
    } 
    
    # read matrix A, cache in memory
    es_conf["es.resource"] = "matrix-a/elem"
    matA_rdd = sc.newAPIHadoopRDD(
        inputFormatClass="org.elasticsearch.hadoop.mr.EsInputFormat",
        keyClass="org.apache.hadoop.io.NullWritable", 
        valueClass="org.elasticsearch.hadoop.mr.LinkedMapWritable", 
        conf=es_conf).cache()

    # read matrix B, cache in memory
    es_conf["es.resource"] = "matrix-b/elem"
    matB_rdd = sc.newAPIHadoopRDD(
        inputFormatClass="org.elasticsearch.hadoop.mr.EsInputFormat",
        keyClass="org.apache.hadoop.io.NullWritable", 
        valueClass="org.elasticsearch.hadoop.mr.LinkedMapWritable", 
        conf=es_conf).cache()


    matA_count = matA_rdd.count()
    matB_count = matB_rdd.count()

    # D is the average density of the input matrices
    D = (matA_count + matB_count) / float(M*N + N*P)

    max_dim = max(M,N,P)

    # G is the replication factor
    G = int(round(sqrt(sqrt(D * max_dim**2 / 2))))

    # GRP_SIZE is the number of rows/cols in each grouping
    GRP_SIZE = int(ceil(max_dim / float(G)))


    # map A and B to the appropriate groups
    A_groups = matA_rdd.flatMap(group_mapper_A)
    B_groups = matB_rdd.flatMap(group_mapper_B)

    # union the results
    mapped_union = A_groups.union(B_groups)

    # get partial sums for elements of C
    partial_results = mapped_union.groupByKey().flatMap(partialSums)

    # now reduce the groups by summing up the partial sums for each element, 
    # discarding zeros
    matrix_C = partial_results.reduceByKey(lambda a,b: a+b).filter(lambda item: item[1] != 0)

    # map to docs appropriate for ES, cache results
    result_docs = matrix_C.map(lambda item: ('%s-%s' % (item[0][0],item[0][1]), {
        'row': item[0][0],
        'col': item[0][1],
        'val': item[1]
    })).cache()

    # write results out to ES
    es_conf["es.resource"] = "matrix-c/elem"
    result_docs.saveAsNewAPIHadoopFile(
        path='-', 
        outputFormatClass="org.elasticsearch.hadoop.mr.EsOutputFormat",
        keyClass="org.apache.hadoop.io.NullWritable", 
        valueClass="org.elasticsearch.hadoop.mr.LinkedMapWritable", 
        conf=es_conf)

    # compute some useful stats (matrix norm is Frobenius norm)
    matC_count = result_docs.count()
    matC_zeros = M*P - matC_count
    matC_density = matC_count / float(M*P)
    matC_norm = sqrt(result_docs.map(lambda item: item[1]['val']**2).reduce(lambda a,b: a+b))

    matB_zeros = N*P - matB_count
    matB_density = matB_count / float(N*P)
    matB_norm = sqrt(matB_rdd.map(lambda item: item[1]['val']**2).reduce(lambda a,b: a+b))
    
    matA_zeros = M*N - matA_count
    matA_density = matA_count / float(M*N)
    matA_norm = sqrt(matA_rdd.map(lambda item: item[1]['val']**2).reduce(lambda a,b: a+b))

    mapped_grouped = mapped_union.groupByKey()
    mapped_group_count_average = mapped_grouped.map(lambda i: len(i[1])).reduce(lambda a,b: a+b) / mapped_grouped.count()

    
    # this section is a way to print out the matrices validation
    # can only be used with small matrices, for obvious reasons
    ##########################
    matA = matA_rdd.map(lambda i: ((i[1]['row'],i[1]['col']), i[1]['val'])).collect()
    matB = matB_rdd.map(lambda i: ((i[1]['row'],i[1]['col']), i[1]['val'])).collect()
    matC = matrix_C.collect()
  
    def print_matrix(A, M, N):
        matrix = [[0 for j in range(N)] for i in range(M)]
        for result in A:
            row = result[0][0]
            col = result[0][1]
            matrix[row-1][col-1] = result[1]
        for i in range(M):
            print(','.join([str(matrix[i][j]) for j in range(N)]) + ',')

    print('A:')
    print_matrix(matA, M, N)
    print('B:')
    print_matrix(matB, N, P)
    print('C:')
    print_matrix(matC, M, P)
    ##########################

    # print out some stats
    print('-' * 20)
    print('A: count: %s  zero_count: %s, density: %s, norm: %s' % (matA_count, matA_zeros, matA_density, matA_norm))
    print('B: count: %s  zero_count: %s, density: %s, norm: %s' % (matB_count, matB_zeros, matB_density, matB_norm))
    print('C: count: %s  zero_count: %s, density: %s, norm: %s' % (matC_count, matC_zeros, matC_density, matC_norm))

    print('mapped_group_count_average: %s' % mapped_group_count_average)

    elapsed = round(time() - start_time, 2)

    if elapsed > 120:
        if elapsed > 3600:
            print("--- %s hours ---" % round(elapsed / 3600, 2))
        else:
            print("--- %s minutes ---" % round(elapsed / 60, 2))
    else:
        print("--- %s seconds ---" % elapsed)

    # save stats to ES    
    es_client.index(index='matrix-mult-stats', doc_type='result',  
        body={
            'nodes': 1,
            'elap_sec': elapsed,
            'time': int(1000*time()),
            'g': G,
            'n': N,
            'm': M,
            'p': P,
            'd': D,
            'a_den': matA_density,
            'b_den': matB_density,
            'c_den': matC_density,
            'rel_den': matC_density / D,
            'ab_norm': sqrt(matA_norm * matB_norm),
            'a_norm': matA_norm,
            'b_norm': matB_norm,
            'c_norm': matC_norm,
            'a_ct': matA_count,
            'b_ct': matB_count,
            'c_ct': matC_count,
            'grp_cnt_avg': mapped_group_count_average
        }
    )

    sc.stop()
