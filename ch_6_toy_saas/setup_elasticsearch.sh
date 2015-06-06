#!/usr/bin/env bash

sudo apt-get -y update
sudo apt-get -y upgrade

# install openjdk-7 
sudo apt-get purge openjdk*
sudo apt-get -y install openjdk-7-jdk

# # check java version
# java -version
# # java version "1.7.0_65"

# install curl
sudo apt-get -y install curl

# install Elasticsearch 1.5.1
wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.5.1.tar.gz -O elasticsearch.tar.gz
tar -xf elasticsearch.tar.gz
rm elasticsearch.tar.gz
sudo mv elasticsearch-* elasticsearch
sudo mv elasticsearch /usr/local/share

# set up ES as service
curl -L http://github.com/elasticsearch/elasticsearch-servicewrapper/tarball/master | tar -xz
sudo mv *servicewrapper*/service /usr/local/share/elasticsearch/bin/
rm -Rf *servicewrapper*
sudo /usr/local/share/elasticsearch/bin/service/elasticsearch install
sudo ln -s 'readlink -f /usr/local/share/elasticsearch/bin/service/elasticsearch' /usr/local/bin/rcelasticsearch
 
# start ES service
sudo service elasticsearch start


# # test ES
# curl localhost:9200
# curl -XGET http://127.0.0.1:9200/_cluster/health?pretty
# curl -XGET http://localhost:9200/_cluster/state/nodes?pretty


# install ES HQ
cd /usr/local/share/elasticsearch/
./bin/plugin -install royrusso/elasticsearch-HQ

# enable cors (to be able to use Sense)
sudo echo "http.cors.enabled: true" >> /usr/local/share/elasticsearch/config/elasticsearch.yml
sudo service elasticsearch restart
