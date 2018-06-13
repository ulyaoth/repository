#!/bin/bash
 
# This script is supposed to run as the user "ulyaoth".

# Set version for module.
moduleversion=5.3.2

# Get the passenger version 
passenger5()
{
sudo rm -rf  /usr/local/ulyaoth/passenger5
sudo mkdir -p /usr/local/ulyaoth/passenger5
sudo chown -R ulyaoth:ulyaoth /usr/local/ulyaoth
cd /usr/local/ulyaoth/passenger5
git clone -b stable-5.0 git://github.com/phusion/passenger.git
cd /usr/local/ulyaoth/passenger5/passenger
git checkout release-$moduleversion
git submodule update --init --recursive
cd /home/ulyaoth
mv /usr/local/ulyaoth/passenger5/passenger/* /usr/local/ulyaoth/passenger5/
rm -rf /usr/local/ulyaoth/passenger5/passenger
sudo chown -R ulyaoth:ulyaoth /usr/local/ulyaoth
}

# create module folder used to build
passenger5

# Create build environment.
rpmdev-setuptree

# Download spec file.
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-modules/SPECS/ulyaoth-nginx-passenger5-module.spec -O /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-passenger5-module.spec
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-modules/SPECS/ulyaoth-nginx-mainline-passenger5-module.spec -O /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-mainline-passenger5-module.spec


# Download additional files specified in spec file.
spectool /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-passenger5-module.spec -g -R
spectool /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-mainline-passenger5-module.spec -g -R

# Install all requirements
if type dnf 2>/dev/null
then
  sudo dnf builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-passenger5-module.spec
  sudo dnf builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-mainline-passenger5-module.spec
elif type yum 2>/dev/null
then
  sudo yum-builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-passenger5-module.spec
  sudo yum-builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-mainline-passenger5-module.spec
fi

# export variables
export QA_RPATHS=$[ 0x0001|0x0002 ]

# Build the rpm.
rpmbuild -ba /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-passenger5-module.spec
passenger5
rpmbuild -ba /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-mainline-passenger5-module.spec

# Clean non related rpms
find /home/ulyaoth/rpmbuild/RPMS/x86_64/ | grep -v "passenger5" |xargs rm
find /home/ulyaoth/rpmbuild/RPMS/noarch/ | grep -v "passenger5" |xargs rm
find /home/ulyaoth/rpmbuild/SRPMS/ | grep -v "passenger5" |xargs rm
find /home/ulyaoth/rpmbuild/SRPMS/ | grep -v "passenger5" |xargs rm