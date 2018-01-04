# This script is supposed to run as the user "ulyaoth".

# Set required variables.
ulyaothos=`cat /etc/ulyaoth`

# Create build environment.
rpmdev-setuptree

# Download spec file.
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth/SPECS/ulyaoth.spec -O /home/ulyaoth/rpmbuild/SPECS/ulyaoth.spec

# Change spec file to correct operating system.
sed -i "s/sbagmeijer/$ulyaothos/g" /home/ulyaoth/rpmbuild/SPECS/ulyaoth.spec

# Download additional files specified in spec file.
spectool /home/ulyaoth/rpmbuild/SPECS/ulyaoth.spec -g -R

# If Amazon Linux 2 change repo file.
if [ "$ulyaothos" == "amazonlinux2" ]
then
  sed -i "s/amzn/amzn2/g" /home/ulyaoth/rpmbuild/SOURCES/ulyaoth-amazonlinux.repo
fi

# Build the rpm.
rpmbuild -ba /home/ulyaoth/rpmbuild/SPECS/ulyaoth.spec