import os
import random
import time
from datetime import datetime

from flask import Flask, request, render_template, session, flash, redirect, \
    url_for, jsonify

from celery import Celery

from elasticsearch import Elasticsearch


app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'


# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'


# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


ES_HOST = {
    "host" : "localhost", 
    "port" : 9200
}
es = Elasticsearch(hosts = [ES_HOST])         


@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')


@app.route('/sparktask', methods=['POST'])
def sparktask():
    task = spark_job_task.apply_async()

    if not es.indices.exists('spark-jobs'):
        print("creating '%s' index..." % ('spark-jobs'))
        res = es.indices.create(index='spark-jobs', body={
            "settings" : {
                "number_of_shards": 1,
                "number_of_replicas": 0
            }
        })
        print(res)

    es.index(index='spark-jobs', doc_type='job', id=task.id, body={
        'current': 0, 
        'total': 100,
        'status': 'Spark job pending..',
        'start_time': datetime.utcnow()
    })

    return jsonify({}), 202, {'Location': url_for('taskstatus', task_id=task.id)}


@app.route('/status/<task_id>')
def taskstatus(task_id, methods=['GET']):
    
    task = spark_job_task.AsyncResult(task_id)

    if task.state == 'FAILURE':
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    else:
        # otherwise get the task info from ES
        es_task_info = es.get(index='spark-jobs',doc_type='job',id=task_id)
        response = es_task_info['_source']
        response['state'] = task.state

    return jsonify(response)


@celery.task(bind=True)
def spark_job_task(self):

    task_id = self.request.id

    master_path = 'local[2]'

    project_dir = '~/qbox-blog-code/ch_6_toy_saas/'

    jar_path = '~/spark/jars/elasticsearch-hadoop-2.1.0.Beta2.jar'

    spark_code_path =  project_dir + 'es_spark_test.py'

    os.system("~/spark/bin/spark-submit --master %s --jars %s %s %s" % 
        (master_path, jar_path, spark_code_path, task_id))

    return {'current': 100, 'total': 100, 'status': 'Task completed!', 'result': 42} 


if __name__ == '__main__':
    app.run(debug=True)


# some helpful sense code:
# http://sense.qbox.io/gist/4f7ed0e6aa51f6badd9d27de979741e4b8768205
