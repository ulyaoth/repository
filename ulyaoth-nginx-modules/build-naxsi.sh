#!/bin/bash
 
# This script is supposed to run as the user "ulyaoth".

# Set version for module.
moduleversion=0.55.3

# create module folder used to build
wget https://github.com/nbs-system/naxsi/archive/$moduleversion.tar.gz
tar xvf v$moduleversion.tar.gz
mv naxsi-module-$moduleversion /home/ulyaoth/naxsi-module
rm -rf v$moduleversion.tar.gz

# Create build environment.
rpmdev-setuptree

# Download spec file.
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-modules/SPECS/ulyaoth-nginx-naxsi-module.spec -O /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-naxsi-module.spec
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-modules/SPECS/ulyaoth-nginx-mainline-naxsi-module.spec -O /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-mainline-naxsi-module.spec


# Download additional files specified in spec file.
spectool /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-naxsi-module.spec -g -R
spectool /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-mainline-naxsi-module.spec -g -R

# Install all requirements
if type dnf 2>/dev/null
then
  sudo dnf builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-naxsi-module.spec
  sudo dnf builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-mainline-naxsi-module.spec
elif type yum 2>/dev/null
then
  sudo yum-builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-naxsi-module.spec
  sudo yum-builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-mainline-naxsi-module.spec
fi

# export variables
export QA_RPATHS=$[ 0x0001|0x0002 ]

# Build the rpm.
rpmbuild -ba /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-naxsi-module.spec
rpmbuild -ba /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-mainline-naxsi-module.spec

# Clean non related rpms
find /home/ulyaoth/rpmbuild/RPMS/x86_64/ | grep -v "-naxsi-" |xargs rm