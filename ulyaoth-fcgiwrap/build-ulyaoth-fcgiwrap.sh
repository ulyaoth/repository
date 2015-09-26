buildarch="$(uname -m)"
fcgiwrapversion=1.1.0

useradd ulyaoth
cd /home/ulyaoth/
su ulyaoth -c "rpmdev-setuptree"
su ulyaoth -c "wget https://github.com/gnosek/fcgiwrap/archive/'"$fcgiwrapversion"'.tar.gz"
su ulyaoth -c "tar xvzf '"$fcgiwrapversion"'.tar.gz"
su ulyaoth -c "mv /home/ulyaoth/fcgiwrap-'"$fcgiwrapversion"' /home/ulyaoth/fcgiwrap"
su ulyaoth -c "sed -i 's/http/fcgiwrap/g' /home/ulyaoth/fcgiwrap/systemd/fcgiwrap.service"
su ulyaoth -c "tar cvf fcgiwrap.tar.gz fcgiwrap"
su ulyaoth -c "mv fcgiwrap.tar.gz /home/ulyaoth/rpmbuild/SOURCES/"
su ulyaoth -c "rm -rf /home/ulyaoth/fcgiwrap/ '"$fcgiwrapversion"'.tar.gz"
cd /home/ulyaoth/rpmbuild/SPECS/
su ulyaoth -c "wget https://raw.githubusercontent.com/sbagmeijer/ulyaoth/master/Repository/ulyaoth-fcgiwrap/SPEC/ulyaoth-fcgiwrap.spec"

if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-fcgiwrap.spec
fi

if grep -q -i "release 22" /etc/fedora-release
then
dnf builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-fcgiwrap.spec
else
yum-builddep -y /home/ulyaoth/rpmbuild/SPECS/ulyaoth-fcgiwrap.spec
fi

su ulyaoth -c "rpmbuild -bb ulyaoth-fcgiwrap.spec"
cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i686/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i386/* /root/
rm -rf /home/ulyaoth/rpmbuild/
rm -rf /root/build-ulyaoth-fcgiwrap.sh
