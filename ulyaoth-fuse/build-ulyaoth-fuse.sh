buildarch="$(uname -m)"

useradd ulyaoth
usermod -Gulyaoth ulyaoth
cd /home/ulyaoth/
su ulyaoth -c "rpmdev-setuptree"
cd /home/ulyaoth/rpmbuild/SPECS
su ulyaoth -c "wget https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-fuse/SPECS/ulyaoth-fuse.spec"

if [ "$arch" != "x86_64" ]
then
sed -i '/BuildArch: x86_64/c\BuildArch: '"$buildarch"'' ulyaoth-fuse.spec
fi

if type dnf 2>/dev/null
then
  dnf builddep -y ulyaoth-fuse.spec
elif type yum 2>/dev/null
then
  yum-builddep -y ulyaoth-fuse.spec
fi

su ulyaoth -c "spectool ulyaoth-fuse.spec -g -R"
su ulyaoth -c "rpmbuild -ba ulyaoth-fuse.spec"
cp /home/ulyaoth/rpmbuild/SRPMS/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/x86_64/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i686/* /root/
cp /home/ulyaoth/rpmbuild/RPMS/i386/* /root/
rm -rf /root/build-ulyaoth-fuse.sh
rm -rf /home/ulyaoth/rpmbuild