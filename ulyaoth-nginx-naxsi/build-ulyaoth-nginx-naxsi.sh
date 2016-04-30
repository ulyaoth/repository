ulyaothos=`cat /etc/ulyaoth`
arch="$(uname -m)"
buildarch="$(uname -m)"
naxsiversion=0.54

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
su ulyaoth -c "wget https://github.com/nbs-system/naxsi/archive/'"$naxsiversion"'.tar.gz"
su ulyaoth -c "tar xvzf '"$naxsiversion"'.tar.gz"
su ulyaoth -c "cp -rf naxsi-'"$naxsiversion"'/* /etc/nginx/modules/naxsi/"
su ulyaoth -c "rm -rf naxsi-'"$naxsiversion"' '"$naxsiversion"'.tar.gz"
su ulyaoth -c "cp /etc/nginx/modules/naxsi/naxsi_config/naxsi_core.rules /home/ulyaoth/rpmbuild/SOURCES/"
cd /etc/nginx/modules/
su ulyaoth -c "tar cvf naxsi.tar.gz naxsi"
su ulyaoth -c "mv naxsi.tar.gz /home/ulyaoth/rpmbuild/SOURCES/"
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-nginx-naxsi/SPECS/ulyaoth-nginx-naxsi.spec"

if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-nginx-naxsi.spec
fi

if type dnf 2>/dev/null
then
  dnf builddep -y ulyaoth-nginx-naxsi.spec
elif type yum 2>/dev/null
then
  yum-builddep -y ulyaoth-nginx-naxsi.spec
fi

su ulyaoth -c "spectool ulyaoth-nginx-naxsi.spec -g -R"
su ulyaoth -c "rpmbuild -bb ulyaoth-nginx-naxsi.spec"
su ulyaoth -c "rm -rf /home/ulyaoth/rpmbuild/BUILD/*"
su ulyaoth -c "rm -rf /home/ulyaoth/rpmbuild/BUILDROOT/*"
su ulyaoth -c "rm -rf /home/ulyaoth/rpmbuild/RPMS/*"
su ulyaoth -c "rm -rf /home/ulyaoth/rpmbuild/SOURCES/naxsi.tar.gz"
cd /etc/nginx/modules/
su ulyaoth -c "tar cvf naxsi.tar.gz naxsi"
su ulyaoth -c "mv naxsi.tar.gz /home/ulyaoth/rpmbuild/SOURCES/"
cd /home/ulyaoth/rpmbuild/SPECS/
su ulyaoth -c "rpmbuild -ba ulyaoth-nginx-naxsi.spec"

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