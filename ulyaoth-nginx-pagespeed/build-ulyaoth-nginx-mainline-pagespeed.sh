ulyaothos=`cat /etc/ulyaoth`
arch="$(uname -m)"
buildarch="$(uname -m)"

if [ "$arch" == "i686" ]
then
arch="i386"
fi

if grep -q -i "release 6" /etc/redhat-release
then
wget -O /etc/yum.repos.d/slc6-devtoolset.repo http://linuxsoft.cern.ch/cern/devtoolset/slc6-devtoolset.repo
yum install devtoolset-2 -y --nogpg
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
echo yeah Fedora!
fi

useradd ulyaoth
cd /home/ulyaoth/
mkdir -p /etc/nginx/modules/pagespeed
chown -R ulyaoth:ulyaoth /etc/nginx
su ulyaoth -c "rpmdev-setuptree"

su ulyaoth -c "wget https://github.com/openresty/headers-more-nginx-module/archive/v0.28.tar.gz"
su ulyaoth -c "tar xvf v0.28.tar.gz"
su ulyaoth -c "mv headers-more-nginx-module-0.28 /etc/nginx/modules/headersmore"
su ulyaoth -c "rm -rf v0.28.tar.gz"

su ulyaoth -c "wget https://github.com/pagespeed/ngx_pagespeed/archive/v1.11.33.0-beta.zip"
su ulyaoth -c "wget https://dl.google.com/dl/page-speed/psol/1.11.33.0.tar.gz"
su ulyaoth -c "unzip v1.11.33.0-beta.zip"
su ulyaoth -c "tar xvf 1.11.33.0.tar.gz"
su ulyaoth -c "cp -rf ngx_pagespeed-1.11.33.0-beta/* /etc/nginx/modules/pagespeed/"
su ulyaoth -c "mv psol/ /etc/nginx/modules/pagespeed/"

if [ "$arch" == "x86_64" ]
then
su ulyaoth -c "rm -rf /etc/nginx/modules/pagespeed/psol/lib/Debug/linux/ia32"
su ulyaoth -c "rm -rf /etc/nginx/modules/pagespeed/psol/lib/Release/linux/ia32"
else
su ulyaoth -c "rm -rf /etc/nginx/modules/pagespeed/psol/lib/Debug/linux/x64"
su ulyaoth -c "rm -rf /etc/nginx/modules/pagespeed/psol/lib/Release/linux/x64"
fi

su ulyaoth -c "rm -rf 1.11.33.0.tar.gz ngx_pagespeed-1.11.33.0-beta v1.11.33.0-beta.zip"
cd /etc/nginx/modules/pagespeed/
su ulyaoth -c "tar cvf pagespeed.tar.gz scripts/ test/"
su ulyaoth -c "mv pagespeed.tar.gz /home/ulyaoth/rpmbuild/SOURCES/"
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-pagespeed/SPECS/ulyaoth-nginx-mainline-pagespeed.spec"

if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-nginx-mainline-pagespeed.spec
fi

if type dnf 2>/dev/null
then
  dnf builddep -y ulyaoth-nginx-mainline-pagespeed.spec
elif type yum 2>/dev/null
then
  yum-builddep -y ulyaoth-nginx-mainline-pagespeed.spec
fi

su ulyaoth -c "spectool ulyaoth-nginx-mainline-pagespeed.spec -g -R"


if grep -q -i "release 6" /etc/redhat-release
then
su ulyaoth -c "export CC=/opt/rh/devtoolset-2/root/usr/bin/gcc && export CXX=/opt/rh/devtoolset-2/root/usr/bin/g++ && rpmbuild -ba ulyaoth-nginx-mainline-pagespeed.spec"
else
su ulyaoth -c "rpmbuild -ba ulyaoth-nginx-mainline-pagespeed.spec"
fi

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
rm -rf /etc/nginx