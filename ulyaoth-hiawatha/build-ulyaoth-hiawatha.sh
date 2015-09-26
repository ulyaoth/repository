buildarch="$(uname -m)"

useradd ulyaoth
usermod -Gulyaoth ulyaoth
cd /home/ulyaoth/
su ulyaoth -c "rpmdev-setuptree"
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-hiawatha/SPECS/ulyaoth-hiawatha.spec"

if grep -q -i "release 19" /etc/fedora-release
then
  if [ "$buildarch" != "x86_64" ]
  then
    yum install -y https://downloads.ulyaoth.net/rpm/Fedora/i686/ulyaoth-1.0.7-1.fc19.i686.rpm
  else
    yum install -y https://downloads.ulyaoth.net/rpm/Fedora/x86_64/ulyaoth-1.0.7-1.fc19.x86_64.rpm
  fi
elif grep -q -i "release 20" /etc/fedora-release
then
  if [ "$buildarch" != "x86_64" ]
  then
    yum install -y https://downloads.ulyaoth.net/rpm/Fedora/i686/ulyaoth-1.0.7-1.fc20.i686.rpm
  else
    yum install -y https://downloads.ulyaoth.net/rpm/Fedora/x86_64/ulyaoth-1.0.7-1.fc20.x86_64.rpm
  fi
elif grep -q -i "release 21" /etc/fedora-release
then
  if [ "$buildarch" != "x86_64" ]
  then
    yum install -y https://downloads.ulyaoth.net/rpm/Fedora/i686/ulyaoth-1.0.7-1.fc21.i686.rpm
  else
    yum install -y https://downloads.ulyaoth.net/rpm/Fedora/x86_64/ulyaoth-1.0.7-1.fc21.x86_64.rpm
  fi
elif grep -q -i "release 22" /etc/fedora-release
then
  if [ "$buildarch" != "x86_64" ]
  then
    dnf install -y https://downloads.ulyaoth.net/rpm/Fedora/i686/ulyaoth-1.0.7-1.fc22.i686.rpm
  else
    dnf install -y https://downloads.ulyaoth.net/rpm/Fedora/x86_64/ulyaoth-1.0.7-1.fc22.x86_64.rpm
  fi
elif grep -q -i "rhel" /etc/ulyaoth && grep -q -i "release 6" /etc/redhat-release
then
  if [ "$buildarch" != "x86_64" ]
  then
    yum install -y https://downloads.ulyaoth.net/rpm/rhel/i686/ulyaoth-1.0.7-1.el6.i686.rpm
  else
    yum install -y https://downloads.ulyaoth.net/rpm/rhel/x86_64/ulyaoth-1.0.7-1.el6.x86_64.rpm
  fi  
elif grep -q -i "rhel" /etc/ulyaoth && grep -q -i "release 7" /etc/redhat-release
then
  yum install -y https://downloads.ulyaoth.net/rpm/rhel/x86_64/ulyaoth-1.0.7-1.el7.x86_64.rpm
elif grep -q -i "CentOS" /etc/ulyaoth && grep -q -i "release 6" /etc/centos-release
then
  if [ "$buildarch" != "x86_64" ]
  then
    yum install -y https://downloads.ulyaoth.net/rpm/CentOS/i686/ulyaoth-1.0.7-1.el6.i686.rpm
  else
    yum install -y https://downloads.ulyaoth.net/rpm/CentOS/x86_64/ulyaoth-1.0.7-1.el6.x86_64.rpm
  fi
elif grep -q -i "CentOS" /etc/ulyaoth && grep -q -i "release 7" /etc/redhat-release
then
  yum install -y https://downloads.ulyaoth.net/rpm/CentOS/x86_64/ulyaoth-1.0.7-1.el7.centos.x86_64.rpm
elif grep -q -i "OracleLinux" /etc/ulyaoth && grep -q -i "release 6" /etc/oracle-release
then
  if [ "$buildarch" != "x86_64" ]
  then
    yum install -y https://downloads.ulyaoth.net/rpm/OracleLinux/i686/ulyaoth-1.0.7-1.el6.i686.rpm
  else
    yum install -y https://downloads.ulyaoth.net/rpm/OracleLinux/x86_64/ulyaoth-1.0.7-1.el6.x86_64.rpm
  fi
elif grep -q -i "OracleLinux" /etc/ulyaoth && grep -q -i "release 7" /etc/oracle-release
then
  yum install -y https://downloads.ulyaoth.net/rpm/OracleLinux/x86_64/ulyaoth-1.0.7-1.el7.x86_64.rpm
elif grep -q -i "scientific" /etc/ulyaoth && grep -q -i "release 6" /etc/redhat-release
then
  if [ "$buildarch" != "x86_64" ]
  then
    yum install -y https://downloads.ulyaoth.net/rpm/scientific/i686/ulyaoth-1.0.7-1.el6.i686.rpm
  else
    yum install -y https://downloads.ulyaoth.net/rpm/scientific/x86_64/ulyaoth-1.0.7-1.el6.x86_64.rpm
  fi
elif grep -q -i "scientific" /etc/ulyaoth && grep -q -i "release 7" /etc/redhat-release
then
  yum install -y https://downloads.ulyaoth.net/rpm/scientific/x86_64/ulyaoth-1.0.7-1.el7.x86_64.rpm
fi

if [ "$buildarch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-hiawatha.spec
fi

if grep -q -i "release 22" /etc/fedora-release
then
dnf builddep -y ulyaoth-hiawatha.spec
else
yum-builddep -y ulyaoth-hiawatha.spec
fi

su ulyaoth -c "spectool ulyaoth-hiawatha.spec -g -R"
su ulyaoth -c "rpmbuild -bb ulyaoth-hiawatha.spec"
cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i686/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i386/* /root/
rm -rf /root/build-ulyaoth-hiawatha.sh
rm -rf /home/ulyaoth/rpmbuild