#!/bin/bash
 
if [ $# -lt 1 ]; then
  echo "Usage: $1 stable or mainline."
  echo "Usage: $2 (module name, example: headers-more)"
  exit 1
fi

if [ "$1" = "stable" ]; then
nginxversion="nginx"
elif [ "$1" = "mainline" ]; then
nginxversion="nginx-mainline"
else
echo "We only support the input stable or mainline."
exit 1
fi

if [ "$2" = "headers-more" ]; then
module="headers-more-module"
moduleversion=0.30
elif [ "$2" = "echo" ]; then
module="echo-module"
moduleversion=0.59
else
echo "We only support limited modules please see the Github readme for more information."
exit 1
fi

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
cd /home/ulyaoth/

if [ "$module" = "headers-more-module" ]; then
su ulyaoth -c "wget https://github.com/openresty/headers-more-nginx-module/archive/v$moduleversion.tar.gz"
su ulyaoth -c "tar xvf v$moduleversion.tar.gz"
su ulyaoth -c "mv headers-more-nginx-module-$moduleversion /home/ulyaoth/$module"
su ulyaoth -c "rm -rf v$moduleversion.tar.gz"
elif [ "$module" = "echo-module" ]; then
su ulyaoth -c "wget https://github.com/openresty/echo-nginx-module/archive/v$moduleversion.tar.gz"
su ulyaoth -c "tar xvf v$moduleversion.tar.gz"
su ulyaoth -c "mv echo-nginx-module-$moduleversion /home/ulyaoth/$module"
su ulyaoth -c "rm -rf v$moduleversion.tar.gz"
fi

su ulyaoth -c "rpmdev-setuptree"
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-modules/SPECS/ulyaoth-$nginxversion-$module.spec"


if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-$nginxversion-$module.spec
fi

if type dnf 2>/dev/null
then
  dnf builddep -y ulyaoth-$nginxversion-$module.spec
elif type yum 2>/dev/null
then
  yum-builddep -y ulyaoth-$nginxversion-$module.spec
fi

su ulyaoth -c "spectool ulyaoth-$nginxversion-$module.spec -g -R"
su ulyaoth -c "rpmbuild -ba ulyaoth-$nginxversion-$module.spec"

if [ "$ulyaothos" == "amazonlinux" ]
then
  cp /home/ulyaoth/rpmbuild/SRPMS/*$2* /home/ec2-user/
  cp /home/ulyaoth/rpmbuild/RPMS/x86_64/*$2* /home/ec2-user/
  cp /home/ulyaoth/rpmbuild/RPMS/i686/*$2* /home/ec2-user/
  cp /home/ulyaoth/rpmbuild/RPMS/i386/*$2* /home/ec2-user/
else
  cp /home/ulyaoth/rpmbuild/SRPMS/*$2* /root/
  cp /home/ulyaoth/rpmbuild/RPMS/x86_64/*$2* /root/
  cp /home/ulyaoth/rpmbuild/RPMS/i686/*$2* /root/
  cp /home/ulyaoth/rpmbuild/RPMS/i386/*$2* /root/
fi

rm -rf /root/build-ulyaoth-*
rm -rf /home/ulyaoth/$module
rm -rf /home/ulyaoth/rpmbuild