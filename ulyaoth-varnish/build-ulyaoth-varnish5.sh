# Required variables.
ulyaothos=`cat /etc/ulyaoth`
buildarch="$(uname -m)"

# Install EPEL for rhel6 based os.

# fix ldd
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-varnish/SOURCES/ulyaoth-varnish5.conf -O /etc/ld.so.conf.d/ulyaoth-varnish5.conf
/sbin/ldconfig

# Create build user and go to it's home directory, and create the rpmbuild directory.
useradd ulyaoth
usermod -Gulyaoth ulyaoth
cd /home/ulyaoth/
su ulyaoth -c "rpmdev-setuptree"
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-varnish/SPECS/ulyaoth-varnish5.spec"

# Install all required dependencies from spec file.
if type dnf 2>/dev/null
then
  dnf builddep -y ulyaoth-varnish5.spec
elif type yum 2>/dev/null
then
  yum-builddep -y ulyaoth-varnish5.spec
fi

# Download all source files as specifiec in spec file.
su ulyaoth -c "spectool ulyaoth-varnish5.spec -g -R"

# Build the actual rpm and source rpm.
su ulyaoth -c "rpmbuild -ba ulyaoth-varnish5.spec"

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
rm -rf /etc/ld.so.conf.d/ulyaoth-varnish5.conf
/sbin/ldconfig