#!/bin/bash

ulyaothos=`cat /etc/ulyaoth`
passengerversion=5.0.30

if grep -q -i "release 6" /etc/redhat-release
then
yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm
elif grep -q -i "release 6" /etc/centos-release
then
yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm
else
echo yeah Fedora!
fi

useradd ulyaoth
cd /home/ulyaoth/
su ulyaoth -c "rpmdev-setuptree"
wget https://github.com/phusion/passenger/archive/release-$passengerversion.tar.gz
tar xvf release-$passengerversion.tar.gz
cp -rf passenger-release-$passengerversion/* /usr/local/ulyaoth/passenger/5/"
rm -rf passenger-release-$passengerversion release-$passengerversion.tar.gz"
rm -rf /usr/local/ulyaoth/passenger/5/packaging
chown -R ulyaoth:ulyaoth /usr/local/ulyaoth
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/sbagmeijer/repository/master/ulyaoth-nginx-modules/SPECS/ulyaoth-nginx-passenger5-module.spec"

if type dnf 2>/dev/null
then
  dnf builddep -y ulyaoth-nginx-passenger5-module.spec
elif type yum 2>/dev/null
then
  yum-builddep -y ulyaoth-nginx-passenger5-module.spec
fi

su ulyaoth -c "spectool ulyaoth-nginx-passenger5-module.spec -g -R"
su ulyaoth -c "rpmbuild -bb ulyaoth-nginx-passenger5-module.spec"

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

rm -rf /root/build-ulyaoth-*.sh
rm -rf /home/ulyaoth/rpmbuild
rm -rf /usr/local/ulyaoth