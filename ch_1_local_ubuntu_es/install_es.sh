
# install oracle java 8
sudo apt-get purge openjdk*   # just in case
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install oracle-java8-installer

# install curl
sudo apt-get install curl

# install Elasticsearch 1.3.2
wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.3.4.tar.gz -O elasticsearch.tar.gz
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

# http://localhost:9200/_plugin/HQ/

# # stop ES service
# sudo service elasticsearch stop


# # directories
# /usr/local/share/elasticsearch


# install pip and the python ES client
sudo apt-get install python-setuptools
sudo easy_install pip
sudo pip install elasticsearch