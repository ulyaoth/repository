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
elif grep -q -i "release 7" /etc/oracle-release
then
yum install -y http://mirror.centos.org/centos/7/os/x86_64/Packages/GeoIP-devel-1.5.0-9.el7.x86_64.rpm
else
echo No extra installation required for this OS!
fi

useradd ulyaoth
usermod -Gulyaoth ulyaoth
mkdir -p /etc/nginx/modules
chown -R ulyaoth:ulyaoth /etc/nginx
cd /home/ulyaoth/
su ulyaoth -c "rpmdev-setuptree"
su ulyaoth -c "wget https://github.com/openresty/headers-more-nginx-module/archive/v0.28.tar.gz"
su ulyaoth -c "tar xvf v0.28.tar.gz"
su ulyaoth -c "mv headers-more-nginx-module-0.28 /etc/nginx/modules/headersmore"
su ulyaoth -c "rm -rf v0.28.tar.gz"
chown -R ulyaoth:ulyaoth /etc/nginx
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx/SPECS/ulyaoth-nginx.spec"


if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-nginx.spec
fi

if type dnf 2>/dev/null
then
  dnf builddep -y ulyaoth-nginx.spec
elif type yum 2>/dev/null
then
  yum-builddep -y ulyaoth-nginx.spec
fi

su ulyaoth -c "spectool ulyaoth-nginx.spec -g -R"
su ulyaoth -c "rpmbuild -ba ulyaoth-nginx.spec"

if [ "$ulyaothos" == "amazonlinux" ]
then
  cp /home/ulyaoth/rpmbuild/SRPMS/* /ec2-user/
  cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /ec2-user/
  cp /home/ulyaoth/rpmbuild/RPMS/i686/* /ec2-user/
  cp /home/ulyaoth/rpmbuild/RPMS/i386/* /ec2-user/
else
  cp /home/ulyaoth/rpmbuild/SRPMS/* /root/
  cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /root/
  cp /home/ulyaoth/rpmbuild/RPMS/i686/* /root/
  cp /home/ulyaoth/rpmbuild/RPMS/i386/* /root/
fi

rm -rf /root/build-ulyaoth-*
rm -rf /home/ulyaoth/rpmbuild
rm -rf /etc/nginx