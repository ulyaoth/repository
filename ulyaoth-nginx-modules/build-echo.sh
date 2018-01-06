#!/bin/bash
 
# This script is supposed to run as the user "ulyaoth".

# Set version for module.
moduleversion=0.61

# create module folder used to build
wget https://github.com/openresty/echo-nginx-module/archive/v$moduleversion.tar.gz
tar xvf v$moduleversion.tar.gz
mv echo-nginx-module-$moduleversion /home/ulyaoth/echo-module
rm -rf v$moduleversion.tar.gz

# Create build environment.
rpmdev-setuptree

# Download spec file.
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-modules/SPECS/ulyaoth-nginx-echo-module.spec -O /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-echo-module.spec
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-modules/SPECS/ulyaoth-nginx-mainline-echo-module.spec -O /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-mainline-echo-module.spec


# Download additional files specified in spec file.
spectool /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-echo-module.spec -g -R
spectool /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-mainline-echo-module.spec -g -R

# Install all requirements
if type dnf 2>/dev/null
then
  sudo dnf builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-echo-module.spec
  sudo dnf builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-mainline-echo-module.spec
elif type yum 2>/dev/null
then
  sudo yum-builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-echo-module.spec
  sudo yum-builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-mainline-echo-module.spec
fi

# export variables
export QA_RPATHS=$[ 0x0001|0x0002 ]

# Build the rpm.
rpmbuild -ba /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-echo-module.spec
rpmbuild -ba /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-mainline-echo-module.spec

# Clean non related rpms
find /home/ulyaoth/rpmbuild/RPMS/x86_64/ | grep -v "-echo-" |xargs rm