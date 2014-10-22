
# download spark
wget http://d3kbcqa49mib13.cloudfront.net/spark-1.1.0-bin-hadoop2.4.tgz

# extract, clean up
tar -xf spark-1.1.0-bin-hadoop2.4.tgz
rm spark-1.1.0-bin-hadoop2.4.tgz
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


./bin/spark-submit --jars jars/elasticsearch-hadoop-2.1.0.Beta2.jar /media/sf_code/training_2014/spark/python/ESTest.py
