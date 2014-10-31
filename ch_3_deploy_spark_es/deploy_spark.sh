
# create SSH key, if needed
ssh-keygen -t rsa -C "<your_email>"
# start the ssh-agent in the background, if needed
eval "$(ssh-agent -s)"
# add the key
ssh-add ~/.ssh/id_rsa

# show key value
cat ~/.ssh/id_rsa.pub
#[now copy your new public key to the clipboard]

# EC2 dashboard -> Key Pairs -> Import Key Pair -> [paste public key contents]
# I named my key "ubuntu-spark"

# set environment variables for use with Spark deployment script:
export CLUSTER=sparkcluster
export INSTANCE=t2.small
export REGION=us-west-2
export AWS_ACCESS_KEY_ID=<YOUR_ACCESS_KEY>
export AWS_SECRET_ACCESS_KEY=<YOUR_SECRET_ACCESS_KEY>

cd ~

# launch a cluster with 2 worker nodes
./spark/ec2/spark-ec2 -k ubuntu-spark -i ~/.ssh/id_rsa.pub -s 2 -r $REGION -t $INSTANCE launch $CLUSTER

# log in to cluster
./spark/ec2/spark-ec2 -k ubuntu-spark -i ~/.ssh/id_rsa.pub -r $REGION login $CLUSTER

# create jars directory
mkdir spark/jars; cd spark/jars
# get elasticsearch-hadoop jar
wget http://central.maven.org/maven2/org/elasticsearch/elasticsearch-hadoop/2.1.0.Beta2/elasticsearch-hadoop-2.1.0.Beta2.jar
# make code directory
cd ..; mkdir code
exit

# back on local VM
export HOST=ec2-54-69-163-110.us-west-2.compute.amazonaws.com

export CODEFILE=~/local_code/qbox-blog-code/ch_3_deploy_spark_es/es_spark_cloud.py

# # [edit code file if needed]
# # test code file locally
# export JARFILE=~/spark/jars/elasticsearch-hadoop-2.1.0.Beta2.jar
# ./spark/bin/spark-submit --master local[4] --jars $JARFILE $CODEFILE
# # delete and rebuild index
# python build_index_qbox.py

# upload code file to master node
scp -i ~/.ssh/id_rsa.pub $CODEFILE root@$HOST:spark/code

# log back into cluster master
./spark/ec2/spark-ec2 -k ubuntu-spark -i ~/.ssh/id_rsa.pub -r $REGION login $CLUSTER

# run our script on master
./spark/bin/spark-submit --master local --jars spark/jars/elasticsearch-hadoop-2.1.0.Beta2.jar spark/code/es_spark_cloud.py
# log out
exit

# terminate cluster
./spark/ec2/spark-ec2 -k ubuntu-spark -i ~/.ssh/id_rsa.pub -r $REGION destroy $CLUSTER
