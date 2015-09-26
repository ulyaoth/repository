arch="$(uname -m)"
buildarch="$(uname -m)"
ironbeeversion=0.12.2

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
echo No additional packages required for your OS.
fi

useradd ulyaoth
cd /home/ulyaoth/
mkdir -p /etc/nginx/modules/ironbee
chown -R ulyaoth:ulyaoth /etc/nginx
su ulyaoth -c "rpmdev-setuptree"
su ulyaoth -c "wget https://github.com/ironbee/ironbee/archive/v'"$ironbeeversion"'.tar.gz"
su ulyaoth -c "tar xvzf v'"$ironbeeversion"'.tar.gz"
su ulyaoth -c "cp -rf ironbee-'"$ironbeeversion"'/* /etc/nginx/modules/ironbee/"
su ulyaoth -c "rm -rf ironbee-'"$ironbeeversion"' v'"$ironbeeversion"'.tar.gz"
cd /etc/nginx/modules/
su ulyaoth -c "tar cvzf ironbee.tar.gz ironbee"
su ulyaoth -c "mv ironbee.tar.gz /home/ulyaoth/rpmbuild/SOURCES/"
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-nginx-ironbee/SPECS/ulyaoth-nginx-ironbee.spec"

if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-nginx-ironbee.spec
fi

if grep -q -i "release 22" /etc/fedora-release
then
dnf builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-ironbee.spec
else
yum-builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-nginx-ironbee.spec
fi

su ulyaoth -c "spectool ulyaoth-nginx-ironbee.spec -g -R"
su ulyaoth -c "NGINXIB_CONFIG_FILE=/etc/nginx/modules/ironbee/servers/nginx/config.nginx rpmbuild -bb ulyaoth-nginx-ironbee.spec"
cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i686/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i386/* /root/
rm -rf /home/ulyaoth/rpmbuild/
rm -rf /etc/nginx
rm -rf /root/build-ulyaoth-nginx-ironbee.sh