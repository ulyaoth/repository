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
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tengine/SPECS/ulyaoth-tengine-selinux.spec -O /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tengine-selinux.spec

# Download selinux file
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tengine/SELinux/ulyaoth-tengine.txt -O /home/ulyaoth/ulyaoth-tengine.txt

# Create Selinux file
audit2allow -M ulyaoth-tengine < ulyaoth-tengine.txt

# move selinux file to rpmbuild sources
mv /home/ulyaoth/ulyaoth-tengine.pp /home/ulyaoth/rpmbuild/SOURCES/

# Install all requirements
if type dnf 2>/dev/null
then
  sudo dnf install -y policycoreutils-python
  sudo dnf builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tengine-selinux.spec
elif type yum 2>/dev/null
then
  sudo yum install -y policycoreutils-python
  sudo yum-builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tengine-selinux.spec
fi

# Download additional files specified in spec file.
spectool /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tengine-selinux.spec -g -R

# Build the rpm.
rpmbuild -ba /home/ulyaoth/rpmbuild/SPECS/ulyaoth-tengine-selinux.spec