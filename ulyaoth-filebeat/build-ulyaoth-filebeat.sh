arch="$(uname -m)"
buildarch="$(uname -m)"
filebeatversion=1.0.1

if [ "$arch" == "i686" ]
then
arch="i386"
fi

if grep -q -i "release 6" /etc/redhat-release
then
yum install -y http://ftp.acc.umu.se/mirror/fedora/epel/6/$arch/epel-release-6-8.noarch.rpm
fi

if type dnf 2>/dev/null
then
  dnf install go golang -y
elif type yum 2>/dev/null
then
  yum install go golang -y
fi


useradd ulyaoth
cd /home/ulyaoth/
su ulyaoth -c "rpmdev-setuptree"
su ulyaoth -c "wget https://github.com/elastic/beats/archive/v'"$filebeatversion"'.tar.gz"
su ulyaoth -c "tar xvzf v'"$filebeatversion"'.tar.gz"
su ulyaoth -c "mkdir -p src/github.com/elastic"
su - ulyaoth -c "mv beats-'"$filebeatversion"' src/github.com/elastic/beats"
su - ulyaoth -c "export GOPATH=$HOME && cd /home/ulyaoth/src/github.com/elastic/beats/filebeat/ && gmake"
su ulyaoth -c "mv /home/ulyaoth/src/github.com/elastic/beats/filebeat/filebeat /home/ulyaoth/rpmbuild/SOURCES/"
su ulyaoth -c "rm -rf src v'"$filebeatversion"'.tar.gz"
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-filebeat/SPECS/ulyaoth-filebeat.spec"

if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-filebeat.spec
fi

su ulyaoth -c "spectool ulyaoth-filebeat.spec -g -R"
su ulyaoth -c "rpmbuild -bb ulyaoth-filebeat.spec"
cp /home/ulyaoth/rpmbuild/SRPMS/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i686/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i386/* /root/
rm -rf /home/ulyaoth/rpmbuild
rm -rf /root/build-ulyaoth-filebeat.sh