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
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-mbedtls/SPECS/ulyaoth-mbedtls2.6.spec -O /home/ulyaoth/rpmbuild/SPECS/ulyaoth-mbedtls2.6.spec

# Remove old cmake
if type dnf 2>/dev/null
then
  sudo dnf remove -y cmake*
elif type yum 2>/dev/null
then
  sudo yum remove -y cmake*
fi

# Install all requirements
if type dnf 2>/dev/null
then
  sudo dnf builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-mbedtls2.6.spec
elif type yum 2>/dev/null
then
  sudo yum-builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-mbedtls2.6.spec
fi

# Download additional files specified in spec file.
spectool /home/ulyaoth/rpmbuild/SPECS/ulyaoth-mbedtls2.6.spec -g -R

# Build the rpm.
rpmbuild -ba /home/ulyaoth/rpmbuild/SPECS/ulyaoth-mbedtls2.6.spec