ulyaothos=`cat /etc/ulyaoth`
arch="$(uname -m)"
buildarch="$(uname -m)"


if grep -q -i "release 6" /etc/redhat-release
then
su root -c "yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm"
elif grep -q -i "release 6" /etc/centos-release
then
su root -c "yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm"
elif grep -q -i "release 7" /etc/oracle-release
then
su root -c "yum install -y http://mirror.centos.org/centos/7/os/x86_64/Packages/GeoIP-devel-1.5.0-9.el7.x86_64.rpm"
else
echo No extra installation required for this OS!
fi

su root -c "useradd ulyaoth"
su root -c "usermod -Gulyaoth ulyaoth"
cd /home/ulyaoth/
su ulyaoth -c "rpmdev-setuptree"
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tengine/SPECS/ulyaoth-tengine.spec"

if type dnf 2>/dev/null
then
  su root -c "dnf builddep -y ulyaoth-tengine.spec"
elif type yum 2>/dev/null
then
  su root -c "yum-builddep -y ulyaoth-tengine.spec"
fi


su ulyaoth -c "spectool ulyaoth-tengine.spec -g -R"
su ulyaoth -c "rpmbuild -ba ulyaoth-tengine.spec"

su root -c "cp /home/ulyaoth/rpmbuild/SRPMS/* /home/ec2-user/"
su root -c "cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /home/ec2-user/"
su root -c "cp /home/ulyaoth/rpmbuild/RPMS/i686/* /home/ec2-user/"
su root -c "cp /home/ulyaoth/rpmbuild/RPMS/i386/* /home/ec2-user/"
su root -c "chown ec2-user:ec2-user /home/ec2-user/*.rpm"