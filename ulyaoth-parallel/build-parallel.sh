# This script is supposed to run as the user "ulyaoth".

rpmdev-setuptree

wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-parallel/SPECS/ulyaoth-parallel.spec -O /home/ulyaoth/rpmbuild/SPECS/ulyaoth-parallel.spec

spectool /home/ulyaoth/rpmbuild/SPECS/ulyaoth-parallel.spec -g -R
rpmbuild -ba /home/ulyaoth/rpmbuild/SPECS/ulyaoth-parallel.spec

cp /home/ulyaoth/rpmbuild/SRPMS/* /home/ulyaoth/
cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /home/ulyaoth/
cp /home/ulyaoth/rpmbuild/RPMS/noarch/* /home/ulyaoth/
