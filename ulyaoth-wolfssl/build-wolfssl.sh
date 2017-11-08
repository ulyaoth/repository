# This script is supposed to run as the user "ulyaoth".

# Create build environment.
rpmdev-setuptree

# Download spec file.
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-wolfssl/SPECS/ulyaoth-wolfssl.spec -O /home/ulyaoth/rpmbuild/SPECS/ulyaoth-wolfssl.spec

# Download additional files specified in spec file.
spectool /home/ulyaoth/rpmbuild/SPECS/ulyaoth-wolfssl.spec -g -R

# Build the rpm.
rpmbuild -ba /home/ulyaoth/rpmbuild/SPECS/ulyaoth-wolfssl.spec

# Copy the file to Ulyaoth home folder.
cp /home/ulyaoth/rpmbuild/SRPMS/* /home/ulyaoth/
cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /home/ulyaoth/
cp /home/ulyaoth/rpmbuild/RPMS/noarch/* /home/ulyaoth/