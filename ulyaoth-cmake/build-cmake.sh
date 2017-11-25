# This script is supposed to run as the user "ulyaoth".

# Get OS
ulyaothos=`cat /etc/ulyaoth`

# If OS for rhel is 6 install additional packages.
if [ "$ulyaothos" == "redhat6" ] || [ "$ulyaothos" == "oraclelinux6" ] || [ "$ulyaothos" == "scientificlinux6" ] || [ "$ulyaothos" == "centos6" ]
then
  # Install newer g++
  sudo yum install -y http://ftp.scientificlinux.org/linux/scientific/6x/external_products/softwarecollections/yum-conf-softwarecollections-2.0-1.el6.noarch.rpm
  sudo yum install -y devtoolset-7-gcc-c++
  
  # Export newer g++ to environment
  export CC=/opt/rh/devtoolset-7/root/usr/bin/gcc
  export CXX=/opt/rh/devtoolset-7/root/usr/bin/g++
fi

# Clean repository because AMI could have old data.
if type dnf 2>/dev/null
then
  sudo dnf clean all
elif type yum 2>/dev/null
then
  sudo yum clean all
fi

# Create build environment.
rpmdev-setuptree

# Download spec file.
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-cmake/SPECS/ulyaoth-cmake.spec -O /home/ulyaoth/rpmbuild/SPECS/ulyaoth-cmake.spec

# Install all requirements
if type dnf 2>/dev/null
then
  sudo dnf builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-cmake.spec
elif type yum 2>/dev/null
then
  sudo yum-builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-cmake.spec
fi

# Download additional files specified in spec file.
spectool /home/ulyaoth/rpmbuild/SPECS/ulyaoth-cmake.spec -g -R

# Build the rpm.
rpmbuild -ba /home/ulyaoth/rpmbuild/SPECS/ulyaoth-cmake.spec