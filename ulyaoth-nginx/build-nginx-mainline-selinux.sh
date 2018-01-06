#!/bin/bash
 
# This script is supposed to run as the user "ulyaoth".

# Create build environment.
rpmdev-setuptree

# Install additional required packages.
if type dnf 2>/dev/null
then
  dnf install -y policycoreutils-python checkpolicy selinux-policy-devel policycoreutils-python-utils
elif type yum 2>/dev/null
then
  yum install -y policycoreutils-python checkpolicy selinux-policy-devel policycoreutils-python-utils
fi

# Create the selinux policy and move to SOURCE.
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx/SELinux/ulyaoth-nginx-mainline.txt
audit2allow -M ulyaoth-nginx-mainline < ulyaoth-nginx-mainline.txt
mv ulyaoth-nginx-mainline.pp /home/ulyaoth/rpmbuild/SOURCES/

# Download spec file.
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx/SPECS/ulyaoth-nginx-mainline-selinux.spec -O /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-mainline-selinux.spec

# Download additional files specified in spec file.
spectool /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-mainline-selinux.spec -g -R

# Install all requirements
if type dnf 2>/dev/null
then
  sudo dnf builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-mainline-selinux.spec
elif type yum 2>/dev/null
then
  sudo yum-builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-mainline-selinux.spec
fi

# Build the rpm.
rpmbuild -ba /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-mainline-selinux.spec 