# ON FRESH NEW UBUNTU 14 VM

# add code directory as shared folder from VirtualBox UI
# to access shared folder at /media/sf_code
sudo usermod -a -G vboxsf <USERNAME>
 # then restart

 # VirtualBoxVM -> Devices -> Install Guest Additions CD Image
 # if it fails, run this from the terminal:
 # sudo apt-get install virtualbox-guest-additions-iso
 # then restart and try again


# install sublime text
sudo add-apt-repository ppa:webupd8team/sublime-text-3
sudo apt-get update
sudo apt-get install sublime-text-installer


# install, set up git
sudo apt-get install git

ssh-keygen -t rsa -C "<YOUR_EMAIL>"
# start the ssh-agent in the background
eval "$(ssh-agent -s)"
# Agent pid 59566
ssh-add ~/.ssh/id_rsa

cat < ~/.ssh/id_rsa.pub

[copy public key to github]

# test
ssh -T git@github.com

git config --global user.email "<YOUR_EMAIL>"
git config --global user.name "<YOUR_NAME>"

# code repo
git clone # ON FRESH NEW UBUNTU 14 VM

# add code directory as shared folder from VirtualBox UI
# to access shared folder at /media/sf_code
sudo usermod -a -G vboxsf <USERNAME>
 # then restart

 # VirtualBoxVM -> Devices -> Install Guest Additions CD Image
 # if it fails, run this from the terminal:
 # sudo apt-get install virtualbox-guest-additions-iso
 # then restart and try again


# install sublime text
sudo add-apt-repository ppa:webupd8team/sublime-text-3
sudo apt-get update
sudo apt-get install sublime-text-installer


# install, set up git
sudo apt-get install git

ssh-keygen -t rsa -C "<YOUR_EMAIL>"
# start the ssh-agent in the background
eval "$(ssh-agent -s)"
# Agent pid 59566
ssh-add ~/.ssh/id_rsa

cat < ~/.ssh/id_rsa.pub

[copy public key to github]

# test
ssh -T git@github.com

git config --global user.email "<YOUR_EMAIL>"
git config --global user.name "<YOUR_NAME>"

# code repo
git clone # ON FRESH NEW UBUNTU 14 VM

# add code directory as shared folder from VirtualBox UI
# to access shared folder at /media/sf_code
sudo usermod -a -G vboxsf <USERNAME>
 # then restart

 # VirtualBoxVM -> Devices -> Install Guest Additions CD Image
 # if it fails, run this from the terminal:
 # sudo apt-get install virtualbox-guest-additions-iso
 # then restart and try again


# install sublime text
sudo add-apt-repository ppa:webupd8team/sublime-text-3
sudo apt-get update
sudo apt-get install sublime-text-installer


# install, set up git
sudo apt-get install git

ssh-keygen -t rsa -C "<YOUR_EMAIL>"
# start the ssh-agent in the background
eval "$(ssh-agent -s)"
# Agent pid 59566
ssh-add ~/.ssh/id_rsa

cat < ~/.ssh/id_rsa.pub

[copy public key to github]

# test
ssh -T git@github.com

git config --global user.email "<YOUR_EMAIL>"
git config --global user.name "<YOUR_NAME>"

# code repo
git clone https://github.com/sloanahrens/qbox-blog-code.git


# install java
sudo apt-get purge openjdk*
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install oracle-java8-installer




# install java
sudo apt-get purge openjdk*
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install oracle-java8-installer




# install oracle java 8
sudo apt-get purge openjdk*
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install oracle-java8-installer

