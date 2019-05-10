#!/bin/bash
 
# This script is supposed to run as the user "ulyaoth".

# Set required variables.
ulyaothos=`cat /etc/ulyaoth`

if [ "$ulyaothos" == "amazonlinux2" ]
then
  # If Amazon Linux 2 change repo file.
  ulyaothos=`cat /etc/ulyaoth`  
else
  ulyaothos=`cat /etc/ulyaoth | sed 's/[0-9]*//g'`
fi

# Create build environment.
rpmdev-setuptree

# Download spec file.
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth/SPECS/ulyaoth.spec -O /home/ulyaoth/rpmbuild/SPECS/ulyaoth.spec

# Change spec file to correct operating system.
sed -i "s/changme/$ulyaothos/g" /home/ulyaoth/rpmbuild/SPECS/ulyaoth.spec

# Download additional files specified in spec file.
spectool /home/ulyaoth/rpmbuild/SPECS/ulyaoth.spec -g -R

# Install all requirements
if type dnf 2>/dev/null
then
  sudo dnf builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth.spec
elif type yum 2>/dev/null
then
  sudo yum-builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth.spec
fi

# Build the rpm.
rpmbuild -ba /home/ulyaoth/rpmbuild/SPECS/ulyaoth.spec 