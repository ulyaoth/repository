# This script is supposed to run as the user "ulyaoth".

# Create build environment.
rpmdev-setuptree

# Download spec file.
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-openssl/SPECS/ulyaoth-openssl0.9.8.spec -O /home/ulyaoth/rpmbuild/SPECS/ulyaoth-openssl0.9.8.spec

# Download additional files specified in spec file.
spectool /home/ulyaoth/rpmbuild/SPECS/ulyaoth-openssl0.9.8.spec -g -R

# Install all requirements
if type dnf 2>/dev/null
then
  sudo dnf builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-openssl0.9.8.spec
elif type yum 2>/dev/null
then
  sudo yum-builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-openssl0.9.8.spec
fi

# export variables
export QA_RPATHS=$[ 0x0001|0x0002 ]

# Build the rpm.
rpmbuild -ba /home/ulyaoth/rpmbuild/SPECS/ulyaoth-openssl0.9.8.spec