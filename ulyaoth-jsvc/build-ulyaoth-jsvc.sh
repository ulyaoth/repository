arch="$(uname -m)"
buildarch="$(uname -m)"

useradd ulyaoth
su ulyaoth -c "rpmdev-setuptree"

cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-jsvc/SPEC/ulyaoth-jsvc.spec"

if [ "$arch" != "x86_64" ]
then
  sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-jsvc.spec
fi


if grep -q -i "release 22" /etc/fedora-release &>/dev/null || grep -q -i "release 23" /etc/fedora-release
then
dnf builddep -y ulyaoth-jsvc.spec
else
yum-builddep -y ulyaoth-jsvc.spec
fi

su ulyaoth -c "spectool ulyaoth-jsvc.spec -g -R"
su ulyaoth -c "rpmbuild -ba ulyaoth-jsvc.spec"
cp /home/ulyaoth/rpmbuild/SRPMS/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i686/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i386/* /root/
rm -rf /home/ulyaoth/rpmbuild