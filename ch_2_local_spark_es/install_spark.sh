
# download spark
wget http://d3kbcqa49mib13.cloudfront.net/spark-1.1.0-bin-hadoop2.4.tgz -O spark.tgz

# extract, clean up
tar -xf spark.tgz
rm spark.tgz
sudo mv spark-* spark

# run spark
cd ~/spark
./bin/pyspark

# run spark with 4 cores
./bin/pyspark --master local[4]


# get elasticsearch-hadoop adapter
cd ~/spark # or equivalent
mkdir jars; cd jars
wget http://central.maven.org/maven2/org/elasticsearch/elasticsearch-hadoop/2.1.0.Beta2/elasticsearch-hadoop-2.1.0.Beta2.jar
cd ..

# run spark with elasticsearch-hadoop jar
./bin/pyspark --master local[4] --jars jars/elasticsearch-hadoop-2.1.0.Beta2.jar

# run es_spark_test.py
./spark/bin/spark-submit --master local[4] --jars spark/jars/elasticsearch-hadoop-2.1.0.Beta2.jar ~/local_code/qbox-blog-code/ch_2_local_spark_es/es_spark_test.py

./spark/bin/spark-submit --master local[4] --jars spark/jars/elasticsearch-hadoop-2.1.0.Beta2.jar ~/local_code/qbox-blog-code/ch_4_matrix_mult/es_spark_mm.py

# http://sense.qbox.io/gist/46c166c983d8fa40bbe5af4004e694eb674d3e04