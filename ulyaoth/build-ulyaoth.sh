# This script is supposed to run as the user "ulyaoth".

# Set required variables.
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
sed -i "s/sbagmeijer/$ulyaothos/g" /home/ulyaoth/rpmbuild/SPECS/ulyaoth.spec

# Download additional files specified in spec file.
spectool /home/ulyaoth/rpmbuild/SPECS/ulyaoth.spec -g -R

# Build the rpm.
rpmbuild -ba /home/ulyaoth/rpmbuild/SPECS/ulyaoth.spec