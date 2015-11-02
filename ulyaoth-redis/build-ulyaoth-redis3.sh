buildarch="$(uname -m)"

useradd ulyaoth
cd /home/ulyaoth

su ulyaoth -c "rpmdev-setuptree"

cd /home/ulyaoth/rpmbuild/SPECS/
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-redis/SPECS/ulyaoth-redis3.spec"

if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-redis3.spec
fi

if grep -q -i "release 22" /etc/fedora-release
then
dnf builddep -y ulyaoth-redis3.spec
else
yum-builddep -y ulyaoth-redis3.spec
fi

su ulyaoth -c "spectool ulyaoth-redis3.spec -g -R"
su ulyaoth -c "rpmbuild -ba ulyaoth-redis3.spec"
cp /home/ulyaoth/rpmbuild/SRPMS/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i686/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i386/* /root/

rm -rf /home/ulyaoth/rpmbuild
rm -rf /root/build-ulyaoth-redis3.sh