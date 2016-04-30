ulyaothos=`cat /etc/ulyaoth`
arch="$(uname -m)"
buildarch="$(uname -m)"
ironbeeversion=0.12.2

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
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-ironbee/SPECS/ulyaoth-nginx-ironbee.spec"

if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-nginx-ironbee.spec
fi

if type dnf 2>/dev/null
then
  dnf builddep -y ulyaoth-nginx-ironbee.spec
elif type yum 2>/dev/null
then
  yum-builddep -y ulyaoth-nginx-ironbee.spec
fi

su ulyaoth -c "spectool ulyaoth-nginx-ironbee.spec -g -R"
su ulyaoth -c "NGINXIB_CONFIG_FILE=/etc/nginx/modules/ironbee/servers/nginx/config.nginx rpmbuild -ba ulyaoth-nginx-ironbee.spec"

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
rm -rf /etc/nginx