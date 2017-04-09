# Required variables.
ulyaothos=`cat /etc/ulyaoth`
buildarch="$(uname -m)"

# fix ldd
wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-lua/SOURCES/ulyaoth-lua5.3.conf -O /etc/ld.so.conf.d/ulyaoth-lua5.3.conf
/sbin/ldconfig

# Create build user and go to it's home directory, and create the rpmbuild directory.
useradd ulyaoth
usermod -Gulyaoth ulyaoth
cd /home/ulyaoth/
su ulyaoth -c "rpmdev-setuptree"
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-lua/SPECS/ulyaoth-lua5.3.spec"

# Install all required dependencies from spec file.
if type dnf 2>/dev/null
then
  dnf builddep -y ulyaoth-lua5.3.spec
elif type yum 2>/dev/null
then
  yum-builddep -y ulyaoth-lua5.3.spec
fi

# Download all source files as specifiec in spec file.
su ulyaoth -c "spectool ulyaoth-lua5.3.spec -g -R"

# Build the actual rpm and source rpm.
su ulyaoth -c "QA_RPATHS=\$[ 0x0001|0x0002 ] rpmbuild -ba ulyaoth-lua5.3.spec"

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
rm -rf /etc/ld.so.conf.d/ulyaoth-lua5.3.conf
/sbin/ldconfig