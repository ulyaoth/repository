# This script is supposed to run as the user "ulyaoth".

# Set required variables.
ulyaothos=`cat /etc/ulyaoth`

# Create build environment.
rpmdev-setuptree

# Download spec file.
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-varnish/SPECS/ulyaoth-varnish5.1.spec -O /home/ulyaoth/rpmbuild/SPECS/ulyaoth-varnish5.1.spec

# Change required package for Amazon Linux 2
if [ "$ulyaothos" == "amazonlinux2" ]
then
  sed -i "s/jemalloc-devel/memkind-devel/g" /home/ulyaoth/rpmbuild/SPECS/ulyaoth-varnish5.1.spec
  sed -i "s/jemalloc/memkind/g" /home/ulyaoth/rpmbuild/SPECS/ulyaoth-varnish5.1.spec
fi

# Install all requirements
if type dnf 2>/dev/null
then
  sudo dnf builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-varnish5.1.spec
  sudo dnf install -y python34
elif type yum 2>/dev/null
then
  sudo yum-builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-varnish5.1.spec
  sudo yum install -y python34
fi

# Download additional files specified in spec file.
spectool /home/ulyaoth/rpmbuild/SPECS/ulyaoth-varnish5.1.spec -g -R

# Build the rpm.
rpmbuild -ba /home/ulyaoth/rpmbuild/SPECS/ulyaoth-varnish5.1.spec