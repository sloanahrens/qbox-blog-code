
# set environment variables for use with Spark deployment script:
export CLUSTER=sparkcluster
export INSTANCE=t2.small
export REGION=us-west-2
export NODES=5
export AWS_ACCESS_KEY_ID=<YOUR_ACCESS_KEY>
export AWS_SECRET_ACCESS_KEY=<YOUR_SECRET_ACCESS_KEY>

cd ~

# launch a cluster
./spark/ec2/spark-ec2 -k ubuntu-spark -i ~/.ssh/id_rsa.pub -s $NODES -r $REGION -t $INSTANCE launch $CLUSTER

# log in to cluster
./spark/ec2/spark-ec2 -k ubuntu-spark -i ~/.ssh/id_rsa.pub -r $REGION login $CLUSTER

# create jars directory
mkdir spark/jars; cd spark/jars
# get elasticsearch-hadoop jar
wget http://central.maven.org/maven2/org/elasticsearch/elasticsearch-hadoop/2.1.0.Beta2/elasticsearch-hadoop-2.1.0.Beta2.jar

# get the code
cd ~
git clone https://github.com/sloanahrens/qbox-blog-code.git

# install pip and the python ES client
sudo yum -y install python-setuptools
sudo easy_install pip
sudo pip install elasticsearch

# run the script
python ~/qbox-blog-code/ch_4_matmult/random_mm.py

exit


# terminate cluster
./spark/ec2/spark-ec2 -k ubuntu-spark -i ~/.ssh/id_rsa.pub -r $REGION destroy $CLUSTER
