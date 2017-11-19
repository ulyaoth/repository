# This script is supposed to run as the user "ulyaoth".

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
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tengine/SPECS/ulyaoth-tengine.spec -O /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tengine.spec

# Install all requirements
if type dnf 2>/dev/null
then
  sudo dnf builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tengine.spec
elif type yum 2>/dev/null
then
  sudo yum-builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tengine.spec
fi

# Download additional files specified in spec file.
spectool /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tengine.spec -g -R

# Build the rpm.
rpmbuild -ba /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tengine.spec