# ON FRESH NEW UBUNTU 14 VM

# To set up guest additions (makes VM much more user-friendly):
# VirtualBoxVM menu -> Devices -> Install Guest Additions CD Image
# if it fails (media locked error), run this from the terminal:
# sudo apt-get install virtualbox-guest-additions-iso
# then restart and try again
# if that doesn't work, power down the VM,
# then remove the cd drive from the VM using the VirtualBox UI,
# then add it back and try again

# To add a shared folder between host os and guest os:
# add directory <DIR_NAME> as shared folder from VirtualBox UI
# folder will be at /media/sf_<DIR_NAME>
# to access it your user will need permissions, so run:
sudo usermod -a -G vboxsf <USERNAME>
 # then restart



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
#[now copy your new public key to GitHub via the website]

# test
ssh -T git@github.com

git config --global user.email "<YOUR_EMAIL>"
git config --global user.name "<YOUR_NAME>"


# download code repo
git clone https://github.com/sloanahrens/qbox-blog-code.git

