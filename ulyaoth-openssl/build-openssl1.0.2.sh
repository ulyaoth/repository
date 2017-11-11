# This script is supposed to run as the user "ulyaoth".

# Create build environment.
rpmdev-setuptree

# Download spec file.
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-openssl/SPECS/ulyaoth-openssl1.0.2.spec -O /home/ulyaoth/rpmbuild/SPECS/ulyaoth-openssl1.0.2.spec

# Download additional files specified in spec file.
spectool /home/ulyaoth/rpmbuild/SPECS/ulyaoth-openssl1.0.2.spec -g -R

# Install all requirements
if type dnf 2>/dev/null
then
  sudo dnf builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-openssl1.0.2.spec
elif type yum 2>/dev/null
then
  sudo yum-builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-openssl1.0.2.spec
fi

# Build the rpm.
QA_RPATHS=\$[ 0x0001|0x0002 ] rpmbuild -ba /home/ulyaoth/rpmbuild/SPECS/ulyaoth-openssl1.0.2.spec

# Copy the file to Ulyaoth home folder.
cp /home/ulyaoth/rpmbuild/SRPMS/* /home/ulyaoth/
cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /home/ulyaoth/
cp /home/ulyaoth/rpmbuild/RPMS/noarch/* /home/ulyaoth/