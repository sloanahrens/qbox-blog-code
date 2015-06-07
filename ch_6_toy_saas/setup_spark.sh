#!/usr/bin/env bash

sudo apt-get -y update
sudo apt-get -y upgrade

# # install openjdk-7 
# sudo apt-get purge openjdk*
# sudo apt-get -y install openjdk-7-jdk

# spark
wget http://d3kbcqa49mib13.cloudfront.net/spark-1.3.1-bin-hadoop2.6.tgz -O spark.tgz
tar -xf spark.tgz
rm spark.tgz
sudo mv spark-* ~/spark

# get elasticsearch-hadoop adapter
cd ~/spark # or equivalent
mkdir jars; cd jars
wget http://central.maven.org/maven2/org/elasticsearch/elasticsearch-hadoop/2.1.0.Beta2/elasticsearch-hadoop-2.1.0.Beta2.jar
# newer version of the adapter causes an error I haven't tracked down yet:
# wget http://central.maven.org/maven2/org/elasticsearch/elasticsearch-hadoop/2.0.2/elasticsearch-hadoop-2.0.2.jar

