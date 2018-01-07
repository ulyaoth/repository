#!/bin/bash
 
# This script is supposed to run as the user "ulyaoth".

# Set version for module.
moduleversion=0.05
develkitversion=0.3.0

# create module folder used to build
wget https://github.com/openresty/array-var-nginx-module/archive/v$moduleversion.tar.gz
tar xvf v$moduleversion.tar.gz
mv array-var-nginx-module-$moduleversion /home/ulyaoth/array-var-module
rm -rf v$moduleversion.tar.gz
wget https://github.com/simpl/ngx_devel_kit/archive/v$develkitversion.tar.gz
tar xvf v$develkitversion.tar.gz
mv ngx_devel_kit-$develkitversion /home/ulyaoth/devel-kit-module
rm -rf v$develkitversion.tar.gz

# Create build environment.
rpmdev-setuptree

# Download spec file.
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-modules/SPECS/ulyaoth-nginx-array-var-module.spec -O /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-array-var-module.spec
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-modules/SPECS/ulyaoth-nginx-mainline-array-var-module.spec -O /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-mainline-array-var-module.spec


# Download additional files specified in spec file.
spectool /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-array-var-module.spec -g -R
spectool /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-mainline-array-var-module.spec -g -R

# Install all requirements
if type dnf 2>/dev/null
then
  sudo dnf builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-array-var-module.spec
  sudo dnf builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-mainline-array-var-module.spec
elif type yum 2>/dev/null
then
  sudo yum-builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-array-var-module.spec
  sudo yum-builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-mainline-array-var-module.spec
fi

# export variables
export QA_RPATHS=$[ 0x0001|0x0002 ]

# Build the rpm.
rpmbuild -ba /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-array-var-module.spec
rpmbuild -ba /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-mainline-array-var-module.spec

# Clean non related rpms
find /home/ulyaoth/rpmbuild/RPMS/x86_64/ | grep -v "-array-" |xargs rm