arch="$(uname -m)"
buildarch="$(uname -m)"
headersmoreversion=0.29
ajpversion=0.2.6

if [ "$arch" == "i686" ]
then
arch="i386"
fi

if grep -q -i "release 6" /etc/redhat-release
then
yum install -y http://ftp.acc.umu.se/mirror/fedora/epel/6/$arch/epel-release-6-8.noarch.rpm
elif grep -q -i "release 6" /etc/centos-release
then
yum install -y http://ftp.acc.umu.se/mirror/fedora/epel/6/$arch/epel-release-6-8.noarch.rpm
elif grep -q -i "release 7" /etc/oracle-release
then
yum install -y http://mirror.centos.org/centos/7/os/x86_64/Packages/GeoIP-devel-1.5.0-9.el7.x86_64.rpm
else
echo No additional packages required for your OS!
fi

useradd ulyaoth
usermod -Gulyaoth ulyaoth
mkdir -p /etc/nginx/modules
chown -R ulyaoth:ulyaoth /etc/nginx
cd /home/ulyaoth/
su ulyaoth -c "rpmdev-setuptree"

# Temp fix for headersmore for dynamic modules
su ulyaoth -c "wget https://github.com/sbagmeijer/headers-more-nginx-module/archive/master.zip"
su ulyaoth -c "unzip master.zip"
su ulyaoth -c "mv headers-more-nginx-module-master /etc/nginx/modules/headersmore"
su ulyaoth -c "rm -rf master.zip"

# AWS Auth Module
su ulyaoth -c "wget https://github.com/sbagmeijer/ngx_aws_auth/archive/master.zip"
su ulyaoth -c "unzip master.zip"
su ulyaoth -c "mv ngx_aws_auth-master /etc/nginx/modules/awsauth"
su ulyaoth -c "rm -rf master.zip"

# PAM Auth Module
su ulyaoth -c "wget https://github.com/sbagmeijer/ngx_http_auth_pam_module/archive/master.zip"
su ulyaoth -c "unzip master.zip"
su ulyaoth -c "mv ngx_http_auth_pam_module-master /etc/nginx/modules/pamauth"
su ulyaoth -c "rm -rf master.zip"

# AJP Module
su ulyaoth -c "wget https://github.com/yaoweibin/nginx_ajp_module/archive/master.zip"
su ulyaoth -c "unzip master.zip"
su ulyaoth -c "mv nginx_ajp_module-master /etc/nginx/modules/ajp"
su ulyaoth -c "rm -rf master.zip"

chown -R ulyaoth:ulyaoth /etc/nginx
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx/SPECS/ulyaoth-nginx-mainline.spec"

if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-nginx-mainline.spec
fi

if type dnf 2>/dev/null
then
  dnf builddep -y ulyaoth-nginx-mainline.spec
elif type yum 2>/dev/null
then
  yum-builddep -y ulyaoth-nginx-mainline.spec
fi

su ulyaoth -c "spectool ulyaoth-nginx-mainline.spec -g -R"
su ulyaoth -c "rpmbuild -ba ulyaoth-nginx-mainline.spec"
cp /home/ulyaoth/rpmbuild/SRPMS/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i686/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i386/* /root/
rm -rf /etc/nginx
rm -rf /root/build-ulyaoth-nginx-mainline.sh
rm -rf /home/ulyaoth/rpmbuild
