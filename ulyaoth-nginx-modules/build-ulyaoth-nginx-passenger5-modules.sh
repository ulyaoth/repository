#!/bin/bash

ulyaothos=`cat /etc/ulyaoth`
passengerversion="5.0.30"

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
mkdir -p /usr/local/ulyaoth/passenger/5
cd /usr/local/ulyaoth/passenger/5
git clone -b stable-5.0 git://github.com/phusion/passenger.git
cd /usr/local/ulyaoth/passenger/5/passenger
git checkout release-$passengerversion
git submodule update --init --recursive
mv /usr/local/ulyaoth/passenger/5/passenger/* /usr/local/ulyaoth/passenger/5/
rm -rf /usr/local/ulyaoth/passenger/5/passenger
chown -R ulyaoth:ulyaoth /usr/local/ulyaoth
su ulyaoth -c "rpmdev-setuptree"
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