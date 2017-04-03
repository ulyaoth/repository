# Required variables.
ulyaothos=`cat /etc/ulyaoth`
buildarch="$(uname -m)"

# Install EPEL.
if grep --quiet "release 6" /etc/redhat-release || grep --quiet "release 6" /etc/oracle-release || grep --quiet "release 6" /etc/centos-release; then
  yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm
elif grep --quiet "release 7" /etc/redhat-release || grep --quiet "release 7" /etc/oracle-release || grep --quiet "release 7" /etc/centos-release; then
  yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
fi

if [ "$ulyaothos" == "amazonlinux" ]
then
  yum-config-manager --enable epel
fi

# Install ulyaoth repository for dependencies.
if [ "$ulyaothos" == "fedora" ]
then
if type dnf 2>/dev/null
then
  dnf install https://downloads.ulyaoth.net/rpm/ulyaoth-latest.fedora.x86_64.rpm -y
elif type yum 2>/dev/null
then
  yum install https://downloads.ulyaoth.net/rpm/ulyaoth-latest.fedora.x86_64.rpm -y
fi
elif [ "$ulyaothos" == "redhat" ]
then
  yum install https://downloads.ulyaoth.net/rpm/ulyaoth-latest.redhat.x86_64.rpm -y
elif [ "$ulyaothos" == "amazonlinux" ]
then
  yum install https://downloads.ulyaoth.net/rpm/ulyaoth-latest.amazonlinux.x86_64.rpm -y
elif [ "$ulyaothos" == "centos" ]
then
  yum install https://downloads.ulyaoth.net/rpm/ulyaoth-latest.centos.x86_64.rpm -y
elif [ "$ulyaothos" == "oraclelinux" ]
then 
  yum install https://downloads.ulyaoth.net/rpm/ulyaoth-latest.oraclelinux.x86_64.rpm -y
elif [ "$ulyaothos" == "scientificlinux" ]
then
  yum install https://downloads.ulyaoth.net/rpm/ulyaoth-latest.scientificlinux.x86_64.rpm -y
fi

# Create build user and go to it's home directory, and create the rpmbuild directory.
useradd ulyaoth
usermod -Gulyaoth ulyaoth
cd /home/ulyaoth/
su ulyaoth -c "rpmdev-setuptree"
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-hitch/SPECS/ulyaoth-hitch.spec"

# Install all required dependencies from spec file.
if type dnf 2>/dev/null
then
  dnf builddep -y ulyaoth-hitch.spec
elif type yum 2>/dev/null
then
  yum-builddep -y ulyaoth-hitch.spec
fi

# Download all source files as specifiec in spec file.
su ulyaoth -c "spectool ulyaoth-hitch.spec -g -R"

# Build the actual rpm and source rpm.
su ulyaoth -c "QA_RPATHS=\$[ 0x0001|0x0002 ] rpmbuild -ba ulyaoth-hitch.spec"

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