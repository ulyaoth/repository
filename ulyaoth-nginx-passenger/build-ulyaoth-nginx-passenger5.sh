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
else
echo yeah Fedora!
fi

useradd ulyaoth
cd /root
rpmdev-setuptree
mkdir -p /etc/nginx/modules
cd /etc/nginx/modules
wget http://s3.amazonaws.com/phusion-passenger/releases/passenger-5.0.18.tar.gz
tar xvf passenger-5.0.18.tar.gz
mv passenger-5.0.18 passenger
rm -rf /etc/nginx/modules/passenger/packaging
tar cvf passenger.tar.gz passenger
mv passenger.tar.gz /root/rpmbuild/SOURCES/
cd /root/rpmbuild/SOURCES
wget http://nginx.org/download/nginx-1.8.0.tar.gz
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-passenger/SOURCES/logrotate
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-passenger/SOURCES/nginx.conf
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-passenger/SOURCES/nginx.init
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-passenger/SOURCES/nginx.service
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-passenger/SOURCES/nginx.suse.init
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-passenger/SOURCES/nginx.suse.logrotate
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-passenger/SOURCES/nginx.sysconf
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-passenger/SOURCES/nginx.upgrade.sh
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-passenger/SOURCES/nginx.vh.default.conf
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-passenger/SOURCES/nginx.vh.example_ssl.conf
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-passenger/SOURCES/nginx.vh.passenger5.conf
cd /root/rpmbuild/SPECS
wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-passenger/SPECS/ulyaoth-nginx-passenger5.spec
cd /home/ulyaoth/
chown -R ulyaoth:ulyaoth /etc/nginx/
mv /root/rpmbuild /home/ulyaoth/
chown -R ulyaoth:ulyaoth /home/ulyaoth/rpmbuild
cd /home/ulyaoth/rpmbuild/SPECS

if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-nginx-passenger5.spec
fi

if grep -q -i "release 22" /etc/fedora-release
then
dnf builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-passenger5.spec
else
yum-builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-passenger5.spec
fi

su ulyaoth -c "rpmbuild -bb ulyaoth-nginx-passenger5.spec"
rm -rf /home/ulyaoth/rpmbuild/BUILD/*
rm -rf /home/ulyaoth/rpmbuild/BUILDROOT/*
rm -rf /home/ulyaoth/rpmbuild/RPMS/*
rm -rf /home/ulyaoth/rpmbuild/SOURCES/passenger.tar.gz
cd /etc/nginx/modules
tar cvf passenger.tar.gz passenger
mv passenger.tar.gz /home/ulyaoth/rpmbuild/SOURCES/
chown -R ulyaoth:ulyaoth /home/ulyaoth/rpmbuild
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "rpmbuild -bb ulyaoth-nginx-passenger5.spec"
cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i686/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i386/* /root/
