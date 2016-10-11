# Required variables.
ulyaothos=`cat /etc/ulyaoth`
buildarch="$(uname -m)"

# Create build user and go to it's home directory, and create the rpmbuild directory.
useradd ulyaoth
usermod -Gulyaoth ulyaoth
cd /home/ulyaoth/
su ulyaoth -c "rpmdev-setuptree"
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-haproxy/SPECS/ulyaoth-haproxy1.4.spec"

# Install all required dependencies from spec file.
if type dnf 2>/dev/null
then
  dnf builddep -y ulyaoth-haproxy1.4.spec
elif type yum 2>/dev/null
then
  yum-builddep -y ulyaoth-haproxy1.4.spec
fi

# Download all source files as specifiec in spec file.
su ulyaoth -c "spectool ulyaoth-haproxy1.4.spec -g -R"

# Build the actual rpm and source rpm.
su ulyaoth -c "rpmbuild -ba ulyaoth-haproxy1.4.spec"

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