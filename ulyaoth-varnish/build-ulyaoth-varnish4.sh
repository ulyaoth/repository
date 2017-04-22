# Required variables.
ulyaothos=`cat /etc/ulyaoth`
buildarch="$(uname -m)"

# Install EPEL for rhel6 based os.
if grep --quiet "release 6" /etc/redhat-release || grep --quiet "release 6" /etc/oracle-release || grep --quiet "release 6" /etc/centos-release; then
  yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm
elif grep --quiet "release 7" /etc/redhat-release || grep --quiet "release 7" /etc/oracle-release || grep --quiet "release 7" /etc/centos-release; then
  yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
fi

# Create build user and go to it's home directory, and create the rpmbuild directory.
useradd ulyaoth
usermod -Gulyaoth ulyaoth
cd /home/ulyaoth/
su ulyaoth -c "rpmdev-setuptree"
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-varnish/SPECS/ulyaoth-varnish4.spec"

# Install all required dependencies from spec file.
if type dnf 2>/dev/null
then
  dnf builddep -y ulyaoth-varnish4.spec
elif type yum 2>/dev/null
then
  yum-builddep -y ulyaoth-varnish4.spec
fi

# Download all source files as specifiec in spec file.
su ulyaoth -c "spectool ulyaoth-varnish4.spec -g -R"

# Build the actual rpm and source rpm.
su ulyaoth -c "rpmbuild -ba ulyaoth-varnish4.spec"

# Copy the rpms to root directory.
if [ "$ulyaothos" == "amazonlinux" ]
then
  cp /home/ulyaoth/rpmbuild/SRPMS/* /home/ec2-user/
  cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /home/ec2-user/
  cp /home/ulyaoth/rpmbuild/RPMS/i686/* /home/ec2-user/
  cp /home/ulyaoth/rpmbuild/RPMS/i386/* /home/ec2-user/
else
  cp /home/ulyaoth/rpmbuild/SRPMS/* /root/
  cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /root/
  cp /home/ulyaoth/rpmbuild/RPMS/i686/* /root/
  cp /home/ulyaoth/rpmbuild/RPMS/i386/* /root/
fi

# Clean
rm -rf /root/build-ulyaoth-*
rm -rf /home/ulyaoth/rpmbuild