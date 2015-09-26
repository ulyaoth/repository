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

useradd ulyaoth
cd /home/ulyaoth/
mkdir -p /etc/nginx/modules/naxsi
chown -R ulyaoth:ulyaoth /etc/nginx
su ulyaoth -c "rpmdev-setuptree"
su ulyaoth -c "wget https://github.com/nbs-system/naxsi/archive/master.zip"
su ulyaoth -c "unzip master.zip"
su ulyaoth -c "cp -rf naxsi-master/* /etc/nginx/modules/naxsi/"
su ulyaoth -c "rm -rf naxsi-master master.zip"
su ulyaoth -c "cp /etc/nginx/modules/naxsi/naxsi_config/naxsi_core.rules /home/ulyaoth/rpmbuild/SOURCES/"
cd /etc/nginx/modules/
su ulyaoth -c "tar cvf naxsi.tar.gz naxsi"
su ulyaoth -c "mv naxsi.tar.gz /home/ulyaoth/rpmbuild/SOURCES/"
cd /home/ulyaoth/rpmbuild/SOURCES/
su ulyaoth -c "wget http://nginx.org/download/nginx-1.9.4.tar.gz"
su ulyaoth -c "wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-naxsi/SOURCES/logrotate"
su ulyaoth -c "wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-naxsi/SOURCES/nginx-naxsi.conf"
su ulyaoth -c "wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-naxsi/SOURCES/nginx.init"
su ulyaoth -c "wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-naxsi/SOURCES/nginx.service"
su ulyaoth -c "wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-naxsi/SOURCES/nginx.suse.init"
su ulyaoth -c "wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-naxsi/SOURCES/nginx.suse.logrotate"
su ulyaoth -c "wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-naxsi/SOURCES/nginx.sysconf"
su ulyaoth -c "wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-naxsi/SOURCES/nginx.upgrade.sh"
su ulyaoth -c "wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-naxsi/SOURCES/nginx.vh.default-naxsi.conf"
su ulyaoth -c "wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-naxsi/SOURCES/nginx.vh.example_ssl.conf"
su ulyaoth -c "wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-naxsi/SOURCES/nbs.rules"
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-naxsi/SPECS/ulyaoth-nginx-mainline-naxsi-masterbuild.spec"

if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-nginx-mainline-naxsi-masterbuild.spec
fi

if grep -q -i "release 22" /etc/fedora-release
then
dnf builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-mainline-naxsi-masterbuild.spec
else
yum-builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-mainline-naxsi-masterbuild.spec
fi

su ulyaoth -c "rpmbuild -bb ulyaoth-nginx-mainline-naxsi-masterbuild.spec"
su ulyaoth -c "rm -rf /home/ulyaoth/rpmbuild/BUILD/*"
su ulyaoth -c "rm -rf /home/ulyaoth/rpmbuild/BUILDROOT/*"
su ulyaoth -c "rm -rf /home/ulyaoth/rpmbuild/RPMS/*"
su ulyaoth -c "rm -rf /home/ulyaoth/rpmbuild/SOURCES/naxsi.tar.gz"
cd /etc/nginx/modules/
su ulyaoth -c "tar cvf naxsi.tar.gz naxsi"
su ulyaoth -c "mv naxsi.tar.gz /home/ulyaoth/rpmbuild/SOURCES/"
cd /home/ulyaoth/rpmbuild/SPECS/
su ulyaoth -c "rpmbuild -bb ulyaoth-nginx-mainline-naxsi-masterbuild.spec"
cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i686/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i386/* /root/
rm -rf /home/ulyaoth/rpmbuild/
rm -rf /etc/nginx
rm -rf /root/build-ulyaoth-nginx-mainline-naxsi-masterbuild.sh