ulyaothos=`cat /etc/ulyaoth`
arch="$(uname -m)"
buildarch="$(uname -m)"

if [ "$arch" == "i686" ]
then
arch="i386"
fi

if grep -q -i "release 6" /etc/redhat-release
then
yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm
elif grep -q -i "release 6" /etc/centos-release
then
yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm
else
echo yeah Fedora!
fi

if type dnf 2>/dev/null
then
  dnf install -y go golang
elif type yum 2>/dev/null
then
  yum install -y go golang
fi

useradd ulyaoth
cd /home/ulyaoth/
su ulyaoth -c "rpmdev-setuptree"
su ulyaoth -c "git clone git://github.com/jgrahamc/httpdiff.git"
su ulyaoth -c "cd /home/ulyaoth/httpdiff/ && go build"
su ulyaoth -c "mv /home/ulyaoth/httpdiff/httpdiff /home/ulyaoth/rpmbuild/SOURCES/"
su ulyaoth -c "rm -rf /home/ulyaoth/httpdiff/"
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-httpdiff/SPECS/ulyaoth-httpdiff.spec"

if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-httpdiff.spec
fi

su ulyaoth -c "rpmbuild -ba ulyaoth-httpdiff.spec"

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

rm -rf /root/build-ulyaoth-*
rm -rf /home/ulyaoth/rpmbuild