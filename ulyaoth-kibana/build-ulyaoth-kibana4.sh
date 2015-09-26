arch="$(uname -m)"
buildarch="$(uname -m)"

if [ "$arch" == "i686" ]
then
arch="i386"
fi

useradd ulyaoth
cd /home/ulyaoth
su ulyaoth -c "rpmdev-setuptree"
cd /home/ulyaoth/rpmbuild/SOURCES/

if [ "$arch" != "x86_64" ]
then
su ulyaoth -c "wget https://download.elasticsearch.org/kibana/kibana/kibana-4.1.2-linux-x86.tar.gz"
else
su ulyaoth -c "wget https://download.elasticsearch.org/kibana/kibana/kibana-4.1.2-linux-x64.tar.gz"
fi

su ulyaoth -c "wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-kibana/SOURCES/kibana.init"
su ulyaoth -c "wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-kibana/SOURCES/kibana.service"
cd /home/ulyaoth/rpmbuild/SPECS/
su ulyaoth -c "wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-kibana/SPECS/ulyaoth-kibana4.spec"

if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-kibana4.spec
fi

if grep -q -i "release 22" /etc/fedora-release
then
dnf builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-kibana4.spec
else
yum-builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-kibana4.spec
fi

su ulyaoth -c "rpmbuild -bb ulyaoth-kibana4.spec"
cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i686/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i386/* /root/
su ulyaoth -c "rm -rf /home/ulyaoth/rpmbuild"
rm -rf /root/build-ulyaoth-kibana4.sh