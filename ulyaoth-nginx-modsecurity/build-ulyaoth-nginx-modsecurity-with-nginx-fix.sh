arch="$(uname -m)"
buildarch="$(uname -m)"

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
echo yeah Fedora!
fi

if grep -q -i "release 22" /etc/fedora-release
then
dnf install -y pcre pcre-devel libxml2 libxml2-devel curl curl-devel httpd-devel yajl-devel lua-devel lua-static ssdeep-devel systemd-devel
else
yum install -y pcre pcre-devel libxml2 libxml2-devel curl curl-devel httpd-devel yajl-devel lua-devel lua-static ssdeep-devel systemd-devel
fi

useradd ulyaoth
cd /root
rpmdev-setuptree
mkdir -p /etc/nginx/modules
cd /etc/nginx/modules
git clone -b nginx_refactoring https://github.com/SpiderLabs/ModSecurity.git modsecurity
cd modsecurity
./autogen.sh
./configure --enable-standalone-module
make
cd /etc/nginx/modules
tar cvf modsecurity.tar.gz modsecurity
mv modsecurity.tar.gz /root/rpmbuild/SOURCES/
cd /root/rpmbuild/SOURCES
wget http://nginx.org/download/nginx-1.8.0.tar.gz
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-modsecurity/SOURCES/logrotate
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-modsecurity/SOURCES/modsecurity.conf
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-modsecurity/SOURCES/nginx.conf
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-modsecurity/SOURCES/nginx.init
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-modsecurity/SOURCES/nginx.service
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-modsecurity/SOURCES/nginx.suse.init
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-modsecurity/SOURCES/nginx.suse.logrotate
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-modsecurity/SOURCES/nginx.sysconf
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-modsecurity/SOURCES/nginx.upgrade.sh
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-modsecurity/SOURCES/nginx.vh.default-modsecurity.conf
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-modsecurity/SOURCES/nginx.vh.example_ssl.conf
cd /root/rpmbuild/SPECS
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-modsecurity/SPECS/ulyaoth-nginx-modsecurity.spec
cd /home/ulyaoth/
chown -R ulyaoth:ulyaoth /etc/nginx/
mv /root/rpmbuild /home/ulyaoth/
chown -R ulyaoth:ulyaoth /home/ulyaoth/rpmbuild
cd /home/ulyaoth/rpmbuild/SPECS

if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-nginx-modsecurity.spec
fi

if grep -q -i "release 22" /etc/fedora-release
then
dnf builddep -y ulyaoth-nginx-modsecurity.spec
else
yum-builddep -y ulyaoth-nginx-modsecurity.spec
fi

su ulyaoth -c "rpmbuild -bb ulyaoth-nginx-modsecurity.spec"
rm -rf /home/ulyaoth/rpmbuild/BUILD/*
rm -rf /home/ulyaoth/rpmbuild/BUILDROOT/*
rm -rf /home/ulyaoth/rpmbuild/RPMS/*
rm -rf /home/ulyaoth/rpmbuild/SOURCES/modsecurity.tar.gz
cd /etc/nginx/modules
tar cvf modsecurity.tar.gz modsecurity
mv modsecurity.tar.gz /home/ulyaoth/rpmbuild/SOURCES/
chown -R ulyaoth:ulyaoth /home/ulyaoth/rpmbuild
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "rpmbuild -bb ulyaoth-nginx-modsecurity.spec"
cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i686/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i386/* /root/
