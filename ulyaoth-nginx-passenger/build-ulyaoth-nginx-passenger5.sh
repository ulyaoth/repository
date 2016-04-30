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
else
echo yeah Fedora!
fi


useradd ulyaoth
cd /home/ulyaoth/
su ulyaoth -c "rpmdev-setuptree"
mkdir -p /etc/nginx/modules
chown -R ulyaoth:ulyaoth /etc/nginx/
su ulyaoth -c "wget https://github.com/openresty/headers-more-nginx-module/archive/v0.28.tar.gz"
su ulyaoth -c "tar xvf v0.28.tar.gz"
su ulyaoth -c "mv headers-more-nginx-module-0.28 /etc/nginx/modules/headersmore"
su ulyaoth -c "rm -rf v0.28.tar.gz"


cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-passenger/SPECS/ulyaoth-nginx-passenger5.spec"
cd /etc/nginx/modules
wget http://s3.amazonaws.com/phusion-passenger/releases/passenger-5.0.27.tar.gz
tar xvf passenger-5.0.27.tar.gz
mv passenger-5.0.27 passenger
rm -rf /etc/nginx/modules/passenger/packaging
tar cvf passenger.tar.gz passenger
mv passenger.tar.gz /home/ulyaoth/rpmbuild/SOURCES/
chown -R ulyaoth:ulyaoth /etc/nginx/
chown -R ulyaoth:ulyaoth /home/ulyaoth/rpmbuild
cd /home/ulyaoth/rpmbuild/SPECS

if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-nginx-passenger5.spec
fi

if type dnf 2>/dev/null
then
  dnf builddep -y ulyaoth-nginx-passenger5.spec
elif type yum 2>/dev/null
then
  yum-builddep -y ulyaoth-nginx-passenger5.spec
fi

su ulyaoth -c "spectool ulyaoth-nginx-passenger5.spec -g -R"
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
su ulyaoth -c "rpmbuild -ba ulyaoth-nginx-passenger5.spec"

if [ "$ulyaothos" == "amazonlinux" ]
then
  cp /home/ulyaoth/rpmbuild/SRPMS/* /ec2-user/
  cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /ec2-user/
  cp /home/ulyaoth/rpmbuild/RPMS/i686/* /ec2-user/
  cp /home/ulyaoth/rpmbuild/RPMS/i386/* /ec2-user/
else
  cp /home/ulyaoth/rpmbuild/SRPMS/* /root/
  cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /root/
  cp /home/ulyaoth/rpmbuild/RPMS/i686/* /root/
  cp /home/ulyaoth/rpmbuild/RPMS/i386/* /root/
fi

rm -rf /root/build-ulyaoth-*.sh
rm -rf /home/ulyaoth/rpmbuild