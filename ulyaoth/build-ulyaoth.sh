# This script is supposed to run as the user "ulyaoth".

# Set required variables.
ulyaothos=`cat /etc/ulyaoth | sed 's/[0-9]*//g'`

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